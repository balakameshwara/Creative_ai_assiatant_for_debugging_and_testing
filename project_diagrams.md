# AI-Powered Software Engineering Tool - Diagrams

## 1. System Architecture Diagram

This diagram illustrates the comprehensive high-level architecture of the system, including all currently implemented agents.

```mermaid
graph TD
    Client[VS Code Extension / HTTP Client]
    
    subgraph "Backend Server (FastAPI)"
        API[API Endpoints: /analyze, /debug, /test, /ingest]
        Orch[Agent Orchestrator]
        
        subgraph "Agents Layer"
            Debug[Debugger Agent]
            Test[Tester Agent]
            Integrity[Code Integrity Agent]
            Editor[File Editor Agent]
            MultiFile[Multi-File Analysis Agent]
        end
        
        subgraph "RAG System"
            Context[Project Context Manager]
            VectorDB[(ChromaDB)]
        end
    end
    
    External[Google Gemini API]

    %% Client Interactions
    Client -->|HTTP POST| API
    
    %% API to Orchestrator
    API -->|Dispatch Requests| Orch
    
    %% Orchestrator to Agents
    Orch -->|Invoke| Debug
    Orch -->|Invoke| Test
    Orch -->|Invoke| Integrity
    Orch -.->|Internal Invoke| Editor
    Orch -.->|Internal Invoke| MultiFile
    
    %% Context Management
    Orch -->|Manage/Retrieve| Context
    Context <-->|Read/Write Vectors| VectorDB
    
    %% Agent to LLM
    Debug <-->|LLM Inference (w/ Fallback)| External
    Test <-->|LLM Inference (w/ Fallback)| External
    Integrity <-->|LLM Inference (w/ Fallback)| External
    Editor <-->|LLM Inference (w/ Fallback)| External
    MultiFile <-->|LLM Inference (w/ Fallback)| External
```

## 2. Sequence Diagram (Debug Flow)

This sequence diagram outlines the process of a typical request, using the `/debug` endpoint as an example.

```mermaid
sequenceDiagram
    participant User
    participant Server as FastAPI Server (/debug)
    participant Orch as Agent Orchestrator
    participant Context as Project Context (RAG)
    participant Agent as Debugger Agent
    participant LLM as Google Gemini API

    User->>Server: POST /debug {code, error}
    Server->>Orch: run_debugger(code, error)
    
    %% Context Retrieval
    Orch->>Context: retrieve_context(code + error)
    Context-->>Orch: relevant_documents
    Orch->>Orch: format context string
    
    %% Agent Processing
    Orch->>Agent: process({code, error, context})
    Agent->>Agent: construct PromptTemplate
    
    %% LLM Interaction with Retry logic
    loop Fallback Models & Retries
        Agent->>LLM: invoke(prompt)
        alt Success
            LLM-->>Agent: JSON Response Wrapper
        else Rate Limit / Error
            LLM-->>Agent: Resource Exhausted (429) / Error
            Agent->>Agent: Wait (Exponential Backoff) & Retry
        end
    end
    
    Agent->>Agent: parse JSON response
    Agent-->>Orch: Parsed Dict (root_cause, fixed_code, breakpoints)
    
    Orch-->>Server: Result Dict
    Server-->>User: 200 OK {debug_info}
```
