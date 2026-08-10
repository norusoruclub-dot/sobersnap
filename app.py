import time
from PIL import Image
import streamlit as st

st.set_page_config(
    page_title="SoberSnap - 酔い止めVlog", page_icon="🍷", layout="centered"
)

if "step" not in st.session_state:
    st.session_state.step = "start"
if "party_title" not in st.session_state:
    st.session_state.party_title = ""
if "logs" not in st.session_state:
    st.session_state.logs = (
        []
    )  # 構造: {"type": "ドリンク" or "おつまみ", "name": 名前, "image": 画像データ}
if "warning_level" not in st.session_state:
    st.session_state.warning_level = 0
if "uploaded_image" not in st.session_state:
    st.session_state.uploaded_image = None
if "temp_name" not in st.session_state:
    st.session_state.temp_name = ""


# --- 1. スタート画面 ---
if st.session_state.step == "start":
    st.title("🍷 SoberSnap (ベータ版)")
    st.subheader("お酒に飲まれない、大人のスマートディナーVlog")

    st.markdown("---")
    st.session_state.party_title = st.text_input(
        "今日の飲み会タイトル", "例：有森代と久々片町デート"
    )

    if st.button(
        "飲み会をスタートする 🚀", type="primary", use_container_width=True
    ):
        if st.session_state.party_title:
            st.session_state.step = "main"
            st.session_state.logs = []
            st.session_state.warning_level = 0
            st.session_state.uploaded_image = None
            st.rerun()
        else:
            st.warning("タイトルを入力してください。")


# --- 2. メイン画面（記録・修正・スライドショー） ---
elif st.session_state.step == "main":
    st.title(f"🍻 {st.session_state.party_title}")

    if st.session_state.warning_level == 1:
        st.warning("⚠️ **【注意】少し回ってきたかも？ お水を一杯挟みましょう！**")
    elif st.session_state.warning_level >= 2:
        st.error(
            "🚨 **【警告】判断力が低下しています！ ペースを落としてお水を飲んでください！**"
        )

    st.markdown("---")

    # タブ切り替え（「記録する」と「本日の思い出スライドショー」）
    tab_record, tab_slideshow = st.tabs(["📸 記録する", "🎬 思い出スライドショー"])

    with tab_record:
        st.subheader("📸 記録する")
        upload_type = st.radio(
            "何を記録しますか？", ["乾杯・お酒", "おつまみ・料理"], horizontal=True
        )

        uploaded_file = st.file_uploader(
            "写真を撮影 (またはアップロード) ", type=["jpg", "jpeg", "png"]
        )

        if uploaded_file is not None:
            image = Image.open(uploaded_file)
            st.session_state.uploaded_image = image
            st.image(image, caption="撮影された画像", use_column_width=True)

            if upload_type == "乾杯・お酒":
                drink_name = st.text_input(
                    "ドリンク名を入力", "生ビール", key="input_drink_name"
                )
                if st.button("このドリンクを記録する 🍻", use_container_width=True):
                    st.session_state.logs.append(
                        {
                            "type": "ドリンク",
                            "name": drink_name,
                            "image": st.session_state.uploaded_image,
                        }
                    )
                    st.session_state.warning_level += 1
                    st.success(
                        f"「{drink_name}」を記録しました！お水も一緒にどうぞ✨"
                    )
                    time.sleep(1)
                    st.rerun()
            else:
                food_name = st.text_input(
                    "おつまみ・料理名を入力", "つき出し", key="input_food_name"
                )
                if st.button("このおつまみを記録する 🍳", use_container_width=True):
                    st.session_state.logs.append(
                        {
                            "type": "おつまみ",
                            "name": food_name,
                            "image": st.session_state.uploaded_image,
                        }
                    )
                    st.success(f"「{food_name}」を記録しました！")
                    time.sleep(1)
                    st.rerun()

        st.markdown("---")
        st.subheader("📝 本日のログ一覧（テキスト確認）")
        if not st.session_state.logs:
            info_text = (
                "まだ記録がありません。上のカメラから撮影して記録を追加しましょう！"
            )
            st.info(info_text)
        else:
            for i, log in enumerate(st.session_state.logs):
                if log["type"] == "ドリンク":
                    st.markdown(f"🍺 **ドリンク {i+1}**: {log['name']}")
                else:
                    st.markdown(f"🍽️ **フード {i+1}**: {log['name']}")

        st.markdown("---")
        if st.button("🏁 飲み会を終了して振り返る", use_container_width=True):
            st.session_state.step = "summary"
            st.rerun()

    with tab_slideshow:
        st.subheader("🎬 思い出スライドショー ＆ 字幕")
        if not st.session_state.logs:
            st.info(
                "まだ写真の記録がありません。「記録する」タブから写真を追加してください。"
            )
        else:
            st.markdown(
                "撮影した写真が、当時の字幕（記録名）と一緒にスライド形式で流れます！"
            )

            # スライドショー風に番号を選んで表示、またはすべて順番に表示
            slide_index = st.slider(
                "スライドを選択",
                0,
                len(st.session_state.logs) - 1,
                0,
                format_func=lambda x: f"写真 {x+1}: {st.session_state.logs[x]['name']}",
            )

            current_log = st.session_state.logs[slide_index]

            # 画像と字幕の表示
            st.image(
                current_log["image"],
                caption=f"【{current_log['type']}】 {current_log['name']}",
                use_column_width=True,
            )

            # 映画の字幕風のスタイリッシュなBOX
            st.markdown(
                f"""
                <div style="background-color: #1e293b; color: #ffffff; padding: 20px; border-radius: 10px; text-align: center; font-size: 22px; font-weight: bold; margin-top: 15px;">
                    💬 字幕: 「 {current_log['name']} 」
                </div>
                """,
                unsafe_allow_html=True,
            )


# --- 3. 終了・振り返り画面 ---
elif st.session_state.step == "summary":
    st.title("🎉 お疲れ様でした！本日のVlogまとめ")
    st.subheader(f"飲み会タイトル: {st.session_state.party_title}")

    st.markdown("---")
    st.subheader("🎬 思い出のハイライト（スライドショー）")

    if not st.session_state.logs:
        st.info("記録はありませんでした。")
    else:
        for i, log in enumerate(st.session_state.logs):
            st.markdown(f"### シーン {i+1}: {log['type']}")
            st.image(log["image"], use_column_width=True)
            st.markdown(
                f"""
                <div style="background-color: #0f172a; color: #38bdf8; padding: 15px; border-radius: 8px; text-align: center; font-size: 20px; font-weight: bold; margin-bottom: 20px;">
                    🎞️ 字幕: {log['name']}
                </div>
                """,
                unsafe_allow_html=True,
            )

    st.markdown("---")
    if st.button("🔄 最初からやり直す", type="primary", use_container_width=True):
        st.session_state.step = "start"
        st.session_state.logs = []
        st.session_state.warning_level = 0
        st.rerun()
