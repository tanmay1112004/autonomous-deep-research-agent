"""
Autonomous Deep Research Agent
Uses LangGraph workflow with reflection loop for quality research reports
"""

import os
from datetime import datetime
from typing import TypedDict, Annotated, List, Literal
import operator

import streamlit as st
from langchain_google_genai import ChatGoogleGenerativeAI
from langgraph.graph import StateGraph, END
from tavily import TavilyClient


# ============================================================================
# YOUR API KEYS (Directly embedded - works immediately)
# ============================================================================

GEMINI_API_KEY = "gemini_api_key"
TAVILY_API_KEY = ""
GEMINI_MODEL = "gemini-2.5-flash"


# ============================================================================
# STATE DEFINITION
# ============================================================================

class ResearchState(TypedDict):
    """State maintained throughout the research workflow"""
    topic: str
    sources: Annotated[List[dict], operator.add]
    draft_report: str
    critique: str
    final_report: str
    iteration: int
    max_iterations: int


# ============================================================================
# RESEARCH AGENT CLASS
# ============================================================================

class ResearchAgent:
    """Multi-agent research system with search, synthesis, critique, and revision"""
    
    def __init__(self):
        """Initialize LLM and search client with hardcoded API keys"""
        self.llm = ChatGoogleGenerativeAI(
            model=GEMINI_MODEL,
            google_api_key=GEMINI_API_KEY,
            temperature=0.2,
            top_p=0.95,
        )
        self.tavily = TavilyClient(api_key=TAVILY_API_KEY)
    
    def search_node(self, state: ResearchState) -> dict:
        """Phase 1: Search web for relevant information"""
        topic = state["topic"]
        
        try:
            results = self.tavily.search(
                query=topic,
                search_depth="advanced",
                max_results=10
            )
            
            sources = []
            for result in results.get("results", []):
                sources.append({
                    "title": result.get("title"),
                    "url": result.get("url"),
                    "content": result.get("content"),
                    "score": result.get("score")
                })
            
            return {"sources": sources}
            
        except Exception as e:
            st.error(f"Search error: {str(e)}")
            return {"sources": []}
    
    def synthesize_node(self, state: ResearchState) -> dict:
        """Phase 2: Create initial draft from search results"""
        topic = state["topic"]
        sources = state["sources"]
        
        if not sources:
            return {"draft_report": "No information found for this topic."}
        
        # Format sources for LLM
        source_text = self._format_sources(sources)
        
        prompt = f"""You are a research assistant. Create a comprehensive research report on: {topic}

Based on the following sources (note: they may contain contradictory information):

{source_text}

Requirements:
1. Identify and address contradictory information explicitly
2. Cite sources as [Source X] in the text
3. Organize with clear sections:
   - Executive Summary
   - Key Findings
   - Contradictions Analysis
   - Conclusion
   - Further Research Needed
4. Be objective and factual
5. Include specific dates and statistics where available

Generate the full research report:
"""
        
        try:
            response = self.llm.invoke(prompt)
            return {
                "draft_report": response.content,
                "iteration": state.get("iteration", 0) + 1
            }
        except Exception as e:
            return {"draft_report": f"Error generating report: {str(e)}"}
    
    def critique_node(self, state: ResearchState) -> dict:
        """Phase 3: Self-critique the draft for gaps and improvements"""
        draft = state["draft_report"]
        topic = state["topic"]
        
        prompt = f"""You are a critical peer reviewer. Evaluate this research report on "{topic}":

REPORT:
{draft}

Provide a structured critique covering:
1. Missing information or gaps (be specific)
2. Unresolved contradictions
3. Weakly supported claims (which need more evidence)
4. Suggestions for improvement (actionable)
5. Overall quality score (1-10)

Format as clear bullet points. Be constructive and specific.
"""
        
        try:
            response = self.llm.invoke(prompt)
            return {"critique": response.content}
        except Exception as e:
            return {"critique": f"Critique error: {str(e)}"}
    
    def revise_node(self, state: ResearchState) -> dict:
        """Phase 4: Revise the report based on critique"""
        draft = state["draft_report"]
        critique = state["critique"]
        topic = state["topic"]
        sources = state["sources"]
        
        source_citations = self._format_source_citations(sources)
        
        prompt = f"""You are a researcher revising a report based on peer feedback.

TOPIC: {topic}

CURRENT DRAFT:
{draft}

PEER CRITIQUE:
{critique}

SOURCES USED:
{source_citations}

Revise the report to address all critique points. 
- Maintain professional tone and citations [Source X]
- If critique suggests missing information, note what additional research would verify it
- Strengthen weak claims with better evidence from sources
- Resolve or explicitly note contradictions

Produce the final, polished report:
"""
        
        try:
            response = self.llm.invoke(prompt)
            return {"final_report": response.content}
        except Exception as e:
            return {"final_report": f"Revision error: {str(e)}\n\nOriginal draft:\n{draft}"}
    
    def should_continue(self, state: ResearchState) -> Literal["critique", "revise", "end"]:
        """Decision logic for reflection loop"""
        iteration = state.get("iteration", 0)
        max_iter = state.get("max_iterations", 2)
        
        if iteration >= max_iter:
            return "end"
        elif "draft_report" in state and "critique" not in state:
            return "critique"
        elif "critique" in state and "final_report" not in state:
            return "revise"
        else:
            return "end"
    
    # ------------------------------------------------------------------------
    # Helper Methods
    # ------------------------------------------------------------------------
    
    def _format_sources(self, sources: List[dict]) -> str:
        """Format sources for LLM consumption"""
        formatted = []
        for i, src in enumerate(sources[:8]):
            formatted.append(
                f"SOURCE {i+1} ({src['title']} - {src['url']}):\n{src['content'][:1500]}"
            )
        return "\n\n".join(formatted)
    
    def _format_source_citations(self, sources: List[dict]) -> str:
        """Format source citations for revision phase"""
        citations = []
        for i, src in enumerate(sources[:5]):
            citations.append(f"- [{i+1}] {src['title']}: {src['url']}")
        return "\n".join(citations)


