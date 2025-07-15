"""
Login page for the Sacbeh application.
Provides user authentication functionality with a clean, minimalist interface.
"""

import streamlit as st
import os
import base64
from controller.app_controller import AppController


def render_login_page():
    """
    Render the login page with authentication form.
    """
    # Get the singleton controller instance
    controller = AppController()
    
    # Custom CSS for login page
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
    </style>
    """, unsafe_allow_html=True)
    
    # Back button
    if st.button("← Back", key="back_button"):
        st.session_state.navigate_to = 'welcome'
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
        st.markdown('<h2 style="color: #0066cc; text-align: center; margin-bottom: 2rem; font-size: 1.8rem;">Sign In</h2>', unsafe_allow_html=True)
        
        # Login form
        with st.form("login_form"):
            email = st.text_input("Email", placeholder="Enter your email")
            password = st.text_input("Password", type="password", placeholder="Enter your password")
            
            # Remember me checkbox
            remember_me = st.checkbox("Remember me")
            
            # Submit button
            submit_button = st.form_submit_button("Sign In")
            
            if submit_button:
                if email and password:
                    # Here you would typically validate credentials
                    # For now, we'll just show a success message
                    st.success("Login successful! Redirecting...")
                    # In a real app, you would set session state and redirect
                    st.session_state.logged_in = True
                    st.session_state.user_email = email
                    st.rerun()
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


if __name__ == "__main__":
    render_login_page() 