import streamlit as st

st.set_page_config(page_title="Simple Button Test", layout="wide")

st.title("Simple Button Type Test")

st.header("Testing type parameter support")

# Test 1: Regular button with type
st.subheader("Regular Button")
try:
    if st.button("Test Button", type="primary"):
        st.success("Regular button with type='primary' works!")
except Exception as e:
    st.error(f"Regular button error: {e}")

# Test 2: Form submit button with type
st.subheader("Form Submit Button")
try:
    with st.form("test_form"):
        if st.form_submit_button("Test Submit", type="primary"):
            st.success("Form submit button with type='primary' works!")
except Exception as e:
    st.error(f"Form submit button error: {e}")

# Test 3: Check what parameters are actually supported
st.header("Parameter Support Check")

st.markdown("""
**Regular st.button() parameters:**
- `label` (required)
- `key` (optional)
- `help` (optional)
- `on_click` (optional)
- `args` (optional)
- `kwargs` (optional)
- `type` (optional) - "primary" or "secondary"

**Form submit button parameters:**
- `label` (required)
- `key` (optional)
- `help` (optional)
- `on_click` (optional)
- `args` (optional)
- `kwargs` (optional)
- `type` (optional) - "primary" or "secondary" (may not be supported)
""")

st.header("Alternative Approach")
st.markdown("""
If form submit buttons don't support the `type` parameter, we might need to:
1. Use CSS classes instead of the `kind` attribute
2. Target form submit buttons differently
3. Use a different approach for styling form buttons
""")

# Test without type parameter
st.subheader("Form Submit Button (no type parameter)")
with st.form("test_form2"):
    if st.form_submit_button("Test Submit (no type)"):
        st.success("Form submit button without type parameter works!")

st.markdown("""
**Next Steps:**
1. Check if form submit buttons actually support the `type` parameter
2. If not, we need to update our CSS approach
3. Consider using CSS classes or different selectors for form buttons
""") 