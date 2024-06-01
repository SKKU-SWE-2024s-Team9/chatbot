import unittest
import sys
import os

# 현재 파일의 부모 디렉토리의 부모 디렉토리를 sys.path에 추가하여 모듈 검색 경로를 수정합니다.
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from search_agent.main import SearchAgent

class TestSearchAgent(unittest.TestCase):
    def setUp(self):
        # 직접 작성한 CSV 파일을 사용하여 SearchAgent 초기화
        self.agent = SearchAgent('labs_data.csv', 'clubs_data.csv')

    def test_run_lab_recommendation(self):
        response = self.agent.run('Can you recommend some Lab about NLP?')
        self.assertIn("Name:", response)
        print("Lab Recommendation Response:", response)

    def test_run_club_recommendation(self):
        response = self.agent.run('Can you recommend some Club about technology?')
        self.assertIn("Name:", response)
        print("Club Recommendation Response:", response)

if __name__ == '__main__':
    unittest.main()
