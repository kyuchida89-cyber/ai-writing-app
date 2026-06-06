"""ツール共通で使うデータ構造とUIヘルパー。"""

from collections.abc import Callable
from dataclasses import dataclass

import streamlit as st

from config import DEFAULT_MODEL
from gemini_client import GeminiError, generate_stream


@dataclass(frozen=True)
class ToolSpec:
    """1つのライティングツールの定義。"""

    key: str          # 内部識別子（ユニーク）
    label: str        # サイドバー表示名（絵文字付き）
    description: str   # ツール冒頭の説明文
    render: Callable[[], None]  # UIを描画する関数


def run_generation(
    prompt: str,
    *,
    system_instruction: str | None = None,
    temperature: float = 0.7,
    state_key: str = "result",
) -> None:
    """プロンプトを実行し、結果をストリーミング表示＋セッションに保存する。

    生成中のスピナー、エラー表示、結果のセッション保持をまとめて行う。
    呼び出しパラメータも保存し、show_result_actions の「再生成」で再利用する。
    """
    model = st.session_state.get("model") or DEFAULT_MODEL
    # 同条件での再生成に使うため、最後の呼び出し内容を控えておく
    st.session_state[f"{state_key}_lastcall"] = {
        "prompt": prompt,
        "system_instruction": system_instruction,
        "temperature": temperature,
    }
    placeholder = st.empty()
    collected: list[str] = []

    def _stream():
        # st.write_stream に渡しつつ、全文を collected に蓄積する
        for piece in generate_stream(
            prompt,
            system_instruction=system_instruction,
            model=model,
            temperature=temperature,
        ):
            collected.append(piece)
            yield piece

    try:
        with st.spinner("AIが生成中です…"):
            placeholder.write_stream(_stream())
    except GeminiError as exc:
        st.error(str(exc))
        return

    st.session_state[state_key] = "".join(collected)


def show_result_actions(state_key: str = "result") -> None:
    """生成結果に対する再生成ボタン・文字数表示・コピー用エリアを表示する。"""
    result = st.session_state.get(state_key)
    if not result:
        return

    col1, col2 = st.columns([1, 2])
    with col1:
        # 直前と同じ条件でもう一度生成する（temperature により別案が得られる）
        can_regen = bool(st.session_state.get(f"{state_key}_lastcall"))
        if can_regen and st.button("🔄 再生成", key=f"{state_key}_regen"):
            run_generation(state_key=state_key, **st.session_state[f"{state_key}_lastcall"])
            result = st.session_state.get(state_key, result)
    with col2:
        st.caption(f"文字数：{len(result)}")

    with st.expander("📋 生成結果をコピー / 編集", expanded=False):
        st.text_area(
            "結果テキスト（選択してコピーできます）",
            value=result,
            height=300,
            key=f"{state_key}_copyarea",
        )
        st.download_button(
            "💾 テキストファイルで保存",
            data=result,
            file_name=f"{state_key}.txt",
            mime="text/plain",
            key=f"{state_key}_download",
        )
