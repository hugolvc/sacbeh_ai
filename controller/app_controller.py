"""
Singleton controller for the Sacbeh application.
Manages application state and coordinates between view and model components.
"""

from typing import Dict, Any, Optional
from model.data_models import User, AppState


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