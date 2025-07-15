"""
Main entry point for the Sacbeh application.
Initializes the MVC components and starts the Streamlit server.
"""

import streamlit as st
import sys
from pathlib import Path
from controller.app_controller import AppController
from view.pages.welcome import render_welcome_page
from view.pages.login import render_login_page
from model.data_models import User, UserRole, UserStatus

# Add the project root to Python path to ensure imports work correctly
project_root = Path(__file__).parent
if str(project_root) not in sys.path:
    sys.path.insert(0, str(project_root))


def initialize_application():
    """
    Initialize the application and its components.
    This function sets up the controller and any necessary application state.
    """
    try:
        # Initialize the singleton controller
        controller = AppController()
        
        # Set up initial application state
        controller.update_app_state(
            debug_mode=False,
            maintenance_mode=False,
            features_enabled=["welcome_page", "user_management", "data_validation"]
        )
        
        # Add some sample users for demonstration
        
        sample_users = [
            User(
                email="admin@sacbeh.com",
                name="Admin User",
                role=UserRole.ADMIN,
                status=UserStatus.ACTIVE
            ),
            User(
                email="user@sacbeh.com",
                name="Regular User",
                role=UserRole.USER,
                status=UserStatus.ACTIVE
            ),
            User(
                email="guest@sacbeh.com",
                name="Guest User",
                role=UserRole.GUEST,
                status=UserStatus.ACTIVE
            )
        ]
        
        for user in sample_users:
            controller.add_user(user)
        
        return True
        
    except Exception as e:
        st.error(f"❌ Failed to initialize application: {str(e)}")
        return False


def main():
    """
    Main function that runs the Sacbeh application.
    """
    # Application title and configuration
    st.set_page_config(
        page_title="Sacbeh - MVC Application",
        page_icon="🏛️",
        layout="wide",
        initial_sidebar_state="expanded"
    )
    
    # Custom CSS for consistent styling
    st.markdown("""
    <style>
    .stApp {
        background-color: #f8f9fa;
    }
    .main .block-container {
        padding-top: 2rem;
        padding-bottom: 2rem;
    }
    .stButton > button {
        border-radius: 8px;
        font-weight: 500;
    }
    .stAlert {
        border-radius: 8px;
    }
    </style>
    """, unsafe_allow_html=True)
    
    # Initialize the application
    if initialize_application():
        # Handle page routing
        if 'current_page' not in st.session_state:
            st.session_state.current_page = 'welcome'
        
        # Check for page navigation
        if 'navigate_to' in st.session_state:
            st.session_state.current_page = st.session_state.navigate_to
            del st.session_state.navigate_to
        
        # Render the appropriate page
        if st.session_state.current_page == 'login':
            render_login_page()
        else:
            render_welcome_page()
    else:
        # Show error page if initialization fails
        st.error("""
        ## Application Initialization Failed
        
        The Sacbeh application could not be started. Please check:
        
        1. All dependencies are installed: `pip install -r requirements.txt`
        2. Python version is 3.8 or higher
        3. All required files are present in the project directory
        
        If the problem persists, please check the console output for more details.
        """)


if __name__ == "__main__":
    main() 