# ============================================================================
# GRAPH CONSTRUCTION
# ============================================================================

def build_research_graph(agent: ResearchAgent):
    """Build the LangGraph workflow"""
    workflow = StateGraph(ResearchState)
    
    # Add nodes
    workflow.add_node("search", agent.search_node)
    workflow.add_node("synthesize", agent.synthesize_node)
    workflow.add_node("critique", agent.critique_node)
    workflow.add_node("revise", agent.revise_node)
    
    # Define flow
    workflow.set_entry_point("search")
    workflow.add_edge("search", "synthesize")
    
    # Conditional edges for reflection loop
    workflow.add_conditional_edges(
        "synthesize",
        agent.should_continue,
        {
            "critique": "critique",
            "revise": "revise",
            "end": END
        }
    )
    workflow.add_conditional_edges(
        "critique",
        agent.should_continue,
        {
            "revise": "revise",
            "end": END
        }
    )
    workflow.add_edge("revise", END)
    
    return workflow.compile()


# ============================================================================
# STREAMLIT UI
# ============================================================================

def main():
    """Main Streamlit application"""
    st.set_page_config(
        page_title="Deep Research Agent",
        page_icon="🔬",
        layout="wide",
        initial_sidebar_state="expanded"
    )
    
    st.title("🔬 Autonomous Deep Research Agent")
    st.caption("Powered by Gemini 2.0 Flash + Tavily Search + LangGraph Reflection Loop")
    
    # Sidebar configuration
    with st.sidebar:
        st.header("⚙️ Configuration")
        
        # Show API status
        st.success("✅ API Keys Configured")
        st.info(f"📡 Model: {GEMINI_MODEL}")
        
        st.markdown("---")
        st.markdown("### 🧠 Research Process")
        st.markdown("""
        1. **Search** - Web crawling via Tavily
        2. **Synthesize** - Initial draft creation
        3. **Critique** - Self-reflection on gaps
        4. **Revise** - Quality improvement
        5. **Loop** - Multiple iterations for quality
        """)
        
        st.markdown("---")
        iterations = st.slider(
            "Reflection Iterations",
            min_value=1,
            max_value=3,
            value=2,
            help="More iterations = higher quality but slower"
        )
        
        if st.button("🔄 Reset Session"):
            st.cache_data.clear()
            st.rerun()
    
    # Topic input
    st.markdown("### 📝 Research Topic")
    topic = st.text_area(
        "Enter your research question or topic",
        placeholder="Example: 'Compare the latest advancements in quantum computing: superconducting qubits vs trapped ions - commercial applications 2025'",
        height=100,
        label_visibility="collapsed"
    )
    
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        start_button = st.button("🚀 Start Deep Research", type="primary", use_container_width=True)
    
    if start_button:
        if not topic.strip():
            st.error("❌ Please enter a research topic")
            return
        
        # Initialize and run
        with st.spinner("Initializing research agent..."):
            agent = ResearchAgent()
            graph = build_research_graph(agent)
        
        initial_state = {
            "topic": topic,
            "sources": [],
            "draft_report": "",
            "critique": "",
            "final_report": "",
            "iteration": 0,
            "max_iterations": iterations
        }
        
        # Progress tracking
        progress_bar = st.progress(0)
        status_text = st.empty()
        output_container = st.container()
        
        final_report = None
        total_steps = 3 + (iterations * 2)
        current_step = 0
        
        for output in graph.stream(initial_state):
            current_step += 1
            progress_bar.progress(current_step / total_steps)
            
            if "search" in output:
                status_text.info("🔍 Phase 1: Searching web sources...")
                num_sources = len(output["search"].get("sources", []))
                st.success(f"✅ Found {num_sources} relevant sources")
                
            elif "synthesize" in output:
                status_text.info("📝 Phase 2: Synthesizing research...")
                with output_container.expander("📄 Initial Draft", expanded=False):
                    st.markdown(output["synthesize"]["draft_report"])
                    
            elif "critique" in output:
                status_text.info("🔎 Phase 3: Critical analysis in progress...")
                with output_container.expander("📋 Peer Critique", expanded=False):
                    st.markdown(output["critique"]["critique"])
                    
            elif "revise" in output:
                status_text.info("✏️ Phase 4: Refining and improving...")
                final_report = output["revise"]["final_report"]
                with output_container.expander("📊 Final Research Report", expanded=True):
                    st.markdown(final_report)
        
        # Completion
        progress_bar.progress(1.0)
        status_text.success("✅ Research Complete!")
        
        # Export options
        if final_report:
            st.markdown("---")
            col1, col2, col3 = st.columns(3)
            
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            
            with col1:
                st.download_button(
                    label="📥 Download Markdown",
                    data=final_report,
                    file_name=f"research_report_{timestamp}.md",
                    mime="text/markdown"
                )
            
            with col2:
                st.download_button(
                    label="📄 Download Text",
                    data=final_report,
                    file_name=f"research_report_{timestamp}.txt",
                    mime="text/plain"
                )
            
            with col3:
                st.success("✅ Report Ready!")
    
    else:
        # Show example topics
        with st.expander("💡 Example Research Topics", expanded=False):
            st.markdown("""
            - **Technology**: *"Compare GPT-4 vs Claude vs Gemini - capabilities, pricing, and use cases 2025"*
            - **Science**: *"Latest breakthroughs in nuclear fusion: practical timeline and commercial challenges"*
            - **Business**: *"AI agent market analysis: trends, key players, and predictions for 2025-2026"*
            - **Health**: *"CRISPR gene editing: current clinical applications, successes, and ethical considerations"*
            - **Energy**: *"Solid-state batteries vs lithium-ion: technical progress and commercialization status"*
            """)


# ============================================================================
# ENTRY POINT
# ============================================================================

if __name__ == "__main__":
    main()