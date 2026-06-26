# ⚖️ وكيل التدقيق والامتثال المؤسسي الذكي

وكيل ذكي (AI Agent) مبني على **LangGraph** و **Google Gemini** و **ChromaDB**، يقوم بتحليل العقود ومراجعتها مقابل القوانين المحفوظة، مع عرض الاستشهادات بنصوص القانون وأرقام الصفحات.

---

## 🧠 آلية العمل

1. **ارفع عقداً PDF** واطرح سؤالاً مثل: "حلل العقد وأبرز مدى التزامه بنظام حماية البيانات".
2. الوكيل ينفذ ثلاث مراحل:
   - 📝 **التخطيط**: يضع خطة تدقيق قانونية.
   - 🔍 **البحث**: يسترجع المواد القانونية من ChromaDB.
   - 📊 **التركيب**: يصدر تقريراً نهائياً بالمخالفات والتوصيات.

---

## 🛠️ التقنيات

| المكون | الوصف |
|--------|-------|
| **LangGraph** | تنسيق تدفق الوكيل |
| **Google Gemini 2.5 Flash** | النموذج اللغوي (مجاني وسريع) |
| **ChromaDB** | قاعدة بيانات متجهة للقوانين |
| **HuggingFace Embeddings** | تضمينات محلية مجانية |
| **Streamlit** | واجهة المستخدم |

---

## 📦 التثبيت

### 1. المتطلبات
- Python 3.10+
- مفتاح Google Gemini API (احصل عليه مجانًا من [Google AI Studio](https://aistudio.google.com/apikey))

### 2. الإعداد
```bash
git clone https://github.com/areejalmoufleh/Enterprise-RAG-Assistant.git
cd compliance_agent
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt