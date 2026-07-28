from typing import Dict, Any
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

from models.llm_loader import KaggleRemoteLLM
from prompts.qa_prompt import QA_SYSTEM_PROMPT, QA_USER_TEMPLATE
from chains.retriever_chain import retrieve_documents, format_context


def build_qa_chain():
    llm = KaggleRemoteLLM(system_prompt=QA_SYSTEM_PROMPT, temperature=0.3, max_new_tokens=600)
    prompt = ChatPromptTemplate.from_template(QA_USER_TEMPLATE)
    chain = prompt | llm | StrOutputParser()
    return chain


def answer_question(optimized_question: str, original_question: str = None) -> Dict[str, Any]:
    
    documents = retrieve_documents(optimized_question)
    context = format_context(documents)

    chain = build_qa_chain()
    answer = chain.invoke({
        "context": context,
        "question": original_question or optimized_question,
    })

    return {
        "answer": answer,
        "sources": [
            {"content": doc.page_content, "metadata": doc.metadata}
            for doc in documents
        ],
    }
