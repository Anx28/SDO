import json
import re

def extract_links(data):
    links = []
    if isinstance(data, dict):
        for key, value in data.items():
            links.extend(extract_links(value))
    elif isinstance(data, list):
        for item in data:
            links.extend(extract_links(item))
    elif isinstance(data, str):
        # Поиск ссылок на Google документы или таблицы
        pattern = r'https://docs\.google\.com/(?:document|spreadsheets)/d/[^\s"\'<>]+'
        matches = re.findall(pattern, data)
        links.extend(matches)
    return links

filename = 'result.json'

with open(filename, 'r', encoding='utf-8') as f:
    data = json.load(f)

links = extract_links(data)

print("Найдены следующие ссылки на Google документы и таблицы:")
for link in links:
    print(link)
