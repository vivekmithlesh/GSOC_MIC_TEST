from bs4 import BeautifulSoup
import os

def extract_articles_from_sgm(file_path, output_dir):
    with open(file_path, 'r', encoding='latin1') as file:
        soup = BeautifulSoup(file.read(), 'html.parser')
        for idx, reuter in enumerate(soup.find_all('reuters')):
            title = reuter.title.string if reuter.title else "No Title"
            body = reuter.body.string if reuter.body else ""
            if body:
                file_name = f"{idx}_{title[:50].replace(' ', '_').replace('/', '-')}.txt"
                file_path = os.path.join(output_dir, file_name)
                with open(file_path, 'w', encoding='utf-8') as out:
                    out.write(f"{title}\n{body}")