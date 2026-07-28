import sys
import os

# عشان نقدر نعمل import للملفات اللي في روت المشروع (config, chains, models...)
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import streamlit as st

from config import KAGGLE_API_URL
from models.llm_loader import check_server_health
from chains.prompt_optimizer import optimize_prompt
from chains.qa_chain import answer_question


st.set_page_config(page_title="Traffic Law Assistant", page_icon="🚦", layout="wide")

st.title("🚦 Intelligent Traffic Law Assistant")
st.caption("مساعد ذكي للإجابة على أسئلة قانون المرور المصري — الموديلات شغالة على Kaggle عن طريق ngrok")

# ---------------- Sidebar: حالة الاتصال بالسيرفر ----------------
with st.sidebar:
    st.subheader("⚙️ إعدادات الاتصال")
    st.text(f"API URL:\n{KAGGLE_API_URL}")

    if st.button("🔄 اختبار الاتصال بسيرفر Kaggle"):
        with st.spinner("جاري التحقق..."):
            is_healthy = check_server_health(KAGGLE_API_URL)
        if is_healthy:
            st.success("السيرفر شغال ومتصل ✅")
        else:
            st.error("لا يمكن الوصول للسيرفر ❌ — تأكد إن سيشن Kaggle شغالة ولينك ngrok محدث في .env")

    st.divider()
    st.subheader("📚 قاعدة المعرفة")
    st.write("- بيانات رخص القيادة (license_info.docx)")
    st.write("- بيانات المخالفات (violations.xlsx)")

# ---------------- Session State ----------------
if "history" not in st.session_state:
    st.session_state.history = []  # كل عنصر: {question, optimized, answer, sources}

if "optimized_prompt" not in st.session_state:
    st.session_state.optimized_prompt = ""

if "user_prompt" not in st.session_state:
    st.session_state.user_prompt = ""

# علم بسيط: لو اتحدد، بنصفّر الحقل هنا (في بداية الـ run) قبل ما الـ widget يتعرض،
# بدل ما نعدّل القيمة بعد إنشاء الـ widget مباشرة (ده اللي كان بيسبب الخطأ)
if st.session_state.get("_clear_optimized", False):
    st.session_state.optimized_prompt = ""
    st.session_state._clear_optimized = False

# ---------------- منطقة إدخال السؤال ----------------
st.subheader("💬 اسأل عن قانون المرور")

user_prompt = st.text_area(
    "اكتب سؤالك هنا:",
    value=st.session_state.user_prompt,
    height=100,
    placeholder="مثال: عايز أعرف شروط رخصة القيادة الخصوصية",
)

col1, col2, col3 = st.columns([1, 1, 2])

with col1:
    optimize_clicked = st.button("✨ Optimize Prompt")

with col2:
    send_clicked = st.button("📨 Send to Chatbot", type="primary")

# ---------------- زر Optimize Prompt ----------------
if optimize_clicked:
    if not user_prompt.strip():
        st.warning("اكتب سؤال الأول قبل التحسين.")
    else:
        with st.spinner("جاري تحسين السؤال..."):
            try:
                optimized = optimize_prompt(user_prompt)
                st.session_state.optimized_prompt = optimized
                st.session_state.user_prompt = user_prompt
            except ConnectionError as e:
                st.error(str(e))

if st.session_state.optimized_prompt:
    st.text_area(
        "🔍 السؤال بعد التحسين (يمكنك تعديله):",
        key="optimized_prompt",
        height=100,
    )

# ---------------- زر Send to Chatbot ----------------
if send_clicked:
    if not user_prompt.strip():
        st.warning("اكتب سؤال الأول.")
    else:
        final_query = st.session_state.optimized_prompt or user_prompt
        with st.spinner("جاري البحث وتوليد الإجابة..."):
            try:
                result = answer_question(optimized_question=final_query, original_question=user_prompt)
                st.session_state.history.append({
                    "question": user_prompt,
                    "optimized": final_query,
                    "answer": result["answer"],
                    "sources": result["sources"],
                })
                # نطلب التصفير في الـ run الجاي (مش دلوقتي) عشان نتجنب خطأ Streamlit
                st.session_state._clear_optimized = True
                st.rerun()
            except ConnectionError as e:
                st.error(str(e))

# ---------------- عرض المحادثة ----------------
st.divider()
st.subheader("🗂️ سجل المحادثة")

for item in reversed(st.session_state.history):
    with st.chat_message("user"):
        st.markdown(item["question"])
        if item["optimized"] != item["question"]:
            st.caption(f"🔍 السؤال بعد التحسين: {item['optimized']}")

    with st.chat_message("assistant"):
        st.markdown(item["answer"])
        with st.expander("📎 المصادر المسترجعة (Retrieved Sources)"):
            for i, src in enumerate(item["sources"], start=1):
                st.markdown(f"**Source {i}** — `{src['metadata'].get('source', 'unknown')}`")
                st.code(src["content"])