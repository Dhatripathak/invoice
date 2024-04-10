import pandas as pd
import requests
from bs4 import BeautifulSoup
import json
import os


output_folder = 'extracted_articles'
if not os.path.exists(output_folder):
    os.makedirs(output_folder)


def extract_data(url):
   
    response = requests.get(url)
    
   
    if response.status_code == 200:
      
        soup = BeautifulSoup(response.text, 'html.parser')
        
       
        title = soup.find('span', class_=['td-bred-no-url-last', 'tdb-bred-no-url-last']).get_text(strip=True)
        


        parent_div = soup.find_all('div', class_='td-ss-main-content')

        if parent_div:
            for div in parent_div:
                content_div = div.find('div', class_='td-post-content tagdiv-type')

                if content_div:
                   
                    for pre_tag in content_div.find_all('pre'):
                        pre_tag.extract()

                   
                    content = ' '.join([tag.get_text(strip=True) for tag in content_div.find_all(['p', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'ul', 'ol', 'li'])])
                
        else:
            parent_div = soup.find_all('div', class_='td_block_wrap tdb_single_content tdi_130 td-pb-border-top td_block_template_1 td-post-content tagdiv-type')
            if parent_div:
                for div in parent_div:
                    content_div = div.find('div', class_='tdb-block-inner td-fix-index')

                    if content_div:
                     
                        for pre_tag in content_div.find_all('pre'):
                            pre_tag.extract()

                       
                        content = ' '.join([tag.get_text(strip=True) for tag in content_div.find_all(['p', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'ul', 'ol', 'li'])])
        
       
        return {
            'title': title,
            'content': content
        }
    else:
       
        print(f"Failed to retrieve data from {url}")
        return None


df = pd.read_excel('Input.xlsx')

extracted_data = []

for index, row in df.iterrows():
    url_id = row['URL_ID']
    url = row['URL']
    data = extract_data(url)
    if data:
        extracted_data.append(data)
        print(f"Data extracted from article {url_id}")
        print(f"Title: {data['title']}")
        print(f"Content: {data['content']}")
        print()
        title = data['title']
        content = data['content']
        file_name = os.path.join(output_folder, f"{url_id}.txt")
        with open(file_name, 'w', encoding='utf-8') as f:
            f.write(f"{title}\n\n")
            f.write(f"{content}\n")
        print(f"Article {url_id} saved as {file_name}")

print("Data extraction complete!")