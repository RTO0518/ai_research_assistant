# 📚 企业智能知识库问答助手

基于 **LangChain + 智谱AI + Chroma + Streamlit** 构建的 RAG 问答系统。支持上传 PDF / Word 文档，通过自然语言提问，系统从文档中检索相关信息并生成答案，同时标注来源。

## ✨ 功能特点

- 📄 **多格式支持**：支持 PDF、Word（.docx）文档，自动提取文本内容。
- 🔍 **语义检索**：使用智谱 Embedding 模型将文档向量化，结合向量检索召回相关片段。
- 💬 **智能问答**：调用智谱 `glm-4-flash` 大模型，基于检索到的上下文生成准确答案。
- 🖥️ **交互界面**：基于 Streamlit 搭建，开箱即用，支持多轮对话历史。
- 📦 **国产化技术栈**：完全基于智谱 AI 服务，无需外网代理。

## 🛠️ 技术栈

- **Python 3.9+**
- **LangChain**：RAG 流程编排
- **智谱AI**：`glm-4-flash`（对话） + `embedding-3`（向量化）
- **Chroma**：轻量级向量数据库
- **Streamlit**：前端界面

## 🚀 快速开始

### 1. 克隆仓库
```bash
git clone https://github.com/RTO0518/ai_research_assistant.git
cd ai_research_assistant
2. 创建虚拟环境并安装依赖
bash
python -m venv venv
# Windows
venv\Scripts\activate
# Mac/Linux
source venv/bin/activate

pip install -r requirements.txt
3. 配置智谱 API Key
在项目根目录创建 .env 文件，填入你的智谱 API Key：

text
ZHIPUAI_API_KEY=你的密钥
4. 准备知识库文档
将需要问答的 PDF 或 Word 文件放入 docs/ 文件夹（支持 .pdf, .docx）。

5. 构建向量库
bash
python ingest.py
运行后会生成 chroma_db 文件夹，里面是向量化后的数据。

6. 启动问答界面
bash
streamlit run app.py
浏览器会自动打开 http://localhost:8501，即可开始提问。

📂 项目结构
text
ai_research_assistant/
├── app.py                  # Streamlit 前端界面
├── ingest.py               # 文档加载与向量化脚本
├── qa_new.py               # 问答核心逻辑（检索+生成）
├── requirements.txt        # 依赖列表
├── .env                    # 环境变量（API Key，不上传）
├── docs/                   # 存放原始文档
├── chroma_db/              # 向量数据库（自动生成）
└── README.md
💡 使用示例
在输入框中提问，例如：

“Spring Boot 的核心特性有哪些？”

“文献综述里提到了哪些研究方法？”

“外文翻译的作者是谁？”

系统会返回答案，并显示参考来源。

🔧 主要实现
文档处理（ingest.py）
使用 PyPDFLoader 和 Docx2txtLoader 加载文件

通过 RecursiveCharacterTextSplitter 切分为文本块（chunk_size=400，overlap=50）

调用智谱 embedding-3 模型向量化，存入 Chroma

问答流程（qa_new.py）
用户输入问题 → 向量检索召回 Top-3 相关片段

拼接上下文与 Prompt → 调用 glm-4-flash 生成答案

返回答案并显示来源文档

🎯 未来优化方向
增加重排序（Rerank）模块，进一步提升检索精度

支持多轮对话中的上下文理解（查询改写）

前端增加文件上传功能，动态扩展知识库

部署到云端（Streamlit Cloud / 阿里云）

📄 开源协议
MIT License

👤 作者
RTO0518 – 盐城工学院 网络工程专业 2026届

欢迎 Star ⭐，感谢支持！
