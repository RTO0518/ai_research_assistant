import os
from dotenv import load_dotenv

from langchain_community.vectorstores import Chroma
from langchain_community.embeddings import ZhipuAIEmbeddings
from langchain_openai import ChatOpenAI
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
from operator import itemgetter


load_dotenv()

embeddings = ZhipuAIEmbeddings(model="embedding-3")
vectorstore = Chroma(persist_directory="./chroma_db", embedding_function=embeddings)
retriever = vectorstore.as_retriever(search_kwargs={"k": 30})

template = """你是一个企业内部文档问答助手。请根据以下检索到的片段回答问题。如果片段中没有相关信息，请说"未找到相关信息"。请附上答案来源的文档名称（如果有）。

检索到的片段：
{context}

问题：{question}
答案："""
prompt = PromptTemplate.from_template(template)

llm = ChatOpenAI(
    model="glm-4-flash",
    temperature=0.1,
    max_tokens=512,
    openai_api_key=os.getenv("ZHIPUAI_API_KEY"),
    openai_api_base="https://open.bigmodel.cn/api/paas/v4/"
)

def format_docs(docs):
    return "\n\n".join([doc.page_content for doc in docs])

chain = (
    {"context": itemgetter("question") | retriever | format_docs, "question": itemgetter("question")}
    | prompt
    | llm
    | StrOutputParser()
)

def ask(question, history=""):
    docs = retriever.invoke(question)
    # 添加调试打印
    print("检索到的前3个片段：")
    for i, doc in enumerate(docs[:3]):
        print(f"片段{i+1}: {doc.page_content[:200]}...")
    print("---")
    top_docs = docs[:3]
    context = "\n\n".join([doc.page_content for doc in top_docs])
    final_prompt = prompt.format(context=context, question=question)
    response = llm.invoke(final_prompt)
    answer = response.content if hasattr(response, 'content') else response
    sources = set(os.path.basename(doc.metadata.get('source', '未知来源')) for doc in top_docs)
    return answer, sources