from enum import Enum
from dataclasses import dataclass, field, asdict
from typing import Callable, Any, Optional
from pathlib import Path
import time
import json

from rag_pipeline import (
    load_documents,
    create_chunks,
    build_embeddings,
    build_faiss_index,
    retrieve,
)


class ToolName(Enum):
    RETRIEVAL = "retrieval"
    SUMMARIZE = "summarize"


@dataclass
class ToolResult:
    tool: ToolName
    success: bool
    output: Any
    duration_ms: float
    error: Optional[str] = None


@dataclass
class Tool:
    name: ToolName
    description: str
    function: Callable[[str], Any]

    def execute(self, input_text: str) -> ToolResult:
        start = time.time()
        try:
            output = self.function(input_text)
            duration = (time.time() - start) * 1000
            return ToolResult(self.name, True, output, duration)
        except Exception as e:
            duration = (time.time() - start) * 1000
            return ToolResult(self.name, False, None, duration, str(e))


@dataclass
class AgentTrace:
    query: str
    steps: list = field(default_factory=list)
    final_answer: Optional[str] = None

    def add_step(self, step_type: str, content: dict):
        self.steps.append({
            "step_number": len(self.steps) + 1,
            "type": step_type,
            "content": content
        })


class RetrievalTool:
    def __init__(self):
        documents = load_documents(Path("data"))
        chunks = create_chunks(documents)
        self.model, embeddings = build_embeddings(chunks)
        self.index = build_faiss_index(embeddings)
        self.chunks = chunks

    def __call__(self, query: str) -> dict:
        results, latency = retrieve(query, self.model, self.index, self.chunks, k=3)

        return {
            "query": query,
            "sources": [r["source"] for r in results],
            "chunks": [r["content"] for r in results],
            "latency_ms": latency
        }

    @property
    def description(self) -> str:
        return "Use this tool to search for information from documents."


class SummarizeTool:
    def __init__(self):
        self.last_context = None

    def set_context(self, text: str):
        self.last_context = text

    def __call__(self, instruction: str) -> dict:
        if not self.last_context:
            return {
                "summary": "No content available to summarize. Retrieve information first.",
                "success": False
            }

        short_summary = self.last_context[:300].replace("\n", " ")

        return {
            "summary": f"Summary based on retrieved context: {short_summary}...",
            "success": True
        }

    @property
    def description(self) -> str:
        return "Use this tool to summarize previously retrieved information."


class SimpleAgent:
    def __init__(self, retrieval_tool: Tool, summarize_tool: Tool, summarize_function):
        self.retrieval_tool = retrieval_tool
        self.summarize_tool = summarize_tool
        self.summarize_function = summarize_function

    def route_query(self, query: str) -> tuple[ToolName, str]:
        q = query.lower()
        summary_keywords = ["summarize", "summary", "brief", "key points", "overview", "tldr"]

        for word in summary_keywords:
            if word in q:
                return ToolName.SUMMARIZE, f"Detected summarization keyword: '{word}'"

        return ToolName.RETRIEVAL, "Defaulted to retrieval for information-seeking query"

    def run(self, query: str) -> tuple[str, AgentTrace]:
        trace = AgentTrace(query=query)

        trace.add_step("thought", {
            "reasoning": f"Analyzing query: {query}"
        })

        selected_tool, reasoning = self.route_query(query)

        trace.add_step("routing", {
            "decision": selected_tool.value,
            "reasoning": reasoning
        })

        if selected_tool == ToolName.RETRIEVAL:
            result = self.retrieval_tool.execute(query)
            trace.add_step("action", {
                "tool": selected_tool.value,
                "success": result.success,
                "sources": result.output["sources"] if result.success else [],
                "duration_ms": result.duration_ms
            })

            if result.success:
                combined_context = "\n".join(result.output["chunks"])
                self.summarize_function.set_context(combined_context)
                final_answer = f"Retrieved sources: {result.output['sources']}"
            else:
                final_answer = f"Retrieval failed: {result.error}"

        else:
            result = self.summarize_tool.execute(query)
            trace.add_step("action", {
                "tool": selected_tool.value,
                "success": result.success,
                "duration_ms": result.duration_ms
            })

            if result.success:
                final_answer = result.output["summary"]
            else:
                final_answer = result.output["summary"]

        trace.final_answer = final_answer
        trace.add_step("answer", {
            "final_answer": final_answer
        })

        return final_answer, trace


def save_trace(trace: AgentTrace, trace_num: int, output_dir: Path):
    output_dir.mkdir(exist_ok=True)

    output_path = output_dir / f"trace_{trace_num:02d}.json"
    output_path.write_text(json.dumps(asdict(trace), indent=2), encoding="utf-8")


def main():
    retrieval_impl = RetrievalTool()
    summarize_impl = SummarizeTool()

    retrieval_tool = Tool(
        name=ToolName.RETRIEVAL,
        description=retrieval_impl.description,
        function=retrieval_impl
    )

    summarize_tool = Tool(
        name=ToolName.SUMMARIZE,
        description=summarize_impl.description,
        function=summarize_impl
    )

    agent = SimpleAgent(retrieval_tool, summarize_tool, summarize_impl)

    evaluation_tasks = [
        "What is RAG?",
        "What is the role of a vector database?",
        "How do embeddings help retrieval?",
        "What does grounding mean in RAG?",
        "What are the main steps in a RAG pipeline?",
        "Summarize the key points",
        "Give me a brief overview",
        "Provide a summary",
        "What happens if retrieval returns irrelevant chunks?",
        "Summarize the previous information"
    ]

    output_dir = Path("agent_traces")

    print("=" * 60)
    print("RUNNING AGENT EVALUATION")
    print("=" * 60)

    for i, query in enumerate(evaluation_tasks, start=1):
        answer, trace = agent.run(query)
        save_trace(trace, i, output_dir)

        print(f"Task {i}: {query}")
        print(f"Final answer: {answer[:120]}...")
        print("-" * 60)

    print(f"\nSaved {len(evaluation_tasks)} traces to: {output_dir}")
    print("Agent Step 5 complete: 10 traces saved successfully.")


if __name__ == "__main__":
    main()