# app.py
import streamlit as st
import pypdf
from agent import build_graph

st.set_page_config(page_title="وكيل التدقيق المؤسسي", page_icon="⚖️")
st.title("وكيل التدقيق والامتثال المؤسسي الذكي")
st.markdown("ارفع عقداً (PDF) واطلب من الوكيل تحليله وفقاً للقوانين المحفوظة.")

uploaded_file = st.file_uploader("📄 ارفع ملف العقد (PDF)", type="pdf")
query = st.text_input("✍️ سؤال التدقيق", "حلل العقد وأبرز مدى التزامه بنظام حماية البيانات الشخصية")

if uploaded_file and query:
    # استخراج النص من PDF
    reader = pypdf.PdfReader(uploaded_file)
    contract_text = ""
    for page in reader.pages:
        contract_text += page.extract_text() or ""
    
    st.success("تم استخراج النص من العقد. جارٍ تشغيل الوكيل...")
    
    # إنشاء الوكيل
    graph = build_graph()
    initial_state = {
        "query": query,
        "contract_text": contract_text,
        "plan": "",
        "legal_context": "",
        "final_report": ""
    }
    
    # تشغيل التدفق مع عرض المراحل
    with st.status("🧠 الوكيل يعمل", expanded=True) as status:
        st.write("### 🧭 مرحلة التخطيط")
        # نمرر الحالة أولاً للحصول على الخطة (لاحظ أن invoke يشغل كامل الرسم)
        # لكننا نريد عرض المراحل خطوة بخطوة، لذا سنشغل الرسم جزئياً.
        # نستخدم graph.stream للحصول على الأحداث
        for output in graph.stream(initial_state):
            for node, state_update in output.items():
                if node == "planner":
                    st.write(f"**الخطة:**\n{state_update.get('plan', '')}")
                elif node == "researcher":
                    st.write(f"**السياق القانوني:**\n{state_update.get('legal_context', '')}")
                elif node == "synthesizer":
                    st.write(f"**التقرير النهائي:**\n{state_update.get('final_report', '')}")
        
        status.update(label="تم الانتهاء", state="complete")