from typing import Dict, Any, List, Optional
import json
import re
import os
import sys
import tempfile
import subprocess
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

class BaseAgent:
    def __init__(self):
        self.fallback_models = ["gemini-2.5-flash", "gemini-2.0-flash", "gemini-1.5-pro", "gemini-1.5-flash"]

    def _run_with_fallback(self, prompt_template, inputs, require_json=False):
        rate_limit_exception = None

        for i, model_name in enumerate(self.fallback_models):
            print(f"DEBUG: Attempting with model: {model_name}")
            try:
                # create fresh LLM and chain for this model
                llm = ChatGoogleGenerativeAI(model=model_name, temperature=0, convert_system_message_to_human=True)
                chain = prompt_template | llm | StrOutputParser()
                # Use fewer retries per model to fail over faster
                return self._run_with_retry(chain, inputs, max_retries=2, require_json=require_json)
            except Exception as e:
                error_str = str(e)
                if "RESOURCE_EXHAUSTED" in error_str or "429" in error_str:
                    print(f"WARNING: Model {model_name} rate limited. Switching to next model...")
                    rate_limit_exception = e
                    last_exception = e
                    continue
                elif "NOT_FOUND" in error_str or "404" in error_str:
                    print(f"WARNING: Model {model_name} not found (404). Switching to next model...")
                    last_exception = e
                    continue
                else:
                    raise e # Re-raise non-rate-limit errors immediately
        
        # Prioritize raising a rate limit exception if one was encountered, instead of a 404 not found mask
        raise rate_limit_exception or last_exception or Exception("All fallback models exhausted API quota.")

    def process(self, input_data: Dict[str, Any]) -> Any:
        raise NotImplementedError

    def _run_with_retry(self, chain, inputs, max_retries=5, require_json=False):
        import time
        import random
        import hashlib
        import json
        import os

        # --- Caching Logic ---
        cache_dir = ".cache"
        if not os.path.exists(cache_dir):
            os.makedirs(cache_dir)

        # Create a unique key based on inputs
        # sort_keys=True ensures consistent JSON string for same data
        input_str = json.dumps(inputs, sort_keys=True)
        input_hash = hashlib.sha256(input_str.encode("utf-8")).hexdigest()
        cache_file = os.path.join(cache_dir, f"{input_hash}.json")

        if os.path.exists(cache_file):
            print(f"DEBUG: Cache Hit! Loading response from {cache_file}")
            try:
                with open(cache_file, "r", encoding="utf-8") as f:
                    cached_data = json.load(f)["response"]
                    if require_json:
                        return self._parse_json(cached_data)
                    return cached_data
            except Exception as e:
                print(f"Warning: Failed to read or parse cache: {e}")
        # ---------------------

        for attempt in range(max_retries):
            try:
                result = chain.invoke(inputs)
                
                parsed_result = None
                if require_json:
                    parsed_result = self._parse_json(result) # Validate before caching
                
                # Save to cache on success
                try:
                    with open(cache_file, "w", encoding="utf-8") as f:
                        json.dump({"inputs": inputs, "response": result}, f, indent=2)
                except Exception as e:
                    print(f"Warning: Failed to write to cache: {e}")
                
                return parsed_result if require_json else result
            except Exception as e:
                print(f"DEBUG: Caught exception type: {type(e).__name__}, str: {e}")
                # Check for Resource Exhausted, generic 429, or transient network/parsing errors
                error_str = str(e)
                error_repr = repr(e)
                error_type = type(e).__name__
                
                if ("RESOURCE_EXHAUSTED" in error_str or 
                    "429" in error_str or 
                    "RESOURCE" in error_repr or 
                    "RemoteProtocolError" in error_type or 
                    "ConnectError" in error_type or
                    "Server disconnected" in error_str or
                    "ValueError" in error_type):
                    
                    if attempt == max_retries - 1:
                        raise e
                    
                    # Exponential backoff: 5, 10, 20, 40, 80...
                    wait_time = 5 * (2 ** attempt) + random.uniform(0, 1)
                    print(f"Rate limited or Network Error (Attempt {attempt + 1}/{max_retries}). Retrying in {wait_time:.2f} seconds...")
                    time.sleep(wait_time)
                else:
                    raise e
        return None

    def _parse_json(self, response: str) -> Dict[str, Any]:
        """
        Parses a JSON string from the LLM response, handling markdown code blocks.
        """
        try:
            # Clean up markdown code blocks if present
            cleaned_response = response.strip()
            if cleaned_response.startswith("```json"):
                cleaned_response = cleaned_response[7:]
            elif cleaned_response.startswith("```"): # Handle generic code blocks
                cleaned_response = cleaned_response[3:]
            
            if cleaned_response.endswith("```"):
                cleaned_response = cleaned_response[:-3]
            
            return json.loads(cleaned_response.strip(), strict=False)
        except json.JSONDecodeError as e:
            print(f"ERROR: Failed to parse JSON response: {e}")
            # Fallback: try to find a JSON object in the string
            try:
                match = re.search(r"\{.*\}", response, re.DOTALL)
                if match:
                    return json.loads(match.group(0), strict=False)
            except Exception:
                pass
            raise ValueError(f"Failed to parse JSON response: {e}")

