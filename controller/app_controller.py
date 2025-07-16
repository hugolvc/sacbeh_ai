"""
Singleton controller for the Sacbeh application.
Manages application state and coordinates between view and model components.
"""

from typing import Dict, Any, Optional
from model.data_models import User, AppState
from controller.auth_controller import AuthController


class AppController:
    """
    Singleton controller that manages the application state and model interactions.
    This controller is shared among all pages of the view and exclusively manages the model.
    """
    
    _instance: Optional['AppController'] = None
    _initialized: bool = False
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(AppController, cls).__new__(cls)
        return cls._instance
    
    def __init__(self):
        if not self._initialized:
            self._app_state = AppState()
            self._users: Dict[str, User] = {}
            self._session_data: Dict[str, Any] = {}
            self._auth_controller = AuthController()
            self._initialized = True
    
    @property
    def app_state(self) -> AppState:
        """Get the current application state."""
        return self._app_state
    
    @property
    def users(self) -> Dict[str, User]:
        """Get all registered users."""
        return self._users.copy()
    
    @property
    def session_data(self) -> Dict[str, Any]:
        """Get current session data."""
        return self._session_data.copy()
    
    @property
    def auth_controller(self) -> AuthController:
        """Get the authorization controller."""
        return self._auth_controller
    
    def add_user(self, user: User) -> bool:
        """
        Add a new user to the system.
        
        Args:
            user: User object to add
            
        Returns:
            bool: True if user was added successfully, False if user already exists
        """
        if user.email in self._users:
            return False
        
        self._users[user.email] = user
        return True
    
    def get_user(self, email: str) -> Optional[User]:
        """
        Get a user by email.
        
        Args:
            email: User's email address
            
        Returns:
            User object if found, None otherwise
        """
        return self._users.get(email)
    
    def update_app_state(self, **kwargs) -> None:
        """
        Update the application state with new values.
        
        Args:
            **kwargs: Key-value pairs to update in the app state
        """
        for key, value in kwargs.items():
            if hasattr(self._app_state, key):
                setattr(self._app_state, key, value)
    
    def set_session_data(self, key: str, value: Any) -> None:
        """
        Set session data for the current user session.
        
        Args:
            key: Session data key
            value: Session data value
        """
        self._session_data[key] = value
    
    def get_session_data(self, key: str, default: Any = None) -> Any:
        """
        Get session data for the current user session.
        
        Args:
            key: Session data key
            default: Default value if key doesn't exist
            
        Returns:
            Session data value or default
        """
        return self._session_data.get(key, default)
    
    def clear_session_data(self) -> None:
        """Clear all session data."""
        self._session_data.clear()
    
    def get_app_info(self) -> Dict[str, Any]:
        """
        Get application information for display.
        
        Returns:
            Dictionary containing app information
        """
        return {
            "name": "Sacbeh",
            "version": "1.0.0",
            "architecture": "MVC",
            "total_users": len(self._users),
            "app_state": self._app_state.dict()
        }
    
    # Authorization convenience methods
    def is_authenticated(self) -> bool:
        """Check if a user is currently authenticated."""
        return self._auth_controller.is_authenticated()
    
    def get_current_user(self) -> Optional[Dict[str, Any]]:
        """Get information about the currently authenticated user."""
        return self._auth_controller.get_current_user()
    
    def login_user(self, email: str, password: str, 
                   ip_address: str = None, user_agent: str = None) -> tuple[bool, str]:
        """Authenticate a user and create a session."""
        return self._auth_controller.login_user(email, password, ip_address, user_agent)
    
    def logout_user(self) -> bool:
        """Logout the current user."""
        return self._auth_controller.logout_user()
    
    def register_user(self, email: str, password: str, name: str, 
                     role: str = "user") -> tuple[bool, str]:
        """Register a new user in the system."""
        from model.data_models import UserRole as UserRoleEnum
        role_enum = UserRoleEnum(role)
        return self._auth_controller.register_user(email, password, name, role_enum)
    
    def has_permission(self, permission: str) -> bool:
        """Check if the current user has a specific permission."""
        from model.auth_models import Permission as PermissionEnum
        permission_enum = PermissionEnum(permission)
        return self._auth_controller.has_permission(permission_enum)
    
    def has_role(self, role_name: str) -> bool:
        """Check if the current user has a specific role."""
        return self._auth_controller.has_role(role_name)
    
    def get_user_permissions(self) -> list[str]:
        """Get all permissions for the current user."""
        return self._auth_controller.get_user_permissions()
    
    def get_user_roles(self) -> list[str]:
        """Get all roles for the current user."""
        return self._auth_controller.get_user_roles()
    
    def verify_session(self, session_token: str) -> bool:
        """Verify if a session token is valid."""
        return self._auth_controller.verify_session(session_token)
    
    def get_session_token(self) -> Optional[str]:
        """Get the current session token."""
        return self._auth_controller.get_session_token() 