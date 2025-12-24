from langchain_gigachat.chat_models import GigaChat
import API

# documents_agent - не реализован

def router_agent(query: str) -> str:
    prompt = f"""
    Выбери одного агента для запроса пользователя. 
    Варианты:
    - academic_agent — учебные вопросы, диплом, статьи научные
    - documents_agent — правила университета, факультета и прочее

    Возвращай только имя агента.

    Вопрос: {query}
    """
    response = llm.invoke(prompt).content.strip()
    print(f"[ROUTER] Вопрос: {query}")
    print(f"[ROUTER] Выбран агент: {response}")
    return response

llm = GigaChat(
    credentials=API.api_key,
    verify_ssl_certs=False,
)