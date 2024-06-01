import requests
import pandas as pd
import os

class APIClient:
    def __init__(self, base_url):
        self.base_url = base_url
        self.session = requests.Session()

    def get_data(self, endpoint):
        url = f"{self.base_url}/{endpoint}"
        response = self.session.get(url)
        if response.status_code == 200:
            return response.json()
        else:
            print(f"Failed to get data: {response.status_code}")
            response.raise_for_status()

    def save_to_csv(self, data, filename):
        df = pd.DataFrame(data)
        if not os.path.isfile(filename):
            df.to_csv(filename, mode='w', index=False, header=True)
        else:
            df.to_csv(filename, mode='a', index=False, header=False)
        print(f"Data saved to {filename}")

def main():
    base_url = "http://localhost:3000/api"

    # API 클라이언트 초기화
    client = APIClient(base_url)

    # Lab 데이터 가져오기
    lab_data = client.get_data("labs")
    client.save_to_csv(lab_data, "labs_data.csv")

    # Club 데이터 가져오기
    club_data = client.get_data("clubs")
    client.save_to_csv(club_data, "clubs_data.csv")

if __name__ == "__main__":
    main()
