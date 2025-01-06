import re
import logging
from dotenv import load_dotenv
import os
from openai import OpenAI

# 加载环境变量
load_dotenv(dotenv_path="./.env")


# 从环境变量中获取 API Key
api_key = "sk-Spy1NUixDFsybFtxLxlvBrdi7DCqkavx0HtPOFECEL97Vl3H"
if not api_key:
    raise ValueError("OPENAI_API_KEY is not set in the environment variables.")

# 初始化 OpenAI 客户端
client = OpenAI(
    api_key=api_key,  # 确保传递 api_key
    base_url="https://api.moonshot.cn/v1"
)

def parse_log(raw_log: str) -> str:
    """
    调用 AI 接口解析日志，返回 AI 生成的结果。

    :param raw_log: 原始日志内容
    :return: AI 生成的日志分析结果
    """
    try:
        completion = client.chat.completions.create(
            model="moonshot-v1-32k",  # 使用指定的 Moonshot 模型
            messages=[
                {"role": "system", "content": "直接根据日志中的STEP内容生成一段简洁明了的指导书，以中文生成，仅包含指导书标题和内容。"},
                {"role": "user", "content": raw_log},  # 传递日志内容给 AI
            ],
            max_tokens=1000,
            temperature=0.7,
        )

        # 获取并返回 AI 返回的结果
        ai_response = completion.choices[0].message.content
        logging.debug(f"AI Response: {ai_response}")
        return ai_response

    except Exception as e:
        logging.error(f"Error while calling AI API: {e}")
        return "Error generating log analysis."
