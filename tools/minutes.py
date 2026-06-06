"""議事録整形ツール。"""

import streamlit as st

from tools.common import ToolSpec, run_generation, show_result_actions

SYSTEM = (
    "あなたは議事録作成のプロフェッショナルです。会議のメモや文字起こしから、"
    "決定事項・ToDo・論点を漏れなく整理し、誰が読んでも分かる構造化された議事録に"
    "仕上げます。メモにない事実は創作せず、不明な点は推測しません。"
)


def render() -> None:
    st.subheader("🗒 議事録整形")
    st.caption("会議のメモや文字起こしを、構造化された議事録にまとめます。")

    notes = st.text_area(
        "会議のメモ・文字起こし",
        height=250,
        placeholder="箇条書きのメモや録音の文字起こしを貼り付けてください",
    )

    col1, col2 = st.columns(2)
    with col1:
        title = st.text_input("会議名（任意）", placeholder="例：週次定例MTG")
        date = st.text_input("日付（任意）", placeholder="例：2026-06-05")
    with col2:
        attendees = st.text_input("参加者（任意）", placeholder="例：山田, 佐藤, 田中")
        style = st.selectbox("詳しさ", ["要点のみ簡潔に", "標準", "発言も含め詳細に"])

    if st.button("議事録を作成", type="primary", disabled=not notes):
        prompt = f"""次のメモから議事録を作成してください。
以下のMarkdown構成で出力してください。

# 議事録
- 会議名 / 日付 / 参加者（分かる範囲で）
## 決定事項
## ToDo（担当者・期限が分かれば併記）
## 議論の要点
## 次回までの課題・備考

詳しさは「{style}」でお願いします。
メモにない情報は推測で補わず、不明な項目は「（記載なし）」としてください。

# 会議情報
会議名：{title or "（記載なし）"}
日付：{date or "（記載なし）"}
参加者：{attendees or "（記載なし）"}

# メモ・文字起こし
{notes}
"""
        run_generation(prompt, system_instruction=SYSTEM, temperature=0.3, state_key="minutes_result")

    show_result_actions("minutes_result")


SPEC = ToolSpec(
    key="minutes",
    label="🗒 議事録整形",
    description="会議メモや文字起こしを構造化された議事録にまとめます。",
    render=render,
)
