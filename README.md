# AI-Powered Software Engineering Intelligence Tool

Welcome to the AI-Powered Software Engineering Intelligence Tool! This repository contains a powerful, full-stack application designed to seamlessly integrate advanced AI directly into your development workflow. 

It acts as an intelligent coding pair-programmer by assisting with debugging, testing, and comprehensive code integrity checks right inside Visual Studio Code.

## 🚀 Key Features

*   **Intelligent Code Analysis**: Effortlessly check the integrity of your code using advanced AI agents to identify potential issues, standard compliance, and structure validation.
*   **Automated Debugging**: Automatically debug specific, complex snags in your code. By leveraging AI along with dynamic file modification capability, the system can tackle bugs intelligently and apply robust fixes using dynamic strategies.
*   **Automatic Test Generation**: Quickly spin up unit tests across various frameworks. Increase your test coverage with a single command!
*   **Advanced modifications**: Handles large codebase operations through a dynamic, three-strategy file system mechanism (Full Rewrite, Search/Replace, and targeted Line-Number Edits), completely eliminating conventional context truncation for very large files.
*   **Premium VS Code Dashboard**: Uses an intuitive, glassmorphic UI integrated right into your VS Code interface, moving beyond simple text logs to fully parse and render rich analytics out-of-the-box.

## 🏗️ Architecture

The solution uses a hybrid, deeply integrated architecture:
1.  **Backend Layer (Python/FastAPI)**: Performs the heavy lifting utilizing LangChain architecture, intelligent agent orchestrators, a Vector Database component (ChromaDB) for historical queries, and tight LLM integration.
2.  **Frontend Client (VS Code Extension)**: A lightweight, visually stunning client that efficiently captures context from your local editor, bridges the communication gap with the underlying backend, and renders complex code modifications natively.

## 🛠️ Setup Instructions

### 1. Backend Service Setup

**Requirements:** `Python 3.9+`

1. Navigate to the `backend` directory:
   ```bash
   cd backend
   ```
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Environment Configuration:
   - Rename `.env.example` to `.env`
   - Add your `OPENAI_API_KEY` (or the respective supported LLM Provider Key) to `.env`
4. Start the Application Server:
   ```bash
   python server.py
   ```
   *The server acts as the central AI hub, and starts correctly at `http://localhost:8000`.*

### 2. VS Code Extension Setup

**Requirements:** `Node.js`, `npm`

1. Navigate to the `extension` directory:
   ```bash
   cd extension
   ```
2. Install npm dependencies:
   ```bash
   npm install
   ```
3. Compile the typescript code:
   ```bash
   npm run compile
   ```
4. **Deploy in VS Code**:
   - Open the primary `extension` folder in VS Code.
   - Press `F5` to open a new Extension Development Host window with the client pre-installed.

## 💡 Usage Guide

Once everything is up and running in your Extension Host:

1.  **Analyze Source Integrity**:
    - Open your required working file.
    - Run from the command palette: `AI SE: Analyze Code`.
    - Check the parsed insights in the dynamic dashboard view!

2.  **Debug Complex Logic**:
    - Highlight the exact text snippet to debug (or target the entire file).
    - Run from the command palette: `AI SE: Debug Code`.
    - Drop in the precise errors when prompted, then sit back while the tool applies the logic fix back into your editor workspace.

3.  **Generate Comprehensive Tests**:
    - Focus on a code file.
    - Run from the command palette: `AI SE: Generate Tests`.
    - Implement newly generated unit tests rapidly into your test harness from the output dashboard.

## 🛡️ License

This project is licensed individually. Please see relevant license terms where applicable.
