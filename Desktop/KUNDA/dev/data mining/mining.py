import requests
from bs4 import BeautifulSoup
import csv

URL = "https://kunda.house/listing/"
HEADERS = {
    "User-Agent": "Chrome/91.0.4472.124"
}

def get_data(url):
    response = requests.get(url, headers=HEADERS)
    if response.status_code != 200:
        raise ValueError(f"Failed to connect. Check your script Status code: {response.status_code}")
    soup = BeautifulSoup(response.content, "html.parser")
    titles = soup.find_all("h3", class_="title-sin_item dis-flex-wrap-center")
    
    cleaned_titles = set()
    for title in titles:
        text = title.text.strip()
        text = text.replace('"', '')
        text = text.replace('| Room | For Rent', '')
        text = text.replace('| Rooms', '')
        text = text.replace('| For Rent', '')
        text = text.replace(', Birmingham', '')
        cleaned_titles.add(text)
    
    return list(cleaned_titles)
    
def save_to_csv(data, filename="trainingdata.csv"):
    with open(filename, mode='w', encoding='utf-8', newline='') as file:
        writer = csv.writer(file, delimiter='|')
        for item in data:
            writer.writerow([item])
            
            
if __name__ == "__main__":
    scraped_data = get_data(URL)
    save_to_csv(scraped_data)