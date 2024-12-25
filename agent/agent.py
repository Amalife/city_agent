from langgraph.graph import StateGraph, END
from typing_extensions import TypedDict
from agent.tools.tools import web_search_tool, question_router, generate_chain
from agent.logger.logger import app_logger

# Состояние графа агента
class GraphState(TypedDict):
    # Вопрос пользователя 
    question: str
    # Информация, полученная от поисковика
    documents: str
    # Ответ агента
    generation: str

# Описание вершины графа поисковика
def web_search(state: GraphState):
    """
    Поиск в интернете, основанный на вопросе от пользователя
    """

    app_logger.info("Running web search")
    question = state["question"]

    # Получаем информацию из рузельтатов поиска
    docs = web_search_tool.invoke({"query": question})
    web_results = "\n".join([d["content"] for d in docs])
    app_logger.info("Found data: %s", web_results)
    # Обновляем состояние графа
    return {"documents": web_results, "question": question}

# Описание вершины графа генерации ответа
def generate(state: GraphState):
    """
    Генерация ответа на вопрос
    """
    app_logger.info("Generation")
    question = state["question"]
    # Если documents пустой, заполняем его словом EMPTY для промпта
    if state.get("documents"):
        documents = state["documents"]
    else:
        documents = "EMPTY"

    # Генерируем ответ от модели
    generation = generate_chain.invoke({"context": documents, "question": question})
    # Обновляем состояние графа
    return {"documents": documents, "question": question, "generation": generation}

# Описание вершины графа направления в другие вершины при получении вопрса пользователя
def route_question(state: GraphState):
    """
    Направление вопроса пользователя
    """
    app_logger.info("Routing")
    question = state["question"]
    app_logger.info("question %s", question)
    # Спрашиваем роутер, куда направить вопрос пользователя
    source = question_router.invoke({"question": question})
    app_logger.info("obtain source %s", source)
    # Если роутер возвращает web_search, то идем в поиск, а затем в генерацию, иначе сразу в генерацию
    if source == "web_search":
        app_logger.info("route question to web search")
        return "websearch"
    else:
        app_logger.info("route question to generation")
        return "generate"

# Построение графа агента
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