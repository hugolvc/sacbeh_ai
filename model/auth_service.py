"""
Authorization service for handling authentication and authorization operations.
"""

from typing import Optional, List, Dict, Any, Set, Tuple
from datetime import datetime, timedelta
import json

from .auth_models import (
    UserAuth, Role, UserRole, Session, LoginAttempt, 
    AuthStatus, Permission, AuthUtils
)
from .data_connectors import DatabaseConnector, DatabaseConnectorFactory
from .data_models import User, UserRole as UserRoleEnum


class AuthService:
    """
    Service class for handling authentication and authorization operations.
    Uses the database connector for data persistence.
    """
    
    def __init__(self, connector: Optional[DatabaseConnector] = None):
        """
        Initialize the auth service with a database connector.
        
        Args:
            connector: Database connector instance (creates default SQLite if None)
        """
        self.connector = connector or DatabaseConnectorFactory.create_connector("sqlite")
        self.session_timeout = timedelta(hours=24)  # 24 hours
        self.max_failed_attempts = 5
        self.lockout_duration = timedelta(minutes=30)  # 30 minutes
    
    def register_user(
        self, email: str, password: str, name: str, 
        role: UserRoleEnum = UserRoleEnum.USER
    ) -> Tuple[bool, str]:
        """
        Register a new user in the system.
        
        Args:
            email: User's email address
            password: Plain text password
            name: User's full name
            role: User's role
            
        Returns:
            Tuple of (success, message)
        """
        try:
            # Normalize email (lowercase and trim whitespace)
            email = email.lower().strip()
            
            # Validate password strength
            is_strong, issues = AuthUtils.is_password_strong(password)
            if not is_strong:
                return False, f"Password is not strong enough: {', '.join(issues)}"
            
            # Check if user already exists (case-insensitive)
            existing_user = self.get_user_auth_by_email(email)
            if existing_user:
                return False, "User with this email already exists"
            
            # Hash password
            password_hash, salt = AuthUtils.hash_password(password)
            
            # Create user auth record
            user_auth = UserAuth(
                email=email,
                password_hash=password_hash,
                salt=salt,
                status=AuthStatus.ACTIVE,
                email_verified=True
            )
            
            # Insert user auth
            user_id = self._insert_user_auth(user_auth)
            if not user_id:
                return False, "Failed to create user account"
            
            # Assign default role
            role_id = self._get_role_id_by_name(role.value)
            if role_id:
                self._assign_role_to_user(user_id, role_id)
            
            return True, "User registered successfully. You can now log in."
            
        except Exception as e:
            return False, f"Registration failed: {str(e)}"
    
    def authenticate_user(self, email: str, password: str, 
                         ip_address: str = None, user_agent: str = None) -> Tuple[bool, str, Optional[Session]]:
        """
        Authenticate a user with email and password.
        
        Args:
            email: User's email address
            password: Plain text password
            ip_address: IP address of the login attempt
            user_agent: User agent string
            
        Returns:
            Tuple of (success, message, session)
        """
        try:
            # Normalize email for case-insensitive lookup
            email = email.lower().strip()
            
            # Get user auth record
            user_auth = self.get_user_auth_by_email(email)
            if not user_auth:
                self._record_login_attempt(email, ip_address, user_agent, False, "User not found")
                return False, "Invalid email or password", None
            
            # Check if account is locked
            if user_auth.status == AuthStatus.LOCKED:
                if user_auth.locked_until and datetime.now() < user_auth.locked_until:
                    self._record_login_attempt(email, ip_address, user_agent, False, "Account locked")
                    return False, "Account is temporarily locked", None
                else:
                    # Unlock account if lock period has expired
                    self._unlock_account(user_auth.id)
                    user_auth.status = AuthStatus.ACTIVE
            
            # Verify password
            if not AuthUtils.verify_password(password, user_auth.password_hash, user_auth.salt):
                self._handle_failed_login(user_auth, ip_address, user_agent)
                return False, "Invalid email or password", None
            
            # Check if email is verified
            if not user_auth.email_verified:
                self._record_login_attempt(email, ip_address, user_agent, False, "Email not verified")
                return False, "Please verify your email address before logging in", None
            
            # Reset failed login attempts
            self._reset_failed_attempts(user_auth.id)
            
            # Update last login
            self._update_last_login(user_auth.id)
            
            # Create session
            session = self._create_session(user_auth.id, ip_address, user_agent)
            
            # Record successful login
            self._record_login_attempt(email, ip_address, user_agent, True)
            
            return True, "Login successful", session
            
        except Exception as e:
            return False, f"Authentication failed: {str(e)}", None
    
    def verify_session(self, session_token: str) -> Tuple[bool, Optional[Dict[str, Any]]]:
        """
        Verify if a session token is valid and return user information.
        
        Args:
            session_token: Session token to verify
            
        Returns:
            Tuple of (is_valid, user_info)
        """
        try:
            session = self.get_session_by_token(session_token)
            if not session:
                return False, None
            
            # Check if session is active and not expired
            if not session.is_active or datetime.now() > session.expires_at:
                self._invalidate_session(session_token)
                return False, None
            
            # Update last activity
            self._update_session_activity(session_token)
            
            # Get user information
            user_auth = self.get_user_auth_by_id(session.user_id)
            if not user_auth:
                return False, None
            
            # Get user roles and permissions
            roles = self.get_user_roles(session.user_id)
            permissions = self.get_user_permissions(session.user_id)
            
            user_info = {
                "user_id": session.user_id,
                "email": user_auth.email,
                "roles": [role.name for role in roles],
                "permissions": [perm.value for perm in permissions],
                "session_token": session_token
            }
            
            return True, user_info
            
        except Exception:
            return False, None
    
    def logout_user(self, session_token: str) -> bool:
        """
        Logout a user by invalidating their session.
        
        Args:
            session_token: Session token to invalidate
            
        Returns:
            True if logout successful, False otherwise
        """
        try:
            return self._invalidate_session(session_token)
        except Exception:
            return False
    
    def has_permission(self, user_id: int, permission: Permission) -> bool:
        """
        Check if a user has a specific permission.
        
        Args:
            user_id: User ID
            permission: Permission to check
            
        Returns:
            True if user has permission, False otherwise
        """
        try:
            user_permissions = self.get_user_permissions(user_id)
            return permission in user_permissions
        except Exception:
            return False
    
    def has_role(self, user_id: int, role_name: str) -> bool:
        """
        Check if a user has a specific role.
        
        Args:
            user_id: User ID
            role_name: Role name to check
            
        Returns:
            True if user has role, False otherwise
        """
        try:
            user_roles = self.get_user_roles(user_id)
            return any(role.name == role_name for role in user_roles)
        except Exception:
            return False
    
    def get_user_auth_by_email(self, email: str) -> Optional[UserAuth]:
        """Get user authentication record by email (case-insensitive)."""
        try:
            # Normalize email for case-insensitive lookup
            email = email.lower().strip()
            results = self.connector.execute_query(
                "SELECT * FROM user_auth WHERE LOWER(email) = ?", (email,)
            )
            if results:
                return self._row_to_user_auth(results[0])
            return None
        except Exception:
            return None
    
    def get_user_auth_by_id(self, user_id: int) -> Optional[UserAuth]:
        """Get user authentication record by ID."""
        try:
            results = self.connector.execute_query(
                "SELECT * FROM user_auth WHERE id = ?", (user_id,)
            )
            if results:
                return self._row_to_user_auth(results[0])
            return None
        except Exception:
            return None
    
    def get_session_by_token(self, session_token: str) -> Optional[Session]:
        """Get session by token."""
        try:
            results = self.connector.execute_query(
                "SELECT * FROM sessions WHERE session_token = ?", (session_token,)
            )
            if results:
                return self._row_to_session(results[0])
            return None
        except Exception:
            return None
    
    def get_user_roles(self, user_id: int) -> List[Role]:
        """Get all roles assigned to a user."""
        try:
            query = """
                SELECT r.* FROM roles r
                JOIN user_roles ur ON r.id = ur.role_id
                WHERE ur.user_id = ? AND ur.is_active = 1
                AND (ur.expires_at IS NULL OR ur.expires_at > ?)
            """
            results = self.connector.execute_query(query, (user_id, datetime.now().isoformat()))
            return [self._row_to_role(row) for row in results]
        except Exception:
            return []
    
    def get_user_permissions(self, user_id: int) -> Set[Permission]:
        """Get all permissions for a user based on their roles."""
        try:
            roles = self.get_user_roles(user_id)
            permissions = set()
            for role in roles:
                permissions.update(role.permissions)
            return permissions
        except Exception:
            return set()
    
    def _insert_user_auth(self, user_auth: UserAuth) -> Optional[int]:
        """Insert a new user auth record and return the ID."""
        try:
            query = """
                INSERT INTO user_auth (email, password_hash, salt, status, created_at, password_changed_at, email_verified)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            """
            self.connector.execute_update(query, (
                user_auth.email,
                user_auth.password_hash,
                user_auth.salt,
                user_auth.status.value,
                user_auth.created_at.isoformat(),
                user_auth.password_changed_at.isoformat(),
                1 if user_auth.email_verified else 0
            ))
            
            # Get the inserted ID
            results = self.connector.execute_query(
                "SELECT last_insert_rowid() as id"
            )
            return results[0]["id"] if results else None
        except Exception:
            return None
    
    def _get_role_id_by_name(self, role_name: str) -> Optional[int]:
        """Get role ID by name."""
        try:
            results = self.connector.execute_query(
                "SELECT id FROM roles WHERE name = ?", (role_name,)
            )
            return results[0]["id"] if results else None
        except Exception:
            return None
    
    def _assign_role_to_user(self, user_id: int, role_id: int) -> bool:
        """Assign a role to a user."""
        try:
            query = """
                INSERT INTO user_roles (user_id, role_id, assigned_at)
                VALUES (?, ?, ?)
            """
            self.connector.execute_update(query, (
                user_id, role_id, datetime.now().isoformat()
            ))
            return True
        except Exception:
            return False
    
    def _create_session(self, user_id: int, ip_address: str = None, 
                       user_agent: str = None) -> Session:
        """Create a new session for a user."""
        session_token = AuthUtils.generate_session_token()
        expires_at = datetime.now() + self.session_timeout
        
        query = """
            INSERT INTO sessions (session_token, user_id, created_at, expires_at, ip_address, user_agent, last_activity)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """
        self.connector.execute_update(query, (
            session_token,
            user_id,
            datetime.now().isoformat(),
            expires_at.isoformat(),
            ip_address,
            user_agent,
            datetime.now().isoformat()
        ))
        
        return Session(
            session_token=session_token,
            user_id=user_id,
            created_at=datetime.now(),
            expires_at=expires_at,
            ip_address=ip_address,
            user_agent=user_agent
        )
    
    def _handle_failed_login(self, user_auth: UserAuth, ip_address: str = None, user_agent: str = None) -> None:
        """Handle a failed login attempt."""
        new_attempts = user_auth.failed_login_attempts + 1
        
        if new_attempts >= self.max_failed_attempts:
            # Lock account
            locked_until = datetime.now() + self.lockout_duration
            self.connector.execute_update(
                """
                UPDATE user_auth 
                SET failed_login_attempts = ?, status = ?, locked_until = ?
                WHERE id = ?
                """,
                (new_attempts, AuthStatus.LOCKED.value, locked_until.isoformat(), user_auth.id)
            )
        else:
            # Just increment failed attempts
            self.connector.execute_update(
                "UPDATE user_auth SET failed_login_attempts = ? WHERE id = ?",
                (new_attempts, user_auth.id)
            )
    
    def _reset_failed_attempts(self, user_id: int) -> None:
        """Reset failed login attempts for a user."""
        self.connector.execute_update(
            "UPDATE user_auth SET failed_login_attempts = 0 WHERE id = ?",
            (user_id,)
        )
    
    def _unlock_account(self, user_id: int) -> None:
        """Unlock a user account."""
        self.connector.execute_update(
            """
            UPDATE user_auth 
            SET status = ?, locked_until = NULL, failed_login_attempts = 0
            WHERE id = ?
            """,
            (AuthStatus.ACTIVE.value, user_id)
        )
    
    def _update_last_login(self, user_id: int) -> None:
        """Update the last login timestamp for a user."""
        self.connector.execute_update(
            "UPDATE user_auth SET last_login = ? WHERE id = ?",
            (datetime.now().isoformat(), user_id)
        )
    
    def _record_login_attempt(self, email: str, ip_address: str = None, user_agent: str = None, 
                            success: bool = False, failure_reason: str = None) -> None:
        """Record a login attempt."""
        # Normalize email for consistent storage
        email = email.lower().strip()
        query = """
            INSERT INTO login_attempts (email, ip_address, user_agent, success, attempted_at, failure_reason)
            VALUES (?, ?, ?, ?, ?, ?)
        """
        self.connector.execute_update(query, (
            email, ip_address, user_agent, success, 
            datetime.now().isoformat(), failure_reason
        ))
    
    def _invalidate_session(self, session_token: str) -> bool:
        """Invalidate a session."""
        try:
            self.connector.execute_update(
                "UPDATE sessions SET is_active = 0 WHERE session_token = ?",
                (session_token,)
            )
            return True
        except Exception:
            return False
    
    def _update_session_activity(self, session_token: str) -> None:
        """Update the last activity timestamp for a session."""
        self.connector.execute_update(
            "UPDATE sessions SET last_activity = ? WHERE session_token = ?",
            (datetime.now().isoformat(), session_token)
        )
    
    def _row_to_user_auth(self, row: Dict[str, Any]) -> UserAuth:
        """Convert database row to UserAuth object."""
        return UserAuth(
            id=row["id"],
            email=row["email"],
            password_hash=row["password_hash"],
            salt=row["salt"],
            status=AuthStatus(row["status"]),
            failed_login_attempts=row["failed_login_attempts"],
            locked_until=datetime.fromisoformat(row["locked_until"]) if row["locked_until"] else None,
            password_changed_at=datetime.fromisoformat(row["password_changed_at"]),
            created_at=datetime.fromisoformat(row["created_at"]),
            last_login=datetime.fromisoformat(row["last_login"]) if row["last_login"] else None,
            email_verified=bool(row["email_verified"]),
            verification_token=row["verification_token"]
        )
    
    def _row_to_session(self, row: Dict[str, Any]) -> Session:
        """Convert database row to Session object."""
        return Session(
            id=row["id"],
            session_token=row["session_token"],
            user_id=row["user_id"],
            created_at=datetime.fromisoformat(row["created_at"]),
            expires_at=datetime.fromisoformat(row["expires_at"]),
            ip_address=row["ip_address"],
            user_agent=row["user_agent"],
            is_active=bool(row["is_active"]),
            last_activity=datetime.fromisoformat(row["last_activity"])
        )
    
    def _row_to_role(self, row: Dict[str, Any]) -> Role:
        """Convert database row to Role object."""
        permissions_str = row["permissions"]
        permissions = set(Permission(p.strip()) for p in permissions_str.split(","))
        
        return Role(
            id=row["id"],
            name=row["name"],
            description=row["description"],
            permissions=permissions,
            is_default=bool(row["is_default"]),
            created_at=datetime.fromisoformat(row["created_at"]),
            updated_at=datetime.fromisoformat(row["updated_at"])
        ) 