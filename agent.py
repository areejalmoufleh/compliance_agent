import os
from typing import TypedDict
from decouple import config  # لتحميل المفتاح من .env بأمان
from langgraph.graph import StateGraph, END
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import HumanMessage, SystemMessage
from tools import lookup_law

# تعريف الحالة
class AgentState(TypedDict):
    query: str
    contract_text: str
    plan: str
    legal_context: str
    final_report: str

# تحميل المفتاح من متغير البيئة
GOOGLE_API_KEY = config('GOOGLE_API_KEY')

# نموذج Gemini (يستخدم المفتاح من .env)
llm = ChatGoogleGenerativeAI(model="gemini-2.5-flash", google_api_key=GOOGLE_API_KEY)

# العقدة 1: المخطط
def planner_node(state: AgentState):
    system_msg = SystemMessage(content="أنت وكيل تدقيق قانوني ذكي. مهمتك وضع خطة واضحة لفحص عقد بناءً على القوانين المعمول بها. أعد الخطة فقط دون تنفيذ.")
    user_prompt = f"العقد:\n{state['contract_text']}\n\nسؤال المستخدم: {state['query']}\n\nضع خطة تدقيق محكمة."
    response = llm.invoke([system_msg, HumanMessage(content=user_prompt)])
    return {"plan": response.content}

# العقدة 2: الباحث (يستخدم الأداة)
def researcher_node(state: AgentState):
    plan = state['plan']
    extraction_prompt = f"استناداً إلى خطة التدقيق التالية، اقترح 3 استعلامات بحث دقيقة بالعربية للبحث في قاعدة القوانين:\n{plan}\nأعد الاستعلامات فقط، كل منها في سطر."
    queries_resp = llm.invoke([HumanMessage(content=extraction_prompt)])
    queries = [q.strip("- ") for q in queries_resp.content.split("\n") if q.strip()][:3]
    results = []
    for q in queries:
        res = lookup_law.invoke(q)
        results.append(f"نتيجة البحث عن '{q}':\n{res}")
    return {"legal_context": "\n\n".join(results)}

# العقدة 3: المركب
def synthesizer_node(state: AgentState):
    system_msg = SystemMessage(content="أنت مدقق قانوني محترف. أعد تقريراً يتضمن: المخالفات المحتملة، البنود المتوافقة، توصيات التعديل، مع الاستشهاد بنصوص القانون وأرقام الصفحات. استخدم العربية الفصحى.")
    user_prompt = f"العقد:\n{state['contract_text']}\n\nالقوانين المسترجعة:\n{state['legal_context']}\n\nالسؤال: {state['query']}\n\nاكتب التقرير النهائي."
    response = llm.invoke([system_msg, HumanMessage(content=user_prompt)])
    return {"final_report": response.content}

# بناء الرسم البياني
def build_graph():
    workflow = StateGraph(AgentState)
    workflow.add_node("planner", planner_node)
    workflow.add_node("researcher", researcher_node)
    workflow.add_node("synthesizer", synthesizer_node)
    workflow.set_entry_point("planner")
    workflow.add_edge("planner", "researcher")
    workflow.add_edge("researcher", "synthesizer")
    workflow.add_edge("synthesizer", END)
    return workflow.compile()