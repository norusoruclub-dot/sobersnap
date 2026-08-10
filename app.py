import time
from PIL import Image
import streamlit as st

st.set_page_config(page_title="SoberSnap", page_icon="🍷", layout="centered")

# 初期化
if "step" not in st.session_state:
    st.session_state.step = "start"
if "party_title" not in st.session_state:
    st.session_state.party_title = "飲み会"
if "logs" not in st.session_state:
    st.session_state.logs = []
if "warning_level" not in st.session_state:
    st.session_state.warning_level = 0
if "quiz_active" not in st.session_state:
    st.session_state.quiz_active = False
if "uploader_key" not in st.session_state:
    st.session_state.uploader_key = 0  # アップロード欄をリセットするためのキー

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

    # クイズ表示
    if st.session_state.quiz_active:
        st.info("💡 **【酔い覚ましクイズ】次の一杯に行く前に一息！**")
        if st.button("クイズに答える / スキップ", use_container_width=True):
            st.session_state.quiz_active = False
            st.rerun()

    tab1, tab2 = st.tabs(["📸 記録", "🎬 思い出"])

    with tab1:
        upload_type = st.radio(
            "何を記録？", ["乾杯・お酒", "おつまみ・料理"], horizontal=True
        )

        # 動的なキーを使うことで、記録するたびにアップローダーを完全に初期化する
        uploaded_file = st.file_uploader(
            "写真を選択",
            type=["jpg", "jpeg", "png"],
            key=f"uploader_{st.session_state.uploader_key}",
        )

        if uploaded_file is not None:
            try:
                image = Image.open(uploaded_file)
                image.thumbnail((1024, 1024))
                st.image(image, use_container_width=True)

                default_name = (
                    "生ビール" if upload_type == "乾杯・お酒" else "つき出し"
                )
                name = st.text_input("名前を入力", default_name)

                if st.button("記録する 📝", use_container_width=True):
                    st.session_state.logs.append(
                        {"type": upload_type, "name": name, "image": image}
                    )
                    if upload_type == "乾杯・お酒":
                        st.session_state.warning_level += 1
                        st.session_state.quiz_active = True

                    # アップローダーのキーを更新してフォームをリセット・次へ備える
                    st.session_state.uploader_key += 1
                    st.success("記録しました！")
                    time.sleep(1)
                    st.rerun()
            except Exception:
                st.error("画像の処理に失敗しました。")

    with tab2:
        if not st.session_state.logs:
            st.info("まだ記録はありません")
        else:
            max_val = len(st.session_state.logs) - 1
            if max_val == 0:
                idx = 0
                st.write(f"写真 1: {st.session_state.logs[0]['name']}")
            else:
                idx = st.slider("写真選択", 0, max_val, 0)

            log = st.session_state.logs[idx]
            st.image(log["image"], use_container_width=True)
            st.markdown(
                f"<div style='background:#1e293b; color:white; padding:15px; border-radius:10px; text-align:center; font-size:18px;'>💬 {log['name']}</div>",
                unsafe_allow_html=True,
            )

    st.markdown("---")
    if st.button("🏁 終了して振り返る", use_container_width=True):
        st.session_state.step = "summary"
        st.rerun()

# --- 3. 振り返り ---
elif st.session_state.step == "summary":
    st.title("🎉 本日のまとめ")
    if not st.session_state.logs:
        st.info("記録はありません。")
    else:
        for log in st.session_state.logs:
            st.image(log["image"], use_container_width=True)
            st.markdown(f"### 🎞️ {log['name']}")

    if st.button("最初からやり直す", use_container_width=True):
        st.session_state.clear()
        st.rerun()
