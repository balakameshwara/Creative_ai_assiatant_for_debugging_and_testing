# System Architecture

The following diagram illustrates the high-level architecture of the AI-Powered Software Engineering Tool.

```mermaid
graph TD
    Client[VS Code Extension / User]
    
    subgraph "Backend Server (FastAPI)"
        API[API Endpoints]
        Orch[Agent Orchestrator]
        
        subgraph "Agents Layer"
            Debug[Debugger Agent]
            Test[Tester Agent]
            Integrity[Code Integrity Agent]
        end
        
        subgraph "RAG System"
            Context[Project Context Manager]
            VectorDB[(ChromaDB)]
        end
    end
    
    External[Google Gemini API]

    %% Connections
    Client -->|HTTP POST /analyze, /debug, /test| API
    API -->|Dispatch| Orch
    
    Orch -->|Invoke| Debug
    Orch -->|Invoke| Test
    Orch -->|Invoke| Integrity
    
    Orch -->|Manage| Context
    Context <-->|Read/Write Vectors| VectorDB
    
    Debug -->|Context Retrieval| Context
    Test -->|Context Retrieval| Context
    
    Debug <-->|LLM Inference| External
    Test <-->|LLM Inference| External
    Integrity <-->|LLM Inference| External
```

## Component Description

1.  **Client**: The interface (VS Code Extension or HTTP Client) sending code analysis requests.
2.  **API Layer**: Python FastAPI server handling HTTP requests and routing them to the orchestrator.
3.  **Agent Orchestrator**: Central controller that manages the lifecycle of agents and context retrieval.
4.  **Agents**: Specialized AI agents powered by LLMs (Google Gemini) to perform specific tasks:
    *   **Debugger**: Analyzes errors and code to suggest fixes.
    *   **Tester**: Generates unit tests.
    *   **Integrity**: Checks for code quality and security issues.
5.  **RAG System**: Retrieval-Augmented Generation module.
    *   **Project Context**: Manages file ingestion and query retrieval.
    *   **ChromaDB**: Vector database storing embeddings of the project's codebase for efficient context matching.
6.  **External**: Google Gemini API provides the generative capabilities for the agents.
