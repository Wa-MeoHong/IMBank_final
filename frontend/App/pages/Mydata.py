import streamlit as st
import requests
import pandas as pd
import json
import os
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm
import seaborn as sns
import numpy as np

st.set_page_config(page_title="MyData", layout="centered")

url = "http://localhost:50000"

def go_back_mydata():
    if "mydata_page" in st.session_state:
        del st.session_state["mydata_page"]
    if "account_data" in st.session_state:
        del st.session_state["account_data"]    
    if "account_num" in st.session_state:
        del st.session_state["account_num"]
    if "before_month" in st.session_state:
        del st.session_state["before_month"]
    if "graph_data" in st.session_state:
        del st.session_state["graph_data"]

def change_page(num):
    st.session_state["mydata_page"] = num

# Matplotlib 글꼴 꾸미기. 
# 껏다 키기도 해야함
# 
@st.cache_data
def fontRegistered():
    fonts_dir = os.getcwd() + "/App/Storage/fonts"
    font_files = fm.findSystemFonts()
    #st.write(font_files)
    #st.write([(f.name, f.fname) for f in fm.fontManager.ttflist if 'Nanum' in f.name])
    font_name = "NanumSquare"
    plt.rc('font', family=font_name)


def analyze_data(df):
    now_dir = os.path.dirname(os.path.dirname(os.path.realpath(__file__))) + "/Storage/analyze_data/"
    jsonfile = now_dir + "field_dict.json"
    with open(jsonfile, 'r') as f:
        field_dict = json.load(f)
    # st.write(field_dict)
    df["거래일시"] = pd.to_datetime(df["거래일시"])
    df["거래일시"] = df["거래일시"].dt.strftime("%Y-%m")
    df["메모"] = df["메모"].map(field_dict)
    df["메모"] = df["메모"].fillna("기타")

    #print(df.isnull())
    #st.dataframe(df)
    df.drop(["거래처", "남은금액"], axis=1, inplace=True)
    groups = df.groupby(["거래일시", "메모"])
    summarize_groups = groups.sum()

    #st.dataframe(groups.sum())
    result = pd.DataFrame(summarize_groups).reset_index().sort_values('거래비용', ascending=True)
    # st.dataframe(result)
    group2 = result.groupby(['거래일시'])
    
    fontRegistered()
    plt.rc('font', family='NanumGothic')

    for name, group in group2:
        col1, col2 = st.columns(spec=[0.3, 0.7], gap="small")
        with col1:
            st.dataframe(group)
        with col2:
            palette = sns.color_palette('flare', len(group["메모"]))
            
            plt.barh(group["메모"], group['거래비용'],color=palette )
            plt.title("{}".format(name[0]))
            st.pyplot(plt)
            plt.close()
    
    return result

def summarizing_data(df):
    now_dir = os.path.dirname(os.path.dirname(os.path.realpath(__file__))) + "/Storage/analyze_data/"
    jsonfile = now_dir + "field_dict.json"
    with open(jsonfile, 'r') as f:
        field_dict = json.load(f)
    # st.write(field_dict)
    df["거래일시"] = pd.to_datetime(df["거래일시"])
    df["거래일시"] = df["거래일시"].dt.strftime("%Y-%m")
    df["메모"] = df["메모"].map(field_dict)
    df["메모"] = df["메모"].fillna("기타")
    df.drop(["거래처", "남은금액", "거래일시"], axis=1, inplace=True)


    groups = df.groupby(["메모"])
    summarize_groups = groups.sum()
    result = pd.DataFrame(summarize_groups).reset_index()
    result = result[result['메모'] != '기타'].reset_index()

    # 데이터 추가
    data_gram_val = ["구독", "문화생활", "쇼핑", "식사", "카페", "편의점"]
    for value in data_gram_val:
        if value not in result["메모"].values:
            new_row = {"메모": value, "거래비용": 0}
            length = len(result["메모"].values)
            st.write(length)
            result.loc[length] = [value,0]
    result["비율"] = result["거래비용"] / result["거래비용"].sum()
    top_3 = result["비율"].nlargest(3).index

    result["혜택 비율"] = 0
    result.loc[top_3, '혜택 비율'] = result.loc[top_3, '비율']  # 상위 3개에는 비율 값 할당
    total_ratio_top_3 = result.loc[top_3, '혜택 비율'].sum()
    result.loc[top_3, '혜택 비율'] = (result.loc[top_3, '혜택 비율'] / total_ratio_top_3) * 0.15 * 100

    result.drop(["거래비용", "비율"], axis=1, inplace=True)    
    # st.write(result)
    return result

def Rader_chart(df):
    # 레이더 차트 그리기 위한 데이터
    labels = np.array(list(df["메모"]))
    values = np.array(list(df["혜택 비율"]))

    # st.write(labels)

    #각 항목에 대한 각도 계산
    angles = np.linspace(0, 2 * np.pi, len(labels), endpoint=False).tolist()
    values = np.concatenate((values, [values[0]]))
    angles += angles[:1] # 시작점 복귀

    # 방사형 차트 그리기
    fig, ax = plt.subplots(figsize=(6, 6), subplot_kw={'polar': True})
    ax.fill(angles, values, color='blue', alpha=0.25)
    ax.plot(angles, values, color='blue', linewidth=2)  # 라인 그리기

    ax.set_xticks(angles[:-1])  # 각 축 설정
    ax.set_xticklabels(labels)
    ax.set_yticklabels([])

    ax.set_ylim(-2,10)    # 축 고정

    plt.title('혜택 그래프', size=20, color='black', y=1.1)
    st.pyplot(plt)
    plt.close()

    

