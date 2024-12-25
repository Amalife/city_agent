from langchain_community.tools.tavily_search import TavilySearchResults
from langchain_core.output_parsers.string import StrOutputParser
from langchain_gigachat import GigaChat
from agent.configuration.configuration import configuration
from agent.prompts import START_PROMPT, GENERATE_PROMPT

# Создание функциональности поискового движкаа
web_search_tool = TavilySearchResults(k=3, tavily_api_key=configuration.tavily_key)

# LLM для генерации и роутинга
llm = GigaChat(
    credentials=configuration.gigachat_credentials,
    model="GigaChat-Max",
    scope=configuration.gigachat_scope,
    verify_ssl_certs=configuration.gigachat_verify_ssl,
    temperature=configuration.gigachat_temperature,
)

# промпты для роутера и генерации
question_router = START_PROMPT | llm | StrOutputParser()

generate_chain = GENERATE_PROMPT | llm | StrOutputParser()