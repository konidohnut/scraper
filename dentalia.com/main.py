from scraping.scraper import scrape_clinics
from utils.file_handling import save_to_json


def main():
    url = 'https://dentalia.com/clinica/?nocache=1706725462'
    clinics_data = scrape_clinics(url)
    file_path = "clinics.json"
    save_to_json(clinics_data, file_path)
    print("Data has been scraped and saved to clinics.json")


if __name__ == "__main__":
    main()
