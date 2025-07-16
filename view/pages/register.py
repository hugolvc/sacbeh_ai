"""
Registration page for the Sacbeh application.
Provides user registration functionality with validation and security features.
"""

import streamlit as st
from controller.app_controller import AppController
from model.auth_models import AuthUtils
from view.styles import get_button_css, get_form_input_css, get_app_theme_css


def show_register_page():
    """Display the registration page"""
    controller = AppController()
    
    # Use reusable CSS styling
    st.markdown(f"""
    <style>
    {get_app_theme_css()}
    {get_form_input_css()}
    {get_button_css(["primary", "secondary"])}
    
    .password-strength {{
        padding: 0.5rem;
        border-radius: 5px;
        margin-top: 0.5rem;
        font-size: 0.8rem;
    }}
    .strength-weak {{
        background-color: rgba(255, 0, 0, 0.1);
        color: #ff6b6b;
        border: 1px solid rgba(255, 0, 0, 0.3);
    }}
    .strength-medium {{
        background-color: rgba(255, 165, 0, 0.1);
        color: #ffa500;
        border: 1px solid rgba(255, 165, 0, 0.3);
    }}
    .strength-strong {{
        background-color: rgba(0, 255, 0, 0.1);
        color: #51cf66;
        border: 1px solid rgba(0, 255, 0, 0.3);
    }}
    </style>
    """, unsafe_allow_html=True)
    
    # Add top padding to avoid development bar
    st.markdown("<div style='height: 2rem;'></div>", unsafe_allow_html=True)
    
    # Create columns to center the form
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        # Registration form
        with st.form("registration_form"):
            st.markdown("""
            <div style="text-align: center; margin-bottom: 2rem;">
                <h1 style="color: #ffffff; margin-bottom: 0.5rem;">Create Account</h1>
                <p style="color: #cccccc; font-size: 1rem;">Join Sacbeh AI today</p>
            </div>
            """, unsafe_allow_html=True)
            
            # Form fields
            username = st.text_input("Username", placeholder="Enter your username")
            email = st.text_input("Email", placeholder="Enter your email address")
            password = st.text_input("Password", type="password", placeholder="Enter your password")
            confirm_password = st.text_input("Confirm Password", type="password", placeholder="Confirm your password")
            
            # Password strength indicator
            if password:
                strength = AuthUtils.check_password_strength(password)
                strength_class = f"strength-{strength.lower()}"
                st.markdown(f"""
                <div class="password-strength {strength_class}">
                    Password Strength: {strength}
                </div>
                """, unsafe_allow_html=True)
            
            agree_terms = st.checkbox("I agree to the Terms and Conditions")
            
            # Submit button (will be styled as primary via CSS)
            submit_button = st.form_submit_button("Create Account")
            
            if submit_button:
                if not all([username, email, password, confirm_password]):
                    st.error("Please fill in all fields")
                elif password != confirm_password:
                    st.error("Passwords do not match")
                elif not agree_terms:
                    st.error("Please agree to the Terms and Conditions")
                else:
                    # Attempt registration
                    success, message = controller.register_user(username, email, password)
                    if success:
                        st.success("Registration successful! Please log in.")
                        st.session_state.navigate_to = 'login'
                        st.rerun()
                    else:
                        st.error(f"Registration failed: {message}")
        
        # Login button using primary style
        if st.button("Login", key="login_link", type="primary"):
            st.session_state.navigate_to = 'login'
            st.rerun() 