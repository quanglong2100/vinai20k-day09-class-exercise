"""
Day 9 — Multi-Agent & MCP/A2A
Test suite for student solution.

Run from the day folder:
    pytest tests/ -v
"""

import importlib.util
import sys
import unittest
from pathlib import Path

DAY_DIR = Path(__file__).parent.parent
SOLUTION_DIR = DAY_DIR / "solution"


def _load(path: Path, unique_name: str):
    spec = importlib.util.spec_from_file_location(unique_name, str(path))
    mod = importlib.util.module_from_spec(spec)
    sys.modules[unique_name] = mod
    spec.loader.exec_module(mod)
    return mod


if (SOLUTION_DIR / "solution.py").exists():
    _m = _load(SOLUTION_DIR / "solution.py", f"{DAY_DIR.name}.solution")
elif (SOLUTION_DIR / "app.py").exists():
    _m = _load(SOLUTION_DIR / "app.py", f"{DAY_DIR.name}.solution")
else:
    src = "template.py" if (DAY_DIR / "template.py").exists() else "app.py"
    _m = _load(DAY_DIR / src, f"{DAY_DIR.name}.template")

AgentMessage = getattr(_m, 'AgentMessage')
WorkerAgent = getattr(_m, 'WorkerAgent')
SupervisorAgent = getattr(_m, 'SupervisorAgent')
MCPServer = getattr(_m, 'MCPServer')
MCPClient = getattr(_m, 'MCPClient')
template = _m

def _mock_llm(prompt: str) -> str:
    return f"Mock result for: {prompt[:40]}"


def _make_worker(name: str = "TestWorker", specialty: str = "testing") -> WorkerAgent:
    return WorkerAgent(name=name, specialty=specialty, llm_fn=_mock_llm)


def _make_supervisor() -> SupervisorAgent:
    workers = [
        _make_worker("ResearchAgent", "research and information retrieval"),
        _make_worker("WritingAgent", "writing and summarization"),
        _make_worker("AnalysisAgent", "data analysis and statistics"),
    ]
    return SupervisorAgent(workers=workers, llm_fn=_mock_llm)


def _make_message(task: str = "Do some work") -> AgentMessage:
    return AgentMessage(
        sender="Supervisor",
        receiver="TestWorker",
        task=task,
        context={"key": "value"},
        expected_output_format="plain text",
    )


# ---------------------------------------------------------------------------
# Tests
# ---------------------------------------------------------------------------

class TestWorkerAgent(unittest.TestCase):

    def test_process_returns_agent_message(self):
        worker = _make_worker()
        msg = _make_message()
        response = worker.process(msg)
        self.assertIsInstance(response, AgentMessage)

    def test_process_response_task_matches_input(self):
        worker = _make_worker()
        msg = _make_message("Analyse this data set")
        response = worker.process(msg)
        self.assertEqual(response.task, msg.task)

    def test_process_sender_is_worker_name(self):
        worker = _make_worker("MyWorker")
        msg = _make_message()
        response = worker.process(msg)
        self.assertEqual(response.sender, "MyWorker")

    def test_process_receiver_is_original_sender(self):
        worker = _make_worker()
        msg = _make_message()
        response = worker.process(msg)
        self.assertEqual(response.receiver, msg.sender)

    def test_get_capability_description_is_string(self):
        worker = _make_worker("ResearchAgent", "web research")
        desc = worker.get_capability_description()
        self.assertIsInstance(desc, str)
        self.assertGreater(len(desc), 0)

    def test_get_capability_includes_name(self):
        worker = _make_worker("ResearchAgent", "web research")
        desc = worker.get_capability_description()
        self.assertIn("ResearchAgent", desc)


class TestSupervisorAgent(unittest.TestCase):

    def test_route_returns_worker_agent(self):
        supervisor = _make_supervisor()
        worker = supervisor.route("Research the latest AI news")
        self.assertIsInstance(worker, WorkerAgent)

    def test_route_returns_research_for_research_task(self):
        supervisor = _make_supervisor()
        worker = supervisor.route("research information retrieval facts")
        self.assertIn("Research", worker.name)

    def test_run_returns_dict(self):
        supervisor = _make_supervisor()
        result = supervisor.run("Write a summary of AI trends")
        self.assertIsInstance(result, dict)

    def test_run_has_result_key(self):
        supervisor = _make_supervisor()
        result = supervisor.run("Analyse the data")
        self.assertIn("result", result)

    def test_run_has_trace_key(self):
        supervisor = _make_supervisor()
        result = supervisor.run("Research something")
        self.assertIn("trace", result)

    def test_run_trace_is_list(self):
        supervisor = _make_supervisor()
        result = supervisor.run("Do some work")
        self.assertIsInstance(result["trace"], list)

    def test_run_trace_contains_dicts(self):
        supervisor = _make_supervisor()
        result = supervisor.run("Do some work")
        for entry in result["trace"]:
            self.assertIsInstance(entry, dict)

    def test_run_trace_has_agent_message_keys(self):
        supervisor = _make_supervisor()
        result = supervisor.run("Do some work")
        for entry in result["trace"]:
            self.assertIn("sender", entry)
            self.assertIn("receiver", entry)
            self.assertIn("task", entry)

    def test_run_result_is_string(self):
        supervisor = _make_supervisor()
        result = supervisor.run("Summarize the findings")
        self.assertIsInstance(result["result"], str)


