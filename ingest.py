import os
import re
from dotenv import load_dotenv
from langchain_community.document_loaders import PyPDFLoader
from langchain_community.document_loaders import UnstructuredWordDocumentLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import Chroma
from langchain_community.embeddings import ZhipuAIEmbeddings
from langchain_community.document_loaders import Docx2txtLoader

load_dotenv()

pdf_folder = "docs"
documents = []
for file in os.listdir(pdf_folder):
    file_path = os.path.join(pdf_folder, file)
    if file.endswith(".pdf"):
        print(f"正在加载 PDF: {file}")
        loader = PyPDFLoader(file_path)
        documents.extend(loader.load())
    elif file.endswith(".docx"):
        print(f"正在加载 Word: {file}")
        loader = Docx2txtLoader(file_path)
        documents.extend(loader.load())
print(f"共加载了 {len(documents)} 个文档片段")

def clean_text(text):
    # 移除 URL（用占位符替换）
    text = re.sub(r'https?://\S+', '[URL]', text)
    # 统一破折号（–、—等转为普通减号）
    text = re.sub(r'[\u2010-\u2015\u2212]', '-', text)
    # 移除连续的表格数字（可选）
    text = re.sub(r'\d+\.\d+\s+\d+\.\d+\s+\d+\.\d+', '[DATA]', text)
    # 移除多余空白
    text = re.sub(r'\s+', ' ', text).strip()
    return text

# 在加载完所有文档后执行清洗
for doc in documents:
    doc.page_content = clean_text(doc.page_content)

text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=200,
    chunk_overlap=30,
    separators=["\n\n", "\n", "。", "！", "？", "；", "，", " ", ""]
)
docs = text_splitter.split_documents(documents)
print(f"切分后得到 {len(docs)} 个文档块")

embeddings = ZhipuAIEmbeddings(model="embedding-3")

# 创建空的 Chroma 向量库
vectorstore = Chroma(
    embedding_function=embeddings,
    persist_directory="./chroma_db"
)

# 分批添加文档块，每批不超过64条（智谱API限制）
batch_size = 64
for i in range(0, len(docs), batch_size):
    batch = docs[i:i+batch_size]
    print(f"正在处理第 {i//batch_size + 1} 批，共 {len(batch)} 个文档块...")
    try:
        vectorstore.add_documents(batch)
        print(f"第 {i//batch_size + 1} 批处理完成")
    except Exception as e:
        print(f"第 {i//batch_size + 1} 批处理失败: {e}")
        # 打印当前批次的前几个文本预览，便于排查
        for j, doc in enumerate(batch):
            safe_content = doc.page_content[:100].encode('utf-8', errors='ignore').decode('utf-8')
            print(f"文档 {j} 内容预览: {safe_content}...")
        raise  # 终止，方便查看错误

vectorstore.persist()
print("文档入库完成！向量库保存在 ./chroma_db")