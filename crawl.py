import requests
from bs4 import BeautifulSoup
import os
import time
import random
import re
import sys

def get_html(url):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'}
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        return response.text
    else:
        print(f"Error: Received status code {response.status_code} for URL: {url}")
        return None

def get_chapter_urls(url):
    html = get_html(url)
    if html:
        match = re.search(r'Số chương: (\d+)', html)
        if match:
            total_chapters = int(match.group(1))
            chapter_urls = [f'{url}/chuong-{i}' for i in range(1, total_chapters + 1)]
            return chapter_urls
        
        match = re.search(r'(\d+) chương', html)
        if match:
            total_chapters = int(match.group(1))
            chapter_urls = [f'{url}/chuong-{i}' for i in range(1, total_chapters + 1)]
            return chapter_urls
        
        match = re.search(r'Độ dài: (\d+)', html)
        if match:
            total_chapters = int(match.group(1))
            chapter_urls = [f'{url}/chuong-{i}' for i in range(1, total_chapters + 1)]
            return chapter_urls


    print(f"Error: Could not find chapter URLs for {url}")
    return None

def get_chapter_content(url):
    html = get_html(url)
    if html is None:
        print(f"Error: Could not retrieve HTML content for URL: {url}")
        return None, None
    soup = BeautifulSoup(html, 'html.parser')
    title = soup.find('h1').text if soup.find('h1') else None
    content = soup.find('div', class_='chapter-c').text if soup.find('div', class_='chapter-c') else None
    if content is None:
        print(f"Error: Could not parse content for URL: {url}")
    return title, content

def save_chapter(title, content, path):
    with open(path, 'a', encoding='utf-8') as file:
        # file.write(title + '\n')
        file.write(content + '\n\n')

def crawl(url, path):
    chapter_urls = get_chapter_urls(url)
    if chapter_urls:
        for chapter_url in chapter_urls:
            title, content = get_chapter_content(chapter_url)
            if title and content:
                save_chapter(title, content, path)
                print(f'Saved: {title}')
                time.sleep(random.randint(1, 3))
            else:
                print(f'Error: Could not get content for {chapter_url}')
    else:
        print('Error: No chapter URLs found')

def main():
    name = 'xuan-ha-thu-dong-roi-lai-xuan'
    url = 'https://truyenfull.io/' + name
    path = f'./stories/{name}.txt'
    if os.path.exists(path):
        os.remove(path)
    crawl(url, path)

if __name__ == '__main__':
    main()