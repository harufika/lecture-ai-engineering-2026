"""エージェントの配線テスト。

TestModel は実際のLLMを呼ばない偽モデルで、登録されたツールを全部呼んでから
ダミーの回答を返す。APIキーも利用枠も使わずに、
「ツールが登録され、呼ばれ、結果がモデルに戻るか」を確かめられる。
"""

import pytest

from pydantic_ai import DeferredToolRequests
from pydantic_ai.messages import ToolCallPart, ToolReturnPart
from pydantic_ai.models.test import TestModel

from app.agent import agent

BASE_TOOLS = {"search_glossary", "get_lecture_summary", "make_quiz"}


def _parts(result, kind):
    return [p for m in result.all_messages() for p in m.parts if isinstance(p, kind)]


def test_base_tools_are_registered_and_called():
    model = TestModel()
    with agent.override(model=model):
        result = agent.run_sync("LoRAとは？")

    offered = {t.name for t in model.last_model_request_parameters.function_tools}
    assert BASE_TOOLS <= offered  # 演習でツールを足しても壊れないよう「含む」で判定

    called = {p.tool_name for p in _parts(result, ToolCallPart)}
    assert BASE_TOOLS <= called
    # 承認が必要なツール（requires_approval=True）は、実行されずに承認待ちになるので戻り値が無い
    waiting = len(result.output.approvals) if isinstance(result.output, DeferredToolRequests) else 0
    assert len(_parts(result, ToolReturnPart)) + waiting == len(_parts(result, ToolCallPart))
    assert result.output


def test_glossary_result_reaches_the_model():
    model = TestModel(call_tools=["search_glossary"])
    with agent.override(model=model):
        result = agent.run_sync("RAGとは？")
    returns = _parts(result, ToolReturnPart)
    assert returns and returns[0].tool_name == "search_glossary"


def test_save_learning_log_waits_for_approval(tmp_path, monkeypatch):
    from app import tools

    monkeypatch.setattr(tools, "__file__", str(tmp_path / "app" / "tools.py"))
    result = agent.run_sync(
        "学習内容を保存して",
        model=TestModel(call_tools=["save_learning_log"]),
    )

    assert isinstance(result.output, DeferredToolRequests)
    assert [call.tool_name for call in result.output.approvals] == ["save_learning_log"]
    assert not (tmp_path / "learning_log").exists()


@pytest.mark.parametrize("answer", ["y", "n", "", "yes", EOFError, KeyboardInterrupt])
def test_cli_confirms_before_saving(tmp_path, monkeypatch, capsys, answer):
    from app import tools
    from app.agent import main

    monkeypatch.setattr(tools, "__file__", str(tmp_path / "app" / "tools.py"))
    monkeypatch.setattr("sys.argv", ["app.agent", "学習内容を保存して"])
    monkeypatch.setattr(
        "app.agent.build_model", lambda: TestModel(call_tools=["save_learning_log"])
    )

    def confirm(prompt):
        assert "保存しますか" in prompt
        assert not (tmp_path / "learning_log").exists()
        assert "保存する学習記録：" in capsys.readouterr().out
        if isinstance(answer, type):
            raise answer()
        return answer

    monkeypatch.setattr("builtins.input", confirm)
    main()

    files = list((tmp_path / "learning_log").glob("*.md"))
    if answer == "y":
        assert len(files) == 1
        assert files[0].read_text(encoding="utf-8")
    else:
        assert not files
        assert "保存を拒否しました。" in capsys.readouterr().out
