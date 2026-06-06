"""文章要約ツール。"""

import streamlit as st

from tools.common import ToolSpec, run_generation, show_result_actions

SYSTEM = (
    "あなたは要約のプロです。原文の意味を歪めず、重要な情報を漏らさずに、"
    "指定された形式で分かりやすく要約します。原文にない情報は加えません。"
)


def render() -> None:
    st.subheader("📝 文章要約")
    st.caption("長い文章を、指定の長さ・形式で要約します。")

    text = st.text_area("要約したい文章", height=250, placeholder="記事・議事録・論文などを貼り付けてください")

    col1, col2 = st.columns(2)
    with col1:
        style = st.selectbox("要約形式", ["箇条書き（要点）", "1〜2文の超要約", "段落でまとめる", "3行まとめ"])
    with col2:
        extra = st.selectbox("追加で出力", ["なし", "重要キーワード抽出", "次のアクション提案"])

    if st.button("要約する", type="primary", disabled=not text):
        extra_instruction = ""
        if extra == "重要キーワード抽出":
            extra_instruction = "\n要約の後に「## キーワード」として重要語を5個程度挙げてください。"
        elif extra == "次のアクション提案":
            extra_instruction = "\n要約の後に「## 次のアクション」として取るべき行動を提案してください。"

        prompt = f"""次の文章を「{style}」の形式で要約してください。{extra_instruction}

# 原文
{text}
"""
        run_generation(prompt, system_instruction=SYSTEM, temperature=0.3, state_key="summary_result")

    show_result_actions("summary_result")


SPEC = ToolSpec(
    key="summarize",
    label="📝 文章要約",
    description="長文を指定の形式で簡潔に要約します。",
    render=render,
)
