# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Overview

個人用の AI ライティングツール集。Streamlit を UI に、Google Gemini API をバックエンドに使う。
データベース・認証・ユーザー管理はなく、ローカルで動かす単一プロセスのアプリ。UI・コメント・
プロンプトはすべて日本語。

## Commands

```powershell
pip install -r requirements.txt   # 依存インストール
streamlit run app.py              # 起動（http://localhost:8501）
copy .env.example .env            # APIキー設定の雛形をコピー
```

`.env` に `GEMINI_API_KEY=...` を設定する（必須）。テストやリンタの設定は存在しない。

## Architecture

リクエストの流れは **app.py → tools/<tool>.py の render() → tools/common.py の run_generation() → gemini_client.py → Gemini API**。

- **`app.py`** — エントリポイント。サイドバーでツールとモデルを選び、選択ツールの `render()` を呼ぶだけ。状態は `st.session_state`（`selected_label`, `model`）で受け渡す。
- **`config.py`** — `.env` を `load_dotenv()` で読み込み、`AVAILABLE_MODELS`（表示名→モデルID）と `get_api_key()`（.env → Streamlit secrets の順でフォールバック）を提供。
- **`gemini_client.py`** — Gemini 呼び出しの唯一の窓口。`generate_stream()`（逐次 yield、`st.write_stream` 用）と `generate()`（一括）。例外はすべて `GeminiError` にラップして再送出する。ツールから直接 `google.genai` を触らない。
- **`tools/common.py`** — 横断的な土台。`ToolSpec`（dataclass: key/label/description/render）と、`run_generation()`（スピナー＋ストリーミング表示＋エラー処理＋結果を session_state に保存、加えて再生成用に呼び出しパラメータを `{state_key}_lastcall` に保存）、`show_result_actions()`（🔄再生成ボタン＋文字数表示＋コピー用テキストエリア＋ダウンロードボタン）。ここを直すと全ツールに反映される。
- **`tools/__init__.py`** — `ALL_TOOLS` リストがサイドバーの並び順そのもの。

### ツールの規約（重要）

各ツールモジュールは必ず2つを公開する:

1. `render() -> None` — Streamlit UI を描画。生成は `run_generation(prompt, system_instruction=..., temperature=..., state_key=...)` 経由で呼ぶ。
2. `SPEC = ToolSpec(...)` — モジュール末尾で定義。

新ツール追加は「`tools/` にモジュール作成 → `tools/__init__.py` の `ALL_TOOLS` に `<module>.SPEC` を追加」のみ。app.py の変更は不要。

`state_key` はツールごとにユニークにする（例 `"blog_result"`）。session_state はキーが衝突するとツール間で結果が混ざるため。

### 例外: chat.py

チャットは会話履歴を保持し、`run_generation()` を使わず `generate_stream()` を直接呼ぶ（履歴を1つのプロンプト文字列に整形してから渡す、ステートレスな呼び出し）。`common` への循環 import を避けるため `ToolSpec` をモジュール末尾で import している点に注意。

### プロンプト設計のパターン

各ツールは固定の `SYSTEM` 文字列（役割定義、モジュール冒頭の定数）を `system_instruction` として渡し、ユーザー入力は f-string で見出し付きのプロンプトに組み立てる。temperature はツールの性質に応じて変える（創作系は 0.8、忠実性重視は低め）。
