"""
    file : Streamlit. App.main.py
    writer : Meohong
    first date : 2024-05-01
    Objective : main app ( Service )
    modified :
    ========================================================================
        date    |   no  |                 note
     2024-05-01 |   1   |   first write
     2024-05-02 |   2   |   add login JWT authentication 
    ========================================================================
"""

import streamlit as st
import os
from sidebar import Sidebar

st.set_page_config(page_title="Main", layout="centered")

# 회원 삭제를 진행했다면, 다음과 같은 if문을 통해, 세션 상태를 삭제함
if 'page_resign' in st.session_state:
    del st.session_state["page_resign"]
if 'card_page' in st.session_state:
    del st.session_state["card_page"]
if "gen_cards" in st.session_state:
        del st.session_state["gen_cards"]
if "Card_image_result" in st.session_state:
    del st.session_state["Card_image_result"]
if "mydata_page" in st.session_state:
    del st.session_state["mydata_page"]


st.title("Simple App for IM Challenger")

placeholder = st.container(height=300,border=True)

with placeholder:
    col1, col2, Logined = st.columns(spec=[0.2, 0.6, 0.35], gap="small")

    with col2:
        st.write("### 나만의 학생증 만들기")
        
        card, mydata = st.columns(2, gap="large")
    
        if 'token' not in st.session_state:
            st.page_link("pages/CardDesign.py", label="**카드 디자인**",icon="💳", use_container_width=True, disabled=True)
            st.page_link("pages/Mydata.py", label="**마이 데이터**",icon="📑", use_container_width=True, disabled=True)
        else:
            st.page_link("pages/CardDesign.py", label="**카드 디자인**",icon="💳", use_container_width=True)
            st.page_link("pages/Mydata.py", label="**마이 데이터**",icon="📑", use_container_width=True)

    with Logined:
        login, signup = st.columns(2, gap="small")
        with login:
            if 'token' not in st.session_state:
                st.page_link("pages/login.py", label="***Login***",icon="🆔")
            else:
                st.page_link("pages/logout.py", label="***Logout***", icon="🔐")
        with signup:
            if 'token' not in st.session_state:
                st.page_link("pages/UserData.py", label="***Signup***",icon="📝")
            else:
                st.page_link("pages/UserData.py", label="***Modify***",icon="💾")