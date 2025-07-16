"""
Login page for the Sacbeh application.
Provides user authentication functionality with a clean, minimalist interface.
"""

import streamlit as st
import os
import base64
from controller.app_controller import AppController
from view.styles import get_button_css, get_form_input_css, get_app_theme_css


def render_login_page():
    """
    Render the login page with authentication form.
    """
    # Get the singleton controller instance
    controller = AppController()
    
    # Use reusable CSS styling
    st.markdown(f"""
    <style>
    {get_app_theme_css()}
    {get_form_input_css()}
    {get_button_css(["primary", "secondary"])}
    </style>
    """, unsafe_allow_html=True)
    
    # Back button using secondary style
    if st.button("← Back", key="back_button", type="secondary"):
        st.session_state.navigate_to = 'welcome'
        st.rerun()
    
    # Add top padding to avoid development bar
    st.markdown("<div style='height: 2rem;'></div>", unsafe_allow_html=True)
    
    # Create columns to center the form
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        # Title
        st.markdown('<h2 style="color: #0066cc; text-align: center; margin-bottom: 2rem; font-size: 1.8rem;">Sign In</h2>', unsafe_allow_html=True)
        
        # Login form
        with st.form("login_form"):
            email = st.text_input("Email", placeholder="Enter your email")
            password = st.text_input("Password", type="password", placeholder="Enter your password")
            
            # Remember me checkbox
            remember_me = st.checkbox("Remember me")
            
            # Submit button (will be styled as primary via CSS)
            submit_button = st.form_submit_button("Sign In")
            
            if submit_button:
                if email and password:
                    # Use the authorization controller for authentication
                    success, message = controller.login_user(email, password)
                    
                    if success:
                        st.success("Login successful! Redirecting...")
                        # Store session token in session state
                        session_token = controller.get_session_token()
                        if session_token:
                            st.session_state.session_token = session_token
                        st.session_state.logged_in = True
                        st.session_state.user_email = email
                        st.rerun()
                    else:
                        st.error(f"Login failed: {message}")
                else:
                    st.error("Please enter both email and password.")
        
        # Additional options
        st.markdown("""
        <div style="text-align: center; margin-top: 2rem;">
            <a href="#" style="color: #0066cc; text-decoration: none; font-size: 0.9rem;">Forgot password?</a>
        </div>
        <div style="text-align: center; margin-top: 1rem;">
            <span style="color: #cccccc; font-size: 0.9rem;">Don't have an account? </span>
            <a href="#" style="color: #0066cc; text-decoration: none; font-size: 0.9rem;">Sign up</a>
        </div>
        """, unsafe_allow_html=True)
        
        # Registration link using primary style
        if st.button("Create New Account", key="register_link", type="primary"):
            st.session_state.navigate_to = 'register'
            st.rerun()


if __name__ == "__main__":
    render_login_page() 