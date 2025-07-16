"""
Authorization models for the Sacbeh application.
Defines authentication and authorization data structures.
"""

from datetime import datetime, timedelta
from typing import Optional, List, Dict, Any, Set
from pydantic import BaseModel, EmailStr, Field, validator, SecretStr
from enum import Enum
import hashlib
import secrets


class Permission(str, Enum):
    """System permissions enumeration."""
    READ = "read"
    WRITE = "write"
    DELETE = "delete"
    ADMIN = "admin"
    USER_MANAGEMENT = "user_management"
    SYSTEM_CONFIG = "system_config"


class AuthStatus(str, Enum):
    """Authentication status enumeration."""
    ACTIVE = "active"
    LOCKED = "locked"
    EXPIRED = "expired"
    PENDING_VERIFICATION = "pending_verification"


class UserAuth(BaseModel):
    """
    User authentication model with secure password handling.
    """
    id: Optional[int] = Field(default=None, description="Unique user ID")
    email: EmailStr = Field(..., description="User's email address")
    password_hash: str = Field(..., description="Hashed password")
    salt: str = Field(..., description="Password salt for security")
    status: AuthStatus = Field(default=AuthStatus.ACTIVE, description="Authentication status")
    failed_login_attempts: int = Field(default=0, description="Number of failed login attempts")
    locked_until: Optional[datetime] = Field(default=None, description="Account lock expiration")
    password_changed_at: datetime = Field(default_factory=datetime.now, description="Password change timestamp")
    created_at: datetime = Field(default_factory=datetime.now, description="Account creation timestamp")
    last_login: Optional[datetime] = Field(default=None, description="Last successful login")
    email_verified: bool = Field(default=False, description="Email verification status")
    verification_token: Optional[str] = Field(default=None, description="Email verification token")
    
    @validator('password_hash')
    def validate_password_hash(cls, v):
        """Validate password hash format."""
        if len(v) != 64:  # SHA-256 hash length
            raise ValueError('Invalid password hash format')
        return v
    
    @validator('salt')
    def validate_salt(cls, v):
        """Validate salt format."""
        if len(v) != 32:  # 32-character salt
            raise ValueError('Invalid salt format')
        return v
    
    class Config:
        json_encoders = {
            datetime: lambda v: v.isoformat()
        }


class Role(BaseModel):
    """
    Role model defining user roles and their permissions.
    """
    id: Optional[int] = Field(default=None, description="Unique role ID")
    name: str = Field(..., min_length=1, max_length=50, description="Role name")
    description: str = Field(..., max_length=200, description="Role description")
    permissions: Set[Permission] = Field(default_factory=set, description="Role permissions")
    is_default: bool = Field(default=False, description="Whether this is a default role")
    created_at: datetime = Field(default_factory=datetime.now, description="Role creation timestamp")
    updated_at: datetime = Field(default_factory=datetime.now, description="Last update timestamp")
    
    @validator('name')
    def validate_name(cls, v):
        """Validate role name format."""
        if not v.replace('_', '').replace('-', '').isalnum():
            raise ValueError('Role name must contain only alphanumeric characters, underscores, and hyphens')
        return v.lower()
    
    class Config:
        json_encoders = {
            datetime: lambda v: v.isoformat()
        }


class UserRole(BaseModel):
    """
    User-role association model for many-to-many relationship.
    """
    id: Optional[int] = Field(default=None, description="Unique association ID")
    user_id: int = Field(..., description="User ID")
    role_id: int = Field(..., description="Role ID")
    assigned_at: datetime = Field(default_factory=datetime.now, description="Role assignment timestamp")
    assigned_by: Optional[int] = Field(default=None, description="ID of user who assigned this role")
    expires_at: Optional[datetime] = Field(default=None, description="Role expiration timestamp")
    is_active: bool = Field(default=True, description="Whether this role assignment is active")
    
    class Config:
        json_encoders = {
            datetime: lambda v: v.isoformat()
        }


