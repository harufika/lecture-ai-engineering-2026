# 通常版：宿題の3レベル

## 実行概要

ADK版と検索引数・呼び出し回数を比較するため、通常版を `--trace` 付きで実行した。

## 実行コマンド

```bash
uv run python -m app.agent --trace "AIE2026の講座の宿題にある「3レベル」とは何ですか？"
```

## 実行出力

```text
[model] gemini-3.5-flash-lite
AIE2026の講座における「3レベル」とは、宿題の構成を表す以下の3つの段階のことです。

1. **基礎**：講義内容の確認
2. **実装**：自分でコードを書く
3. **発展**：調査や試行

この3レベルのうち、**どれか1つ**に取り組めばその回の宿題は完了となります。原則として採点は行われません。

第1回

--- trace ---
[tool call]   search_glossary({'query': '3レベル'})
[tool return] search_glossary -> [{"term": "宿題の3レベル", "lecture": 1, "definition": "AIE2026の宿題の構成。「基礎（講義内容の確認）」「実装（自分でコードを書く）」「発展（調査や試行）」の3段階があり、どれか1つに取り組…
[usage] RunUsage(cost=Decimal('0.0006940'), details={'text_prompt_tokens': 1355},input_text_tokens=1355, input_tokens=1355, output_tokens=115, requests=2, tool_calls=1)
```

## 呼び出し回数

- ツール：`search_glossary(query="3レベル")` を1回。
- LLM：2回。

## 観察

ADK版と検索ツール・引数・回数が一致した。回答の主要な内容と関連する講義回も一致した。
