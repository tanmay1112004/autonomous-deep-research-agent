# README.md

```markdown
# 🔬 Autonomous Deep Research Agent

An intelligent multi-agent research system that autonomously browses the web, synthesizes information, self-critiques, and produces high-quality research reports with source citations.

![Python Version](https://img.shields.io/badge/python-3.12+-blue.svg)
![Streamlit](https://img.shields.io/badge/streamlit-1.35.0-red.svg)
![LangGraph](https://img.shields.io/badge/langgraph-0.2.16-green.svg)
![License](https://img.shields.io/badge/license-MIT-blue.svg)

## 🎯 Features

- **🤖 Multi-Agent Architecture**: Search, Synthesize, Critique, and Revise agents working in harmony
- **🔄 Reflection Loop**: Self-critique mechanism that iteratively improves report quality
- **🔍 Real-time Web Search**: Powered by Tavily API for up-to-date information
- **🧠 Advanced LLM**: Built on Google's Gemini 2.0 Flash model
- **📊 Source Citations**: Every claim cites its source with URLs
- **🎨 Streamlit UI**: Beautiful, interactive web interface
- **📥 Export Options**: Download reports as Markdown or plain text
- **⚠️ Contradiction Handling**: Explicitly identifies and addresses conflicting information

## 🏗️ Architecture

```
┌─────────────┐
│   Search    │ → Web crawling via Tavily API
└──────┬──────┘
       ↓
┌─────────────┐
│ Synthesize  │ → Initial draft with citations
└──────┬──────┘
       ↓
┌─────────────┐
│  Critique   │ → Self-reflection on gaps & contradictions
└──────┬──────┘
       ↓
┌─────────────┐
│   Revise    │ → Quality improvement based on feedback
└──────┬──────┘
       ↓
   [LOOP] ←────┘ (Multiple iterations for quality)
```

## 📋 Prerequisites

- Python 3.12 or higher
- API Keys:
  - **Gemini API Key** from [Google AI Studio](https://aistudio.google.com/app/apikey)
  - **Tavily API Key** from [Tavily](https://app.tavily.com/) (free tier available)

## 🚀 Quick Start

### 1. Clone the Repository

```bash
git clone https://github.com/yourusername/deep-research-agent.git
cd deep-research-agent
```

### 2. Create Virtual Environment

```bash
# Windows
python -m venv venv
venv\Scripts\activate

# Mac/Linux
python3 -m venv venv
source venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure API Keys

Open `research_agent.py` and replace the API keys with your own:

```python
GEMINI_API_KEY = "your-gemini-api-key-here"
TAVILY_API_KEY = "your-tavily-api-key-here"
```

### 5. Run the Application

#### Streamlit Web Interface (Recommended)

```bash
streamlit run research_agent.py
```

Then open your browser to `http://localhost:8501`

#### Command Line Interface

```bash
python -c "from research_agent import run_research_cli; run_research_cli()"
```

## 📖 Usage Guide

### Streamlit UI Mode

1. **Enter Research Topic**: Type your research question or topic
2. **Set Reflection Loops**: Choose 1-3 iterations (more = higher quality)
3. **Click Start**: Watch the research process unfold in real-time
4. **Review Output**: 
   - Initial Draft
   - Peer Critique
   - Final Report
5. **Download**: Save your report as Markdown or text

### Example Topics

Try these research questions:

- **Technology**: *"Compare GPT-4 vs Claude vs Gemini - capabilities, pricing, and use cases 2025"*
- **Science**: *"Latest breakthroughs in nuclear fusion: practical timeline and commercial challenges"*
- **Business**: *"AI agent market analysis: trends, key players, and predictions for 2025-2026"*
- **Health**: *"CRISPR gene editing: current clinical applications, successes, and ethical considerations"*
- **Energy**: *"Solid-state batteries vs lithium-ion: technical progress and commercialization status"*

## 📁 Project Structure

```
deep-research-agent/
├── research_agent.py      # Main application code
├── requirements.txt       # Python dependencies
├── README.md             # This file
└── research_reports/     # Generated reports (auto-created)
```

## 🧠 How It Works

### Phase 1: Search
The agent uses Tavily API to search the web for relevant, up-to-date information on your topic. It collects up to 10 high-quality sources.

