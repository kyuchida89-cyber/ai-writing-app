"""各AIライティングツールを集約するパッケージ。

ALL_TOOLS は (key, ToolSpec) の順序付きリストで、app.py がサイドバーの
ナビゲーション生成に利用する。
"""

from tools import (
    blog,
    catchcopy,
    chat,
    email_reply,
    minutes,
    press_release,
    rewrite,
    sns,
    summarize,
    translate,
)

# サイドバーに表示する順序
ALL_TOOLS = [
    blog.SPEC,
    press_release.SPEC,
    email_reply.SPEC,
    minutes.SPEC,
    summarize.SPEC,
    rewrite.SPEC,
    sns.SPEC,
    catchcopy.SPEC,
    translate.SPEC,
    chat.SPEC,
]
