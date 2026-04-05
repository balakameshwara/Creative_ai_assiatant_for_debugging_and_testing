import * as vscode from 'vscode';
import axios from 'axios';
import * as cp from 'child_process';
import * as os from 'os';
import * as path from 'path';

const BACKEND_URL = 'http://localhost:8000';

let serverProcess: cp.ChildProcess | undefined;

export function activate(context: vscode.ExtensionContext) {
    console.log('AI SE Intelligence Platform (Dashboard Pro) is now active!');

    // Start Backend Server
    const backendPath = path.join(__dirname, '..', '..', 'backend', 'server.py');
    serverProcess = cp.spawn('python', [backendPath]);

    serverProcess.stdout?.on('data', (d) => console.log(`[Backend] ${d}`));
    serverProcess.stderr?.on('data', (d) => console.error(`[Backend Error] ${d}`));

    // Command: Analyze Code
    let analyzeDisposable = vscode.commands.registerCommand('ai-se-tool.analyzeCode', async () => {
        const editor = vscode.window.activeTextEditor;
        if (!editor) return vscode.window.showErrorMessage('Open a file to analyze.');
        const code = editor.document.getText(editor.selection) || editor.document.getText();
        try {
            vscode.window.showInformationMessage('Running Code Analysis...');
            const response = await axios.post(`${BACKEND_URL}/analyze`, { code });
            await generateAndOpenReport('Code Intelligence Dashboard', response.data.analysis);
        } catch (error: any) { handleError(error); }
    });

    // Command: Debug Code
    let debugDisposable = vscode.commands.registerCommand('ai-se-tool.debugCode', async () => {
        const editor = vscode.window.activeTextEditor;
        if (!editor) return vscode.window.showErrorMessage('Open code to debug.');
        const code = editor.document.getText(editor.selection) || editor.document.getText();
        const errorInput = await vscode.window.showInputBox({ prompt: "What error are you seeing?" });
        if (!errorInput) return;
        try {
            vscode.window.showInformationMessage('Analyzing Bug & Generating Fix...');
            const response = await axios.post(`${BACKEND_URL}/debug`, { code, error: errorInput });
            
            // Map AI Breakpoints to VS Code Breakpoints
            let debugInfo = response.data.debug_info;
            if (typeof debugInfo === 'string') {
                try { debugInfo = JSON.parse(debugInfo); } catch (e) { }
            }
            
            if (debugInfo && debugInfo.breakpoints && Array.isArray(debugInfo.breakpoints)) {
                const newBps: vscode.Breakpoint[] = [];
                debugInfo.breakpoints.forEach((bp: any) => {
                    // Extract line number
                    const match = String(bp).match(/\b(\d+)\b/);
                    if (match) {
                        const lineNum = parseInt(match[1]) - 1; // VS Code is 0-indexed
                        if (lineNum >= 0 && lineNum < editor.document.lineCount) {
                            const uri = editor.document.uri;
                            const pos = new vscode.Position(lineNum, 0);
                            const location = new vscode.Location(uri, pos);
                            newBps.push(new vscode.SourceBreakpoint(location, true));
                        }
                    }
                });

                if (newBps.length > 0) {
                    vscode.debug.addBreakpoints(newBps);
                    vscode.window.showInformationMessage(`Added ${newBps.length} AI-suggested breakpoint(s).`);
                }
            }

            await generateAndOpenReport('Automated Bug Fix Dashboard', response.data.debug_info);
        } catch (error: any) { handleError(error); }
    });

    // Command: Generate Tests
    let testDisposable = vscode.commands.registerCommand('ai-se-tool.generateTests', async () => {
        const editor = vscode.window.activeTextEditor;
        if (!editor) return vscode.window.showErrorMessage('Open code to test.');
        const code = editor.document.getText(editor.selection) || editor.document.getText();
        try {
            vscode.window.showInformationMessage('Generating Automated Test Suite...');
            const response = await axios.post(`${BACKEND_URL}/test`, { code });
            await generateAndOpenReport('Test Intelligence Dashboard', response.data.tests);
        } catch (error: any) { handleError(error); }
    });

    context.subscriptions.push(analyzeDisposable, debugDisposable, testDisposable);
}

