"""メール返信文作成ツール。"""

import streamlit as st

from tools.common import ToolSpec, run_generation, show_result_actions

SYSTEM = (
    "あなたは日本のビジネスメールに精通したアシスタントです。"
    "失礼のない、簡潔で的確な日本語のメール文面を作成します。"
    "宛名・挨拶・本文・結びの構成を守り、過度に冗長にならないようにします。"
)


def render() -> None:
    st.subheader("📧 メール返信文作成")
    st.caption("受け取ったメールと、伝えたい要点を入れると返信文を作成します。")

    received = st.text_area("受信したメール本文", height=180, placeholder="返信したいメールを貼り付けてください")
    points = st.text_area("返信で伝えたい内容・要点", height=100, placeholder="例：日程は来週月曜でOK。資料は明日送る。")

    col1, col2 = st.columns(2)
    with col1:
        tone = st.selectbox("丁寧さ", ["とても丁寧（社外・目上）", "標準（ビジネス）", "ややフランク（社内・親しい相手）"])
    with col2:
        sender = st.text_input("自分の署名（任意）", placeholder="例：山田太郎")

    if st.button("返信文を生成", type="primary", disabled=not (received or points)):
        prompt = f"""次のメールに対する返信文を作成してください。

# 受信したメール
{received or "（本文なし。新規メールとして作成）"}

# 返信で伝えたい要点
{points or "受信内容に対して適切に返信"}

# 丁寧さのレベル
{tone}

# 署名
{sender or "（署名なし）"}

件名案も先頭に「件名：」として提案してください。
"""
        run_generation(prompt, system_instruction=SYSTEM, temperature=0.6, state_key="email_result")

    show_result_actions("email_result")


SPEC = ToolSpec(
    key="email",
    label="📧 メール返信文作成",
    description="受信メールと要点から、適切な返信文を作成します。",
    render=render,
)
