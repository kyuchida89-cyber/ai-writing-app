"""翻訳ツール。"""

import streamlit as st

from tools.common import ToolSpec, run_generation, show_result_actions

SYSTEM = (
    "あなたは熟練の翻訳者です。原文のニュアンス・文体・トーンを保ちつつ、"
    "対象言語として自然な訳文を作ります。直訳調ではなく、その言語のネイティブが"
    "読んで自然な表現を選びます。"
)

LANGUAGES = ["日本語", "英語", "中国語(簡体)", "韓国語", "フランス語", "ドイツ語", "スペイン語", "イタリア語"]


def render() -> None:
    st.subheader("🌐 翻訳")
    st.caption("自然な訳文を生成します。トーン指定や用途も反映できます。")

    text = st.text_area("翻訳したい文章", height=180, placeholder="翻訳したいテキストを入力してください")

    col1, col2, col3 = st.columns(3)
    with col1:
        src = st.selectbox("元の言語", ["自動判定", *LANGUAGES])
    with col2:
        dst = st.selectbox("翻訳先の言語", LANGUAGES, index=1)
    with col3:
        style = st.selectbox("文体", ["自然・標準", "フォーマル", "カジュアル", "ビジネス"])

    explain = st.checkbox("補足説明（ニュアンスや別案）を付ける", value=False)

    if st.button("翻訳する", type="primary", disabled=not text):
        src_part = "" if src == "自動判定" else f"元の言語は{src}です。"
        explain_part = "\n訳文の後に「## 補足」として、ニュアンスの注意点や別の言い回し案を加えてください。" if explain else ""
        prompt = f"""次の文章を{dst}に翻訳してください。{src_part}
文体は「{style}」でお願いします。{explain_part}

# 原文
{text}
"""
        run_generation(prompt, system_instruction=SYSTEM, temperature=0.3, state_key="translate_result")

    show_result_actions("translate_result")


SPEC = ToolSpec(
    key="translate",
    label="🌐 翻訳",
    description="自然で文体を保った翻訳を行います。",
    render=render,
)
