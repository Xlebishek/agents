from langchain_gigachat.chat_models import GigaChat
from langchain.tools import tool
from langchain.agents import create_agent
from langgraph.checkpoint.memory import InMemorySaver
import arxiv
import API


llm_academic = GigaChat(
    credentials=API.api_key,
    verify_ssl_certs=False
)

# заглушка
def schedule_agent(query: str) -> str:
    return "Пары в четверг: 10:00 (ауд. 231), 13:40 (ауд. 512)."

'''schedule_tool = Tool(
    name="schedule_agent",
    func=schedule_agent,
    description="Отвечает за расписание."
)'''


@tool(description="Поиск статей для выбранной темы диплома")
def arxiv_search(query: str) -> str:

    client = arxiv.Client()

    search = arxiv.Search(
        query=query,
        max_results=3,
        sort_by=arxiv.SortCriterion.Relevance
    )

    results = []
    for result in client.results(search):
        results.append({
            "title": result.title,
            "summary": result.summary,
            "published": result.published.date().isoformat(),
            "pdf_url": result.pdf_url
        })


    output = ""
    for i, a in enumerate(results, start=1):
        output += f"{i}. {a['title']} ({a['published']}, {a["pdf_url"]})\n\n"
    return output


tools_academic = [arxiv_search]

system_prompt = f"""
    Ты академический помощник. Можешь придумать темы диплома для студента(не более 3), вызывать инструменты.
    Студент задаст вопрос, ты отвечаешь.

    Правила:

    1. Лишнего не пиши, если не просят.
    2. Если ответить не можешь, возвращай error одним словом
    """

academic_agent = create_agent(model=llm_academic, tools=tools_academic, system_prompt=system_prompt, checkpointer=InMemorySaver())

def ask_academic_agent(query: str, user_name: str) -> str:
    print(f'[ACADEMIC] Вопрос {query}')

    response = academic_agent.invoke({"messages": [("user", query)]},
                                     {"configurable": {"thread_id": user_name}})["messages"][-1].content

    print(f'[ACADEMIC] Ответ: {response}')

    return response

agents_dict = {
    "schedule_agent": schedule_agent,
    "academic_agent": ask_academic_agent,
}