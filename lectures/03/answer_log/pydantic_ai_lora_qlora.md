# 通常版：LoRAとQLoRAの違い

## 実行概要

ADK版との比較用に再実行し、最終回答・trace・usageを記録した。保存依頼を含まない質問を使用した。

## 実行コマンド

```bash
uv run python -m app.agent --trace "LoRAとQLoRAの違いは？"
```

モデル：`gemini-3.5-flash-lite`。

## 実行出力

```text
[model] gemini-3.5-flash-lite
LoRAとQLoRAの主な違いは、**ベースモデルの重みの精度（ビット数）とメモリ効率**にあります。

* **LoRA（Low-Rank Adaptation）**
  * 事前学習済みの重みはそのまま（通常は16ビットなどの精度）固定し、重みの更新分を小さな低ランク行列で近似してそこだけを学習するPEFT手法です。学習パラメータを大幅に削減できます。
* **QLoRA（Quantized LoRA）**
  * LoRAの仕組みに加えて、ベースモデルの重みをさらに**4ビットなどに量子化**してメモリを大幅に節約した上で、LoRAによる学習を行う手法です。これにより、より大きなモデルをより小さなGPUメモリでも扱えるようになります。

第2回

--- trace ---
[tool call]   search_glossary({'query': 'LoRA'})
[tool call]   search_glossary({'query': 'QLoRA'})
[tool return] search_glossary -> [{"term": "LoRA", "lecture": 2, "definition": "事前学習済みの重みは固定したまま、重みの更新分を2つの小さな行列の積（低ランク行列）で表し、その小さな行列だけを学習するPEFT手法。学習するパラ…
[tool return] search_glossary -> [{"term": "QLoRA", "lecture": 2, "definition": "ベースモデルの重みを4ビットなどに量子化してメモリを節約したうえで、LoRAで学習する手法。より大きなモデルを小さなGPUで扱える。本講座の第2…
[usage] RunUsage(cost=Decimal('0.0010454'), details={'text_prompt_tokens': 1768}, input_text_tokens=1768, input_tokens=1768, output_tokens=206, requests=2, tool_calls=2)
```

## 呼び出し回数

- ツール：`search_glossary`、各用語に1回ずつ、合計2回。
- LLM：2回。
- usage：`requests=2`、`tool_calls=2`、`input_tokens=1768`、`output_tokens=206`。

## 観察

LoRAとQLoRAを個別に検索してから回答する流れ。ADK版とツール名・引数・呼び出し回数が一致した。回答の表現や詳しさには違いがあるが、LoRAの低ランク行列による学習とQLoRAの量子化併用という主要な内容は一致した。
