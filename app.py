import time
from PIL import Image
import streamlit as st
import random

st.set_page_config(page_title="SoberSnap", page_icon="🍷", layout="centered")

# 初期化
if "step" not in st.session_state: st.session_state.step = "start"
if "logs" not in st.session_state: st.session_state.logs = []
if "warning_level" not in st.session_state: st.session_state.warning_level = 0
if "quiz_active" not in st.session_state: st.session_state.quiz_active = False

# --- 1. スタート ---
if st.session_state.step == "start":
    st.title("🍷 SoberSnap")
    title = st.text_input("飲み会タイトル", "有嘉代と片町デート")
    if st.button("スタート 🚀"):
        st.session_state.party_title = title
        st.session_state.step = "main"
        st.rerun()

# --- 2. メイン ---
elif st.session_state.step == "main":
    st.title(f"🍻 {st.session_state.party_title}")
    
    # クイズ表示
    if st.session_state.quiz_active:
        st.subheader("💡 酔い覚ましクイズ")
        if st.button("次のドリンクを飲む前にクイズ！"):
            st.info("「ウコンの力の成分は？」→ 正解：クルクミン")
            st.session_state.quiz_active = False
            st.rerun()

    tab1, tab2 = st.tabs(["📸 記録", "🎬 思い出"])
    
    with tab1:
        upload_type = st.radio("何を記録？", ["乾杯・お酒", "おつまみ・料理"], horizontal=True)
        uploaded_file = st.file_uploader("写真を選択", type=["jpg", "jpeg", "png"])

        if uploaded_file:
            # エラー防止：バイナリデータとして開き、画像を表示
            image = Image.open(uploaded_file)
            st.image(image, use_column_width=True)
            
            name = st.text_input("名前", "生ビール" if upload_type=="乾杯・お酒" else "つき出し")
            
            if st.button("記録する"):
                st.session_state.logs.append({"type": upload_type, "name": name, "image": image})
                if upload_type == "乾杯・お酒":
                    st.session_state.warning_level += 1
                    st.session_state.quiz_active = True # クイズフラグON
                st.success("記録しました！")
                time.sleep(1)
                st.rerun()

    with tab2:
        if not st.session_state.logs:
            st.write("まだ記録はありません")
        else:
            idx = st.slider("写真選択", 0, len(st.session_state.logs)-1, 0)
            log = st.session_state.logs[idx]
            st.image(log["image"], use_column_width=True)
            st.markdown(f"### 💬 {log['name']}")

    if st.button("終了して振り返る"):
        st.session_state.step = "summary"
        st.rerun()

# --- 3. 振り返り ---
elif st.session_state.step == "summary":
    st.title("本日のまとめ")
    for log in st.session_state.logs:
        st.image(log["image"], use_column_width=True)
        st.write(f"### {log['name']}")
    if st.button("最初から"):
        st.session_state.clear()
        st.rerun()
