# Day 9 — Reflection
## Multi-Agent System Architecture

**Deliverable:** ASCII architecture diagram + comparative analysis paragraph

---

## Section 1 — Architecture Diagram

Draw your full multi-agent system as ASCII art. Your diagram must show:
- The Supervisor agent
- All Worker agents
- The PipelineAgent (if used)
- The MCPServer with registered tools
- Message flow arrows between components

```
[paste your ASCII diagram here]

Example structure to fill in:

User Query
    |
    v
SupervisorAgent ("YourSupervisorName")
    |
    +-- route() --> WorkerAgent("Worker1", "specialty1")
    |                   |
    |                   +-- MCPClient --> MCPServer
    |                       ["tool_1", "tool_2"]
    |
    +-- route() --> WorkerAgent("Worker2", "specialty2")
    |
    v
aggregate_results()
    |
    v
Final Answer
```

---

## Section 2 — Monolithic vs. Multi-Agent Comparison

**Write 1 paragraph (100–200 words) comparing your multi-agent system to a monolithic single-agent approach:**

Consider:
- What does your multi-agent system do better?
- What does it do worse (e.g., latency, complexity, debugging difficulty)?
- For your specific domain, is the added complexity of multi-agent worth it?

> *Your paragraph:*

---

## Section 3 — Production Considerations

**If you were deploying this multi-agent system to production, what are the 3 biggest risks?**

| Risk | Likelihood (H/M/L) | Impact (H/M/L) | Mitigation |
|------|-------------------|----------------|------------|
| | | | |
| | | | |
| | | | |
