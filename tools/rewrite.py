"""文章リライト・校正ツール。"""

import streamlit as st

from tools.common import ToolSpec, run_generation, show_result_actions

SYSTEM = (
    "あなたは熟練の日本語校正者・編集者です。誤字脱字や不自然な表現を直し、"
    "指示された方向に文章を洗練させます。元の意図は保ちます。"
)


def render() -> None:
    st.subheader("🔄 文章リライト・校正")
    st.caption("文章の校正、言い換え、トーン変更を行います。")

    text = st.text_area("対象の文章", height=200, placeholder="リライト・校正したい文章を入力してください")

    mode = st.selectbox(
        "やりたいこと",
        [
            "誤字脱字・文法の校正",
            "より自然で読みやすく",
            "丁寧・フォーマルにする",
            "カジュアル・親しみやすくする",
            "簡潔に短くする",
            "詳しく膨らませる",
        ],
    )
    show_diff = st.checkbox("変更点の説明も付ける", value=False)

    if st.button("リライトする", type="primary", disabled=not text):
        diff_instruction = "\n最後に「## 主な変更点」として何をどう直したか箇条書きで説明してください。" if show_diff else ""
        prompt = f"""次の文章を「{mode}」という方針でリライトしてください。
まず修正後の文章を提示してください。{diff_instruction}

# 元の文章
{text}
"""
        run_generation(prompt, system_instruction=SYSTEM, temperature=0.5, state_key="rewrite_result")

    show_result_actions("rewrite_result")


SPEC = ToolSpec(
    key="rewrite",
    label="🔄 文章リライト・校正",
    description="校正・言い換え・トーン変更で文章を磨きます。",
    render=render,
)
