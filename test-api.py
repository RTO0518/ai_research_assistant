import os
from dotenv import load_dotenv
from zhipuai import ZhipuAI

# 加载 .env 文件中的环境变量
load_dotenv()

# 从环境变量获取 API Key
api_key = os.getenv("ZHIPUAI_API_KEY")
if not api_key:
    raise ValueError("请在 .env 文件中设置 ZHIPUAI_API_KEY")

# 初始化客户端
client = ZhipuAI(api_key=api_key)

# 调用模型
response = client.chat.completions.create(
    model="glm-4-flash",
    messages=[{"role": "user", "content": "你好，请介绍一下你自己"}]
)

print(response.choices[0].message.content)