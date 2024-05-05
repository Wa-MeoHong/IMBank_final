"""
    file : Streamlit. App.Userdata.py
    writer : Meohong
    first date : 2024-05-02
    Objective : Signup, Modifing User Data ( Service )
    modified :
    ========================================================================
        date    |   no  |                 note
     2024-05-01 |   1   |   first write

    ========================================================================
"""
import streamlit as st
import requests


placeholder = st.empty()

# Fastapi URL
url = "http://localhost:50000"

def signup():
    with placeholder.form('Sign Up'):
        col1, col2 = st.columns(spec=[0.85, 0.15], gap="small")
        #st.markdown("#### Enter your credentials")
        with col1:
            st.markdown("### Sign Up Form")
        with col2:
            st.page_link("main.py", label="***Go Back***", icon="⬅️")

        empty1, col3, empty2 = st.columns(spec=[0.1, 0.8, 0.1])
        with col3:
            side1, side2 = st.columns(spec=2)
            with side1:
                name = st.text_input("**Name**")
                email = st.text_input("**Email**")
                password = st.text_input("**Password**", type="password")
            with side2:
                student_id = st.text_input("**Student ID**")
                University = st.text_input("**University**")
                major = st.text_input("**major**")
        submit = st.form_submit_button("Sign Up")

    if submit:
        # If the form is submitted and the email and password are correct,
        # clear the form/container and display a success message

        # 데이터를 묶어 JSON형식으로 제작, 쿼리 파라미터로 들어간다.
        data_user = {
            "name": name,
            "email": email,
            "password": password
        }
        data_student = {
            "user_email": email,
            "student_id": student_id,
            "university_name": University,
            "major": major
        }
        response1 = requests.post(url=url+"/user/signup", params=data_user)
        response2 = requests.post(url=url+"/student/save_student", params=data_student)

        if response1.status_code == 200 and response2.status_code == 200:
            placeholder.empty()
            st.success("Signup successful")
            st.page_link("main.py", label="***Go Back***", icon="⬅️")
        else:
            info = response1.json()
            info2 = response2.json()
            st.error([info, info2])

def Resign():
    st.session_state['page_resign'] = True

def resign():
    token = st.session_state['token']["access_token"]
    header = {
        'accept': 'application/json',
        'Authorization': f'Bearer {token}'
    }
    response_delete_std = requests.delete(url=url+"/student/delete_student", headers=header)
    response_delete_usr = requests.delete(url=url+"/user/resign", headers=header)

    if response_delete_std.status_code == 200 and response_delete_usr.status_code== 200:
        st.success("Remove User data successful")
        del st.session_state["token"]       # 유저정보 삭제로 인한 토큰 삭제
        st.page_link("main.py", label="***Go Back***", icon="⬅️")
    else:
        st.error("Error in Delete User!")

def modify():
    # 토큰 헤더, 중요함.
    try:
        if 'token' not in st.session_state:
            raise

        token = st.session_state['token']["access_token"]
        header = {
            'accept': 'application/json',
            'Authorization': f'Bearer {token}'
        }

    except Exception as e:
        st.error("Not Logined!")
        return

    # 먼저 가져올 데이터는 미리 가져옴
    response1 = requests.get(url=url+"/user/userdata", headers=header)
    if response1.status_code == 200:
        user_data = response1.json()
    else:
        st.stop()
    response2 = requests.get(url=url+"/student/get_student", headers=header)
    if response2.status_code == 200:
        student_data = response2.json()
    else:
        st.stop()


    with placeholder.form('Modify Data'):
        col1, col2 = st.columns(spec=[0.85, 0.15], gap="small")
        #st.markdown("#### Enter your credentials")
        with col1:
            st.markdown("### Modify Form")
        with col2:
            st.page_link("main.py", label="***Go Back***", icon="⬅️")

        empty1, col3, empty2 = st.columns(spec=[0.1, 0.8, 0.1])
        with col3:
            side1, side2 = st.columns(spec=2)
            with side1:
                name = st.text_input(label="**Name**", value=user_data["name"])
                email = st.text_input("**Email**", value=user_data["email"], disabled=True)
                password = st.text_input("**Password**", type="password")
            with side2:
                student_id = st.text_input("**Student ID**", value=student_data["studentid"])
                University = st.text_input("**University**", value=student_data["univ"])
                major = st.text_input("**major**", value=student_data["major"])
        submit_side1, submit_side2, empty_side1 = st.columns(spec=[0.13, 0.13, 0.76])
        with submit_side1:
            submit1 = st.form_submit_button("Modify")
        with submit_side2:
            submit2 = st.form_submit_button("Resign", type="primary")

    if submit1:
        # 데이터를 묶어 JSON형식으로 제작, 쿼리 파라미터로 들어간다.
        data_user = {
            "name": name,
            "email": email,
            "password": password
        }
        data_student = {
            "student_id": student_id,
            "university_name": University,
            "major": major
        }
        # 헤더엔 액세스 토큰이, 그리고, 내용엔 수정할 내용이 담김
        response1 = requests.patch(url=url+"/user/update", params=data_user, headers=header)
        response2 = requests.patch(url=url+"/student/modify_student", params=data_student, headers=header)

        if response1.status_code == 200 and response2.status_code == 200:
            placeholder.empty()
            del st.session_state['token']       # 정보 수정으로 인한 로그인 토큰 초기화
            st.success("Signup successful")     # 성공 메세지
            st.page_link("main.py", label="***Go Back***", icon="⬅️")        # 메뉴 복귀
        else:
            st.error("Error in modifying User Data, {}".format(response1.json()["detail"]))
    
    # 탈퇴한다고 선택하면 나오는 것. 좀 복잡한 로직으로 되어있다.
    if submit2:
        placeholder.empty()
        st.error("정말로 탈퇴하시겠습니까?")
        submit_button1, submit_button2, empty_side2 = st.columns(spec=[0.13,0.14,0.76], gap="small")
        with submit_button1:
            submit_resign = st.button("Resign", type="primary", on_click=Resign)
        with submit_button2:
            submit_goback = st.button("Go back")


if 'token' not in st.session_state:
    signup()
elif 'page_resign' not in st.session_state:
    modify()
else:
    resign()