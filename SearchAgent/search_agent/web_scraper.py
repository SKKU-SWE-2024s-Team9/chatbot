import requests
from bs4 import BeautifulSoup
from langchain.text_splitter import RecursiveCharacterTextSplitter
import re
import pandas as pd
import os

class CustomTextSplitter(RecursiveCharacterTextSplitter):
    def __init__(self, chunk_size, chunk_overlap):
        super().__init__(chunk_size=chunk_size, chunk_overlap=chunk_overlap)
        self.chunk_size = chunk_size
        self.chunk_overlap = chunk_overlap

    def split_text(self, text):
        chunks = []
        paragraphs = text.split('\n')
        current_chunk = ""
        for paragraph in paragraphs:
            if len(paragraph.strip()) <= 2:  # 글자 수가 2개 이하인 단락 건너뛰기
                continue
            if len(current_chunk) + len(paragraph) + 1 > self.chunk_size:
                chunks.append(current_chunk.strip())
                current_chunk = paragraph + "\n"
            else:
                current_chunk += paragraph + "\n"
        if current_chunk:
            chunks.append(current_chunk.strip())
        return chunks

class WebScraper:
    def __init__(self, base_url, output_csv):
        self.base_url = base_url
        self.output_csv = output_csv

    def scrape_and_process(self):
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'}
        try:
            response = requests.get(self.base_url, headers=headers)
            response.raise_for_status()  # HTTP 에러 발생 시 예외 발생
            response.encoding = response.apparent_encoding  # 인코딩 설정

            # BeautifulSoup을 사용하여 HTML 파싱
            soup = BeautifulSoup(response.text, 'html.parser')

            # 특정 태그나 클래스의 텍스트 추출
            content = soup.find_all(['a'])
            original_text = '\n'.join([element.get_text(strip=True) for element in content])

            # 서지정보부터 홈페이지까지의 부분을 제거
            cut_text = re.sub(r'서지정보.*?홈페이지', '', original_text, flags=re.DOTALL)

            # 영어와 개행 문자만 남기고 나머지 문자 제거
            cleaned_text = re.sub(r'[^a-zA-Z\n]', ' ', cut_text).strip()

            splitter = CustomTextSplitter(
                chunk_size=500,
                chunk_overlap=50
            )

            # 텍스트 분할
            split_texts = splitter.split_text(cleaned_text)

            # 데이터프레임 생성
            data = {
                'text': split_texts,
                'source': [self.base_url] * len(split_texts),
                'chunk_id': list(range(1, len(split_texts) + 1))
            }

            df = pd.DataFrame(data)

            # 파일 존재 여부 확인 후 저장
            if not os.path.isfile(self.output_csv):
                df.to_csv(self.output_csv, mode='w', index=False, header=True)
            else:
                df.to_csv(self.output_csv, mode='a', index=False, header=False)

            print(f"Data saved to {self.output_csv}")

        except Exception as e:
            print(f"Failed to load document from {self.base_url}: {e}")

# 사용 예시
if __name__ == "__main__":
    # base_url = "https://scholar.google.com/citations?user=0YEYuGIAAAAJ&hl=ko&oi=ao"
    # base_url = "https://scholar.google.com/citations?hl=ko&user=Ye0pjlAAAAAJ&view_op=list_works&sortby=pubdate"
    base_url = "https://scholar.google.com/citations?user=VQeFpwsAAAAJ&hl=ko&oi=ao"
    output_csv = './labs_data.csv'
    scraper = WebScraper(base_url, output_csv)
    scraper.scrape_and_process()
