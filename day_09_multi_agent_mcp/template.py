"""
Day 9 — Multi-Agent & MCP/A2A
AICB-P1: AI Practical Competency Program, Phase 1

Instructions:
    1. Fill in every section marked with TODO.
    2. Do NOT change class/function signatures.
    3. Copy this file to solution/solution.py when done.
    4. Run: pytest tests/ -v
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Callable


# ---------------------------------------------------------------------------
# Task 1 — Agent Message
# ---------------------------------------------------------------------------

@dataclass
class AgentMessage:
    """
    Structured message passed between agents.

    Fields:
        sender:                Name of the sending agent.
        receiver:              Name of the receiving agent.
        task:                  Description of the task to perform.
        context:               Additional context data (dict).
        expected_output_format: How the response should be formatted.
    """
    sender: str
    receiver: str
    task: str
    context: dict = field(default_factory=dict)
    expected_output_format: str = "plain text"

    def to_dict(self) -> dict[str, Any]:
        """Serialize to a plain dict (for trace logging)."""
        return {
            "sender": self.sender,
            "receiver": self.receiver,
            "task": self.task,
            "context": self.context,
            "expected_output_format": self.expected_output_format,
        }


# ---------------------------------------------------------------------------
# Task 2 — Worker Agent
# ---------------------------------------------------------------------------

class WorkerAgent:
    """
    A specialized agent that handles tasks within a specific domain.
    """

    def __init__(
        self,
        name: str,
        specialty: str,
        llm_fn: Callable[[str], str],
    ) -> None:
        """
        Args:
            name:      Unique name for this worker (e.g. "ResearchAgent").
            specialty: Domain description (e.g. "web research and fact-finding").
            llm_fn:    Function str → str (the LLM).
        """
        self.name = name
        self.specialty = specialty
        self.llm_fn = llm_fn

    def get_capability_description(self) -> str:
        """
        Return a string describing what this agent can do.
        Used by the supervisor to decide routing.

        Returns:
            e.g. "ResearchAgent: Specializes in web research and fact-finding."
        """
        return f"{self.name}: Specializes in {self.specialty}."

    def process(self, message: AgentMessage) -> AgentMessage:
        """
        Process an incoming task message and return a response message.

        Steps:
            1. Build a prompt from the message task + context.
            2. Call llm_fn to get a result.
            3. Return a new AgentMessage with:
               sender = self.name
               receiver = message.sender
               task = message.task  (same task, for trace clarity)
               context = {"result": llm_result, "original_context": message.context}

        Returns:
            AgentMessage — the worker's response.
        """
        # 1. Build a prompt
        prompt = f"Task: {message.task}\nContext: {message.context}\nFormat: {message.expected_output_format}"
        
        # 2. Call llm_fn
        llm_result = self.llm_fn(prompt)
        
        # 3. Return a new AgentMessage
        return AgentMessage(
            sender=self.name,
            receiver=message.sender,
            task=message.task,
            context={"result": llm_result, "original_context": message.context},
            expected_output_format=message.expected_output_format
        )


# ---------------------------------------------------------------------------
# Task 3 — Supervisor Agent
# ---------------------------------------------------------------------------

class SupervisorAgent:
    """
    Orchestrates multiple WorkerAgents.
    Routes tasks, collects results, builds a communication trace.
    """

    def __init__(
        self,
        workers: list[WorkerAgent],
        llm_fn: Callable[[str], str],
    ) -> None:
        """
        Args:
            workers: List of WorkerAgent instances.
            llm_fn:  LLM function for the supervisor's own reasoning.
        """
        # TODO: store workers (build dict by name) and llm_fn
        # TODO: initialise self._trace: list[dict] = []
        self.workers = workers
        self.worker_map = {w.name: w for w in workers}
        self.llm_fn = llm_fn
        self._trace: list[dict] = []
        self._worker_call_counts = {w.name: 0 for w in workers}

    def route(self, task: str) -> WorkerAgent:
        """
        Select the best worker for a given task.

        Simple routing strategy:
            Check each worker's capability description for keyword overlap
            with the task. Return the worker with the most overlapping words.
            If tied or no overlap, return the first worker.

        Args:
            task: The task description string.

        Returns:
            A WorkerAgent instance.
        """
        # TODO: implement keyword-based routing
        task_words = set(task.lower().split())
        best_worker = self.workers[0]
        max_overlap = -1

        for worker in self.workers:
            desc_words = set(worker.get_capability_description().lower().replace(':', '').replace('.', '').split())
            overlap = len(task_words.intersection(desc_words))
            if overlap > max_overlap:
                max_overlap = overlap
                best_worker = worker
        
        return best_worker

    def run(self, task: str) -> dict[str, Any]:
        """
        Execute a task end-to-end with tracing.

        Steps:
            1. Reset self._trace = [].
            2. Route the task to a worker.
            3. Build an AgentMessage and send to the worker.
            4. Append the outgoing message to trace.
            5. Get the worker's response (another AgentMessage).
            6. Append the response to trace.
            7. Aggregate results.
            8. Return {"result": str, "trace": list[dict]}.

        Returns:
            dict with keys:
                "result" (str)        — the final answer
                "trace"  (list[dict]) — list of AgentMessage.to_dict() entries
        """
        # TODO
        self._trace = []
        
        # Route
        worker = self.route(task)
        self._worker_call_counts[worker.name] += 1
        
        # Outgoing message
        msg = AgentMessage(
            sender="Supervisor",
            receiver=worker.name,
            task=task
        )
        self._trace.append(msg.to_dict())
        
        # Process
        response = worker.process(msg)
        self._trace.append(response.to_dict())
        
        # Aggregate
        final_answer = self.aggregate_results([response])
        
        return {
            "result": final_answer,
            "trace": self._trace
        }

    def get_worker_stats(self) -> dict:
        """Return call count per worker across all run() calls.

        Returns:
            Dict mapping worker name → number of times that worker was called

        TODO: Track calls per worker and return the counts
        Note: You may need to add a self._worker_call_counts dict in __init__
        """
        return self._worker_call_counts

    def aggregate_results(self, results: list[AgentMessage]) -> str:
        """
        Combine multiple worker responses into a single answer.

        Args:
            results: List of response AgentMessages.

        Returns:
            A combined answer string.
        """
        # TODO: join result contexts into a summary string
        summaries = []
        for msg in results:
            res = msg.context.get("result", "")
            summaries.append(str(res))
        return " | ".join(summaries)


class PipelineAgent:
    """An agent that chains multiple WorkerAgents sequentially.

    The output of agent N becomes the input task for agent N+1.
    """

    def __init__(self, agents: list) -> None:
        """Initialize with an ordered list of WorkerAgent instances.

        Args:
            agents: List of WorkerAgent instances to chain in order
        """
        self.agents = agents
        self._pipeline_trace: list = []

    def run(self, initial_task: str) -> dict:
        """Run the pipeline, passing output of each agent to the next.

        The initial_task is sent to agents[0]. Each subsequent agent
        receives the 'task' field from the previous agent's output message.

        Args:
            initial_task: Task string for the first agent

        Returns:
            dict with keys:
              - 'result': str — final agent's response content
              - 'steps': int — number of agents executed
              - 'trace': list — list of AgentMessage dicts (one per step)

        TODO: Chain agents, collect trace, return result dict
        """
        self._pipeline_trace = []
        current_task = initial_task
        sender = "PipelineSupervisor"

        for agent in self.agents:
            msg = AgentMessage(sender=sender, receiver=agent.name, task=current_task)
            self._pipeline_trace.append(msg.to_dict())
            
            response = agent.process(msg)
            self._pipeline_trace.append(response.to_dict())
            
            # The result of the LLM becomes the task for the next agent
            current_task = response.context.get("result", "")
            sender = agent.name

        return {
            'result': current_task,
            'steps': len(self.agents),
            'trace': self._pipeline_trace
        }

    def get_pipeline_trace(self) -> list:
        """Return the trace from the most recent run() call.

        Returns:
            List of AgentMessage dicts from the last pipeline execution

        TODO: Return self._pipeline_trace
        """
        return self._pipeline_trace


# ---------------------------------------------------------------------------
# Task 4 — MCP Server & Client
# ---------------------------------------------------------------------------

class MCPServer:
    """
    Mock Model Context Protocol server.
    Manages a registry of tools that agents can call.
    """

    def __init__(self, name: str = "mcp-server") -> None:
        # TODO: store name and initialise self._tools: dict[str, Callable] = {}
        pass

    def register_tool(self, name: str, func: Callable[..., Any]) -> None:
        """
        Register a callable tool.

        Args:
            name: Tool identifier.
            func: The function to call when this tool is invoked.
        """
        # TODO
        raise NotImplementedError("Implement MCPServer.register_tool")

    def call_tool(self, name: str, args: dict[str, Any]) -> dict[str, Any]:
        """
        Invoke a registered tool with keyword arguments.

        Args:
            name: Tool name.
            args: Arguments to pass to the tool.

        Returns:
            The tool's return value (must be a dict).

        Raises:
            KeyError if the tool is not registered.
        """
        # TODO: look up and call the tool
        raise NotImplementedError("Implement MCPServer.call_tool")

    def list_tools(self) -> list[str]:
        """Return list of all registered tool names."""
        # TODO
        raise NotImplementedError("Implement MCPServer.list_tools")


class MCPClient:
    """
    Client that communicates with an MCPServer.
    """

    def __init__(self, server: MCPServer) -> None:
        # TODO: store server reference
        pass

    def list_tools(self) -> list[str]:
        """Return all tool names from the server."""
        # TODO
        raise NotImplementedError("Implement MCPClient.list_tools")

    def use_tool(self, name: str, args: dict[str, Any]) -> dict[str, Any]:
        """
        Call a tool on the server.

        Args:
            name: Tool name.
            args: Arguments dict.

        Returns:
            Tool result dict.
        """
        # TODO
        raise NotImplementedError("Implement MCPClient.use_tool")


# ---------------------------------------------------------------------------
# Entry point for manual testing
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    def mock_llm(prompt: str) -> str:
        return f"Mock response to: {prompt[:50]}..."

    research_worker = WorkerAgent("ResearchAgent", "web research and fact-finding", mock_llm)
    writing_worker = WorkerAgent("WritingAgent", "writing reports and summaries", mock_llm)
    analysis_worker = WorkerAgent("AnalysisAgent", "data analysis and statistics", mock_llm)

    supervisor = SupervisorAgent(
        workers=[research_worker, writing_worker, analysis_worker],
        llm_fn=mock_llm,
    )

    result = supervisor.run("Research the latest trends in AI")
    print("Result:", result["result"])
    print("\nTrace:")
    for step in result["trace"]:
        print(f"  {step['sender']} → {step['receiver']}: {step['task'][:60]}")

    # MCP Demo
    server = MCPServer("tools-server")
    server.register_tool("get_time", lambda: {"time": "12:00"})
    server.register_tool("get_date", lambda: {"date": "2026-03-31"})

    client = MCPClient(server)
    print("\nMCP Tools:", client.list_tools())
    print("Time:", client.use_tool("get_time", {}))
