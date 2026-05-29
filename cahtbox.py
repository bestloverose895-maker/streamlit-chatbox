import os  # 导入os模块,用于获取环境变量
from dotenv import load_dotenv  # 导入load_dotenv函数,用于加载环境变量文件
from openai import OpenAI  # 专门用来连接OpenAI LLM的库
import streamlit as st # 专门用来创建Web应用的库

load_dotenv()  # 从.env文件读取环境变量

client = OpenAI(
    api_key=os.getenv("API_KEY"),
    base_url=os.getenv("BASE_URL")
)
response = client.chat.completions.create(
    model="deepseek-v4-flash",
    messages=[ # 用户消息
        {"role": "system", "content": "你是一个知识渊博的助手侧重的领域是金融和政治"},
        {"role": "system", "content": "用三句话解释什么是比特币"}
    ]
)
print(response.choices[0].message.content)