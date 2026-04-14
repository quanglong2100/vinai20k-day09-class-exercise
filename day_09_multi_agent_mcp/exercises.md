# Day 9 — Exercises
## Multi-Agent & MCP | Lab Worksheet

**Lab Duration:** 3 hours  
**Structure:** Warm-up (20 min) → Core Coding (60 min) → Extended Exercises (60 min) → Reflection (30 min)

---

## Part 1 — Warm-up (0:00–0:20)

### Exercise 1.1 — Architecture Sketch
Before writing any code, design a multi-agent system for YOUR domain (from Day 2):

**Name your Supervisor agent and at least 2 specialized Worker agents:**
- Supervisor: Travel Operations Coordinator
- Worker 1 (name + specialty): FlightAnalyst — Searching flight routes, pricing, and availability.
- Worker 2 (name + specialty): HotelResearcher — Finding accommodations based on budget and amenities.
- Worker 3 (optional): LocalGuide — Planning daily itineraries and suggesting local attractions.

**Draw the message flow as ASCII art (Supervisor → routing → Worker → response → Supervisor):**
```
[ User Query ]
            |
            v
    [ SupervisorAgent ] <-----------------------+
            |                                   |
    (1) route_task()                            |
            |                                   |
            +------> [ Worker: FlightAnalyst ]--+ (2) response
            |                                   |
            +------> [ Worker: HotelResearcher ]+ (2) response
            |                                   |
            +------> [ Worker: LocalGuide ]-----+ (2) response
            |
    (3) aggregate_results()
            |
            v
      [ Final Answer ]
```

**What routing logic would your Supervisor use to decide which worker gets each task?**
The Supervisor uses a keyword-based overlap strategy. It tokenizes the user's task description and compares it against the specialty descriptions of each worker. For example, if the query contains "flight" or "airline," it routes to the FlightAnalyst. If no strong overlap is found, it defaults to the most general-purpose worker.

---

### Exercise 1.2 — Pipeline vs. Supervisor-Worker
**What is the difference between the Pipeline pattern (agents in sequence) and the Supervisor-Worker pattern (central router)?**

Fill in this comparison table:

| Aspect | Pipeline Pattern | Supervisor-Worker Pattern |
|--------|-----------------|--------------------------|
| Task flow | Sequential | Routed |
| Best for | Fixed, multi-step workflows | Dynamic tasks with unknown sub-tasks |
| Failure mode | Cascading (if Step 1 fails, Step 2 stops) | Isolated (one worker failing doesn't stop others) |
| Example use case | Translation -> Summarization | Customer Support (Billing vs. Tech Support) |

**Give a concrete scenario from your domain where Pipeline is better, and one where Supervisor-Worker is better:**
Pipeline is better when: Processing a booking confirmation. Step 1: Extract data from email -> Step 2: Validate against database -> Step 3: Generate PDF receipt. Each step depends strictly on the output of the previous one.
Supervisor-Worker is better when: Handling a general user query like "Help me plan a trip to Tokyo." The Supervisor must decide whether the user needs flight info, hotel info, or sightseeing info (or all three) and delegate accordingly.

---

## Part 2 — Core Coding (0:20–1:20)
Implement all TODOs in `template.py`. Run `pytest tests/` to check progress.

### Checklist
- [ ] `AgentMessage` dataclass — define 5 fields with defaults
- [ ] `AgentMessage.to_dict` — serialize to plain dict
- [ ] `WorkerAgent.__init__` — store name, specialty, llm_fn
- [ ] `WorkerAgent.get_capability_description` — return descriptive string
- [ ] `WorkerAgent.process` — build prompt, call LLM, return response AgentMessage
- [ ] `SupervisorAgent.__init__` — store workers dict, llm_fn, trace, call counts
- [ ] `SupervisorAgent.route` — keyword overlap routing
- [ ] `SupervisorAgent.run` — full task execution with tracing
- [ ] `SupervisorAgent.aggregate_results` — combine worker responses
- [ ] `SupervisorAgent.get_worker_stats` — return call counts per worker
- [ ] `PipelineAgent.__init__` — store agents list and trace
- [ ] `PipelineAgent.run` — chain agents, collect trace
- [ ] `PipelineAgent.get_pipeline_trace` — return trace from last run
- [ ] `MCPServer.__init__` — store name and tools dict
- [ ] `MCPServer.register_tool` — add to registry
- [ ] `MCPServer.call_tool` — look up and invoke
- [ ] `MCPServer.list_tools` — return tool names
- [ ] `MCPClient.__init__` — store server reference
- [ ] `MCPClient.list_tools` — delegate to server
- [ ] `MCPClient.use_tool` — delegate to server

---

## Part 3 — Extended Exercises (1:20–2:20)

### Exercise 3.1 — Domain Supervisor System
Build 2 specialized WorkerAgents for your domain (e.g., "data_retriever" and "response_formatter"). Wire them into a SupervisorAgent. Run 3 different tasks and record the routing decisions:

| Task | Worker Assigned | Worker Response (brief) | Was Routing Correct? |
|------|----------------|------------------------|---------------------|
| | | | |
| | | | |
| | | | |

**Look at `get_worker_stats()` output. Is the workload balanced? What would you change about the routing logic?**
> *Your answer:*

---

### Exercise 3.2 — Pipeline vs. Supervisor Comparison
Build a `PipelineAgent` with 2 workers (worker1 → worker2). Run the same 3 tasks from Exercise 3.1. Compare:

| Task | Pipeline Output (brief) | Supervisor Output (brief) | Which was better? |
|------|------------------------|--------------------------|------------------|
| | | | |
| | | | |
| | | | |

**In your domain, when would a pipeline produce better results than supervisor routing? Explain with a concrete example.**
> *Your answer (2–3 sentences):*

---

### Exercise 3.3 — MCP Tool Integration
Register 2 mock tools on an `MCPServer` relevant to your domain (e.g., "search_knowledge_base" returning a dict with "results" key, "format_response" returning a dict with "formatted" key).

Connect an `MCPClient`. Call each tool and verify the round-trip:

```python
# Paste your code here:
```

**MCP call trace (paste output):**
```
[paste trace here]
```

**What real-world tools would you want to expose via MCP for your AI product?**
> *List at least 3 tools with their purpose:*
> 1.
> 2.
> 3.

---

## Part 4 — Reflection (2:20–2:50)
See `reflection.md`

---

## Submission Checklist
- [ ] All tests pass: `pytest tests/ -v`
- [ ] `PipelineAgent.run` and `get_pipeline_trace` implemented
- [ ] `SupervisorAgent.get_worker_stats` implemented
- [ ] `exercises.md` completed (all tables filled)
- [ ] `reflection.md` written
- [ ] `solution/solution.py` copied