async function generateAndOpenReport(title: string, result: any) {
    const htmlContent = generateHtmlReport(title, result);
    try {
        const timestamp = Date.now();
        // Matching the user's preferred naming convention
        const fileName = `analyze_report_${timestamp}.html`;
        const tempPath = path.join(os.tmpdir(), fileName);
        await vscode.workspace.fs.writeFile(vscode.Uri.file(tempPath), Buffer.from(htmlContent, 'utf8'));

        console.log(`Report location: ${tempPath}`);

        let command: string;
        if (process.platform === 'win32') {
            // Using Start-Process is necessary to force it out of VS Code's internal browser
            command = `powershell -Command "Start-Process '${tempPath}'"`;
        } else if (process.platform === 'darwin') {
            command = `open "${tempPath}"`;
        } else {
            command = `xdg-open "${tempPath}"`;
        }

        cp.exec(command, (err) => {
            if (err) vscode.env.openExternal(vscode.Uri.file(tempPath));
        });
        vscode.window.showInformationMessage('Dashboard launched in external browser.');
    } catch (err: any) {
        vscode.window.showErrorMessage(`Dashboard Launch Error: ${err.message}`);
    }
}

function generateHtmlReport(title: string, result: any): string {
    const { sectionsHtml, sidebarHtml, summaryHtml } = formatResultToDashboard(result);
    return `
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>${title}</title>
    <link href="https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;500;600;700&family=JetBrains+Mono:wght@400;500&display=swap" rel="stylesheet">
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/highlight.js/11.8.0/styles/tokyo-night-dark.min.css">
    <style>
        :root {
            --bg-base: #030712;
            --bg-card: rgba(17, 24, 39, 0.7);
            --bg-card-hover: rgba(31, 41, 55, 0.8);
            --accent: #3b82f6; 
            --accent-glow: rgba(59, 130, 246, 0.5);
            --success: #10b981;
            --danger: #ef4444;
            --warning: #f59e0b;
            --border: rgba(255, 255, 255, 0.1);
            --text-main: #f9fafb;
            --text-muted: #9ca3af;
        }
        
        * { box-sizing: border-box; margin: 0; padding: 0; }
        
        body { 
            font-family: 'Outfit', sans-serif; 
            background: radial-gradient(circle at 15% 50%, rgba(15, 23, 42, 1), var(--bg-base) 60%),
                        radial-gradient(circle at 85% 30%, rgba(23, 15, 36, 1), var(--bg-base) 60%);
            background-color: var(--bg-base); 
            color: var(--text-main); 
            display: flex; 
            height: 100vh; 
            overflow: hidden; 
        }
        
        /* Glassmorphic Sidebar */
        .sidebar { 
            width: 280px; 
            background: rgba(3, 7, 18, 0.6); 
            backdrop-filter: blur(20px);
            -webkit-backdrop-filter: blur(20px);
            border-right: 1px solid var(--border); 
            padding: 32px 20px; 
            display: flex; 
            flex-direction: column; 
            box-shadow: 10px 0 30px rgba(0,0,0,0.5);
            z-index: 10;
        }
        
        .main { 
            flex: 1; 
            padding: 48px 64px; 
            overflow-y: auto; 
            scroll-behavior: smooth; 
        }
        
        .logo { 
            font-size: 1.25rem; 
            font-weight: 700; 
            background: linear-gradient(135deg, #60a5fa, #a78bfa);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            margin-bottom: 40px; 
            display: flex; 
            align-items: center; 
            gap: 12px; 
            letter-spacing: 0.5px;
        }
        
        .nav-link { 
            display: flex; 
            align-items: center; 
            gap: 14px; 
            padding: 14px 16px; 
            color: var(--text-muted); 
            text-decoration: none; 
            border-radius: 12px; 
            margin-bottom: 8px; 
            font-weight: 500;
            transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1); 
            border: 1px solid transparent;
        }
        
        .nav-link:hover { 
            background: rgba(255,255,255,0.05); 
            color: var(--text-main); 
            border: 1px solid rgba(255,255,255,0.1);
            transform: translateX(4px);
            box-shadow: 0 4px 12px rgba(0,0,0,0.2);
        }
        
        h1 {
            font-size: 2.5rem;
            font-weight: 700;
            margin-bottom: 40px;
            letter-spacing: -0.5px;
            animation: fadeInDown 0.8s ease-out;
        }

        .summary-grid { 
            display: grid; 
            grid-template-columns: repeat(auto-fit, minmax(220px, 1fr)); 
            gap: 24px; 
            margin-bottom: 48px; 
            animation: fadeInUp 0.8s ease-out 0.2s both;
        }
        
        .summary-box { 
            background: var(--bg-card); 
            backdrop-filter: blur(12px);
            border: 1px solid var(--border); 
            border-radius: 16px; 
            padding: 24px; 
            transition: transform 0.3s ease, border-color 0.3s ease, box-shadow 0.3s ease;
            position: relative;
            overflow: hidden;
        }

        .summary-box::before {
            content: '';
            position: absolute;
            top: 0; left: 0; right: 0; height: 2px;
            background: linear-gradient(90deg, transparent, var(--accent), transparent);
            opacity: 0;
            transition: opacity 0.3s ease;
        }

        .summary-box:hover {
            transform: translateY(-4px);
            border-color: rgba(255,255,255,0.2);
            box-shadow: 0 10px 25px rgba(0,0,0,0.4);
        }
        .summary-box:hover::before { opacity: 1; }
        
        .card { 
            background: var(--bg-card); 
            backdrop-filter: blur(12px);
            border: 1px solid var(--border); 
            border-radius: 16px; 
            margin-bottom: 40px; 
            overflow: hidden;
            animation: fadeInUp 0.8s ease-out 0.4s both;
            box-shadow: 0 4px 20px rgba(0,0,0,0.2);
        }
        
        .card-header { 
            padding: 20px 28px; 
            background: rgba(255,255,255,0.03); 
            border-bottom: 1px solid var(--border); 
            font-weight: 600; 
            font-size: 1.1rem;
            display: flex; 
            align-items: center; 
            gap: 14px; 
        }
        
        .card-body { 
            padding: 32px 28px; 
            line-height: 1.7; 
            font-size: 1.05rem;
            color: #d1d5db;
        }

        /* Lists and Pills */
        .pill-list {
            display: flex;
            flex-wrap: wrap;
            gap: 12px;
            margin-top: 10px;
        }
        .pill {
            padding: 8px 16px;
            border-radius: 30px;
            font-size: 0.9rem;
            font-weight: 500;
            display: inline-flex;
            align-items: center;
            gap: 8px;
            border: 1px solid var(--border);
            background: rgba(255,255,255,0.05);
            transition: all 0.2s ease;
        }
        .pill:hover { background: rgba(255,255,255,0.1); transform: scale(1.02); }
        .pill.danger { color: #fca5a5; border-color: rgba(239, 68, 68, 0.4); background: rgba(239, 68, 68, 0.1); }
        .pill.warning { color: #fde047; border-color: rgba(245, 158, 11, 0.4); background: rgba(245, 158, 11, 0.1); }
        .pill.success { color: #86efac; border-color: rgba(16, 185, 129, 0.4); background: rgba(16, 185, 129, 0.1); }

        .list-item-ul {
            list-style: none;
            padding: 0;
            margin: 10px 0;
        }
        .list-item-li {
            padding: 12px 16px;
            margin-bottom: 8px;
            background: rgba(0,0,0,0.3);
            border-radius: 8px;
            border-left: 4px solid var(--accent);
            display: flex;
            gap: 12px;
        }

        /* Large Status Indicators */
        .status-hero {
            display: flex;
            align-items: center;
            gap: 20px;
            font-size: 1.5rem;
            font-weight: 600;
        }
        .status-hero i.fa-check-circle { color: var(--success); font-size: 3rem; text-shadow: 0 0 20px rgba(16, 185, 129, 0.5); }
        .status-hero i.fa-times-circle { color: var(--danger); font-size: 3rem; text-shadow: 0 0 20px rgba(239, 68, 68, 0.5); }
        
        .code-block { 
            background: #09090b; 
            border: 1px solid var(--border); 
            border-radius: 12px; 
            margin: 24px 0 10px 0; 
            overflow: hidden; 
            box-shadow: 0 10px 30px rgba(0,0,0,0.5);
        }
        
        .code-top { 
            background: #18181b; 
            padding: 12px 20px; 
            display: flex; 
            justify-content: space-between; 
            align-items: center;
            font-size: 0.8rem; 
            font-weight: 500;
            color: var(--text-muted); 
            border-bottom: 1px solid var(--border);
        }
        
        pre { margin: 0; padding: 24px; overflow-x: auto; }
        code { font-family: 'JetBrains Mono', monospace; font-size: 0.9rem; line-height: 1.6; }
        
        .copy-btn { 
            background: rgba(255,255,255,0.05); 
            border: 1px solid rgba(255,255,255,0.1); 
            color: #d1d5db; 
            cursor: pointer; 
            padding: 6px 12px;
            border-radius: 6px;
            font-family: inherit;
            font-size: 0.8rem;
            transition: all 0.2s ease;
            display: flex; align-items: center; gap: 6px;
        }
        .copy-btn:hover { background: rgba(255,255,255,0.1); color: #fff; }

        @keyframes fadeInDown {
            from { opacity: 0; transform: translateY(-20px); }
            to { opacity: 1; transform: translateY(0); }
        }
        @keyframes fadeInUp {
            from { opacity: 0; transform: translateY(30px); }
            to { opacity: 1; transform: translateY(0); }
        }
    </style>
</head>
<body>
    <div class="sidebar">
        <div class="logo">
            <i class="fas fa-layer-group" style="font-size: 1.5rem;"></i> 
            Dashboard Pro
        </div>
        ${sidebarHtml}
    </div>
    <div class="main">
        <h1>${title}</h1>
        <div class="summary-grid">${summaryHtml}</div>
        <div class="sections">${sectionsHtml}</div>
    </div>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/highlight.js/11.8.0/highlight.min.js"></script>
    <script>
        hljs.configure({ ignoreUnescapedHTML: true });
        hljs.highlightAll();
        function copyCode(id, btnId) {
            const code = document.getElementById(id).innerText;
            navigator.clipboard.writeText(code);
            const btn = document.getElementById(btnId);
            const originalHtml = btn.innerHTML;
            btn.innerHTML = '<i class="fas fa-check" style="color:#10b981;"></i> Copied!';
            btn.style.borderColor = '#10b981';
            setTimeout(() => {
                btn.innerHTML = originalHtml;
                btn.style.borderColor = 'rgba(255,255,255,0.1)';
            }, 2000);
        }
    </script>
</body>
</html>`;
}

