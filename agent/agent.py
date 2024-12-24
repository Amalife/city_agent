from langgraph.graph import StateGraph, END
from typing_extensions import TypedDict
from agent.tools.tools import web_search_tool, question_router, generate_chain
from agent.logger.logger import app_logger

class GraphState(TypedDict):
    question: str
    documents: str
    generation: str

def web_search(state: GraphState):
    """
    Поиск в интернете, основанный на вопросе от пользователя
    """

    app_logger.info("Running web search")
    question = state["question"]

    # Web search
    docs = web_search_tool.invoke({"query": question})
    web_results = "\n".join([d["content"] for d in docs])
    app_logger.info("Found data: %s", web_results)
    return {"documents": web_results, "question": question}

def generate(state: GraphState):
    """
    Генерация ответа на вопрос
    """
    app_logger.info("Generation")
    question = state["question"]
    if state.get("documents"):
        documents = state["documents"]
    else:
        documents = "EMPTY"

    generation = generate_chain.invoke({"context": documents, "question": question})
    return {"documents": documents, "question": question, "generation": generation}

def route_question(state: GraphState):
    """
    Направление вопроса пользователя
    """
    app_logger.info("Routing")
    question = state["question"]
    app_logger.info("question %s", question)
    source = question_router.invoke({"question": question})
    app_logger.info("obtain source %s", source)
    if source == "web_search":
        app_logger.info("route question to web search")
        return "websearch"
    elif source == "generate":
        app_logger.info("route question to generation")
        return "generate"

workflow = StateGraph(GraphState)

workflow.add_node("generate", generate)
workflow.add_node("websearch", web_search)


workflow.add_edge("websearch", "generate")
workflow.add_edge("generate", END)

workflow.set_conditional_entry_point(
    route_question,
    {
        "websearch": "websearch",
        "generate": "generate",
    },
)

app = workflow.compile()