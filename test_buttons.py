import streamlit as st
from view.styles import get_button_css

st.set_page_config(page_title="Button Test", layout="wide")

st.title("Button HTML Structure Test")

# Add comprehensive CSS to test different selectors
st.markdown(f"""
<style>
{get_button_css(["primary", "secondary"])}

/* Additional selectors to test */
.stButton > button {{
    border: 2px solid green !important;
    background: yellow !important;
}}

.stFormSubmitButton > button {{
    border: 2px solid purple !important;
    background: pink !important;
}}

/* Target by kind attribute */
button[kind="primary"] {{
    border: 3px solid orange !important;
}}

button[kind="secondary"] {{
    border: 3px solid blue !important;
}}

/* Debug styles */
[data-testid] {{
    outline: 2px dashed red !important;
    margin: 5px !important;
}}

/* More specific selectors */
[data-testid="stButton"] {{
    background: rgba(255, 0, 0, 0.1) !important;
}}

[data-testid="stFormSubmitButton"] {{
    background: rgba(0, 255, 0, 0.1) !important;
}}
</style>
""", unsafe_allow_html=True)

st.header("Testing Different Button Types")

col1, col2 = st.columns(2)

with col1:
    st.subheader("Regular Buttons")
    
    # Regular button with primary type
    if st.button("Primary Button", type="primary", key="test_primary"):
        st.write("Primary button clicked!")
    
    # Regular button with secondary type  
    if st.button("Secondary Button", type="secondary", key="test_secondary"):
        st.write("Secondary button clicked!")

with col2:
    st.subheader("Form Submit Buttons")
    
    # Form with submit button
    with st.form("test_form"):
        st.text_input("Test input")
        
        # Form submit button with primary type
        if st.form_submit_button("Primary Submit", type="primary"):
            st.write("Primary submit clicked!")
    
    # Another form with secondary submit
    with st.form("test_form2"):
        st.text_input("Test input 2")
        
        # Form submit button with secondary type
        if st.form_submit_button("Secondary Submit", type="secondary"):
            st.write("Secondary submit clicked!")

st.header("CSS Selector Analysis")
st.markdown("""
**Current CSS Selectors Being Tested:**

1. `[data-testid="stButton"] button[kind="primary"]` - Regular primary buttons
2. `[data-testid="stButton"] button[kind="secondary"]` - Regular secondary buttons  
3. `[data-testid="stFormSubmitButton"] button[kind="primary"]` - Form submit primary buttons
4. `[data-testid="stFormSubmitButton"] button[kind="secondary"]` - Form submit secondary buttons
5. `.stButton > button` - All regular buttons (green border)
6. `.stFormSubmitButton > button` - All form submit buttons (purple border)
7. `button[kind="primary"]` - Any button with primary kind (orange border)
8. `button[kind="secondary"]` - Any button with secondary kind (blue border)

**Instructions:**
1. Open browser dev tools (F12)
2. Inspect the buttons above
3. Look at the HTML structure and CSS classes
4. Check which selectors are actually working
""")

# Add some debug info
st.code("""
Expected behavior:
- Regular buttons should have green borders and orange/blue kind borders
- Form submit buttons should have purple borders and orange/blue kind borders
- If kind borders don't appear, it means the kind attribute isn't being set properly
""") 