import time
from PIL import Image
import streamlit as st

st.set_page_config(
    page_title="SoberSnap - 酔い止めVlog", page_icon="🍷", layout="centered"
)

# 初期化処理
if "step" not in st.session_state:
    st.session_state.step = "start"
if "party_title" not in st.session_state:
    st.session_state.party_title = ""
if "logs" not in st.session_state:
    st.session_state.logs = []
if "warning_level" not in st.session_state:
    st.session_state.warning_level = 0
if "last_file_name" not in st.session_state:
    st.session_state.last_file_name = None  # アップロード済みファイル識別用
if "uploaded_image" not in st.session_state:
    st.session_state.uploaded_image = None


# --- 1. スタート画面 ---
if st.session_state.step == "start":
    st.title("🍷 SoberSnap (ベータ版)")
    st.subheader("お酒に飲まれない、大人のスマートディナーVlog")

    st.markdown("---")
    st.session_state.party_title = st.text_input(
        "今日の飲み会タイトル", "例：有嘉代と久々片町デート"
    )

    if st.button(
        "飲み会をスタートする 🚀", type="primary", use_container_width=True
    ):
        if st.session_state.party_title:
            st.session_state.step = "main"
            st.rerun()
        else:
            st.warning("タイトルを入力してください。")


# --- 2. メイン画面 ---
elif st.session_state.step == "main":
    st.title(f"🍻 {st.session_state.party_title}")

    # 警告レベル表示
    if st.session_state.warning_level >= 2:
        st.error("🚨 **【警告】判断力が低下しています！ ペースを落としましょう！**")
    elif st.session_state.warning_level == 1:
        st.warning("⚠️ **【注意】お水を一杯挟みましょう！**")

    tab_record, tab_slideshow = st.tabs(["📸 記録する", "🎬 思い出スライドショー"])

    with tab_record:
        st.subheader("📸 記録する")
        upload_type = st.radio(
            "何を記録しますか？", ["乾杯・お酒", "おつまみ・料理"], horizontal=True
        )

        uploaded_file = st.file_uploader(
            "写真を撮影 (またはアップロード)", type=["jpg", "jpeg", "png"]
        )

        # ファイルが変更されたらキャッシュをクリアして新しい画像を読み込む
        if uploaded_file is not None:
            if uploaded_file.name != st.session_state.last_file_name:
                try:
                    image = Image.open(uploaded_file)
                    image.thumbnail((1024, 1024))
                    st.session_state.uploaded_image = image
                    st.session_state.last_file_name = uploaded_file.name
                except Exception:
                    st.error("画像の読み込みに失敗しました")
        else:
            st.session_state.uploaded_image = None
            st.session_state.last_file_name = None

        if st.session_state.uploaded_image is not None:
            st.image(st.session_state.uploaded_image, use_column_width=True)

            if upload_type == "乾杯・お酒":
                drink_name = st.text_input("ドリンク名", "生ビール")
                if st.button("このドリンクを記録 🍻"):
                    st.session_state.logs.append({"type": "ドリンク", "name": drink_name, "image": st.session_state.uploaded_image})
                    st.session_state.warning_level += 1
                    st.session_state.uploaded_image = None
                    st.success("記録しました！")
                    st.rerun()
            else:
                food_name = st.text_input("おつまみ・料理名", "つき出し")
                if st.button("このおつまみを記録 🍳"):
                    st.session_state.logs.append({"type": "おつまみ", "name": food_name, "image": st.session_state.uploaded_image})
                    st.session_state.uploaded_image = None
                    st.success("記録しました！")
                    st.rerun()

        st.markdown("---")
        if st.button("🏁 飲み会を終了"):
            st.session_state.step = "summary"
            st.rerun()

    with tab_slideshow:
        if not st.session_state.logs:
            st.info("まだ写真がありません。")
        else:
            idx = st.slider("写真を選ぶ", 0, len(st.session_state.logs)-1, 0)
            log = st.session_state.logs[idx]
            st.image(log["image"], use_column_width=True)
            st.markdown(f"<div style='background:#1e293b; padding:20px; border-radius:10px; text-align:center; font-size:20px;'>💬 {log['name']}</div>", unsafe_allow_html=True)

# --- 3. 振り返り画面 ---
elif st.session_state.step == "summary":
    st.title("本日のVlogまとめ")
    for log in st.session_state.logs:
        st.image(log["image"], use_column_width=True)
        st.markdown(f"### {log['name']}")
    
    if st.button("最初からやり直す"):
        st.session_state.clear()
        st.rerun()
