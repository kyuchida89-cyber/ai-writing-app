"""プレスリリース作成ツール。"""

import streamlit as st

from tools.common import ToolSpec, run_generation, show_result_actions

SYSTEM = (
    "あなたは広報・PRの専門家です。報道機関が取り上げたくなる、事実に基づいた"
    "簡潔で説得力のあるプレスリリースを作成します。5W1Hを押さえ、見出し・リード文・"
    "本文・会社概要・問い合わせ先の構成を守り、誇張表現は避けます。"
)


def render() -> None:
    st.subheader("📰 プレスリリース作成")
    st.caption("発表内容から、報道機関向けのプレスリリースを作成します。")

    news = st.text_area(
        "発表したい内容（新商品・サービス・イベントなど）",
        height=140,
        placeholder="例：AIライティングツール『○○』を6月10日にリリース",
    )
    points = st.text_area(
        "盛り込みたいポイント・特徴",
        height=100,
        placeholder="例：無料で使える、8種類のツールを搭載、日本語に特化",
    )

    col1, col2 = st.columns(2)
    with col1:
        company = st.text_input("会社名・発信者（任意）", placeholder="例：株式会社サンプル")
    with col2:
        contact = st.text_input("問い合わせ先（任意）", placeholder="例：広報部 pr@example.com")

    if st.button("プレスリリースを生成", type="primary", disabled=not news):
        prompt = f"""次の内容でプレスリリースを作成してください。
次の構成で、報道機関向けの客観的で簡潔な文体にしてください。

【見出し】
【サブ見出し】
【リード文】要点を1段落でまとめる
【本文】背景・詳細・コメントなど
【会社概要】
【本件に関するお問い合わせ】

事実に基づき、ポイントにない数値や効果は創作しないでください。

# 発表内容
{news}

# ポイント・特徴
{points or "（特になし）"}

# 会社名・発信者
{company or "（記載なし）"}

# 問い合わせ先
{contact or "（記載なし）"}
"""
        run_generation(prompt, system_instruction=SYSTEM, temperature=0.6, state_key="press_result")

    show_result_actions("press_result")


SPEC = ToolSpec(
    key="press_release",
    label="📰 プレスリリース作成",
    description="発表内容から報道機関向けのプレスリリースを作成します。",
    render=render,
)