class TestMCPServer(unittest.TestCase):

    def test_register_tool_adds_to_registry(self):
        server = MCPServer()
        server.register_tool("my_tool", lambda: {"ok": True})
        self.assertIn("my_tool", server.list_tools())

    def test_call_tool_invokes_function(self):
        server = MCPServer()
        called = {"flag": False}

        def my_fn(**kwargs):
            called["flag"] = True
            return {"result": "done"}

        server.register_tool("my_fn", my_fn)
        result = server.call_tool("my_fn", {})
        self.assertTrue(called["flag"])

    def test_call_tool_returns_dict(self):
        server = MCPServer()
        server.register_tool("adder", lambda x, y: {"sum": x + y})
        result = server.call_tool("adder", {"x": 2, "y": 3})
        self.assertIsInstance(result, dict)

    def test_call_unknown_tool_raises(self):
        server = MCPServer()
        with self.assertRaises((KeyError, ValueError)):
            server.call_tool("nonexistent", {})

    def test_list_tools_returns_all_names(self):
        server = MCPServer()
        server.register_tool("tool_a", lambda: {})
        server.register_tool("tool_b", lambda: {})
        tools = server.list_tools()
        self.assertIn("tool_a", tools)
        self.assertIn("tool_b", tools)


class TestMCPClient(unittest.TestCase):

    def _make_server_and_client(self) -> tuple[MCPServer, MCPClient]:
        server = MCPServer()
        server.register_tool("greet", lambda name: {"greeting": f"Hello, {name}!"})
        client = MCPClient(server)
        return server, client

    def test_list_tools_returns_server_tools(self):
        server, client = self._make_server_and_client()
        tools = client.list_tools()
        self.assertIn("greet", tools)

    def test_use_tool_calls_through_to_server(self):
        server, client = self._make_server_and_client()
        result = client.use_tool("greet", {"name": "Alice"})
        self.assertIsInstance(result, dict)

    def test_use_tool_returns_correct_result(self):
        server, client = self._make_server_and_client()
        result = client.use_tool("greet", {"name": "Alice"})
        self.assertIn("greeting", result)
        self.assertIn("Alice", result["greeting"])


def _make_mock_worker(name: str, specialty: str) -> 'template.WorkerAgent':
    """Helper to create a WorkerAgent with a mock LLM."""
    def mock_llm(msg):
        return f"{name} processed: {msg}"
    return template.WorkerAgent(name, specialty, mock_llm)


class TestPipelineAgent(unittest.TestCase):
    def setUp(self):
        self.w1 = _make_mock_worker("retriever", "data retrieval")
        self.w2 = _make_mock_worker("formatter", "response formatting")

    def test_run_returns_required_keys(self):
        pipeline = template.PipelineAgent([self.w1, self.w2])
        result = pipeline.run("Find customer data")
        self.assertIn('result', result)
        self.assertIn('steps', result)
        self.assertIn('trace', result)

    def test_steps_equals_agent_count(self):
        pipeline = template.PipelineAgent([self.w1, self.w2])
        result = pipeline.run("initial task")
        self.assertEqual(result['steps'], 2)

    def test_trace_length_equals_agent_count(self):
        pipeline = template.PipelineAgent([self.w1, self.w2])
        result = pipeline.run("initial task")
        self.assertEqual(len(result['trace']), 2)

    def test_get_pipeline_trace_matches_run_trace(self):
        pipeline = template.PipelineAgent([self.w1, self.w2])
        result = pipeline.run("task")
        self.assertEqual(pipeline.get_pipeline_trace(), result['trace'])

    def test_result_is_string(self):
        pipeline = template.PipelineAgent([self.w1])
        result = pipeline.run("any task")
        self.assertIsInstance(result['result'], str)


class TestGetWorkerStats(unittest.TestCase):
    def setUp(self):
        self.w1 = _make_mock_worker("researcher", "research")
        self.w2 = _make_mock_worker("writer", "writing")

        def supervisor_llm(msg):
            return "researcher"

        self.supervisor = template.SupervisorAgent([self.w1, self.w2], supervisor_llm)

    def test_returns_dict_with_worker_names(self):
        stats = self.supervisor.get_worker_stats()
        self.assertIsInstance(stats, dict)

    def test_initial_stats_are_zero(self):
        stats = self.supervisor.get_worker_stats()
        for name, count in stats.items():
            self.assertEqual(count, 0)

    def test_stats_increment_after_run(self):
        self.supervisor.run("Do some research")
        stats = self.supervisor.get_worker_stats()
        total_calls = sum(stats.values())
        self.assertGreaterEqual(total_calls, 1)


if __name__ == "__main__":
    unittest.main()
