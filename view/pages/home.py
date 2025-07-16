"""
Home page for the Sacbeh application.
Displays the main dashboard after successful user authentication.
"""

import streamlit as st
from controller.app_controller import AppController
from view.styles import get_button_css, get_app_theme_css


def render_home_page():
    """
    Render the home page with user dashboard.
    """
    # Get the singleton controller instance
    controller = AppController()
    
    # Use reusable CSS styling
    st.markdown(f"""
    <style>
    {get_app_theme_css()}
    {get_button_css(["primary", "secondary"])}
    </style>
    """, unsafe_allow_html=True)
    
    # Back button using secondary style
    if st.button("← Back to Welcome", key="back_button", type="secondary"):
        st.session_state.navigate_to = 'welcome'
        st.rerun()
    
    # Add top padding to avoid development bar
    st.markdown("<div style='height: 2rem;'></div>", unsafe_allow_html=True)
    
    # Welcome header
    st.markdown('<h1 style="color: #0066cc; text-align: center; margin-bottom: 2rem;">🏛️ Welcome to Sacbeh</h1>', unsafe_allow_html=True)
    
    # Get current user information
    current_user = controller.get_current_user()
    if current_user:
        user_email = current_user.get('email', 'User')
        user_roles = current_user.get('roles', [])
        
        # Welcome message
        st.markdown(f"""
        <div style="background: linear-gradient(135deg, #f8f9fa, #e9ecef); 
                    padding: 2rem; 
                    border-radius: 15px; 
                    border-left: 5px solid #0066cc; 
                    margin-bottom: 2rem;">
            <h2 style="color: #333; margin-bottom: 1rem;">Welcome back, {user_email}!</h2>
            <p style="color: #666; font-size: 1.1rem; margin-bottom: 0.5rem;">
                You're logged in with the following roles: <strong>{', '.join(user_roles) if user_roles else 'Standard User'}</strong>
            </p>
            <p style="color: #666; font-size: 1rem; margin-bottom: 0;">
                Ready to explore the ancient pathways of knowledge with AI-powered analysis.
            </p>
        </div>
        """, unsafe_allow_html=True)
    
    # Dashboard content
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        <div style="background: white; padding: 1.5rem; border-radius: 10px; box-shadow: 0 2px 10px rgba(0,0,0,0.1);">
            <h3 style="color: #0066cc; margin-bottom: 1rem;">🚀 Quick Actions</h3>
            <ul style="color: #333; line-height: 1.8;">
                <li>Start a new analysis</li>
                <li>View recent projects</li>
                <li>Explore data sources</li>
                <li>Check system status</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div style="background: white; padding: 1.5rem; border-radius: 10px; box-shadow: 0 2px 10px rgba(0,0,0,0.1);">
            <h3 style="color: #0066cc; margin-bottom: 1rem;">📊 Recent Activity</h3>
            <div style="color: #666; font-size: 0.9rem;">
                <p>• Last login: Just now</p>
                <p>• Projects created: 0</p>
                <p>• Analyses completed: 0</p>
                <p>• Data sources connected: 0</p>
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    # Main content area
    st.markdown("""
    <div style="background: white; padding: 2rem; border-radius: 10px; box-shadow: 0 2px 10px rgba(0,0,0,0.1); margin-top: 2rem;">
        <h3 style="color: #0066cc; margin-bottom: 1.5rem;">🎯 Getting Started</h3>
        <p style="color: #333; line-height: 1.6; margin-bottom: 1rem;">
            Welcome to Sacbeh, your AI-powered platform for exploring ancient knowledge pathways. 
            This dashboard is your central hub for managing analyses, projects, and data connections.
        </p>
        <p style="color: #333; line-height: 1.6; margin-bottom: 1rem;">
            <strong>What you can do:</strong>
        </p>
        <ul style="color: #333; line-height: 1.8; margin-bottom: 1rem;">
            <li>Create new analysis projects using AI-powered tools</li>
            <li>Connect to various data sources and databases</li>
            <li>Explore path traversal algorithms</li>
            <li>Generate dynamic visualizations</li>
            <li>Collaborate with team members</li>
        </ul>
        <p style="color: #666; font-style: italic;">
            Ready to begin your journey? Start by creating your first analysis project.
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    # Action buttons
    st.markdown("<div style='height: 2rem;'></div>", unsafe_allow_html=True)
    
    button_cols = st.columns([1, 1, 1, 1, 1, 1, 1, 1, 1])
    with button_cols[3]:
        if st.button("New Analysis", key="new_analysis", type="primary", use_container_width=True):
            st.info("New analysis feature coming soon!")
    
    with button_cols[4]:
        if st.button("View Projects", key="view_projects", type="secondary", use_container_width=True):
            st.info("Project management feature coming soon!")
    
    with button_cols[5]:
        if st.button("Settings", key="settings", type="secondary", use_container_width=True):
            st.info("Settings panel coming soon!")


if __name__ == "__main__":
    render_home_page() 