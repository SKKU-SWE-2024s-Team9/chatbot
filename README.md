# SearchAgent

SearchAgent는 대학생들이 자신의 취향에 맞는 연구실(Lab)과 동아리(Club)을 찾을 수 있도록 도와주는 추천 시스템입니다.

## 기능

- 연구실(Lab) 추천
- 동아리(Club) 추천

## 설치

### 필수 패키지 설치

필요한 패키지를 설치합니다:

```bash
pip install -r requirements.txt

1. 환경 변수 설정
OpenAI API 키를 환경 변수로 설정합니다. 다음 명령어를 터미널에 입력합니다:

export OPENAI_API_KEY="your-openai-api-key"

2. SearchAgent 초기화 및 실행
SearchAgent를 초기화하고 연구실 또는 동아리를 추천받습니다.

from search_agent.main import SearchAgent

# SearchAgent 초기화
agent = SearchAgent('labs_data.csv', 'clubs_data.csv')

# 연구실 추천
lab_recommendation = agent.run('Can you recommend some Lab about NLP?')
print("Lab Recommendation:", lab_recommendation)

# 동아리 추천
club_recommendation = agent.run('Can you recommend some Club about technology?')
print("Club Recommendation:", club_recommendation)

3. 테스트 실행
테스트를 실행하여 패키지가 정상적으로 작동하는지 확인할 수 있습니다.
python -m unittest discover tests

프로젝트 구조

SearchAgent/
│
├── setup.py
├── README.md
├── requirements.txt
├── search_agent/
│   ├── __init__.py
│   ├── csv_processor.py
│   ├── rag_tool.py
│   ├── qa_agent.py
│   ├── lab.py
│   ├── club.py
│   ├── templates.py
│   ├── main.py
│   └── api_client.py
└── tests/
    └── test_search_agent.py















