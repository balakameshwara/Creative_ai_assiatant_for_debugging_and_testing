# AI-Powered Software Engineering Intelligence Tool

Welcome to the **AI-Powered Software Engineering Intelligence Tool**! This repository contains a powerful, full-stack application designed to seamlessly integrate advanced AI directly into your development workflow. 

This project serves as an intelligent coding pair-programmer by assisting with debugging, testing, and comprehensive code integrity checks right inside Visual Studio Code. It has been extensively scaled to handle enterprise-level codebases and deeply integrates with modern AI providers like Google Gemini and OpenAI.

## 🚀 Key Features

*   **Intelligent Code Analysis**: Effortlessly check the integrity of your code using advanced AI agents to identify potential issues, best-practice compliance, and structural validation.
*   **Automated Debugging**: Automatically debug specific, complex snags in your code. By leveraging AI along with dynamic file modification capabilities, the system tackles bugs intelligently and applies robust fixes natively.
*   **Intelligent Test Generation**: Quickly spin up unit tests across various frameworks. Increase your test coverage with a single execution of a command!
*   **Massive Codebase Scalability**: Employs a dynamic, three-strategy code modification system to prevent LLM output payload truncation on huge files (up to 5,000+ lines):
    *   *Full Rewrite*: For short chunks of code needing complete architectural overhauls.
    *   *Search & Replace*: For medium-sized targeted contextual edits.
    *   *Line-Number Edits*: Highly specific localized alterations for massive files.
*   **Premium VS Code Dashboard**: Features an intuitive, glassmorphic UI integrated right into your VS Code interface. Moving beyond simple text logs, it fully parses and renders rich analytics out-of-the-box.
*   **JSON Fault Tolerance**: Robust internal JSON validation with a built-in exponential backoff and retry loop to gracefully handle transient LLM API response errors and quota constraints.
*   **Multi-Provider AI Fallback**: Integrates heavily with the LangChain framework to dynamically route capabilities utilizing state-of-the-art models like Google Gemini 1.5 Pro and Gemini Flash.

## 🧰 Technology Stack

### Backend Service
- **Core Framework**: `Python 3.9+`, `FastAPI`
- **AI Orchestration**: `LangChain`, `Google Generative AI`, `OpenAI`
- **Vector Database**: `ChromaDB` (for efficient Retrieval-Augmented Generation / RAG processes)
- **Evaluation Engine**: `Pytest` (equipped with scripts for advanced multi-language testing frameworks spanning JavaScript, Java, C++, Go, and Rust via large generated datasets)

### Frontend Client
- **Core Engine**: `Node.js`, `TypeScript`, `VS Code Extension API`
- **User Interface**: `HTML/Vanilla CSS/JavaScript` constructed with a stunning Glassmorphic design pattern offering rich interactive data visualizations directly in the editor.

## 🏗️ Architecture & Project Structure

The project incorporates a distinct distributed architecture:
1.  **Backend API**: Acts as the central AI hub, performing heavy lifting natively utilizing LangChain chains, Vector Database embedding memories, and code patching capabilities.
2.  **Frontend Interface**: A lightweight client that securely captures code payloads, synchronizes context with the backend, and automatically applies dynamic edits back into the editor viewport.

```text
major project/
├── backend/                       # Python FastAPI Backend Layer
│   ├── agents.py                  # Core agent orchestration (Tester, Code Integrity, Debugger)
│   ├── check_models.py            # Diagnostic connectivity tools for Google Gemini capabilities
│   ├── evaluate_debugger.py       # Evaluation framework checking iterative agent accuracy
│   ├── generate_multilang_*.py    # Dataset generators for massive algorithmic evaluation benchmarks
│   ├── requirements.txt           # Python backend dependencies
│   ├── server.py                  # FastAPI Application Entrypoint
│   └── ...                        # Supporting scripts, contexts, & virtual environments
├── extension/                     # VS Code Extension Frontend Layer
│   ├── src/                       # TypeScript origin code
│   │   └── extension.ts           # Central logic communicating with the active Editor
│   ├── package.json               # Node.js dependencies and VS Code extension manifest
│   ├── tsconfig.json              # TypeScript compilation specifications
│   └── ...                        
├── architecture.md                # In-depth system architectural design guidelines
├── debug_flow.md                  # Specific breakdown covering the debugging pipeline
└── project_diagrams.md            # Textual/Visual system flow references
```

## 🛠️ Setup Instructions

### 1. Backend Service Setup

1. Navigate to the local `backend` directory:
   ```bash
   cd backend
   ```
2. Install necessary dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Environment Configuration:
   - Duplicate or rename `.env.example` into `.env`
   - Provide your valid target API Keys (e.g., `GOOGLE_API_KEY` for Google Gemini or `OPENAI_API_KEY`) within `.env`
4. Start the Application Server locally:
   ```bash
   python server.py
   ```
   *The server routes traffic efficiently and opens connections at `http://localhost:8000`.*

### 2. VS Code Extension Setup

1. Navigate into the `extension` directory:
   ```bash
   cd extension
   ```
2. Initialize and install frontend dependencies:
   ```bash
   npm install
   ```
3. Compile the typescript code:
   ```bash
   npm run compile
   ```
4. **Deploy in Visual Studio Code**:
   - Open the primary `extension` folder in Visual Studio Code.
   - Press `F5` to open a new instance (Extension Development Host window) natively running the client.

## 💡 Usage Guide

Once everything is up and running in your Extension Host environment:

1.  **Analyze Source Integrity**:
    - Open your required working file.
    - Run from the command palette (CTRL+SHIFT+P): `AI SE: Analyze Code`.
    - Explore the insights in the intelligent Dashboard!

2.  **Debug Complex Logic**:
    - Highlight the exact text snippet you desire to root cause (or focus out for the entire file).
    - Run from the command palette: `AI SE: Debug Code`.
    - Contextualize constraints via the message input prompt, and observe dynamic strategy patching fix the error magically.

3.  **Generate Comprehensive Tests**:
    - Switch your cursor focus to a target logical code file.
    - Run from the command palette: `AI SE: Generate Tests`.
    - Instantly harness fully-featured tests formulated by the AI within your suite.

## 📈 Agent Evaluation

This project maintains rigorous analytical metrics built directly into the codebase. Included within the `backend` directory, evaluation scripts (`evaluate_tester.py`, `evaluate_debugger.py`) consistently benchmark agent capabilities iteratively across auto-generated datasets from cross-compatible paradigms. The project routinely checks its logic implementation pass rates securely to iterate prompts and confirm >90% reliability guarantees natively across deployments.

## 🛡️ License

This codebase is open source and available for testing use natively. Check relevant dependencies for associated licensing criteria.
