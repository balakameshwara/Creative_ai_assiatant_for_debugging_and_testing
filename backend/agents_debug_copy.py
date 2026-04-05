from typing import Dict, Any
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

class BaseAgent:
    def __init__(self, model_name: str = "gemini-1.5-flash"):
        self.llm = ChatGoogleGenerativeAI(model=model_name, temperature=0, convert_system_message_to_human=True)

    def process(self, input_data: Dict[str, Any]) -> str:
        raise NotImplementedError

class DebuggerAgent(BaseAgent):
    def process(self, input_data: Dict[str, Any]) -> str:
        code = input_data.get("code", "")
        error = input_data.get("error", "")
        context = input_data.get("context", "")

        prompt = ChatPromptTemplate.from_template(
            """You are an expert Debugger Agent. 
            Analyze the following code and error message. Use the provided context if relevant.
            
            Code:
            {code}

            Error:
            {error}

            Context:
            {context}

            Identify the root cause and provide a fixed version of the code explanation.
            """
        )
        chain = prompt | self.llm | StrOutputParser()
        return chain.invoke({"code": code, "error": error, "context": context})

class TesterAgent(BaseAgent):
    def process(self, input_data: Dict[str, Any]) -> str:
        code = input_data.get("code", "")
        context = input_data.get("context", "")

        prompt = ChatPromptTemplate.from_template(
            """You are an expert Software Tester Agent.
            Generate comprehensive unit tests for the following code.
            
            Code:
            {code}

            Context:
            {context}

            Return the test code compatible with pytest or unittest.
            """
        )
        chain = prompt | self.llm | StrOutputParser()
        return chain.invoke({"code": code, "context": context})

class CodeIntegrityAgent(BaseAgent):
    def process(self, input_data: Dict[str, Any]) -> str:
        code = input_data.get("code", "")
        
        prompt = ChatPromptTemplate.from_template(
            """You are a Code Integrity Agent.
            Review the following code for style, security vulnerabilities, and best practices.
            
            Code:
            {code}

            Provide a report with:
            1. Security Issues
            2. Style Violations (PEP8 or equivalent)
            3. Performance Improvements
            """
        )
        chain = prompt | self.llm | StrOutputParser()
        return chain.invoke({"code": code})
