"""自由チャット（汎用ライティング相談）ツール。

会話履歴を保持し、アイデア出しや相談に使える対話モード。
"""

import streamlit as st

from config import DEFAULT_MODEL
from gemini_client import GeminiError, generate_stream

SYSTEM = (
    "あなたは有能なライティングアシスタントです。文章作成、アイデア出し、"
    "言葉選び、構成の相談など、書くことに関するあらゆる相談に親身に答えます。"
    "必要なら質問を返し、具体的で実用的な提案をします。"
)

_HISTORY_KEY = "chat_history"


def _build_prompt(history: list[dict]) -> str:
    """会話履歴を1つのプロンプト文字列に変換する。"""
    lines = []
    for msg in history:
        role = "ユーザー" if msg["role"] == "user" else "アシスタント"
        lines.append(f"{role}: {msg['content']}")
    lines.append("アシスタント: ")
    return "\n".join(lines)


def render() -> None:
    st.subheader("💬 自由チャット")
    st.caption("書くことに関する相談・アイデア出しを対話形式で行えます。")

    if _HISTORY_KEY not in st.session_state:
        st.session_state[_HISTORY_KEY] = []

    history = st.session_state[_HISTORY_KEY]

    col1, _ = st.columns([1, 4])
    with col1:
        if st.button("🗑 会話をリセット"):
            st.session_state[_HISTORY_KEY] = []
            st.rerun()

    # これまでの会話を表示
    for msg in history:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

    user_input = st.chat_input("メッセージを入力…")
    if not user_input:
        return

    history.append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.markdown(user_input)

    model = st.session_state.get("model") or DEFAULT_MODEL
    with st.chat_message("assistant"):
        collected: list[str] = []

        def _stream():
            for piece in generate_stream(
                _build_prompt(history),
                system_instruction=SYSTEM,
                model=model,
                temperature=0.8,
            ):
                collected.append(piece)
                yield piece

        try:
            st.write_stream(_stream())
        except GeminiError as exc:
            st.error(str(exc))
            history.pop()  # 失敗したユーザー発話を巻き戻す
            return

    history.append({"role": "assistant", "content": "".join(collected)})


# chat はモジュール末尾で SPEC を定義（common への循環を避けるため直接import）
from tools.common import ToolSpec  # noqa: E402

SPEC = ToolSpec(
    key="chat",
    label="💬 自由チャット",
    description="書くことに関する相談・アイデア出しを対話形式で。",
    render=render,
)
