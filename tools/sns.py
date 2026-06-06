"""SNS投稿文生成ツール。"""

import streamlit as st

from tools.common import ToolSpec, run_generation, show_result_actions

SYSTEM = (
    "あなたはSNSマーケティングに長けたコピーライターです。"
    "各プラットフォームの文化・文字数・ハッシュタグの慣習に合わせて、"
    "目に留まり拡散されやすい投稿文を作成します。"
)

PLATFORM_HINT = {
    "X（旧Twitter）": "140字程度を意識。簡潔でフックのある一言。ハッシュタグは1〜3個。",
    "Instagram": "共感を生むストーリー調。改行を使い読みやすく。ハッシュタグは10個前後。",
    "Facebook": "ややフォーマルで丁寧。少し長めの文章でも可。",
    "LinkedIn": "ビジネス・専門性重視。学びや知見が伝わる落ち着いたトーン。",
    "YouTube概要欄": "動画内容の説明と視聴を促す導線。リンク誘導を意識。",
}


def render() -> None:
    st.subheader("📱 SNS投稿文生成")
    st.caption("伝えたい内容から、各SNS向けの投稿文を生成します。")

    content = st.text_area("投稿したい内容・告知", height=120, placeholder="例：新しいブログ記事を公開しました。在宅ワークの集中術について。")

    col1, col2 = st.columns(2)
    with col1:
        platform = st.selectbox("プラットフォーム", list(PLATFORM_HINT.keys()))
    with col2:
        tone = st.selectbox("トーン", ["親しみやすい", "プロフェッショナル", "ワクワク・ポジティブ", "落ち着いた"])
    variations = st.slider("生成する案の数", 1, 5, 3)

    if st.button("投稿文を生成", type="primary", disabled=not content):
        prompt = f"""次の内容を「{platform}」向けのSNS投稿文にしてください。
案を{variations}パターン、それぞれ「### 案1」のように番号付きで提案してください。

# プラットフォームの特性
{PLATFORM_HINT[platform]}

# トーン
{tone}

# 投稿したい内容
{content}

適切なハッシュタグや絵文字も含めてください。
"""
        run_generation(prompt, system_instruction=SYSTEM, temperature=0.9, state_key="sns_result")

    show_result_actions("sns_result")


SPEC = ToolSpec(
    key="sns",
    label="📱 SNS投稿文生成",
    description="各SNSに最適化した投稿文を複数パターン作成します。",
    render=render,
)
