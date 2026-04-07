import os
import sys
sys.stdout.reconfigure(encoding="utf-8")
from dotenv import load_dotenv
from langchain_anthropic import ChatAnthropic

load_dotenv()

llm = ChatAnthropic(model="claude-sonnet-4-5")
response = llm.invoke("Xin chào!")
print(response.content)
print("\n✅ API kết nối thành công! Sẵn sàng vào bài.")