### Phase 2: Synthesize
The Gemini LLM analyzes all sources and creates a comprehensive draft report with:
- Executive Summary
- Key Findings
- Contradictions Analysis
- Conclusion
- Further Research Needs

### Phase 3: Critique
The agent critically evaluates its own draft, identifying:
- Information gaps
- Unresolved contradictions
- Weakly supported claims
- Improvement suggestions

### Phase 4: Revise
Based on the critique, the agent produces an improved final report with stronger evidence and better organization.

### Reflection Loop
The critique-revise cycle repeats for multiple iterations (configurable), each time improving quality.

## 🛠️ Technical Stack

| Component | Technology |
|-----------|------------|
| LLM | Google Gemini 2.0 Flash |
| Search | Tavily API |
| Workflow | LangGraph |
| UI | Streamlit |
| Language | Python 3.12+ |

## 📊 Sample Output

The agent produces reports with:

```
# Research Report: [Your Topic]

**Generated:** 2025-01-15 14:30:22
**Reflection Loops:** 2

---

## Executive Summary
[Comprehensive overview with key findings]

## Key Findings
1. Finding 1 [Source 1]
2. Finding 2 [Source 3]

## Contradictions Analysis
- Source 2 claims X, while Source 5 suggests Y...

## Conclusion
[Synthesized conclusions with citations]

## Further Research Needed
[Gaps requiring additional investigation]
```

## 🔧 Configuration

Modify the constants in `research_agent.py`:

```python
GEMINI_MODEL = "gemini-2.0-flash-exp"  # Change Gemini model
MAX_SEARCH_RESULTS = 10                 # Number of sources to fetch
SEARCH_DEPTH = "advanced"               # "basic" or "advanced"
```

## 🐛 Troubleshooting

### Issue: "Missing API Keys"
**Solution**: Verify API keys in `research_agent.py` are correct and active.

### Issue: "Model not found"
**Solution**: Update `GEMINI_MODEL` to an available model like `gemini-2.0-flash-exp` or `gemini-pro`.

### Issue: No search results
**Solution**: Broaden your topic or check Tavily API quota.

### Issue: Slow performance
**Solution**: Reduce reflection loops to 1 or use "basic" search depth.

## 📈 Performance Tips

1. **For Quick Answers**: Use 1 reflection loop
2. **For Balanced Quality**: Use 2 reflection loops (default)
3. **For Deep Research**: Use 3 reflection loops
4. **Broad Topics**: Get better results than narrow ones
5. **Recent Topics**: Work best (post-2023)

## 🤝 Contributing

Contributions are welcome! Please:

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Open a Pull Request

## 📝 License

This project is licensed under the MIT License - see below:

```
MIT License

Copyright (c) 2025 Deep Research Agent

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions...

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.
```

## 🙏 Acknowledgments

- [Google Gemini](https://deepmind.google/technologies/gemini/) for LLM capabilities
- [Tavily](https://tavily.com/) for search API
- [LangChain](https://www.langchain.com/) for LangGraph framework
- [Streamlit](https://streamlit.io/) for beautiful UI

## 📧 Contact

For questions or support:
- Open an issue on GitHub
- Email: your-email@example.com

## 🌟 Star History

If you find this useful, please star the repository! ⭐

---

**Built with ❤️ for researchers, students, and knowledge seekers**
```

---

## Optional: Create a `.gitignore` file

```gitignore
# Python
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
venv/
env/
ENV/
.venv

# Streamlit
.streamlit/secrets.toml

# Reports
research_report_*.md
research_report_*.txt
*.md
!README.md

# IDE
.vscode/
.idea/
*.swp
*.swo

# OS
.DS_Store
Thumbs.db

# Logs
*.log
```

---

## Quick Setup Commands (Copy-Paste)

```bash
# 1. Create project
mkdir deep_research_agent && cd deep_research_agent

# 2. Create files
cat > requirements.txt << 'EOF'
streamlit==1.35.0
langgraph==0.2.16
langchain==0.3.0
langchain-google-genai==1.0.10
tavily-python==0.5.0
pydantic==2.9.2
EOF

# 3. Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# 4. Install packages
pip install -r requirements.txt

# 5. Create research_agent.py (copy the code from previous message)

# 6. Run the app
streamlit run research_agent.py
```

