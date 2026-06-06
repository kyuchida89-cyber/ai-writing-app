"""Gemini API との通信をまとめたクライアントモジュール。"""

from collections.abc import Iterator

from google import genai
from google.genai import types

from config import DEFAULT_MODEL, get_api_key


class GeminiError(Exception):
    """Gemini呼び出しに関するエラー。"""


def _get_client() -> genai.Client:
    api_key = get_api_key()
    if not api_key:
        raise GeminiError(
            "APIキーが設定されていません。プロジェクト直下の .env に "
            "GEMINI_API_KEY を設定してください。"
        )
    return genai.Client(api_key=api_key)


def generate_stream(
    prompt: str,
    *,
    system_instruction: str | None = None,
    model: str = DEFAULT_MODEL,
    temperature: float = 0.7,
) -> Iterator[str]:
    """プロンプトに対する応答をストリーミングで逐次返す。

    Streamlit の st.write_stream にそのまま渡せるよう、テキスト断片を yield する。
    """
    client = _get_client()
    config = types.GenerateContentConfig(
        temperature=temperature,
        system_instruction=system_instruction,
    )
    try:
        stream = client.models.generate_content_stream(
            model=model,
            contents=prompt,
            config=config,
        )
        for chunk in stream:
            if chunk.text:
                yield chunk.text
    except Exception as exc:  # noqa: BLE001 - ユーザーに分かる形で再送出
        raise GeminiError(f"生成中にエラーが発生しました: {exc}") from exc


def generate(
    prompt: str,
    *,
    system_instruction: str | None = None,
    model: str = DEFAULT_MODEL,
    temperature: float = 0.7,
) -> str:
    """プロンプトに対する応答を一括で取得する。"""
    return "".join(
        generate_stream(
            prompt,
            system_instruction=system_instruction,
            model=model,
            temperature=temperature,
        )
    )
