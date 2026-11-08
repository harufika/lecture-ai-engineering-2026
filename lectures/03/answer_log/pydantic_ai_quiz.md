# 通常版：第2回の確認問題

## 実行概要

ADK版との比較用に再実行し、最終回答・trace・usageを記録した。

## 実行コマンド

```bash
uv run python -m app.agent --trace "第2回の内容から確認問題を1問出して"
```

モデル：`gemini-3.5-flash-lite`。

## 実行出力

```text
[model] gemini-3.5-flash-lite
第2回から確認問題をお出しします！

**【問題】**
「事前学習」の意味は何でしょうか？

考えてみてくださいね。

（関連する回：第2回）

--- trace ---
[tool call]   make_quiz({'lecture': 2})
[tool return] make_quiz -> {"question": "「事前学習」の意味は？", "answer": "大量の汎用テキストで、次のトークンを予測するようにモデルを学習させる最初の段階。言語の知識や一般的な常識の多くはここで身につく。"}…
[usage] RunUsage(cost=Decimal('0.0005248'), details={'text_prompt_tokens': 1291}, input_text_tokens=1291, input_tokens=1291, output_tokens=55, requests=2, tool_calls=1)
```

## 呼び出し回数

- ツール：`make_quiz(lecture=2)` を1回。
- LLM：2回。
- usage：`requests=2`、`tool_calls=1`、`input_tokens=1291`、`output_tokens=55`。

## 観察

ADK版とツール名・引数・呼び出し回数が一致した。両版ともツールから問題と答えを受け取り、最終回答には問題だけを表示した。通常版は「事前学習」、ADK版は「ランク（LoRAのr）」を出題した。出題する用語は共通関数によるランダム選択。
