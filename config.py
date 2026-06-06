"""アプリ全体の設定とAPIキーの読み込みを担当するモジュール。"""

import os

from dotenv import load_dotenv

load_dotenv()

# 利用可能なGeminiモデル（表示名 -> モデルID）
AVAILABLE_MODELS = {
    "Gemini 2.5 Flash（高速・標準）": "gemini-2.5-flash",
    "Gemini 2.5 Pro（高品質・じっくり）": "gemini-2.5-pro",
    "Gemini 2.5 Flash-Lite（最速・軽量）": "gemini-2.5-flash-lite",
}

DEFAULT_MODEL = "gemini-2.5-flash"


def get_api_key() -> str | None:
    """環境変数(.env)またはStreamlit secretsからAPIキーを取得する。"""
    key = os.getenv("GEMINI_API_KEY")
    if key:
        return key
    # Streamlit Cloud などで secrets を使う場合のフォールバック
    try:
        import streamlit as st

        return st.secrets.get("GEMINI_API_KEY")
    except Exception:
        return None