class DebuggerAgent(BaseAgent):
    def __init__(self):
        super().__init__()
        self.fallback_models = ["gemini-2.5-flash", "gemini-2.0-flash", "gemini-1.5-pro", "gemini-1.5-flash"]

    def process(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        code = input_data.get("code", "")
        error = input_data.get("error", "")
        context = input_data.get("context", "")

        lines = code.split("\n")
        num_lines = len(lines)
        
        base_instructions = """You are an elite Staff Software Engineer and Debugging Expert. 
            Your goal is to flawlessly fix the provided Python code so that it satisfies the expected behavior and resolves the error.
            
            Code to fix:
            {code}

            Error Message / Traceback:
            {error}

            Expected Behavior / Context:
            {context}

            Follow this strict debugging process:
            1. Analyze the Context: Understand precisely what the algorithm or function is supposed to do.
            2. Analyze the Error: What does the error message signify? Where is it originating?
            3. Pinpoint the Fault: Identify the exact lines causing the bug (e.g., off-by-one errors, infinite loops, mutable default arguments, scope issues).
            4. Formulate a Fix: Determine the most minimal, Pythonic, and correct way to fix the code. Avoid rewriting entire blocks unless completely broken. Preserve working logic.
            5. Edge Cases: Double-check for empty inputs, boundary conditions (x=0, n=1, empty lists), and type safety.
            """

        if num_lines < 100:
            # STRATEGY 1: Full Rewrite (for code < 100 lines)
            prompt_str = base_instructions + """
            Output your response in valid JSON format with EXACTLY the following keys:
            {{
                "root_cause": "A precise, technical explanation of why the bug occurred.",
                "fixed_code": "The full, complete, and corrected Python code block. Include necessary imports if missing. Do NOT wrap the code in markdown blocks (e.g. do not use ```python). Just return the raw Python code.",
                "breakpoints": ["List of line numbers or variable names to watch to verify the fix."]
            }}
            Ensure the JSON is strictly valid, with no trailing commas, and escaping quotes inside strings correctly.
            """
            prompt = ChatPromptTemplate.from_template(prompt_str)
            return self._run_with_fallback(prompt, {"code": code, "error": error, "context": context}, require_json=True)
            
        elif num_lines <= 500:
            # STRATEGY 2: Search and Replace Blocks (for code 100 - 500 lines)
            prompt_str = base_instructions + """
            Since the code is moderately long, you must provide EXACT search and replace blocks rather than rewriting the full file.
            Output your response in valid JSON format with EXACTLY the following keys:
            {{
                "root_cause": "A precise, technical explanation of why the bug occurred.",
                "replacements": [
                    {{
                        "search": "exact string block to find in the original code, including exact leading whitespace",
                        "replace": "the new code block to replace it with"
                    }}
                ],
                "breakpoints": ["List of line numbers or variable names to watch to verify the fix."]
            }}
            Ensure the JSON is strictly valid. Do not use trailing commas.
            """
            prompt = ChatPromptTemplate.from_template(prompt_str)
            result = self._run_with_fallback(prompt, {"code": code, "error": error, "context": context}, require_json=True)
            
            if "replacements" in result:
                fixed_code = code
                for rep in result.get("replacements", []):
                    search_str = rep.get("search")
                    replace_str = rep.get("replace")
                    if search_str and replace_str is not None:
                         fixed_code = fixed_code.replace(search_str, replace_str)
                result["fixed_code"] = fixed_code
            elif "fixed_code" not in result:
                result["fixed_code"] = code # fallback to original if parsing fails
            return result
            
        else:
            # STRATEGY 3: Line Number Edits (for code > 500 lines)
            # Prepend line numbers to code layout to assist LLM
            numbered_code = "\n".join([f"{i+1:04d}: {line}" for i, line in enumerate(lines)])
            
            prompt_str = base_instructions + """
            The codebase is extremely long (over 500 lines) and has been prepended with 1-indexed line numbers formatted as '0001: ', '0002: ', etc.
            Do not output the full file. Output EXACTLY the line number ranges to replace.
            
            Output your response in valid JSON format with EXACTLY the following keys:
            {{
                "root_cause": "A precise, technical explanation.",
                "line_edits": [
                    {{
                        "start_line": integer line number to start replacing from (inclusive based on provided code lines),
                        "end_line": integer line number to replace up to (inclusive),
                        "replacement": "the actual code string to insert. DO NOT INCLUDE LINE NUMBER PREFIXES IN YOUR REPLACEMENT CODE! Be mindful of correct indentation."
                    }}
                ],
                "breakpoints": ["Line numbers or variables to watch."]
            }}
            """
            prompt = ChatPromptTemplate.from_template(prompt_str)
            result = self._run_with_fallback(prompt, {"code": numbered_code, "error": error, "context": context}, require_json=True)
            
            if "line_edits" in result:
                edits = result.get("line_edits", [])
                # Apply edits from bottom up so line offset doesn't corrupt subsequent edits
                try:
                    edits = sorted(edits, key=lambda x: int(x["start_line"]), reverse=True)
                    for edit in edits:
                        start = int(edit["start_line"]) - 1
                        end = int(edit["end_line"])
                        if start < 0: start = 0
                        
                        repl_lines = str(edit.get("replacement", "")).split("\n")
                        lines = lines[:start] + repl_lines + lines[end:]
                        
                    result["fixed_code"] = "\n".join(lines)
                except Exception as e:
                    print(f"Failed to apply line edits: {e}")
                    result["fixed_code"] = code # fallback
            elif "fixed_code" not in result:
                result["fixed_code"] = code
                
            return result

class TesterAgent(BaseAgent):
    def process(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        code = input_data.get("code", "")
        context = input_data.get("context", "")

        lines = code.split("\n")
        num_lines = len(lines)
        
        size_instruction = ""
        if num_lines > 300:
            size_instruction = "\nCRITICAL: The provided codebase is quite large. Focus on writing unit tests ONLY for the most critical, core functionality to avoid exceeding output boundaries. Exclude minor getters/setters or peripheral edge cases to save space."

        prompt = ChatPromptTemplate.from_template(
            """You are an expert Software Tester Agent.
            Generate comprehensive unit tests for the following code.{size_instruction}
            
            Code:
            {code}

            Context:
            {context}

            Think step-by-step:
            1. Identify the public interface (functions, classes) of the code.
            2. Determine edge cases, boundary conditions, and typical usage scenarios.
            3. Plan a set of tests to cover these scenarios.
            4. Write the test code using pytest or unittest.
            Assume the code to be tested is available in a module named `target_module`.
            Therefore, you must import the functions/classes to test from `target_module`.

            Output the result in valid JSON format with the following keys:
            {{
                "test_plan": "A brief description of the test coverage and scenarios.",
                "test_code": "The full executable test code compatible with pytest or unittest."
            }}
            Ensure the JSON is valid.
            """
        )
        result = self._run_with_fallback(prompt, {"code": code, "context": context, "size_instruction": size_instruction}, require_json=True)
        
        if "test_code" in result:
            with tempfile.TemporaryDirectory() as temp_dir:
                target_file = os.path.join(temp_dir, "target_module.py")
                test_file = os.path.join(temp_dir, "test_target.py")
                
                with open(target_file, "w", encoding="utf-8") as f:
                    f.write(code)
                    
                with open(test_file, "w", encoding="utf-8") as f:
                    f.write(result["test_code"])
                    
                try:
                    # Run pytest, fallback to unittest if pytest not found
                    process = subprocess.run(
                        [sys.executable, "-m", "pytest", "test_target.py"],
                        cwd=temp_dir,
                        capture_output=True,
                        text=True,
                        timeout=30
                    )
                    
                    if process.returncode != 0 and "No module named pytest" in process.stderr:
                        process = subprocess.run(
                            [sys.executable, "-m", "unittest", "test_target.py"],
                            cwd=temp_dir,
                            capture_output=True,
                            text=True,
                            timeout=30
                        )
                    
                    result["test_results"] = process.stdout + "\n" + process.stderr
                    result["tests_passed"] = (process.returncode == 0)
                except subprocess.TimeoutExpired:
                    result["test_results"] = "Test execution timed out after 30 seconds."
                    result["tests_passed"] = False
                except Exception as e:
                    result["test_results"] = f"Failed to execute tests: {e}"
                    result["tests_passed"] = False
                    
        return result

class CodeIntegrityAgent(BaseAgent):
    def process(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        code = input_data.get("code", "")
        
        lines = code.split("\n")
        num_lines = len(lines)
        
        base_instructions = """You are a Code Integrity Agent.
            Review the following code for style, security vulnerabilities, and best practices.
            
            Code:
            {code}

            Think step-by-step:
            1. Analyze Code: Provide a detailed explanation of what the code is doing.
            2. Scan for Security Vulnerabilities (OWASP Top 10, injection flaws, etc.).
            3. Check for Style Violations (PEP8 for Python, ESLint for JS/TS).
            4. Analyze for Performance Bottlenecks (inefficient loops, N+1 queries).
            5. Review against Best Practices (SOLID principles, clean code).
            """
            
        if num_lines < 100:
            prompt_str = base_instructions + """
            6. Suggest Code: Provide a complete, refactored version of the code that incorporates all your suggestions.

            Output the result in valid JSON format with the following keys:
            {{
                "code_explanation": "A detailed explanation of what the provided code does.",
                "security_issues": ["List of critical vulnerabilities found."],
                "style_violations": ["List of formatting or convention errors."],
                "performance_suggestions": ["List of speed/memory optimization suggestions."],
                "refactoring_suggestions": ["List of ideas to improve readability and maintainability."],
                "suggested_code": "The full refactored code block applying your suggestions. ALWAYS format the code with ```python code ``` markdown wrappers."
            }}
            Ensure the JSON is valid.
            """
            prompt = ChatPromptTemplate.from_template(prompt_str)
            return self._run_with_fallback(prompt, {"code": code}, require_json=True)
            
        elif num_lines <= 500:
            prompt_str = base_instructions + """
            6. Suggest Code: Since the code is moderately long, provide EXACT search and replace blocks rather than rewriting the full file.
            
            Output the result in valid JSON format with EXACTLY the following keys:
            {{
                "code_explanation": "A detailed explanation...",
                "security_issues": ["List of vulnerabilities."],
                "style_violations": ["List of style issues."],
                "performance_suggestions": ["Performance improvements."],
                "refactoring_suggestions": ["Refactoring ideas."],
                "replacements": [
                    {{
                        "search": "exact string block to find in the original code, including exact leading whitespace",
                        "replace": "the new code block to replace it with"
                    }}
                ]
            }}
            Ensure the JSON is valid.
            """
            prompt = ChatPromptTemplate.from_template(prompt_str)
            result = self._run_with_fallback(prompt, {"code": code}, require_json=True)
            
            if "replacements" in result:
                fixed_code = code
                for rep in result.get("replacements", []):
                    search_str = rep.get("search")
                    replace_str = rep.get("replace")
                    if search_str and replace_str is not None:
                         fixed_code = fixed_code.replace(search_str, replace_str)
                result["suggested_code"] = fixed_code
            elif "suggested_code" not in result:
                result["suggested_code"] = code # fallback
            return result
            
        else:
            numbered_code = "\n".join([f"{i+1:04d}: {line}" for i, line in enumerate(lines)])
            prompt_str = base_instructions + """
            6. Suggest Code: The codebase is extremely long (over 500 lines) and has been prepended with 1-indexed line numbers formatted as '0001: ', '0002: ', etc.
            Do not output the full file. Output EXACTLY the line number ranges to replace to apply your refactoring.
            
            Output the result in valid JSON format with EXACTLY the following keys:
            {{
                "code_explanation": "A detailed explanation...",
                "security_issues": ["List of vulnerabilities."],
                "style_violations": ["List of style issues."],
                "performance_suggestions": ["Performance improvements."],
                "refactoring_suggestions": ["Refactoring ideas."],
                "line_edits": [
                    {{
                        "start_line": integer line number to start replacing from (inclusive based on provided code lines),
                        "end_line": integer line number to replace up to (inclusive),
                        "replacement": "the actual code string to insert. DO NOT INCLUDE LINE NUMBER PREFIXES IN YOUR REPLACEMENT CODE! Be mindful of correct indentation."
                    }}
                ]
            }}
            Ensure the JSON is valid.
            """
            prompt = ChatPromptTemplate.from_template(prompt_str)
            result = self._run_with_fallback(prompt, {"code": numbered_code}, require_json=True)
            
            if "line_edits" in result:
                edits = result.get("line_edits", [])
                try:
                    edits = sorted(edits, key=lambda x: int(x["start_line"]), reverse=True)
                    for edit in edits:
                        start = int(edit["start_line"]) - 1
                        end = int(edit["end_line"])
                        if start < 0: start = 0
                        
                        repl_lines = str(edit.get("replacement", "")).split("\n")
                        lines = lines[:start] + repl_lines + lines[end:]
                        
                    result["suggested_code"] = "\n".join(lines)
                except Exception as e:
                    print(f"Failed to apply line edits: {e}")
                    result["suggested_code"] = code
            elif "suggested_code" not in result:
                result["suggested_code"] = code
                
            return result

class FileEditorAgent(BaseAgent):
    def process(self, input_data: Dict[str, Any]) -> str:
        code = input_data.get("code", "")
        instruction = input_data.get("instruction", "")
        
        prompt = ChatPromptTemplate.from_template(
            """You are an expert Senior Software Engineer.
            Your task is to modify the provided code according to the specific instructions.
            
            Code:
            {code}

            Instruction:
            {instruction}

            Return ONLY the full modified code. Do not include markdown formatting (like ```python) or explanations unless explicitly asked.
            Just the raw code.
            """
        )
        return self._run_with_fallback(prompt, {"code": code, "instruction": instruction})

class MultiFileAnalysisAgent(BaseAgent):
    def process(self, input_data: Dict[str, Any]) -> str:
        # Expecting 'files' to be a dictionary of "filename": "content"
        files = input_data.get("files", {})
        question = input_data.get("question", "")
        
        # Format files for the prompt
        files_context = ""
        for name, content in files.items():
            files_context += f"--- {{name}} ---\n{{content}}\n\n"

        prompt = ChatPromptTemplate.from_template(
            """You are an expert Software Architect.
            Analyze the following set of files and answer the user's question.
            
            Files:
            {files_context}

            Question:
            {question}

            Provide a detailed answer based specifically on the provided files.
            """
        )
        return self._run_with_fallback(prompt, {"files_context": files_context, "question": question})
