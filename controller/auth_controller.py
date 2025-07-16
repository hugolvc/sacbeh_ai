"""
Authorization controller for handling authentication and authorization operations.
Acts as the interface between the view and the authorization service.
"""

from typing import Optional, Dict, Any, List, Tuple
from datetime import datetime

from model.auth_service import AuthService
from model.auth_models import Permission, AuthStatus
from model.data_models import User, UserRole as UserRoleEnum
from model.data_connectors import DatabaseConnectorFactory


class AuthController:
    """
    Controller for handling authentication and authorization operations.
    Provides a clean interface for the view layer to interact with authentication.
    """
    
    def __init__(self, connector_type: str = "sqlite", **connector_kwargs):
        """
        Initialize the auth controller with a database connector.
        
        Args:
            connector_type: Type of database connector to use
            **connector_kwargs: Additional arguments for the connector
        """
        connector = DatabaseConnectorFactory.create_connector(connector_type, **connector_kwargs)
        self.auth_service = AuthService(connector)
        self._current_user: Optional[Dict[str, Any]] = None
        self._current_session_token: Optional[str] = None
    
    def register_user(self, email: str, password: str, name: str, 
                     role: UserRoleEnum = UserRoleEnum.USER) -> Tuple[bool, str]:
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
        return self.auth_service.register_user(email, password, name, role)
    
    def login_user(self, email: str, password: str, 
                   ip_address: str = None, user_agent: str = None) -> Tuple[bool, str]:
        """
        Authenticate a user and create a session.
        
        Args:
            email: User's email address
            password: Plain text password
            ip_address: IP address of the login attempt
            user_agent: User agent string
            
        Returns:
            Tuple of (success, message)
        """
        success, message, session = self.auth_service.authenticate_user(
            email, password, ip_address, user_agent
        )
        
        if success and session:
            self._current_session_token = session.session_token
            # Get user info for current session
            self._refresh_current_user()
        
        return success, message
    
    def logout_user(self) -> bool:
        """
        Logout the current user.
        
        Returns:
            True if logout successful, False otherwise
        """
        if self._current_session_token:
            success = self.auth_service.logout_user(self._current_session_token)
            if success:
                self._current_user = None
                self._current_session_token = None
            return success
        return True
    
    def verify_session(self, session_token: str) -> bool:
        """
        Verify if a session token is valid and set current user.
        
        Args:
            session_token: Session token to verify
            
        Returns:
            True if session is valid, False otherwise
        """
        is_valid, user_info = self.auth_service.verify_session(session_token)
        
        if is_valid:
            self._current_session_token = session_token
            self._current_user = user_info
            return True
        
        return False
    
    def get_current_user(self) -> Optional[Dict[str, Any]]:
        """
        Get information about the currently authenticated user.
        
        Returns:
            User information dictionary or None if not authenticated
        """
        return self._current_user
    
    def is_authenticated(self) -> bool:
        """
        Check if a user is currently authenticated.
        
        Returns:
            True if user is authenticated, False otherwise
        """
        return self._current_user is not None
    
    def has_permission(self, permission: Permission) -> bool:
        """
        Check if the current user has a specific permission.
        
        Args:
            permission: Permission to check
            
        Returns:
            True if user has permission, False otherwise
        """
        if not self.is_authenticated():
            return False
        
        return self.auth_service.has_permission(
            self._current_user["user_id"], permission
        )
    
    def has_role(self, role_name: str) -> bool:
        """
        Check if the current user has a specific role.
        
        Args:
            role_name: Role name to check
            
        Returns:
            True if user has role, False otherwise
        """
        if not self.is_authenticated():
            return False
        
        return self.auth_service.has_role(
            self._current_user["user_id"], role_name
        )
    
    def get_user_permissions(self) -> List[str]:
        """
        Get all permissions for the current user.
        
        Returns:
            List of permission names
        """
        if not self.is_authenticated():
            return []
        
        return self._current_user.get("permissions", [])
    
    def get_user_roles(self) -> List[str]:
        """
        Get all roles for the current user.
        
        Returns:
            List of role names
        """
        if not self.is_authenticated():
            return []
        
        return self._current_user.get("roles", [])
    
    def require_authentication(self) -> bool:
        """
        Check if user authentication is required for the current operation.
        This is a placeholder for future implementation of authentication requirements.
        
        Returns:
            True if authentication is required, False otherwise
        """
        return True
    
    def require_permission(self, permission: Permission) -> bool:
        """
        Check if the current user has the required permission.
        
        Args:
            permission: Required permission
            
        Returns:
            True if user has permission, False otherwise
        """
        return self.has_permission(permission)
    
    def require_role(self, role_name: str) -> bool:
        """
        Check if the current user has the required role.
        
        Args:
            role_name: Required role name
            
        Returns:
            True if user has role, False otherwise
        """
        return self.has_role(role_name)
    
    def get_session_token(self) -> Optional[str]:
        """
        Get the current session token.
        
        Returns:
            Current session token or None if not authenticated
        """
        return self._current_session_token
    
    def set_session_token(self, session_token: str) -> bool:
        """
        Set a session token and verify it.
        
        Args:
            session_token: Session token to set
            
        Returns:
            True if token is valid, False otherwise
        """
        return self.verify_session(session_token)
    
    def _refresh_current_user(self) -> None:
        """Refresh the current user information from the session."""
        if self._current_session_token:
            is_valid, user_info = self.auth_service.verify_session(self._current_session_token)
            if is_valid:
                self._current_user = user_info
            else:
                self._current_user = None
                self._current_session_token = None
    
    def get_user_by_email(self, email: str) -> Optional[Dict[str, Any]]:
        """
        Get user information by email (for admin purposes).
        
        Args:
            email: User's email address
            
        Returns:
            User information dictionary or None if not found
        """
        if not self.has_permission(Permission.USER_MANAGEMENT):
            return None
        
        user_auth = self.auth_service.get_user_auth_by_email(email)
        if user_auth:
            roles = self.auth_service.get_user_roles(user_auth.id)
            permissions = self.auth_service.get_user_permissions(user_auth.id)
            
            return {
                "id": user_auth.id,
                "email": user_auth.email,
                "status": user_auth.status.value,
                "roles": [role.name for role in roles],
                "permissions": [perm.value for perm in permissions],
                "created_at": user_auth.created_at.isoformat(),
                "last_login": user_auth.last_login.isoformat() if user_auth.last_login else None,
                "email_verified": user_auth.email_verified
            }
        
        return None
    
    def get_all_users(self) -> List[Dict[str, Any]]:
        """
        Get all users in the system (for admin purposes).
        
        Returns:
            List of user information dictionaries
        """
        if not self.has_permission(Permission.USER_MANAGEMENT):
            return []
        
        # This would need to be implemented in the auth service
        # For now, return empty list
        return []
    
    def change_user_status(self, user_id: int, status: AuthStatus) -> bool:
        """
        Change a user's authentication status (for admin purposes).
        
        Args:
            user_id: User ID
            status: New status
            
        Returns:
            True if status changed successfully, False otherwise
        """
        if not self.has_permission(Permission.USER_MANAGEMENT):
            return False
        
        # This would need to be implemented in the auth service
        # For now, return False
        return False
    
    def assign_role_to_user(self, user_id: int, role_name: str) -> bool:
        """
        Assign a role to a user (for admin purposes).
        
        Args:
            user_id: User ID
            role_name: Role name to assign
            
        Returns:
            True if role assigned successfully, False otherwise
        """
        if not self.has_permission(Permission.USER_MANAGEMENT):
            return False
        
        # This would need to be implemented in the auth service
        # For now, return False
        return False 