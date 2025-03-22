from openai import OpenAI
from config import CONFIG
from langchain_openai import ChatOpenAI
import time
import json
USER_DATA=[{"title":"모순", "author":"양귀자", "rating": 5, "review":"내인생 최고의 책."}, 
           {"title":"악의", "author":"히가시노 게이고", "rating": 5, "review":"제목이 책을 완성. 끝에 끝까지 의심을 놓을 수 없음."},
           {"title":"구의 증명", "author":"최진영", "rating":3.5, "review": "사랑이란 뭘까?"},
           {"title":"귀신들의 땅", "author":"천쓰홍", "rating":3, "review": "폭력과 차별이 인간에게 미치는 영향"}]

client = OpenAI(api_key=CONFIG.assistants_key)
assistant = client.beta.assistants.create(
    name="book curator",
    instructions=("사용자의 독서 히스토리를 가지고 맞춤형 사용자의 페르소나를 분석하고 사용자의 독서 스타일을 구체적으로 제공합니다. "
                 "사용자의 독서 스타일과 사용자의 독서 평점 데이터 및 해당 도서 관련 제공 된 참조 자료를 바탕으로 고객에게 추천 할 수 있는 도서들을 "
                 "구체적인 추천 이유와 함께 5권 내외로 추천해줍니다."),
    model="gpt-4o"
)

thread = client.beta.threads.create()
messages = client.beta.threads.messages.create(thread_id=thread.id, role="user", content=json.dumps(USER_DATA))
run = client.beta.threads.runs.create(
  thread_id=thread.id,
  assistant_id=assistant.id
)
def poll_run(run, thread):
    while run.status != "completed":
        run = client.beta.threads.runs.retrieve(
            thread_id=thread.id,
            run_id=run.id,
        )
        if run.status == "failed":
            break
        time.sleep(0.5)
    return run


run  = poll_run(run, thread)
messages = client.beta.threads.messages.list(thread_id=thread.id)

for m in messages:
    print(f"{m.role}: {m.content[0].text.value}")