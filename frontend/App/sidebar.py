import streamlit as st

def Sidebar():
    with st.sidebar:
        options = st.sidebar.selectbox(
            "Menu",
            ('login','UserData','CardDesign','Mydata' )
        )