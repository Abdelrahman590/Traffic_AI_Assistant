from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

from models.llm_loader import KaggleRemoteLLM
from prompts.optimizer_prompt import OPTIMIZER_SYSTEM_PROMPT, OPTIMIZER_USER_TEMPLATE


def build_prompt_optimizer_chain():
    llm = KaggleRemoteLLM(system_prompt=OPTIMIZER_SYSTEM_PROMPT, temperature=0.2, max_new_tokens=200)

    prompt = ChatPromptTemplate.from_template(OPTIMIZER_USER_TEMPLATE)

    chain = prompt | llm | StrOutputParser()
    return chain


def optimize_prompt(question: str) -> str:
    chain = build_prompt_optimizer_chain()
    return chain.invoke({"question": question}).strip()
