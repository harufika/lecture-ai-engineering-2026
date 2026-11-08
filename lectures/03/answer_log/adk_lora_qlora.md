# ADK版：LoRAとQLoRAの違い

## 実行概要

`--jsonl` 付きで実行し、ツールの呼び出しと最終回答を確認した。先に行ったJSONLなしの実行とは別の実行。

- セッションID：`ab87f69b-8e79-4094-9023-b4e3a5c281a0`
- ログ：`/tmp/agents_log/agent.20261108_063425.log`（実行環境上のパス）
- モデル：`gemini-3.5-flash-lite`

## 実行コマンド・入力

```bash
PYTHONPATH=. uv run --with google-adk adk run --jsonl adk_agent/glossary_agent
```

```text
[user]: LoRAとQLoRAの違いは？
```

## JSONLの実行イベントの整理

1. 最初のモデル応答に2つの `functionCall`：`search_glossary(query="LoRA")` と `search_glossary(query="QLoRA")`。
2. ツール結果のイベントに対応する2つの `functionResponse`。LoRAの検索ではLoRA・ランク・QLoRA、QLoRAの検索ではQLoRA・LoRAの項目が返された。
3. 次のモデル応答に最終回答。

## 最終回答（JSONLのtextを展開）

```text
LoRAとQLoRAの違いは、ベースモデルの重みをそのまま扱うか、量子化してメモリを節約するかにあります。

- **LoRA**
  事前学習済みの重みを固定したまま、重みの更新分を2つの小さな低ランク行列で表し、その部分だけを学習するPEFT（Parameter-Efficient Fine-Tuning）手法です。学習するパラメータを大幅に削減できます。
- **QLoRA**
  LoRAの仕組みをベースにしつつ、ベースモデルの重みを4ビットなどに**量子化**（Quantization）してメモリをさらに節約する手法です。これにより、より大きなモデルを小さなGPUメモリでも効率よく扱うことが可能になります。

関係する回：第2回
```

## 回数・使用量

- ツール：2回。LLM：2回。

| モデル応答 | promptTokenCount | candidatesTokenCount | totalTokenCount |
|---|---:|---:|---:|
| 1回目 | 587 | 37 | 624 |
| 2回目 | 1143 | 160 | 1303 |

## 観察

通常版の再実行結果と、検索ツール・引数・呼び出し回数が一致した。回答の表現や詳しさには違いがあるが、主要な内容と関連する講義回は一致した。
