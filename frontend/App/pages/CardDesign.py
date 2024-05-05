"""
    file : Streamlit. App.CardDesign.py
    writer : Meohong
    first date : 2024-05-03
    Objective : CardDesign( Service )
    modified :
    ========================================================================
        date    |   no  |                 note
     2024-05-03 |   1   |   first write
     2024-05-05 |   2   |   사진 추가
     2024-05-06 |   3   |   사진 합성 기능 추가
     2024-05-06 |   4   |   카드 만들기 -> 마이데이터 넘어가는 기능 추가
    ========================================================================
"""

# 이미지 관련 페이지 
import streamlit as st
import cv2
import requests
import numpy as np

import io
import base64
from PIL import Image
import json
import os
from streamlit_image_select import image_select
from rembg import remove

st.set_page_config(page_title="Card Design", layout="centered")

url = "http://localhost:50000"


def go_back_design():
    if "card_page" in st.session_state:
        del st.session_state["card_page"]
    if "gen_cards" in st.session_state:
        del st.session_state["gen_cards"]
    if "Card_image_result" in st.session_state:
        del st.session_state["Card_image_result"]

def change_page(number):
    st.session_state["card_page"] = number

# 메인페이지, 버튼은 현재 단디 만들기만 활성화
def card_image_main():    
    st.title("Card Design")
    with st.container():
        col1, col2 = st.columns(spec=[0.4, 0.6], gap="small")
        with col1:
            reset = st.button(label="Reset", on_click=go_back_design)
        with col2:
            container_image = st.image("./App/Storage/기본카드템플릿.png",width=400, channels="BGR")

        for _ in range(3):
            st.columns(spec=1)

        empty1, buttons, empty2 = st.columns(spec=[0.1, 0.8, 0.1])
        
        with buttons:
            button_1_left, button_1_right = st.columns(spec=2, gap="small")
            with button_1_left:
                creating = st.button("나만의 우단똑 삽입하기",on_click=change_page, kwargs={"number": 1}, use_container_width=True)
            with button_1_right:
                pattern = st.button("패턴(무늬) 넣기",use_container_width=True)
            button_2_left, button_2_right = st.columns(spec=2, gap="small")
            with button_2_left:
                color_change = st.button("색 바꾸기", use_container_width=True)
            with button_2_right:
                recommend = st.button("추천 프리셋 적용", use_container_width=True)

        empty3 = st.columns(spec=1)
        button_3_left, button_3_right = st.columns(spec=[0.2,0.8], gap="small")
        with button_3_left:
            st.page_link("main.py", label="이전")
        with button_3_right:
            decision = st.button("결정",use_container_width=True)

        if reset:
            st.rerun()

# 페이지 2 단디 이미지 생성
def card_image_2():
    # try:
    #     if 'token' not in st.session_state:
    #         raise

    #     token = st.session_state['token']["access_token"]
    #     header = {
    #         'accept': 'application/json',
    #         'Authorization': f'Bearer {token}'
    #     }

    # except Exception as e:
    #     st.error("Not Logined!")
    
    st.title("Card Design")
    with st.container():
        col1, col2 = st.columns(spec=[0.4, 0.6], gap="small")
        with col1:
            reset = st.button(label="Reset", on_click=go_back_design)
        with col2:
            container_image = st.image("./App/Storage/기본카드템플릿2.png", width=400, channels="BGR")

        for _ in range(3):
            st.columns(spec=1)

        empty1, texts, empty2 = st.columns(spec=[0.1, 0.8, 0.1])
        with texts:
            with st.container(border=True):
                textbox, buttons = st.columns(spec=[0.8, 0.1])
                with textbox:
                    input_value = st.text_input("***Input***", placeholder="만들고 싶은 이미지를 입력하세요")
                with buttons:
                    enter = st.button("⤴️")
                    
        if reset:
            st.rerun()
        if enter and input_value:
            # image_gen_url = url + "/webui/txt2img"
            # json = {
            #     'input_prompt' : input_value
            # }
            # response = requests.post(url=image_gen_url, params=json, headers=header)
            # res = json.loads(response.content)

            # img_list = list(map(lambda x : Image.open(io.BytesIO(base64.b64decode(x))), res))
            change_page(number=2)
            
            # 이미지 오픈
            now_dir = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
            img_path = now_dir + "/Storage/gen_img/"
            img_list = os.listdir(img_path)
            img_list_png = [img for img in img_list if img.endswith(".png")]
            imgs = list(map(lambda x : Image.open(img_path + str(x)), img_list_png))

            st.session_state["gen_cards"] = imgs
            # print("다 만듦")
        if enter and not input_value:
            st.error("Enter input Prompt!")


