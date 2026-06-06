"""AIライティングツール - メインアプリ。

Streamlit + Gemini API による個人用ライティング支援ツール集。
サイドバーでツールを選び、各ツールのUIを表示する。
"""

import streamlit as st

from config import AVAILABLE_MODELS, DEFAULT_MODEL, get_api_key
from tools import ALL_TOOLS

st.set_page_config(
    page_title="AIライティングツール",
    page_icon="🪶",
    layout="centered",
    initial_sidebar_state="expanded",
)


def render_sidebar() -> None:
    """サイドバー：ツール選択・モデル選択・APIキー状態。"""
    with st.sidebar:
        st.title("🪶 AIライティングツール")
        st.caption("Powered by Gemini")

        labels = [spec.label for spec in ALL_TOOLS]
        selected_label = st.radio("ツールを選ぶ", labels, label_visibility="collapsed")
        st.session_state["selected_label"] = selected_label

        st.divider()

        # モデル選択
        model_names = list(AVAILABLE_MODELS.keys())
        chosen = st.selectbox("モデル", model_names, index=0)
        st.session_state["model"] = AVAILABLE_MODELS.get(chosen, DEFAULT_MODEL)

        st.divider()

        # APIキーの状態表示
        if get_api_key():
            st.success("✅ APIキー設定済み")
        else:
            st.error("⚠️ APIキー未設定")
            st.markdown(
                "プロジェクト直下に `.env` を作成し、\n"
                "`GEMINI_API_KEY=...` を設定してください。\n\n"
                "[APIキーを取得](https://aistudio.google.com/apikey)"
            )

        st.divider()
        st.caption("個人用ツール / データベース・認証なし")


def main() -> None:
    render_sidebar()

    selected_label = st.session_state.get("selected_label", ALL_TOOLS[0].label)
    spec = next((s for s in ALL_TOOLS if s.label == selected_label), ALL_TOOLS[0])

    # APIキー未設定時の警告（操作自体は可能だが生成時にエラー表示される）
    if not get_api_key():
        st.warning("APIキーが未設定です。サイドバーの案内に従って `.env` を設定してください。")

    spec.render()


if __name__ == "__main__":
    main()
