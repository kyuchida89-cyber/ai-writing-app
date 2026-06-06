"""キャッチコピー・タイトル生成ツール。"""

import streamlit as st

from tools.common import ToolSpec, run_generation, show_result_actions

SYSTEM = (
    "あなたは数々のヒットを生んだコピーライターです。短く、心を動かし、"
    "行動を促すキャッチコピーやタイトルを生み出します。ありきたりな表現は避けます。"
)


def render() -> None:
    st.subheader("💡 キャッチコピー・タイトル生成")
    st.caption("商品・サービス・記事の魅力的なコピーを量産します。")

    subject = st.text_input("対象（商品・サービス・記事名）", placeholder="例：オーガニックコーヒー豆")
    appeal = st.text_area("アピールしたい特徴・強み", height=100, placeholder="例：農薬不使用、フェアトレード、深いコクと香り")

    col1, col2 = st.columns(2)
    with col1:
        purpose = st.selectbox("用途", ["広告キャッチコピー", "記事タイトル/見出し", "商品キャッチフレーズ", "セールスの一言"])
    with col2:
        direction = st.selectbox("方向性", ["ベネフィット訴求", "好奇心・気になる系", "数字・具体性", "感情に訴える", "おまかせ（色々）"])
    count = st.slider("案の数", 3, 15, 8)

    if st.button("コピーを生成", type="primary", disabled=not subject):
        prompt = f"""次の対象について「{purpose}」を{count}案、考えてください。
方向性は「{direction}」を中心に、バリエーションを持たせてください。
箇条書きで簡潔に列挙してください。

# 対象
{subject}

# 特徴・強み
{appeal or "（特になし）"}
"""
        run_generation(prompt, system_instruction=SYSTEM, temperature=1.0, state_key="copy_result")

    show_result_actions("copy_result")


SPEC = ToolSpec(
    key="catchcopy",
    label="💡 キャッチコピー生成",
    description="広告コピーや記事タイトルを複数案まとめて生成します。",
    render=render,
)
