"""ブログ記事執筆ツール。"""

import streamlit as st

from tools.common import ToolSpec, run_generation, show_result_actions

SYSTEM = (
    "あなたは検索上位の記事を数多く手がけてきたプロのSEOライター兼編集者です。"
    "次の方針で、読者と検索エンジンの双方に評価される自然な日本語のブログ記事を書きます。\n"
    "1. 検索意図の充足：読者がそのテーマで本当に知りたいこと・抱える悩みを先回りして満たす。\n"
    "2. キーワード設計：指定キーワードをタイトル・導入・見出し・本文に自然に配置し、"
    "関連語や共起語も適度に織り込む。不自然な詰め込み（キーワードスタッフィング）は避ける。\n"
    "3. 構成：結論ファースト（PREP）。導入で読者の悩みに共感し記事を読む価値を提示、"
    "Markdownの見出し(##, ###)で論理的に章立てし、最後にまとめと次の行動を促す。\n"
    "4. 可読性：一文を短く、箇条書き・番号リスト・表を適切に使い、流し読みでも要点が伝わるようにする。\n"
    "5. E-E-A-T：具体例・根拠・数値を交え、専門性と信頼性が伝わる記述にする。"
    "事実が不確かな点は断定せず、誇張や虚偽は書かない。\n"
    "6. 出力の冒頭に、検索結果での表示を想定した『タイトル案（32文字前後）』と"
    "『メタディスクリプション案（120文字前後）』を提示してから本文に入る。"
)


def render() -> None:
    st.subheader("✍️ ブログ記事執筆")
    st.caption("テーマと条件を入力すると、構成済みのブログ記事を生成します。")

    topic = st.text_input("記事のテーマ・タイトル", placeholder="例：在宅ワークで集中力を保つ方法")
    keywords = st.text_input("含めたいキーワード（任意・カンマ区切り）", placeholder="例：ポモドーロ, 環境づくり")

    col1, col2, col3 = st.columns(3)
    with col1:
        tone = st.selectbox("トーン", ["丁寧・親しみやすい", "プロフェッショナル", "カジュアル", "熱量高め"])
    with col2:
        length = st.selectbox("文字数の目安", ["約800字", "約1500字", "約3000字"])
    with col3:
        audience = st.text_input("想定読者（任意）", placeholder="例：20代会社員")

    outline_only = st.checkbox("まず構成案（見出しだけ）を作る", value=False)

    if st.button("記事を生成", type="primary", disabled=not topic):
        if outline_only:
            instruction = "記事の見出し構成（アウトライン）だけをMarkdownの箇条書きで提案してください。本文は書かないでください。"
        else:
            instruction = f"上記の条件で、{length}程度のブログ記事を本文まで完成させてください。"

        prompt = f"""次の条件でブログ記事を作成してください。

# テーマ
{topic}

# 含めたいキーワード
{keywords or "指定なし"}

# 想定読者
{audience or "一般読者"}

# トーン
{tone}

# 指示
{instruction}
冒頭にリード文、最後にまとめを入れてください。
"""
        run_generation(prompt, system_instruction=SYSTEM, temperature=0.8, state_key="blog_result")

    show_result_actions("blog_result")


SPEC = ToolSpec(
    key="blog",
    label="✍️ ブログ記事執筆",
    description="テーマからSEOを意識したブログ記事を自動生成します。",
    render=render,
)
