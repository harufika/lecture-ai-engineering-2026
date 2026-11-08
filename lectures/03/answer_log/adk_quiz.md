# ADK版：第2回の確認問題

## 実行概要

`--jsonl` 付きで実行し、問題作成ツールの呼び出しと最終回答を確認した。先のJSONLなしの実行（SFTの出題）とは別の実行。

- セッションID：`7acbfebf-c845-4ac0-bfb7-5f8102e5c83d`
- ログ：`/tmp/agents_log/agent.20261108_064139.log`（実行環境上のパス）
- モデル：`gemini-3.5-flash-lite`

## 実行コマンド・入力

```bash
PYTHONPATH=. uv run --with google-adk adk run --jsonl adk_agent/glossary_agent
```

```text
[user]: 第2回の内容から確認問題を1問出して
```

## JSONLの実行イベントの整理

1. 最初のモデル応答に `make_quiz(lecture=2)` の `functionCall`。
2. ツール結果として次の問題と答えが返された。
3. 次のモデル応答で、答えを含めず問題を表示。

```json
{"question": "「ランク（LoRAのr）」の意味は？", "answer": "LoRAで使う低ランク行列の大きさを決めるハイパーパラメータ。大きいほど表現力が上がるが、学習するパラメータとメモリも増える。"}
```

## 最終回答（JSONLのtextを展開）

```text
それでは、第2回の内容から確認問題を出題します！

**【確認問題】**
「ランク（LoRAの $r$）」の意味は？

（答えは次の復習時に考えてみてくださいね！）

第2回
```

## 回数・使用量

- ツール：1回。LLM：2回。

| モデル応答 | promptTokenCount | candidatesTokenCount | totalTokenCount |
|---|---:|---:|---:|
| 1回目 | 588 | 14 | 602 |
| 2回目 | 668 | 51 | 719 |

## 観察

通常版の再実行結果とツール名・引数・呼び出し回数が一致した。両版とも最終回答には問題だけを表示した。通常版は「事前学習」、ADK版は「ランク（LoRAのr）」を出題した。問題の用語はランダムに選ばれる。
