import os
import time
from PIL import Image
import streamlit as st
import google.generativeai as genai

# APIキーの設定
if "GEMINI_API_KEY" in os.environ:
    genai.configure(api_key=os.environ["GEMINI_API_KEY"])

st.set_page_config(page_title="SoberSnap", page_icon="🍷", layout="centered")

# 初期化
if "step" not in st.session_state:
    st.session_state.step = "start"
if "party_title" not in st.session_state:
    st.session_state.party_title = "飲み会"
if "logs" not in st.session_state:
    st.session_state.logs = []
if "uploader_key" not in st.session_state:
    st.session_state.uploader_key = 0
if "detected_drink" not in st.session_state:
    st.session_state.detected_drink = ""

# --- 1. スタート ---
if st.session_state.step == "start":
    st.title("🍷 SoberSnap")
    title = st.text_input("飲み会タイトル", "有嘉代と片町デートin帆夏")
    if st.button("スタート 🚀", use_container_width=True):
        st.session_state.party_title = title
        st.session_state.step = "main"
        st.rerun()

# --- 2. メイン ---
elif st.session_state.step == "main":
    st.title(f"🍻 {st.session_state.party_title}")
    
    # 画像アップロード
    uploaded_file = st.file_uploader(
        "お酒や飲み物の写真をアップロード", 
        type=["jpg", "jpeg", "png"],
        key=f"uploader_{st.session_state.uploader_key}"
    )
    
    if uploaded_file is not None:
        image = Image.open(uploaded_file)
        st.image(image, use_container_width=True)
        
        # 新しい写真がアップロードされたときだけAI判定を実行
        if "last_file" not in st.session_state or st.session_state.last_file != uploaded_file.name:
            st.session_state.last_file = uploaded_file.name
            with st.spinner("AIが飲み物を判定中..."):
                try:
                    # 安定動作するフラッシュモデルを指定
                    model = genai.GenerativeModel('gemini-1.5-flash')
                    response = model.generate_content([
                        image, 
                        "この画像に写っている飲み物の名前（例：生ビール、ハイボール、ジントニック、ウーロン茶など）を、商品名やカクテル名だけで極めて簡潔に答えてください。余計な説明は一切不要です。"
                    ])
                    st.session_state.detected_drink = response.text.strip()
                except Exception as e:
                    st.session_state.detected_drink = "生ビール" # 万が一エラーの時は生ビールをフォールバック
            st.rerun()
    
    st.write("名前を入力")
    # 判定された結果を強制的に入力欄の初期値として反映
    name_input = st.text_input("ドリンク名", value=st.session_state.detected_drink, key="current_drink_name")
    
    if st.button("記録する 📝", use_container_width=True):
        if name_input:
            st.session_state.logs.append(name_input)
            st.session_state.uploader_key += 1
            st.session_state.detected_drink = ""
            if "last_file" in st.session_state:
                del st.session_state.last_file
            st.success(f"「{name_input}」を記録しました！")
            time.sleep(1)
            st.rerun()
