from langchain_openai import ChatOpenAI
from config import CONFIG
from langchain.schema import HumanMessage
from langchain.prompts import PromptTemplate
from langchain.prompts.chat import (
    ChatPromptTemplate,
    SystemMessagePromptTemplate,
    HumanMessagePromptTemplate,
)
import json

llm=ChatOpenAI(model="gpt-4o-mini", api_key=CONFIG.assistants_key)
my_template="""
당신은 지금부터 북큐레이터입니다. 사용자가 입력하는 도서 리스트를 여러 도서사이트의 출판사 서평,
줄거리 등을 참고하여 분석하고 사용자의 서평으로부터 해당 도서에 대해 감상평이 긍정적인지, 부정적인지를 분석하고,
사용자가 매긴 5점 만점의 평가점수를 참고하여 사용자의 독서스타일을 구체적으로 설명해주십시오. 해당 사용자에게 추천해줄 만한 도서도
다섯개 내외로 추천하고, 추천 이유도 구체적으로 설명해주시길 바랍니다.
이에 대한 응답형식은 독작의 독서 스타일, 추천도서 목록을 json형식으로 응답하십시오.
"""
USER_DATA=[{"title":"모순", "author":"양귀자", "rating": 5, "review":"내인생 최고의 책."}, 
           {"title":"악의", "author":"히가시노 게이고", "rating": 5, "review":"제목이 책을 완성. 끝에 끝까지 의심을 놓을 수 없음."},
           {"title":"구의 증명", "author":"최진영", "rating":3.5, "review": "사랑이란 뭘까?"},
           {"title":"귀신들의 땅", "author":"천쓰홍", "rating":3, "review": "폭력과 차별이 인간에게 미치는 영향"}]
json_data = json.dumps(USER_DATA)
system_message_prompt= SystemMessagePromptTemplate.from_template(my_template)
human_template ="{text}"
human_message_prompt = HumanMessagePromptTemplate.from_template(human_template)
chat_prompt = ChatPromptTemplate.from_messages([system_message_prompt, human_message_prompt])
query = chat_prompt.format_messages(text=f"{json_data}")
print(llm.predict_messages(query))