# 페이지 3, 단디 이미지 생성 후, 이미지 위치 조정
def card_image_3():
    st.title("Card Design")
    imgs = st.session_state["gen_cards"]
    imgs_convert = list(map(lambda x : x.convert("RGB"), imgs))


    # 이미지 합성하기 기능
    def image_synthesis(index, imgs, mv_width=200, mv_height=512):
        now_dir = os.path.dirname(os.path.dirname(os.path.realpath(__file__))) +"/Storage/"
        background_image_url = now_dir+"기본카드템플릿2.png"
        
        # 이미지 열기
        sel_img = imgs[index]
        bg_img = Image.open(background_image_url)
        width, height = (bg_img.size[0], bg_img.size[1])
        # 크기 리사이즈 및 붙이기 용으로, 
        result = Image.new("RGBA", (width, height))

        # st.image(sel_img, width=300)
        # 이미지 덧붙이기
        result.paste(im=sel_img, box=(mv_width,mv_height))
        result2 = Image.alpha_composite(result, bg_img)
        
        # st.image(result2, width=600)

        return result2
    
    with st.container():
        col1, col2 = st.columns(spec=[0.4, 0.6], gap="small")
        with col1:
            reset = st.button(label="Reset", on_click=go_back_design)

        for _ in range(1):
            st.columns(spec=1)

        convert = st.button(label="다음")
        sel_img_index = image_select(
            label = "Generated Image",
            images = imgs_convert,
            return_value="index",
        )
        mv_width = st.slider("Card Horizonal location",min_value=0, max_value= 400, value=10)
        mv_height = st.slider("Card Vertical Location", min_value=10, max_value=1000, value=10)
        
        result = image_synthesis(sel_img_index, imgs, mv_width, mv_height)

        with col2:
            container_image = st.image(result, width=400)
        
        # 버튼을 누르면 다음 페이지로 이동
        if convert:
            change_page(3)

            st.session_state["Card_image_result"] = result
            st.rerun()

# 페이지 4, 배경 설정 
def card_image_4():
    st.title("Card Design")

    # 이미지 오픈
    card_image_proc = st.session_state["Card_image_result"]

    now_dir = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
    img_path = now_dir + "/Storage/card_pattern/"
    img_list = os.listdir(img_path)
    img_list_png = [img for img in img_list if img.endswith(".png")]
    pattern_imgs = list(map(lambda x : Image.open(img_path + str(x)), img_list_png))
    pattern_imgs_convert = list(map(lambda x : x.convert("RGB"), pattern_imgs))


    def pattern_synthesis(pattern_index, pattern_imgs, card_image):
        pattern = pattern_imgs[pattern_index]

        result = Image.alpha_composite(pattern, card_image)

        # st.image(result, width=300)
        return result

    with st.container():
        col1, col2 = st.columns(spec=[0.4, 0.6], gap="small")
        with col1:
            reset = st.button(label="Reset", on_click=go_back_design)
        
        for _ in range(5):
            st.columns(spec=1)
        
        convert = st.button(label="다음")

        pattern_index = image_select(
            label = "Pattern",
            images = pattern_imgs_convert,
            return_value="index",
        )

        result = pattern_synthesis(
            pattern_index=pattern_index,
            pattern_imgs=pattern_imgs,
            card_image=card_image_proc
            )

        with col2:
            container_image = st.image(result, width=400)
        
        if convert:
            # 페이지 전환
            change_page(4)
            
            # 현재 진행상황 저장
            st.session_state["Card_design_result"] = result
            st.rerun()

def card_image_5():
    st.title("Card Design")

    # 현재 진행중인 사항 가져오기
    card_designs = st.session_state["Card_design_result"]

    def change_color(circle, card, colors):
        now_dir = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
        img_path = now_dir + "/Storage/card_pattern/card_pattern_kai/"
        img_list = os.listdir(img_path)
        img_list_png = [img for img in img_list if img.endswith(".png")]
        pattern_imgs = list(map(lambda x : Image.open(img_path + str(x)), img_list_png))
        card_design_result = st.session_state["Card_image_result"]

        if circle == 0:
            image = pattern_imgs[1]
            result = Image.alpha_composite(image, card_design_result)
            st.image(result, width=300)
            st.session_state["Card_design_result"] = result
        elif circle == 1:
            image = pattern_imgs[0]
            result = Image.alpha_composite(image, card_design_result)
            st.session_state["Card_design_result"] = result
        
        st.rerun()


    with st.container():
        col1, col2 = st.columns(spec=[0.4, 0.6], gap="small")
        with col1:
            reset = st.button(label="Reset", on_click=go_back_design)
        
        for _ in range(3):
            st.columns(spec=1)
        
        convert = st.button(label="다음")

        color_side1, color_side2 = st.columns(spec=2, gap="large")
        with color_side1:
            color1 = st.color_picker("Pick Circle 1 Color", '#AAAAAA')
            commit1 = st.button(label="적용")
            if commit1:
                change_color(0, card_designs, color1)

        with color_side2:
            color2 = st.color_picker("Pick Circle 2 Color", '#7E7A7A')
            commit2 = st.button(label="적용2")
            if commit2:
                change_color(1, card_designs, color2)

        with col2:
            container_image = st.image(card_designs, width=400)

        if convert:
            st.session_state["Card_image_result"] = st.session_state["Card_design_result"]
            del st.session_state["Card_design_result"]
            
            change_page(5)
            st.rerun()
        
def card_image_6():
    st.title("Card Design")

    card_final = st.session_state["Card_image_result"]
    
    if "card_page" in st.session_state:
        del st.session_state["card_page"]
    if "gen_cards" in st.session_state:
        del st.session_state["gen_cards"]
    if "Card_image_result" in st.session_state:
        del st.session_state["Card_image_result"]

    with st.container():
        col1, col2 = st.columns(spec=[0.4, 0.6], gap="small")
        with col1:
            st.success("카드를 만들었어요! 이제 마이데이터를 연결해봐요! 큰 혜택이 있을지도?")
            st.page_link("pages/Mydata.py", label="**마이 데이터**",icon="📑", use_container_width=True)
        with col2:
            container_image = st.image(card_final, width=400)


if "card_page" not in st.session_state or st.session_state["card_page"] == 0:
    card_image_main()
elif st.session_state["card_page"] == 1:
    card_image_2()
elif st.session_state["card_page"] == 2:
    card_image_3()
elif st.session_state["card_page"] == 3:
    card_image_4()
elif st.session_state["card_page"] == 4:
    card_image_5()
elif st.session_state["card_page"] == 5:
    card_image_6()
