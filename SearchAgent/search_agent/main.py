from .csv_processor import CSVProcessor
from .rag_tool import RAGTool
from .qa_agent import QAAgent
from .templates import LAB_TEMPLATE, CLUB_TEMPLATE
from .web_scraper import WebScraper
from .api_client import APIClient
from .lab import LabCollection


class SearchAgent:
    def __init__(self, lab_csv, club_csv):
        lab_processor = CSVProcessor(lab_csv, 'recommended.csv')
        lab_processor.process_csv()

        club_processor = CSVProcessor(club_csv, 'recommended_club.csv')
        club_processor.process_csv()

        lab_rag_tool = RAGTool(file_path='recommended.csv', template=LAB_TEMPLATE)
        club_rag_tool = RAGTool(file_path='recommended_club.csv', template=CLUB_TEMPLATE)

        self.qa_agent = QAAgent(rag_tool=lab_rag_tool, club_rag_tool=club_rag_tool)

    def run(self, query):
        answer = self.qa_agent.run(query)
        response = LabCollection.from_string(answer)
        responseJson = None
        if(isinstance(response, str)):
            return response, responseJson
        else:
            responseJson = response.to_json()
            return response, responseJson

def main():
    # 웹 스크레이핑
    base_url = "https://scholar.google.com/citations?user=VQeFpwsAAAAJ&hl=ko&oi=ao"
    output_csv = '/content/drive/MyDrive/Search_Agent_Demo/google_scholar.csv'
    scraper = WebScraper(base_url, output_csv)
    scraper.scrape_and_process()

    # API 클라이언트를 사용하여 데이터 수집
    api_base_url = "http://localhost:3000/api"

    client = APIClient(api_base_url)

    lab_csv = 'labs_data.csv'
    club_csv = 'clubs_data.csv'
    
    lab_data = client.get_data("labs")
    client.save_to_csv(lab_data, lab_csv)
    
    club_data = client.get_data("clubs")
    client.save_to_csv(club_data, club_csv)

    # SearchAgent 실행
    search_agent = SearchAgent(lab_csv, club_csv)
    response, responseJson = search_agent.run('Can you recommend some Lab about NLP?')
    print(response)
    print(responseJson)
    
if __name__ == "__main__":
    main()
