"""
Pydantic models for the Sacbeh application.
Defines the data structures used throughout the application.
"""

from datetime import datetime
from typing import Optional, List, Dict, Any
from pydantic import BaseModel, EmailStr, Field, validator
from enum import Enum


class UserRole(str, Enum):
    """User roles enumeration."""
    ADMIN = "admin"
    USER = "user"
    GUEST = "guest"


class UserStatus(str, Enum):
    """User status enumeration."""
    ACTIVE = "active"
    INACTIVE = "inactive"
    SUSPENDED = "suspended"


class AppTheme(str, Enum):
    """Application theme options."""
    LIGHT = "light"
    DARK = "dark"
    SYSTEM = "system"


class User(BaseModel):
    """
    User model representing application users.
    """
    email: EmailStr = Field(..., description="User's email address")
    name: str = Field(..., min_length=1, max_length=100, description="User's full name")
    role: UserRole = Field(default=UserRole.USER, description="User's role in the system")
    status: UserStatus = Field(default=UserStatus.ACTIVE, description="User's current status")
    created_at: datetime = Field(default_factory=datetime.now, description="User creation timestamp")
    last_login: Optional[datetime] = Field(default=None, description="Last login timestamp")
    preferences: Dict[str, Any] = Field(default_factory=dict, description="User preferences")
    
    @validator('name')
    def validate_name(cls, v):
        """Validate that name contains only letters and spaces."""
        if not v.replace(' ', '').isalpha():
            raise ValueError('Name must contain only letters and spaces')
        return v.title()
    
    class Config:
        json_encoders = {
            datetime: lambda v: v.isoformat()
        }


class AppState(BaseModel):
    """
    Application state model for managing global application state.
    """
    theme: AppTheme = Field(default=AppTheme.SYSTEM, description="Current application theme")
    language: str = Field(default="en", description="Current application language")
    debug_mode: bool = Field(default=False, description="Debug mode status")
    maintenance_mode: bool = Field(default=False, description="Maintenance mode status")
    last_updated: datetime = Field(default_factory=datetime.now, description="Last state update timestamp")
    features_enabled: List[str] = Field(default_factory=list, description="List of enabled features")
    config: Dict[str, Any] = Field(default_factory=dict, description="Application configuration")
    
    class Config:
        json_encoders = {
            datetime: lambda v: v.isoformat()
        }


class SessionData(BaseModel):
    """
    Session data model for managing user session information.
    """
    user_id: Optional[str] = Field(default=None, description="Current user ID")
    session_id: str = Field(..., description="Unique session identifier")
    created_at: datetime = Field(default_factory=datetime.now, description="Session creation timestamp")
    expires_at: datetime = Field(..., description="Session expiration timestamp")
    data: Dict[str, Any] = Field(default_factory=dict, description="Session-specific data")
    
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


# Raw Python data structures (as mentioned in requirements)
class RawDataStructures:
    """
    Container for raw Python data structures used in the application.
    """
    
    # Application constants
    APP_CONSTANTS = {
        "MAX_FILE_SIZE": 10 * 1024 * 1024,  # 10MB
        "SUPPORTED_FORMATS": [".txt", ".pdf", ".doc", ".docx"],
        "DEFAULT_TIMEOUT": 30,
        "MAX_RETRIES": 3
    }
    
    # Feature flags
    FEATURE_FLAGS = {
        "advanced_search": True,
        "file_upload": True,
        "real_time_notifications": False,
        "dark_mode": True,
        "multi_language": False
    }
    
    # UI configuration
    UI_CONFIG = {
        "sidebar_width": 300,
        "main_content_width": 800,
        "max_display_items": 50,
        "refresh_interval": 5000
    }
    
    # Error messages
    ERROR_MESSAGES = {
        "user_not_found": "User not found in the system",
        "invalid_credentials": "Invalid email or password",
        "session_expired": "Your session has expired. Please log in again",
        "permission_denied": "You don't have permission to perform this action",
        "server_error": "An internal server error occurred"
    }
    
    # Success messages
    SUCCESS_MESSAGES = {
        "user_created": "User created successfully",
        "user_updated": "User updated successfully",
        "user_deleted": "User deleted successfully",
        "login_success": "Login successful",
        "logout_success": "Logout successful"
    } 