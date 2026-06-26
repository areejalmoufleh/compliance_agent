# tools.py
from langchain_core.tools import tool
from db import load_law_database

@tool
def lookup_law(query: str) -> str:
    """ابحث في القوانين المحفوظة وأعد المواد ذات الصلة. الاستعلام يجب أن يكون بالعربية."""
    db = load_law_database()
    docs = db.similarity_search(query, k=3)
    result_parts = []
    for doc in docs:
        page = doc.metadata.get('page', 'غير معروف')
        result_parts.append(f"المادة (صفحة {page}):\n{doc.page_content}\n")
    return "\n---\n".join(result_parts)