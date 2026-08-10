import random
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
  st.session_state.logs = []
if "warning_level" not in st.session_state:
  st.session_state.warning_level = 0
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
      st.session_state.logs = []
      st.session_state.warning_level = 0
      st.session_state.uploaded_image = None
      st.rerun()
    else:
      st.warning("タイトルを入力してください。")

# --- 2. メイン画面（記録・修正・ミニテスト） ---
elif st.session_state.step == "main":
  st.title(f"🍻 {st.session_state.party_title}")

  if st.session_state.warning_level == 1:
    st.warning(
        "⚠️ **【注意】少し酔いが回ってきたかも？ お水を一杯挟みましょう！**"
    )
  elif st.session_state.warning_level >= 2:
    st.error(
        "🚨 **【警告】判断力が低下しています！ ペースを落としてお水を飲んでください！**"
    )

  st.markdown("---")

  st.subheader("📸 記録する")
  upload_type = st.radio(
      "何を記録しますか？", ["乾杯・お酒", "おつまみ・料理"], horizontal=True
  )

  uploaded_file = st.file_uploader(
      "写真を撮影（またはアップロード）", type=["jpg", "jpeg", "png"]
  )

  # スマホの写真が重くてリセットされるのを防ぐため、読み込んで縮小・保持する処理
  if uploaded_file is not None:
    try:
      img = Image.open(uploaded_file)
      img.thumbnail((1024, 1024))  # スマホ負荷軽減のため大きさを自動調整
      st.session_state.uploaded_image = img
    except Exception:
      st.error(
          "画像の読み込みに失敗しました。別の画像を選択し直してください。"
      )

  if st.session_state.uploaded_image is not None:
    st.image(
        st.session_state.uploaded_image,
        caption="撮影された画像",
        use_container_width=True,
    )

    if upload_type == "乾杯・お酒":
      default_name = random.choice([
          "生ビール (中ジョッキ)",
          "日本酒 (純米・一合)",
          "ハイボール",
          "赤ワイン",
      ])
      st.write("▼ AIが自動予測しました（名前は自由に変更できます）")
      edited_drink_name = st.text_input(
          "ドリンク名を確認・修正", value=default_name
      )

      if st.button("この内容で記録する", use_container_width=True):
        st.success(f"**{edited_drink_name}** を記録しました！")
        st.session_state.logs.append(
            {"type": "drink", "name": edited_drink_name, "alc": 5.0}
        )
        st.session_state.uploaded_image = None  # 次のためにクリア
        st.session_state.step = "test"
        st.rerun()

    else:
      default_dish = random.choice([
          "先付け・旬の小鉢盛り合わせ",
          "お造り盛り合わせ",
          "牛すじ煮込み",
          "旬の焼き魚",
      ])
      st.write("▼ AIが自動予測しました（名前は自由に変更できます）")
      edited_dish_name = st.text_input(
          "おつまみ名を確認・修正", value=default_dish
      )

      if st.button("このおつまみを記録する", use_container_width=True):
        st.success(f"おつまみ「**{edited_dish_name}**」を記録しました！")
        st.session_state.logs.append(
            {"type": "food", "name": edited_dish_name}
        )
        st.session_state.uploaded_image = None  # 次のためにクリア
        st.rerun()

  st.markdown("---")

  st.subheader("📝 本日のログ一覧")
  if st.session_state.logs:
    for i, log in enumerate(st.session_state.logs):
      if log["type"] == "drink":
        st.write(f"🍺 ドリンク {i+1}: {log['name']}")
      else:
        st.write(f"🍴 フード {i+1}: {log['name']}")
  else:
    st.info("まだ記録がありません。お酒や料理を撮影してみましょう！")

  st.markdown("---")
  if st.button("飲み会を終了してVlogを作成する 🎬", use_container_width=True):
    st.session_state.step = "result"
    st.rerun()

# --- 3. ミニテスト画面 ---
elif st.session_state.step == "test":
  st.title("🧠 脳内・思考力チェックテスト")
  st.write(
      "新しいお酒を楽しく安全に飲むために、簡単な計算テストに答えてください！"
  )

  if "quiz_ans" not in st.session_state:
    num1 = random.randint(10, 40)
    num2 = random.randint(10, 40)
    st.session_state.quiz_ans = num1 + num2
    st.session_state.quiz_text = f"{num1} ＋ {num2} はいくつ？"

  st.markdown(f"### Q. {st.session_state.quiz_text}")
  user_answer = st.text_input("答えを入力してください（半角数字）", key="ans_input")

  if st.button("回答する", type="primary"):
    try:
      if int(user_answer) == st.session_state.quiz_ans:
        st.success("正解！✨ まだまだクリアな状態です！")
        st.session_state.warning_level = max(
            0, st.session_state.warning_level - 1
        )
      else:
        st.error(
            f"おっと、不正解！（正解は"
            f" {st.session_state.quiz_ans}）ちょっと酔いが回ってきたかも…？"
        )
        st.session_state.warning_level += 1
    except ValueError:
      st.warning("数字で入力してください。不正解扱いにします。")
      st.session_state.warning_level += 1

    if "quiz_ans" in st.session_state:
      del st.session_state.quiz_ans
    if "quiz_text" in st.session_state:
      del st.session_state.quiz_text

    time.sleep(1.5)
    st.session_state.step = "main"
    st.rerun()

# --- 4. エンド画面 ---
elif st.session_state.step == "result":
  st.title("🎬 飲み会ストーリーVログ完成！")
  st.success(
      "本日のディナーの記録から、思い出のVログストーリーが生成されました。"
  )

  st.markdown("---")
  st.markdown(f"### 🎞️ タイトル: {st.session_state.party_title}")

  if st.session_state.logs:
    for idx, log in enumerate(st.session_state.logs):
      if log["type"] == "drink":
        st.markdown(
            f"**[シーン {idx+1}] 乾杯・お酒** 🍺  \n-> `{log['name']}`"
            " を美味しくいただきました。"
        )
      else:
        st.markdown(
            f"**[シーン {idx+1}] グルメ** 🍴  \n-> 美味しいおつまみ"
            f" `{log['name']}` と共に最高の時間を堪能。"
        )
  else:
    st.write("本日は記録がありませんでした。")

  st.markdown("---")
  if st.button("最初に戻る（新しい飲み会を始める）", use_container_width=True):
    st.session_state.step = "start"
    st.session_state.logs = []
    st.session_state.warning_level = 0
    st.session_state.uploaded_image = None
    st.rerun()
