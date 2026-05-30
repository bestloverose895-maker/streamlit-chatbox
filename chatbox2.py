import os  # 导入os模块,用于获取环境变量
from openai import OpenAI  # 专门用来连接OpenAI LLM的库
import streamlit as st # 专门用来创建Web应用的库

# 优先从 Streamlit Secrets 读取环境变量（用于部署）
if hasattr(st, "secrets") and "API_KEY" in st.secrets:
    api_key = st.secrets["API_KEY"]
    base_url = st.secrets["BASE_URL"]
else:
    # 本地开发时从 .env 读取
    from dotenv import load_dotenv
    load_dotenv()
    api_key = os.getenv("API_KEY")
    base_url = os.getenv("BASE_URL")

client = OpenAI(
    api_key=api_key,
    base_url=base_url
)

# ==============写页面=====================
st.title("🤖,我是你的专属助理")  # 等同于一个html文件，里面写了一个 <h1> 标签
st.caption("基于OpenAI的Deepseek模型,你可以向我提问,我会回答你的问题") # 副标题


# ==============初始化对话历史=====================
# session_state 是一个会话管理器,用于存储用户会话中的数据
if "messages" not in st.session_state:
    st.session_state.messages = []
    
# ==============显示历史消息=====================
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):   # 创建一个消息容器
        st.write(msg["content"])        # 往消息容器中写入消息内容


# ==============用户输入的内容=====================
if prompt := st.chat_input("请输入你的问题"):   #:= 可以赋值,将用户输入的问题添加到会话历史中,可以判断用户是否输入了内容
    # 将用户的消息添加到会话历史中,并显示在页面上
  
    st.session_state.messages.append({"role": "user", "content": prompt}) 

    # 在页面上展示这句话
    with st.chat_message("user"):
      st.write(prompt)
        
      # 创建一个AI响应的容器
      with st.chat_message("assistant"):
        # 调用 deepseek 模型,获取响应
        response = client.chat.completions.create(
            model="deepseek-v4-flash",
            messages=[ # 用户消息
                {"role": "system", "content": "你是一个知识渊博的助手,侧重的领域是金融和政治,精通裸k技术学。当前日期是2026年5月30日。如果用户询问的事件发生在你的知识截止日期之后，请诚实地告诉用户你不确定，并说明你的知识截止时间。"},
            *st.session_state.messages,#  *为解包操作符,将列表中的元素展开为多个参数,解构到 messages 数组中
            ],
            stream=True,
            
        )
        # 处理流式响应
        full_response = ""
        message_placeholder = st.empty()
        for chunk in response:
            if chunk.choices[0].delta.content:
                full_response += chunk.choices[0].delta.content
                message_placeholder.markdown(full_response)
        
        # 将AI响应添加到会话历史中
        st.session_state.messages.append({"role": "assistant", "content": full_response})