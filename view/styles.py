"""
Reusable CSS styles for the Sacbeh application.
Returns CSS strings that can be used with st.markdown().

BUTTON CENTERING STRATEGY:
For centering Streamlit buttons, use the following approach:
1. Create 7 equal columns: button_cols = st.columns([1, 1, 1, 1, 1, 1, 1])
2. Place button in the middle column: with button_cols[3]:
3. Use use_container_width=True: st.button(..., use_container_width=True)

IMPORTANT: Streamlit only allows one level of column nesting. If you need to center
a button that's already inside a column structure, move the button centering
columns outside of the existing column context.

Example:
# Wrong (nested columns):
col1, col2, col3 = st.columns([1, 2, 1])
with col2:
    button_cols = st.columns([1, 1, 1, 1, 1, 1, 1])  # This won't work!

# Correct (separate column contexts):
col1, col2, col3 = st.columns([1, 2, 1])
with col2:
    # Form content here
# Button centering outside the above columns:
button_cols = st.columns([1, 1, 1, 1, 1, 1, 1])
with button_cols[3]:
    st.button(..., use_container_width=True)
"""

from typing import Dict, List


def get_button_css(button_types: List[str] = None) -> str:
    """
    Get CSS for button styling based on button types.
    
    Args:
        button_types: List of button types to include ("primary", "secondary")
        
    Returns:
        str: CSS string for button styling
    """
    if button_types is None:
        button_types = ["primary", "secondary"]
    
    css_parts = []
    
    if "primary" in button_types:
        css_parts.append("""
        [data-testid="stButton"] button[kind="primary"],
        [data-testid="stFormSubmitButton"] button {
            background: linear-gradient(135deg, #ff6600, #ff8533) !important;
            color: white !important;
            border: none !important;
            border-radius: 10px !important;
            font-weight: 600 !important;
            transition: all 0.3s ease !important;
        }
        [data-testid="stButton"] button[kind="primary"]:hover,
        [data-testid="stFormSubmitButton"] button:hover {
            transform: translateY(-2px) !important;
            box-shadow: 0 5px 15px rgba(255, 102, 0, 0.4) !important;
        }
        """)
    
    if "secondary" in button_types:
        css_parts.append("""
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
        """)
    
    return "\n".join(css_parts)


def get_form_input_css() -> str:
    """
    Get CSS for form input styling.
    
    Returns:
        str: CSS string for form inputs
    """
    return """
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
    .stCheckbox > div > div {
        color: #ffffff !important;
    }
    """


def get_app_theme_css() -> str:
    """
    Get CSS for application theme.
    
    Returns:
        str: CSS string for app theme
    """
    return """
    .stApp {
        background-color: #2d2d2d !important;
    }
    .main .block-container {
        background-color: transparent !important;
        padding: 0 2rem !important;
        margin: 0 !important;
        max-width: none !important;
    }
    """


def get_complete_css(include_buttons: bool = True, include_forms: bool = True, include_theme: bool = True) -> str:
    """
    Get complete CSS for the application.
    
    Args:
        include_buttons: Whether to include button styles
        include_forms: Whether to include form styles
        include_theme: Whether to include theme styles
        
    Returns:
        str: Complete CSS string
    """
    css_parts = []
    
    if include_theme:
        css_parts.append(get_app_theme_css())
    
    if include_forms:
        css_parts.append(get_form_input_css())
    
    if include_buttons:
        css_parts.append(get_button_css())
    
    return "\n".join(css_parts) 