import os
import re
import csv
import dateparser
from bs4 import BeautifulSoup
import spacy
from mic_rules import rule_based_mic_detector

nlp = spacy.load("en_core_web_sm")

def clean_article(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        soup = BeautifulSoup(f, "html.parser")
        text = soup.get_text(separator=' ')
        return ' '.join(text.split())

def extract_countries(text, valid_country_list):
    doc = nlp(text)
    countries = [ent.text for ent in doc.ents if ent.label_ == "GPE"]
    return list(set([c for c in countries if c in valid_country_list]))

def extract_date(text):
    dates = dateparser.search.search_dates(text)
    return str(dates[0][1].date()) if dates else None

def extract_fatalities(text):
    text = text.lower()
    pattern = r'(at least|more than|around|approximately)?\s?(\d{1,4})\s?(soldiers|troops|people|casualties|deaths|killed)'
    matches = re.findall(pattern, text)
    if matches:
        counts = [int(m[1]) for m in matches]
        return min(counts), max(counts)
    return None, None

def process_articles(input_dir, country_list_file):
    results = []
    with open(country_list_file, 'r') as f:
        valid_countries = f.read().splitlines()

    for file in os.listdir(input_dir):
        if not file.endswith(".txt"):
            continue

        path = os.path.join(input_dir, file)
        text = clean_article(path)

        if not rule_based_mic_detector(text):
            continue

        countries = extract_countries(text, valid_countries)
        date = extract_date(text)
        min_kill, max_kill = extract_fatalities(text)

        results.append({
            "file": file,
            "date": date,
            "fatalities_min": min_kill,
            "fatalities_max": max_kill,
            "countries": countries
        })

    return results

def save_results(results, output_file="mic_results.csv"):
    with open(output_file, 'w', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=["file", "date", "fatalities_min", "fatalities_max", "countries"])
        writer.writeheader()
        for r in results:
            r["countries"] = ", ".join(r["countries"])
            writer.writerow(r)

if __name__ == "__main__":
    INPUT_DIR = "./news_articles"
    COUNTRY_LIST = "./states2016.csv"
    OUTPUT_FILE = "mic_results.csv"

    final_results = process_articles(INPUT_DIR, COUNTRY_LIST)
    save_results(final_results, OUTPUT_FILE)
    print(f"✅ Processed and saved {len(final_results)} MIC articles.")