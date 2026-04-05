# Debug Process Flow

The following diagram illustrates the flow of a request to the `/debug` endpoint.

```mermaid
sequenceDiagram
    participant User
    participant Server as Server (/debug)
    participant Orch as Orchestrator
    participant Context as ProjectContext (RAG)
    participant Agent as DebuggerAgent
    participant LLM as Gemini API

    User->>Server: POST /debug {code, error}
    Server->>Orch: run_debugger(code, error)
    Orch->>Context: retrieve_context(code + error)
    Context-->>Orch: relevant_docs
    Orch->>Orch: Format context string
    Orch->>Agent: process({code, error, context})
    Agent->>Agent: Construct Prompt
    Agent->>LLM: invoke(prompt)
    alt Success
        LLM-->>Agent: Analysis & Fix
        Agent-->>Orch: Response String
        Orch-->>Server: Result
        Server-->>User: 200 OK {debug_info}
    else Rate Limit (429)
        LLM-->>Agent: 429 Resource Exhausted
        Agent->>Agent: Retry with Backoff (x5)
        Note right of Agent: If retries fail:
        Agent-->>Server: Raise Exception
        Server-->>User: 429 Too Many Requests
    end
```

## detailed Steps

1.  **Request**: User sends code and error message to `/debug`.
2.  **Orchestration**: `AgentOrchestrator` receives the request.
3.  **Context Retrieval**: `ProjectContext` searches the vector database for relevant existing code or docs.
4.  **Agent Execution**: `DebuggerAgent` prepares the prompt with code, error, and retrieved context.
5.  **LLM Call**: The agent calls Google Gemini API.
    *   **Retry Logic**: The agent has built-in retry logic for transient errors or rate limits (exponential backoff).
6.  **Response**: The analysis and suggested fix are returned to the user.
