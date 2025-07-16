"""
Welcome page for the Sacbeh application.
This is the main landing page that users see when they first visit the application.
"""

import streamlit as st
import os
import base64
from controller.app_controller import AppController
from model.data_models import RawDataStructures
from view.styles import get_app_theme_css


def render_welcome_page():
    """
    Render the welcome page with application information and navigation.
    """
    # Get the singleton controller instance
    controller = AppController()
    
    # Page configuration is handled in main app.py
    
    # Custom CSS for enhanced design
    st.markdown(f"""
    <style>
    {get_app_theme_css()}
    
    .logo-container {{
        text-align: center;
        padding: 8vh 0 2vh 0;
        position: relative;
        z-index: 10;
        width: 100%;
        display: flex;
        justify-content: center;
        align-items: center;
    }}
    .logo-image {{
        display: block;
        margin: 0 auto;
    }}
    .app-title {{
        font-size: 8rem;
        font-weight: 900;
        color: #0066cc;
        text-align: center;
        margin: 0;
        padding: 20vh 0;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.5);
        font-family: 'Arial Black', sans-serif;
        letter-spacing: 0.1em;
        position: relative;
        z-index: 10;
    }}
    .tagline {{
        text-align: center;
        color: #ffffff;
        font-size: 1.5rem;
        font-weight: 300;
        margin: 0 0 3rem 0;
        opacity: 0.9;
        font-style: italic;
    }}
    .content-section {{
        background-color: rgba(0, 0, 0, 0.3);
        border-radius: 15px;
        padding: 2rem;
        margin: 2rem 0;
        border-left: 4px solid #0066cc;
        backdrop-filter: blur(10px);
    }}
    .feature-grid {{
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
        gap: 1.5rem;
        margin: 2rem 0;
    }}
    .feature-card {{
        background-color: rgba(255, 255, 255, 0.9);
        border-radius: 10px;
        padding: 1.5rem;
        border: 1px solid rgba(0, 102, 204, 0.3);
        transition: all 0.3s ease;
    }}
    .feature-card:hover {{
        transform: translateY(-5px);
        box-shadow: 0 10px 25px rgba(0, 102, 204, 0.2);
    }}
    .feature-icon {{
        font-size: 2.5rem;
        margin-bottom: 1rem;
        color: #0066cc;
    }}
    .feature-title {{
        color: #2d2d2d;
        font-size: 1.3rem;
        font-weight: 600;
        margin-bottom: 0.5rem;
    }}
    .feature-description {{
        color: #555555;
        font-size: 0.95rem;
        line-height: 1.5;
    }}
    .cta-button {{
        background: linear-gradient(135deg, #ff6600, #ff8533);
        color: white;
        padding: 1rem 2rem;
        border-radius: 25px;
        text-decoration: none;
        display: inline-block;
        font-weight: 600;
        transition: all 0.3s ease;
        border: none;
        cursor: pointer;
        margin: 2rem auto;
        text-align: center;
    }}
    .cta-button:hover {{
        transform: translateY(-2px);
        box-shadow: 0 5px 15px rgba(255, 102, 0, 0.4);
    }}
    .button-container {{
        text-align: center;
        margin: 2rem 0;
    }}
    .stMarkdown {{
        background-color: transparent !important;
    }}
    .auth-buttons {{
        position: fixed !important;
        top: 4rem !important;
        right: 2rem !important;
        z-index: 1000 !important;
        display: flex !important;
        gap: 1rem !important;
    }}
    .auth-button {{
        background: linear-gradient(135deg, #0066cc, #0052a3) !important;
        color: white !important;
        border: none !important;
        padding: 0.75rem 1.5rem !important;
        border-radius: 20px !important;
        font-weight: 600 !important;
        transition: all 0.3s ease !important;
        box-shadow: 0 2px 10px rgba(0, 102, 204, 0.3) !important;
        cursor: pointer !important;
    }}
    .auth-button:hover {{
        transform: translateY(-2px) !important;
        box-shadow: 0 5px 15px rgba(0, 102, 204, 0.4) !important;
        background: linear-gradient(135deg, #0052a3, #003d7a) !important;
    }}
    .register-button {{
        background: linear-gradient(135deg, #28a745, #20c997) !important;
    }}
    .register-button:hover {{
        background: linear-gradient(135deg, #218838, #1ea085) !important;
    }}

    </style>
    """, unsafe_allow_html=True)
    
    # Authentication buttons in top right corner using secondary style
    col1, col2 = st.columns([1, 1])
    with col1:
        if st.button("Login", key="login_nav_button", type="secondary"):
            st.session_state.navigate_to = 'login'
            st.rerun()
    with col2:
        if st.button("Login", key="register_nav_button", type="secondary"):
            st.session_state.navigate_to = 'login'
            st.rerun()
    
    # Position the buttons with CSS
    st.markdown("""
    <style>
    [data-testid="stButton"] button[kind="secondary"] {
        position: fixed !important;
        top: 4rem !important;
        right: 2rem !important;
        z-index: 1000 !important;
        background: linear-gradient(135deg, #0066cc, #0052a3) !important;
        color: white !important;
        border: none !important;
        padding: 0.75rem 1.5rem !important;
        border-radius: 20px !important;
        font-weight: 600 !important;
        transition: all 0.3s ease !important;
        box-shadow: 0 2px 10px rgba(0, 102, 204, 0.3) !important;
    }
    [data-testid="stButton"] button[kind="secondary"]:hover {
        transform: translateY(-2px) !important;
        box-shadow: 0 5px 15px rgba(0, 102, 204, 0.4) !important;
        background: linear-gradient(135deg, #0052a3, #003d7a) !important;
    }
    </style>
    """, unsafe_allow_html=True)
    
    # Display the Sacbeh logo image
    try:
        # Try to load the logo image
        logo_path = "assets/sacbeh_logo.png"
        if os.path.exists(logo_path):
            st.markdown("""
            <div style="display: flex; justify-content: center; align-items: center; padding: 8vh 0 2vh 0;">
                <img src="data:image/png;base64,{}" style="width: 500px; height: auto;">
            </div>
            """.format(base64.b64encode(open(logo_path, 'rb').read()).decode()), unsafe_allow_html=True)
        else:
            # Fallback to text if image not found
            st.markdown('<h1 class="app-title">SACBEH</h1>', unsafe_allow_html=True)
    except Exception as e:
        # Fallback to text if there's any error
        st.markdown('<h1 class="app-title">SACBEH</h1>', unsafe_allow_html=True)
    
    # Tagline
    st.markdown('<p class="tagline">Navigate Your Data Landscape</p>', unsafe_allow_html=True)
    
    # Orange Start Exploring button
    st.markdown("""
    <div class="button-container">
        <button class="cta-button" onclick="alert('Data exploration features coming soon!')">
            Start Exploring
        </button>
    </div>
    """, unsafe_allow_html=True)
    
    # Features Grid
    try:
        # Load the robot icon
        robot_icon_path = "assets/robot.png"
        if os.path.exists(robot_icon_path):
            robot_icon_base64 = base64.b64encode(open(robot_icon_path, 'rb').read()).decode()
            robot_icon_html = f'<img src="data:image/png;base64,{robot_icon_base64}" style="width: 40px; height: 40px; object-fit: contain;">'
        else:
            robot_icon_html = '🤖'  # Fallback to emoji
    except Exception as e:
        robot_icon_html = '🤖'  # Fallback to emoji
    
    try:
        # Load the network icon
        network_icon_path = "assets/network.png"
        if os.path.exists(network_icon_path):
            network_icon_base64 = base64.b64encode(open(network_icon_path, 'rb').read()).decode()
            network_icon_html = f'<img src="data:image/png;base64,{network_icon_base64}" style="width: 40px; height: 40px; object-fit: contain;">'
        else:
            network_icon_html = '🛤️'  # Fallback to emoji
    except Exception as e:
        network_icon_html = '🛤️'  # Fallback to emoji
    
    try:
        # Load the dynamic icon
        dynamic_icon_path = "assets/dynamic.png"
        if os.path.exists(dynamic_icon_path):
            dynamic_icon_base64 = base64.b64encode(open(dynamic_icon_path, 'rb').read()).decode()
            dynamic_icon_html = f'<img src="data:image/png;base64,{dynamic_icon_base64}" style="width: 40px; height: 40px; object-fit: contain;">'
        else:
            dynamic_icon_html = '🔄'  # Fallback to emoji
    except Exception as e:
        dynamic_icon_html = '🔄'  # Fallback to emoji
    
    try:
        # Load the database icon
        database_icon_path = "assets/database.png"
        if os.path.exists(database_icon_path):
            database_icon_base64 = base64.b64encode(open(database_icon_path, 'rb').read()).decode()
            database_icon_html = f'<img src="data:image/png;base64,{database_icon_base64}" style="width: 40px; height: 40px; object-fit: contain;">'
        else:
            database_icon_html = '🔌'  # Fallback to emoji
    except Exception as e:
        database_icon_html = '🔌'  # Fallback to emoji
    
    st.markdown(f"""
        <h2 style="color: #0066cc; margin-bottom: 1.5rem;">✨ Key Features</h2>
        <div class="feature-grid">
            <div class="feature-card">
                <div class="feature-icon">{robot_icon_html}</div>
                <div class="feature-title">AI-Powered Analysis</div>
                <div class="feature-description">
                    Intelligent data source analysis with automatic dimension discovery and corporate process identification.
                </div>
            </div>
            <div class="feature-card">
                <div class="feature-icon">{network_icon_html}</div>
                <div class="feature-title">Path Traversal</div>
                <div class="feature-description">
                    Navigate through data hierarchies by clicking on chart elements to explore deeper insights.
                </div>
            </div>
            <div class="feature-card">
                <div class="feature-icon">{dynamic_icon_html}</div>
                <div class="feature-title">Dynamic Dimensions</div>
                <div class="feature-description">
                    Switch aggregation dimensions on-the-fly to create new perspectives and data detours.
                </div>
            </div>
            <div class="feature-card">
                <div class="feature-icon">{database_icon_html}</div>
                <div class="feature-title">Universal Connectivity</div>
                <div class="feature-description">
                    Connect to any data source through our abstract factory pattern - databases, APIs, files.
                </div>
            </div>
            <div class="feature-card">
                <div class="feature-icon">⚡</div>
                <div class="feature-title">High Performance</div>
                <div class="feature-description">
                    Handle large datasets efficiently with Pandas and PySpark support for scalable processing.
                </div>
            </div>
        </div>
    """, unsafe_allow_html=True)


if __name__ == "__main__":
    render_welcome_page() 