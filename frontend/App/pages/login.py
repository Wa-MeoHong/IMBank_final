"""
    file : Streamlit. App.login.py
    writer : Meohong
    first date : 2024-05-01
    Objective : Login ( Service )
    modified :
    ========================================================================
        date    |   no  |                 note
     2024-05-01 |   1   |   first write
     2024-05-02 |   2   |   login JWT 1
    ========================================================================
"""
import streamlit as st
import requests
from streamlit_jwt_authenticator import Authenticator

st.set_page_config(page_title="Login", layout="centered")

# Fastapi 호스트
url = "http://localhost:50000"
# 로그인 변수는 페이지를 넘어가면서 저장해야하므로, 

# Create an empty container
empty1, Logins, empty2 = st.columns(spec=[0.3, 0.7, 0.3])

with Logins:
    placeholder = st.empty()

# Insert a form in the container
with placeholder.form("login"):
    col1, col2 = st. columns(spec=[0.7,0.3], gap="small")
    #st.markdown("#### Enter your credentials")
    with col1:
        st.markdown("### Login")        # 로그인
    with col2:
        st.page_link("main.py", label="***Go Back***", icon="⬅️")

    # 이메일, 패스워드 입력 칸
    email = st.text_input("**Email**")
    password = st.text_input("**Password**", type="password")
    submit = st.form_submit_button("Login")

if submit:
    # If the form is submitted and the email and password are correct,
    # clear the form/container and display a success message
    login_url = url + "/user/login"  # 로그인 URL

    # JSON 파일로 만듦
    data = {
        "username": email,
        "password": password,
    }
    # 로그인 헤더는 다음과 같은 헤더 규칙을 따르게 된다.
    headers = {
        'Content-Type': 'application/x-www-form-urlencoded'
    } 
    # 리퀘스트를 FASTAPI 백엔드에 보냄
    response = requests.post(url=login_url, data=data, headers=headers)
    
    # Response를 받게 됨. 만약 Response를 받았다면, status code를 통해 로그인 여부를 판단
    # 200 = 제대로 되었음. 액세스토큰을 받아옴. 로그인 성공
    # 나머지 = 로그인 실패
    if response.status_code == 200:
        # 세션 사용자 토큰을 담는 곳이 세션상태(Session_state)에 없다면, 토큰을 만들어 저장
        if 'token' not in st.session_state:

            placeholder.empty()
            token_info = response.json()
            st.session_state.token = token_info

            st.success("Login successful")
            st.page_link("main.py", label="***Go Back***", icon="⬅️")
        else:
            st.error("Already Logined")
    else:
        info = response.json()
        st.error("Login failed, {}".format(info["detail"]))

else:
    pass