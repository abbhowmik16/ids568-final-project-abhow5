# Milestone 6 Part 2: Agent Report
# 1. Overview

This report documents the Part 2 implementation of Milestone 6: a multi-tool agent controller that integrates retrieval as a decision-triggered tool.

The agent was built with two tools:
- **Retrieval tool**: searches the local document corpus using the RAG retrieval pipeline
- **Summarization tool**: summarizes previously retrieved context

The agent stores routing decisions and action traces for each evaluation task. Ten trace files were saved in the `agent_traces/` folder.

# 2. Tool Definitions
# Retrieval Tool
The retrieval tool wraps the RAG retrieval pipeline from Part 1. It:
- loads local documents
- chunks them
- builds embeddings
- indexes them in FAISS
- retrieves the top 3 most relevant chunks for a query

This tool is used when the user asks for factual information, explanation, or details from the document set.

# Summarization Tool
The summarization tool operates on previously retrieved context. It:
- receives context from the retrieval step
- stores it in memory
- returns a short summary of the stored context

This tool is used when the user asks for a summary, brief overview, or key points.

# 3. Tool Selection Policy
The agent uses a simple heuristic routing policy.

# Routing rules
1. **Summarization**
   - Trigger words include:
     - summarize
     - summary
     - brief
     - key points
     - overview
     - tldr
   - If one of these keywords appears in the user query, the agent routes to the summarization tool.

2. **Retrieval**
   - All other information-seeking queries default to the retrieval tool.

This policy was chosen because it is simple, transparent, and easy to trace.

# 4. Decision Transparency
Each agent run records a structured trace with:
- thought step
- routing decision
- action step
- final answer

This makes the decision process observable and auditable.

Each trace file includes:
- original query
- selected tool
- routing reason
- whether execution succeeded
- final answer

# 5. Evaluation Tasks
The following 10 tasks were used:

1. What is RAG?
2. What is the role of a vector database?
3. How do embeddings help retrieval?
4. What does grounding mean in RAG?
5. What are the main steps in a RAG pipeline?
6. Summarize the key points
7. Give me a brief overview
8. Provide a summary
9. What happens if retrieval returns irrelevant chunks?
10. Summarize the previous information

# 6. Tool Usage Summary
Tool usage across the 10 tasks:

- Retrieval tool used for 6 tasks
- Summarization tool used for 4 tasks

This demonstrates that the agent did not always choose retrieval. It used different tools depending on query intent.

# 7. Evaluation Results
The agent behaved as expected across the 10 tasks.

# Retrieval tasks
The retrieval tool was correctly selected for information-seeking questions such as:
- What is RAG?
- What is the role of a vector database?
- What does grounding mean in RAG?

The results showed relevant source files such as:
- `rag_basics.txt`
- `vector_databases.txt`
- `grounding_evaluation.txt`

# Summarization tasks
The summarization tool was correctly selected for summary-oriented prompts such as:
- Summarize the key points
- Give me a brief overview
- Provide a summary

These tasks used stored context from earlier retrieval steps.

# 8. Failure Case Analysis
The current agent has several limitations:

- Routing is keyword-based rather than LLM-based.
- Summarization depends on prior context being available.
- If the user asks for a summary before any retrieval, the summary tool returns a failure-style message.
- The final answer for retrieval tasks currently reports retrieved sources rather than a fully generated answer.
- The evaluation set is small and handcrafted.

These limitations make the system simple but not yet robust for open-ended real-world use.

# 9. Strengths
The current agent implementation demonstrates the key milestone requirements:
- retrieval is integrated as a callable tool
- there are at least two tools
- routing decisions are visible
- traces are saved for evaluation
- the system supports multi-step behavior by passing retrieval context into the summarizer

# 10. Conclusion
The Part 2 agent successfully implements a basic multi-tool architecture with observable decision-making. Retrieval and summarization were both integrated into the controller, and trace files were generated for 10 evaluation tasks.

The main strengths are transparency and reproducibility. The main areas for future improvement are more advanced routing logic, stronger summarization, and richer final answers for retrieval tasks.