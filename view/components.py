"""
Reusable UI components for the Sacbeh application.
Uses Streamlit's native features for consistent styling.
"""

import streamlit as st
from typing import Optional, Callable, Any


def primary_button(
    text: str, 
    key: str, 
    on_click: Optional[Callable] = None,
    use_container_width: bool = False,
    disabled: bool = False,
    help: Optional[str] = None
) -> bool:
    """
    Create a primary action button with consistent orange styling.
    
    Args:
        text: Button text
        key: Unique key for the button
        on_click: Optional callback function
        use_container_width: Whether to use full container width
        disabled: Whether the button is disabled
        help: Optional help text
        
    Returns:
        bool: True if button was clicked, False otherwise
    """
    return st.button(
        text=text,
        key=key,
        type="primary",
        use_container_width=use_container_width,
        disabled=disabled,
        help=help,
        on_click=on_click
    )


def secondary_button(
    text: str, 
    key: str, 
    on_click: Optional[Callable] = None,
    use_container_width: bool = False,
    disabled: bool = False,
    help: Optional[str] = None
) -> bool:
    """
    Create a secondary action button with consistent Mayan blue styling.
    
    Args:
        text: Button text
        key: Unique key for the button
        on_click: Optional callback function
        use_container_width: Whether to use full container width
        disabled: Whether the button is disabled
        help: Optional help text
        
    Returns:
        bool: True if button was clicked, False otherwise
    """
    return st.button(
        text=text,
        key=key,
        type="secondary",
        use_container_width=use_container_width,
        disabled=disabled,
        help=help,
        on_click=on_click
    )


def form_submit_button(
    text: str,
    use_container_width: bool = False,
    disabled: bool = False,
    help: Optional[str] = None
) -> bool:
    """
    Create a form submit button with consistent primary styling.
    
    Args:
        text: Button text
        use_container_width: Whether to use full container width
        disabled: Whether the button is disabled
        help: Optional help text
        
    Returns:
        bool: True if button was clicked, False otherwise
    """
    return st.form_submit_button(
        label=text,
        use_container_width=use_container_width,
        disabled=disabled,
        help=help
    )


def navigation_button(
    text: str,
    key: str,
    target_page: str,
    use_container_width: bool = False,
    help: Optional[str] = None
) -> bool:
    """
    Create a navigation button that redirects to another page.
    
    Args:
        text: Button text
        key: Unique key for the button
        target_page: Target page to navigate to
        use_container_width: Whether to use full container width
        help: Optional help text
        
    Returns:
        bool: True if button was clicked, False otherwise
    """
    def navigate():
        st.session_state.navigate_to = target_page
        st.rerun()
    
    return st.button(
        text=text,
        key=key,
        type="primary",
        use_container_width=use_container_width,
        help=help,
        on_click=navigate
    ) 