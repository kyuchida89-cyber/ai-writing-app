# 🪶 AIライティングツール

Python + Streamlit + Gemini API で作る、個人用のオールインワン AI ライティングツール集です。
データベースや認証は不要、ローカルですぐ動きます。

## 搭載ツール

| ツール | 内容 |
| --- | --- |
| ✍️ ブログ記事執筆 | テーマからSEOを意識した記事を生成（構成案のみも可） |
| 📰 プレスリリース作成 | 発表内容から報道機関向けのプレスリリースを作成 |
| 📧 メール返信文作成 | 受信メールと要点から適切な返信文を作成 |
| 🗒 議事録整形 | 会議メモ・文字起こしを構造化された議事録にまとめる |
| 📝 文章要約 | 長文を箇条書き・3行などお好みの形式で要約 |
| 🔄 文章リライト・校正 | 校正、言い換え、トーン変更 |
| 📱 SNS投稿文生成 | X / Instagram など各SNS向けに複数案を生成 |
| 💡 キャッチコピー生成 | 広告コピーや記事タイトルを量産 |
| 🌐 翻訳 | 文体を保った自然な翻訳 |
| 💬 自由チャット | 書くことに関する相談・アイデア出し（会話形式） |

## セットアップ

### 1. 依存パッケージのインストール

```powershell
pip install -r requirements.txt
```

### 2. APIキーの設定

[Google AI Studio](https://aistudio.google.com/apikey) で Gemini API キーを取得し、
`.env.example` を `.env` にコピーしてキーを設定します。

```powershell
copy .env.example .env
```

`.env` の中身:

```
GEMINI_API_KEY=取得したキー
```

### 3. 起動

```powershell
streamlit run app.py
```

ブラウザで `http://localhost:8501` が開きます。

## ファイル構成

```
pythonApp/
├── app.py             # メインアプリ（サイドバー＋ツール振り分け）
├── config.py          # 設定・APIキー読み込み・モデル定義
├── gemini_client.py   # Gemini API クライアント（ストリーミング対応）
├── requirements.txt
├── .env.example
└── tools/             # 各ライティングツール
    ├── common.py      # 共通UI・データ構造
    ├── blog.py
    ├── press_release.py
    ├── email_reply.py
    ├── minutes.py
    ├── summarize.py
    ├── rewrite.py
    ├── sns.py
    ├── catchcopy.py
    ├── translate.py
    └── chat.py
```

## ツールの追加方法

1. `tools/` に新しいモジュールを作り、`render()` 関数と `SPEC`（`ToolSpec`）を定義
2. `tools/__init__.py` の `ALL_TOOLS` に追加

これだけでサイドバーに自動で表示されます。
