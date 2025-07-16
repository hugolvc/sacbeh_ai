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
from view.pages.register import render_register_page
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
            features_enabled=["welcome_page", "user_management", "data_validation", "authentication"]
        )
        
        # Initialize session state for authentication
        if 'session_token' not in st.session_state:
            st.session_state.session_token = None
        if 'logged_in' not in st.session_state:
            st.session_state.logged_in = False
        if 'user_email' not in st.session_state:
            st.session_state.user_email = None
        
        # Verify existing session if present
        if st.session_state.session_token:
            if controller.verify_session(st.session_state.session_token):
                st.session_state.logged_in = True
                current_user = controller.get_current_user()
                if current_user:
                    st.session_state.user_email = current_user.get('email')
            else:
                # Clear invalid session
                st.session_state.session_token = None
                st.session_state.logged_in = False
                st.session_state.user_email = None
        
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
    .user-info {
        background-color: rgba(0, 102, 204, 0.1);
        padding: 1rem;
        border-radius: 10px;
        border: 1px solid rgba(0, 102, 204, 0.2);
        margin-bottom: 1rem;
    }
    .logout-button {
        background-color: #dc3545 !important;
        color: white !important;
        border: none !important;
        padding: 0.5rem 1rem !important;
        border-radius: 5px !important;
        font-size: 0.9rem !important;
    }
    .logout-button:hover {
        background-color: #c82333 !important;
    }
    
    /* Global button styling for consistent appearance */
    [data-testid="stButton"] button[kind="primary"] {
        background: linear-gradient(135deg, #ff6600, #ff8533) !important;
        color: white !important;
        border: none !important;
        border-radius: 10px !important;
        font-weight: 600 !important;
        transition: all 0.3s ease !important;
    }
    [data-testid="stButton"] button[kind="primary"]:hover {
        transform: translateY(-2px) !important;
        box-shadow: 0 5px 15px rgba(255, 102, 0, 0.4) !important;
    }
    [data-testid="stButton"] button[kind="secondary"] {
        background: linear-gradient(135deg, #0066cc, #0052a3) !important;
        color: white !important;
        border: none !important;
        border-radius: 10px !important;
        font-weight: 600 !important;
        transition: all 0.3s ease !important;
    }
    [data-testid="stButton"] button[kind="secondary"]:hover {
        transform: translateY(-2px) !important;
        box-shadow: 0 5px 15px rgba(0, 102, 204, 0.4) !important;
    }
    </style>
    """, unsafe_allow_html=True)
    
    # Initialize the application
    if initialize_application():
        controller = AppController()
        
        # Handle page routing
        if 'current_page' not in st.session_state:
            st.session_state.current_page = 'welcome'
        
        # Check for page navigation
        if 'navigate_to' in st.session_state:
            st.session_state.current_page = st.session_state.navigate_to
            del st.session_state.navigate_to
        
        # Show user info and logout button if authenticated
        if st.session_state.logged_in and st.session_state.user_email:
            current_user = controller.get_current_user()
            if current_user:
                col1, col2 = st.columns([3, 1])
                with col1:
                    st.markdown(f"""
                    <div class="user-info">
                        <strong>Welcome, {st.session_state.user_email}</strong><br>
                        <small>Roles: {', '.join(current_user.get('roles', []))}</small><br>
                        <small>Permissions: {', '.join(current_user.get('permissions', []))}</small>
                    </div>
                    """, unsafe_allow_html=True)
                with col2:
                    if st.button("Logout", key="logout_btn", help="Click to logout"):
                        controller.logout_user()
                        st.session_state.session_token = None
                        st.session_state.logged_in = False
                        st.session_state.user_email = None
                        st.session_state.current_page = 'welcome'
                        st.rerun()
        
        # Render the appropriate page
        if st.session_state.current_page == 'login':
            render_login_page()
        elif st.session_state.current_page == 'register':
            render_register_page()
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