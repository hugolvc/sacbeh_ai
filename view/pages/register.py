"""
Registration page for the Sacbeh application.
Provides user registration functionality with validation and security features.
"""

import streamlit as st
from controller.app_controller import AppController
from model.auth_models import AuthUtils


def render_register_page():
    """
    Render the registration page with user registration form.
    """
    # Get the singleton controller instance
    controller = AppController()
    
    # Custom CSS for registration page
    st.markdown("""
    <style>
    .stApp {
        background-color: #2d2d2d !important;
        background-image: 
            radial-gradient(circle at 25% 25%, rgba(0, 102, 204, 0.03) 0%, transparent 50%),
            radial-gradient(circle at 75% 75%, rgba(0, 102, 204, 0.03) 0%, transparent 50%),
            linear-gradient(45deg, rgba(0, 102, 204, 0.02) 25%, transparent 25%, transparent 75%, rgba(0, 102, 204, 0.02) 75%),
            linear-gradient(45deg, rgba(0, 102, 204, 0.02) 25%, transparent 25%, transparent 75%, rgba(0, 102, 204, 0.02) 75%);
        background-size: 200px 200px, 200px 200px, 100px 100px, 100px 100px;
        background-position: 0 0, 100px 100px, 0 0, 50px 50px;
    }
    .main .block-container {
        background-color: transparent !important;
        padding: 0 2rem !important;
        margin: 0 !important;
        max-width: none !important;
    }

    .stTextInput > div > div > input {
        background-color: rgba(255, 255, 255, 0.1) !important;
        border: 1px solid rgba(0, 102, 204, 0.3) !important;
        color: #ffffff !important;
        border-radius: 10px !important;
    }
    .stTextInput > div > div > input:focus {
        border-color: #0066cc !important;
        box-shadow: 0 0 0 2px rgba(0, 102, 204, 0.2) !important;
    }
    .stButton > button {
        background: linear-gradient(135deg, #ff6600, #ff8533) !important;
        color: white !important;
        border: none !important;
        border-radius: 10px !important;
        font-weight: 600 !important;
        transition: all 0.3s ease !important;
    }
    .stButton > button:hover {
        transform: translateY(-2px) !important;
        box-shadow: 0 5px 15px rgba(255, 102, 0, 0.4) !important;
    }
    .stCheckbox > div > div {
        color: #ffffff !important;
    }
    .password-strength {
        padding: 0.5rem;
        border-radius: 5px;
        margin-top: 0.5rem;
        font-size: 0.8rem;
    }
    .strength-weak {
        background-color: rgba(255, 0, 0, 0.1);
        color: #ff6666;
        border: 1px solid rgba(255, 0, 0, 0.3);
    }
    .strength-medium {
        background-color: rgba(255, 165, 0, 0.1);
        color: #ffaa66;
        border: 1px solid rgba(255, 165, 0, 0.3);
    }
    .strength-strong {
        background-color: rgba(0, 255, 0, 0.1);
        color: #66ff66;
        border: 1px solid rgba(0, 255, 0, 0.3);
    }
    </style>
    """, unsafe_allow_html=True)
    
    # Back button
    if st.button("← Back", key="back_button"):
        st.session_state.navigate_to = 'login'
        st.rerun()
    
    # Position the back button with CSS
    st.markdown("""
    <style>
    [data-testid="stButton"] button[kind="secondary"] {
        position: fixed !important;
        top: 4rem !important;
        left: 2rem !important;
        z-index: 1000 !important;
        background: rgba(0, 102, 204, 0.2) !important;
        color: #ffffff !important;
        border: 1px solid rgba(0, 102, 204, 0.3) !important;
        padding: 0.5rem 1rem !important;
        border-radius: 15px !important;
        font-weight: 500 !important;
        transition: all 0.3s ease !important;
    }
    [data-testid="stButton"] button[kind="secondary"]:hover {
        background: rgba(0, 102, 204, 0.3) !important;
        transform: translateY(-1px) !important;
    }
    </style>
    """, unsafe_allow_html=True)
    
    # Add top padding to avoid development bar
    st.markdown("<div style='height: 6rem;'></div>", unsafe_allow_html=True)
    
    # Create columns to center the form
    col1, col2, col3 = st.columns([1, 1, 1])
    
    with col2:
        # Title
        st.markdown('<h2 style="color: #0066cc; text-align: center; margin-bottom: 2rem; font-size: 1.8rem;">Create Account</h2>', unsafe_allow_html=True)
        
        # Registration form
        with st.form("register_form"):
            name = st.text_input("Full Name", placeholder="Enter your full name")
            email = st.text_input("Email", placeholder="Enter your email address")
            password = st.text_input("Password", type="password", placeholder="Enter your password")
            confirm_password = st.text_input("Confirm Password", type="password", placeholder="Confirm your password")
            
            # Role selection
            role = st.selectbox(
                "Role",
                options=["user", "guest"],
                format_func=lambda x: x.title(),
                help="Select your role in the system"
            )
            
            # Terms and conditions
            agree_terms = st.checkbox("I agree to the Terms and Conditions")
            
            # Submit button
            submit_button = st.form_submit_button("Create Account")
            
            # Password strength indicator
            if password:
                is_strong, issues = AuthUtils.is_password_strong(password)
                if is_strong:
                    st.markdown('<div class="password-strength strength-strong">✅ Password is strong</div>', unsafe_allow_html=True)
                elif len(issues) <= 2:
                    st.markdown('<div class="password-strength strength-medium">⚠️ Password could be stronger</div>', unsafe_allow_html=True)
                    for issue in issues:
                        st.markdown(f'<div style="color: #ffaa66; font-size: 0.8rem; margin-left: 1rem;">• {issue}</div>', unsafe_allow_html=True)
                else:
                    st.markdown('<div class="password-strength strength-weak">❌ Password is too weak</div>', unsafe_allow_html=True)
                    for issue in issues:
                        st.markdown(f'<div style="color: #ff6666; font-size: 0.8rem; margin-left: 1rem;">• {issue}</div>', unsafe_allow_html=True)
            
            if submit_button:
                # Validation
                if not name or not email or not password or not confirm_password:
                    st.error("Please fill in all fields.")
                elif password != confirm_password:
                    st.error("Passwords do not match.")
                elif not agree_terms:
                    st.error("Please agree to the Terms and Conditions.")
                else:
                    # Check password strength
                    is_strong, issues = AuthUtils.is_password_strong(password)
                    if not is_strong:
                        st.error("Password does not meet security requirements.")
                    else:
                        # Register user
                        success, message = controller.register_user(email, password, name, role)
                        
                        if success:
                            st.success("Account created successfully! Please check your email for verification.")
                            st.info("You can now log in with your new account.")
                            # Option to redirect to login
                            if st.button("Go to Login"):
                                st.session_state.navigate_to = 'login'
                                st.rerun()
                        else:
                            st.error(f"Registration failed: {message}")
        
        # Additional options
        st.markdown("""
        <div style="text-align: center; margin-top: 2rem;">
            <span style="color: #cccccc; font-size: 0.9rem;">Already have an account? </span>
            <a href="#" style="color: #0066cc; text-decoration: none; font-size: 0.9rem;">Sign in</a>
        </div>
        """, unsafe_allow_html=True)
        
        # Login link
        if st.button("Back to Login", key="login_link"):
            st.session_state.navigate_to = 'login'
            st.rerun()


if __name__ == "__main__":
    render_register_page() 