import streamlit as st
import os
from qa_new import ask  # 导入新的问答函数

st.set_page_config(page_title="企业知识库问答", page_icon="🏢", layout="wide")
st.title("🏢 企业知识库智能问答助手")
st.markdown("上传文档并提问，系统会从内部文档中检索答案并标注来源。")

# 侧边栏：显示文档列表和清空对话按钮
with st.sidebar:
    st.header("📁 知识库文档")
    if os.path.exists("docs"):
        docs_list = os.listdir("docs")
        if docs_list:
            for doc in docs_list:
                st.write(f"- {doc}")
        else:
            st.write("暂无文档")
    else:
        st.write("docs 文件夹不存在")
    
    st.divider()
    if st.button("🗑️ 清空对话"):
        st.session_state.messages = []
        st.rerun()

# 初始化聊天记录
if "messages" not in st.session_state:
    st.session_state.messages = []

# 显示历史消息
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# 接收用户输入
if prompt := st.chat_input("请输入您的问题（例如：员工手册中的请假流程）"):
    # 添加用户消息
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # 获取助手回答
    with st.chat_message("assistant"):
        with st.spinner("正在检索文档并生成答案..."):
            try:
                answer, sources = ask(prompt)  # 假设 ask 接受一个参数，如果有历史需要修改
                st.markdown(answer)
                if sources:
                    with st.expander("查看来源文档"):
                        for src in sources:
                            st.write(f"📄 {src}")
                st.session_state.messages.append({"role": "assistant", "content": answer})
            except Exception as e:
                error_msg = f"出错啦：{str(e)}"
                st.error(error_msg)
                st.session_state.messages.append({"role": "assistant", "content": error_msg})