class Session(BaseModel):
    """
    User session model for managing active sessions.
    """
    id: Optional[int] = Field(default=None, description="Unique session ID")
    session_token: str = Field(..., description="Unique session token")
    user_id: int = Field(..., description="User ID")
    created_at: datetime = Field(default_factory=datetime.now, description="Session creation timestamp")
    expires_at: datetime = Field(..., description="Session expiration timestamp")
    ip_address: Optional[str] = Field(default=None, description="IP address of session")
    user_agent: Optional[str] = Field(default=None, description="User agent string")
    is_active: bool = Field(default=True, description="Whether session is active")
    last_activity: datetime = Field(default_factory=datetime.now, description="Last activity timestamp")
    
    @validator('session_token')
    def validate_session_token(cls, v):
        """Validate session token format."""
        if len(v) != 64:  # 64-character token
            raise ValueError('Invalid session token format')
        return v
    
    @validator('expires_at')
    def validate_expires_at(cls, v, values):
        """Validate that expiration time is after creation time."""
        if 'created_at' in values and v <= values['created_at']:
            raise ValueError('Expiration time must be after creation time')
        return v
    
    class Config:
        json_encoders = {
            datetime: lambda v: v.isoformat()
        }


class LoginAttempt(BaseModel):
    """
    Login attempt tracking model for security monitoring.
    """
    id: Optional[int] = Field(default=None, description="Unique attempt ID")
    email: EmailStr = Field(..., description="Email used in login attempt")
    ip_address: str = Field(..., description="IP address of the attempt")
    user_agent: Optional[str] = Field(default=None, description="User agent string")
    success: bool = Field(..., description="Whether login was successful")
    attempted_at: datetime = Field(default_factory=datetime.now, description="Attempt timestamp")
    failure_reason: Optional[str] = Field(default=None, description="Reason for failure if unsuccessful")
    
    class Config:
        json_encoders = {
            datetime: lambda v: v.isoformat()
        }


# Authentication utility functions
class AuthUtils:
    """Utility class for authentication operations."""
    
    @staticmethod
    def hash_password(password: str, salt: Optional[str] = None) -> tuple[str, str]:
        """
        Hash a password with salt.
        
        Args:
            password: Plain text password
            salt: Optional salt (generated if not provided)
            
        Returns:
            Tuple of (password_hash, salt)
        """
        if salt is None:
            salt = secrets.token_hex(16)  # 32-character hex string
        
        # Combine password and salt
        salted_password = password + salt
        
        # Create SHA-256 hash
        password_hash = hashlib.sha256(salted_password.encode()).hexdigest()
        
        return password_hash, salt
    
    @staticmethod
    def verify_password(password: str, password_hash: str, salt: str) -> bool:
        """
        Verify a password against its hash and salt.
        
        Args:
            password: Plain text password to verify
            password_hash: Stored password hash
            salt: Stored password salt
            
        Returns:
            True if password matches, False otherwise
        """
        expected_hash, _ = AuthUtils.hash_password(password, salt)
        return expected_hash == password_hash
    
    @staticmethod
    def generate_session_token() -> str:
        """
        Generate a secure session token.
        
        Returns:
            64-character hex string token
        """
        return secrets.token_hex(32)
    
    @staticmethod
    def generate_verification_token() -> str:
        """
        Generate a verification token for email verification.
        
        Returns:
            32-character hex string token
        """
        return secrets.token_hex(16)
    
    @staticmethod
    def is_password_strong(password: str) -> tuple[bool, List[str]]:
        """
        Check if a password meets security requirements.
        
        Args:
            password: Password to check
            
        Returns:
            Tuple of (is_strong, list_of_issues)
        """
        issues = []
        
        if len(password) < 8:
            issues.append("Password must be at least 8 characters long")
        
        if not any(c.isupper() for c in password):
            issues.append("Password must contain at least one uppercase letter")
        
        if not any(c.islower() for c in password):
            issues.append("Password must contain at least one lowercase letter")
        
        if not any(c.isdigit() for c in password):
            issues.append("Password must contain at least one digit")
        
        if not any(c in "!@#$%^&*()_+-=[]{}|;:,.<>?" for c in password):
            issues.append("Password must contain at least one special character")
        
        return len(issues) == 0, issues 