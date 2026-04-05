from typing import Dict, Any, List
from agents import DebuggerAgent, TesterAgent, CodeIntegrityAgent, FileEditorAgent, MultiFileAnalysisAgent
from rag_context import ProjectContext

class AgentOrchestrator:
    def __init__(self):
        self.context_module = ProjectContext()
        self.debugger = DebuggerAgent()
        self.tester = TesterAgent()
        self.integrity = CodeIntegrityAgent()
        self.editor = FileEditorAgent()
        self.multi_file = MultiFileAnalysisAgent()

    def ingest_files(self, file_paths: List[str]):
        self.context_module.add_code_files(file_paths)

    def run_debugger(self, code: str, error: str) -> Dict[str, Any]:
        # Retrieve context relevant to the code or error
        relevant_docs = self.context_module.retrieve_context(code + "\n" + error)
        context_str = "\n".join([d.page_content for d in relevant_docs])
        
        return self.debugger.process({
            "code": code,
            "error": error,
            "context": context_str
        })

    def run_tester(self, code: str) -> Dict[str, Any]:
        relevant_docs = self.context_module.retrieve_context(code)
        context_str = "\n".join([d.page_content for d in relevant_docs])
        
        return self.tester.process({
            "code": code,
            "context": context_str
        })

    def run_integrity_check(self, code: str) -> Dict[str, Any]:
        return self.integrity.process({"code": code})

    def run_file_editor(self, code: str, instruction: str) -> str:
        return self.editor.process({"code": code, "instruction": instruction})

    def run_multi_file_analysis(self, files: Dict[str, str], question: str) -> str:
        return self.multi_file.process({"files": files, "question": question})

