import streamlit as st

if 'token' in st.session_state:
        del st.session_state['token']
        st.success("Logout!")
        st.page_link("main.py", label="***Go Back***", icon="⬅️")