function formatResultToDashboard(result: any): any {
    let sections: any[] = [];
    let summaries: any[] = [];
    
    if (typeof result === 'string') {
        try { result = JSON.parse(result); } 
        catch (e) { 
            return { sectionsHtml: `<div class="card"><div class="card-body">${result}</div></div>`, sidebarHtml: '', summaryHtml: '' }; 
        }
    }

    // Determine Agent Type based on output keys
    let agentType = "Unknown Agent";
    if (result.root_cause || result.fixed_code || result.line_edits || result.replacements) agentType = "Debugger Professional";
    else if (result.test_plan || result.test_code) agentType = "Test Engineer";
    else agentType = "Integrity Architect";

    summaries.push({ l: "Active Agent", v: agentType });

    // --- Dynamic Section Parsing ---

    // 1. Text Explanations
    if (result.root_cause) sections.push({ id: "desc", t: "Root Cause Analysis", i: "fas fa-search-plus", c: `<p>${result.root_cause}</p>` });
    if (result.test_plan) sections.push({ id: "plan", t: "Test Strategy", i: "fas fa-bullseye", c: `<p>${result.test_plan}</p>` });
    if (result.code_explanation) sections.push({ id: "exp", t: "Code Analysis", i: "fas fa-microscope", c: `<p>${result.code_explanation}</p>` });

    // 2. Boolean Results (Testing)
    if (result.tests_passed !== undefined) {
        let isPassed = result.tests_passed;
        summaries.push({ l: "Suite Status", v: isPassed ? "<span style='color:var(--success)'>PASSED</span>" : "<span style='color:var(--danger)'>FAILED</span>" });
        sections.push({ 
            id: "status", t: "Execution Results", i: "fas fa-flask", 
            c: `<div class="status-hero">
                  <i class="fas ${isPassed ? 'fa-check-circle' : 'fa-times-circle'}"></i> 
                  <span>Tests have ${isPassed ? 'successfully passed' : 'failed'} execution.</span>
                </div>` 
        });
    }

    // 3. Simple Lists (Alerting/Styling dynamic)
    const renderList = (arr: string[], pillClass: string, icon: string) => {
        if (!arr || arr.length === 0) return "";
        return `<div class="pill-list">` + arr.map(a => `<div class="pill ${pillClass}"><i class="${icon}"></i> ${a}</div>`).join('') + `</div>`;
    };

    if (result.security_issues?.length) sections.push({ id: "sec", t: "Security Vulnerabilities", i: "fas fa-shield-virus", color: "var(--danger)", c: renderList(result.security_issues, "danger", "fas fa-bug") });
    if (result.style_violations?.length) sections.push({ id: "style", t: "Style Violations", i: "fas fa-paint-roller", color: "var(--warning)", c: renderList(result.style_violations, "warning", "fas fa-exclamation-triangle") });
    if (result.breakpoints?.length) sections.push({ id: "bp", t: "Suggested Breakpoints", i: "fas fa-stop-circle", c: renderList(result.breakpoints, "warning", "fas fa-stop-circle") });
    
    // 4. Complex Lists (Refactoring/Suggestions)
    const renderItems = (arr: string[]) => {
        if (!arr || arr.length === 0) return "";
        return `<ul class="list-item-ul">` + arr.map(a => `<li class="list-item-li"><i class="fas fa-caret-right" style="color:var(--accent);margin-top:4px;"></i> <div>${a}</div></li>`).join('') + `</ul>`;
    }
    if (result.performance_suggestions?.length) sections.push({ id: "perf", t: "Performance Improvements", i: "fas fa-tachometer-alt", c: renderItems(result.performance_suggestions) });
    if (result.refactoring_suggestions?.length) sections.push({ id: "refact", t: "Refactoring Ideas", i: "fas fa-recycle", c: renderItems(result.refactoring_suggestions) });

    // 5. Advanced Edit Blocks (Line Edits / Replacements)
    if (result.line_edits?.length) {
        let editsHtml = result.line_edits.map((edit: any) => `
            <div style="background:rgba(0,0,0,0.5); border:1px solid var(--border); border-radius:8px; margin-bottom:16px; overflow:hidden;">
              <div style="padding:10px 16px; background:rgba(255,255,255,0.05); border-bottom:1px solid var(--border); font-family:'JetBrains Mono'; font-size:0.85rem; color:var(--warning);">
                <i class="fas fa-exchange-alt"></i> Lines ${edit.start_line} to ${edit.end_line}
              </div>
              <div style="padding:16px;">${renderCode("python", edit.replacement)}</div>
            </div>
        `).join('');
        sections.push({ id: "linedits", t: "Targeted Line Patches", i: "fas fa-stream", c: editsHtml });
    }

    if (result.replacements?.length) {
        let repsHtml = result.replacements.map((rep: any) => `
            <div style="display:flex; gap:16px; margin-bottom:24px;">
              <div style="flex:1;">
                <div style="color:var(--danger); margin-bottom:8px; font-weight:600;"><i class="fas fa-minus-circle"></i> Original</div>
                ${renderCode("python", rep.search)}
              </div>
              <div style="flex:1;">
                <div style="color:var(--success); margin-bottom:8px; font-weight:600;"><i class="fas fa-plus-circle"></i> Replacement</div>
                ${renderCode("python", rep.replace)}
              </div>
            </div>
        `).join('');
        sections.push({ id: "reps", t: "Search & Replace Blocks", i: "fas fa-random", c: repsHtml });
    }

    // 6. Code Blocks & Terminal Outputs
    if (result.fixed_code) sections.push({ id: "code", t: "Final Reconstructed Code", i: "fas fa-code", c: renderCode("python", result.fixed_code) });
    if (result.suggested_code) sections.push({ id: "code", t: "Refactored Suggestion", i: "fas fa-magic", c: renderCode("python", result.suggested_code) });
    if (result.test_code) sections.push({ id: "code", t: "Automated Suite Code", i: "fas fa-microscope", c: renderCode("python", result.test_code) });
    if (result.test_results) sections.push({ id: "stdout", t: "Terminal Output", i: "fas fa-terminal", c: renderCode("bash", result.test_results) });

    // Aggregate Summary Metric
    let itemsFound = (result.security_issues?.length || 0) + (result.style_violations?.length || 0) + (result.performance_suggestions?.length || 0) + (result.refactoring_suggestions?.length || 0);
    if (itemsFound > 0) summaries.push({ l: "Items Flagged", v: `<span style="color:var(--warning)">${itemsFound} Found</span>` });

    return {
        sidebarHtml: sections.map(s => `<a href="#${s.id}" class="nav-link"><i class="${s.i}" style="width:20px; text-align:center;"></i> ${s.t}</a>`).join(''),
        summaryHtml: summaries.map(s => `
            <div class="summary-box">
                <div style="font-size: 0.75rem; color: var(--text-muted); text-transform: uppercase; font-weight:600; letter-spacing:1px; margin-bottom:8px;">${s.l}</div>
                <div style="font-weight: 700; font-size: 1.4rem; letter-spacing:-0.5px;">${s.v}</div>
            </div>`).join(''),
        sectionsHtml: sections.map(s => `
            <div class="card" id="${s.id}">
                <div class="card-header">
                    <i class="${s.i}" style="color: ${s.color || 'var(--accent)'}; font-size:1.2rem;"></i> ${s.t}
                </div>
                <div class="card-body">${s.c}</div>
            </div>`).join('')
    };
}

let codeCount = 0;
function renderCode(lang: string, code: string): string {
    if (!code) return "";
    const id = `c-${codeCount++}`;
    const btnId = `b-${codeCount}`;
    const clean = code.replace(/```python\n?|```/g, '').trim();
    return `
    <div class="code-block">
        <div class="code-top"><span>${lang.toUpperCase()}</span><button class="copy-btn" id="${btnId}" onclick="copyCode('${id}', '${btnId}')"><i class="far fa-copy"></i> Copy</button></div>
        <pre><code id="${id}" class="language-${lang}">${clean.replace(/&/g, "&amp;").replace(/</g, "&lt;").replace(/>/g, "&gt;")}</code></pre>
    </div>`;
}

function handleError(e: any) { vscode.window.showErrorMessage(`AI SE Error: ${e.message}`); }
export function deactivate() { if (serverProcess) serverProcess.kill(); }