# 마이데이터 메인페이지
def mydata_main():
    token = st.session_state['token']["access_token"]
    header = {
        'accept': 'application/json',
        'Authorization': f'Bearer {token}'
    }

    with st.container():
        st.title("마이데이터 확인")
        account = st.text_input("**Account Number**")
        before_month = st.slider("**Before Months**", min_value=0, max_value=5, value=0)
        account_data = None
        
        buttonside1, buttonside2, buttonside3 = st.columns(spec=3, gap='large')
        with buttonside1:
            commit = st.button(label="확인")
        with buttonside2:
            next = st.button(label="다음")
        with buttonside3:
            reset = st.button(label="리셋")
        if commit:
            if not account:
                st.error("계좌 번호를 입력하세요!")
                return
             
            data = {
                "account_num": account
            }

            account_url = url + "/Mydata/getAccount"
            response1 = requests.get(url=account_url, params=data, headers=header)
            if response1.status_code == 200:
                response_data = response1.json()
                # st.write('account = ', response_data["account_num"])
            else :
                st.error("Invalid Account Number Or No data Account Number")
                st.stop()
            #print(response_data)
        
            # 계좌에 담긴 거래내역 데이터 베이스를 가져옴
            data = {
                "account_num": response_data["account_num"],
                "before_months": before_month
            }
            response2 = requests.get(url=url+"/Mydata/getMonthsData", params=data, headers=header)
            if response2.status_code == 200:
                response_data2 = response2.json()
                account_data = pd.DataFrame(response_data2)
                #st.table(data=account_data.head())
                #st.dataframe(data=account_data)
            else:
                st.error("Error")
                st.stop()

            #st.dataframe(account_data)
            analyze_data(account_data)
            
        if next:
            if account == "":
                st.error("계좌 번호를 입력하세요")
                st.stop()
            st.session_state["mydata_page"] = 1
            st.session_state["account_num"] = account
            st.session_state["before_month"] = before_month
            st.rerun()
        if reset:
            go_back_mydata()
            st.rerun()

def mydata_page_1():
    token = st.session_state['token']["access_token"]
    header = {
        'accept': 'application/json',
        'Authorization': f'Bearer {token}'
    }
    with st.container():
        st.title("마이 혜택 정하기")
        st.subheader("현재 추천해줄만한 혜택 비율이에요")
        button_side1, button_side2  = st.columns(spec=2)
        with button_side1:
            next = st.button(label="다음")
        with button_side2:
            reset = st.button(label="돌아가기")

        # 계좌에 담긴 거래내역 데이터 베이스를 가져옴
        data = {
            "account_num": st.session_state["account_num"],
            "before_months": st.session_state["before_month"]
        }
        response2 = requests.get(url=url+"/Mydata/getMonthsData", params=data, headers=header)
        if response2.status_code == 200:
            response_data2 = response2.json()
            account_data = pd.DataFrame(response_data2)

        # st.dataframe(account_data)
        result = summarizing_data(account_data)       
        
        Rader_chart(result)
        
    if next:
        st.session_state["mydata_page"] = 2
        st.session_state["graph_data"] = result
        st.rerun()
    if reset:
        go_back_mydata()
        st.rerun()

def mydata_page_2():
    result = st.session_state["graph_data"].to_dict()
    labels = list(result["메모"].values())
    values = list(result["혜택 비율"].values())

    with st.container():
        st.title("마이 혜택 정하기")
        st.subheader("커스텀이 가능해요!")
        # st.write(labels)

        button_side1, button_side2  = st.columns(spec=2)
        with button_side1:
            next = st.button(label="다음")
        with button_side2:
            reset = st.button(label="돌아가기")

        val_1, val_2, val_3 = st.columns(spec=3)
        val_4, val_5, val_6 = st.columns(spec=3)

        with val_1:
            new_value_1 = st.text_input(label="구독", value=values[0])
        with val_2:
            new_value_2 = st.text_input(label="문화생활", value=values[1])
        with val_3:
            new_value_3 = st.text_input(label="쇼핑", value=values[2])
        with val_4:
            new_value_4 = st.text_input(label="식사", value=values[3])
        with val_5:
            new_value_5 = st.text_input(label="카페", value=values[4])
        with val_6:
            new_value_6 = st.text_input(label="편의점", value=values[5])

        new_values = list((float(new_value_1), float(new_value_2), float(new_value_3), float(new_value_4), float(new_value_5), float(new_value_6)))
        graph_data = pd.DataFrame({
            '메모' : labels,
            '혜택 비율': new_values
        })

        Rader_chart(graph_data)
    
    if next:
        st.session_state["mydata_page"] = 3
        st.session_state["graph_data"] = graph_data
        st.rerun()
        
    if reset:
        go_back_mydata()
        st.rerun()

def mydata_page_3():
    with st.container():
        result = st.session_state["graph_data"]
        st.title("마이 혜택 정하기")
        st.subheader("완료했어요!")
        st.page_link("main.py", label="메뉴로")
        Rader_chart(result)


if "mydata_page" not in st.session_state or st.session_state["mydata_page"] ==0:
    mydata_main()
elif st.session_state["mydata_page"] == 1: 
    mydata_page_1()
elif st.session_state["mydata_page"] == 2:
    mydata_page_2()
elif st.session_state["mydata_page"] == 3:
    mydata_page_3()