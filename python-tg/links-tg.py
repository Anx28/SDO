import json
import re
import os

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

def find_json_files(directory):
    # Поиск всех JSON-файлов в указанной директории
    return [file for file in os.listdir(directory) if file.endswith('.json')]

def main():
    # Текущая директория, где находится скрипт
    current_directory = os.path.dirname(os.path.abspath(__file__))
    
    # Поиск всех JSON-файлов в текущей директории
    json_files = find_json_files(current_directory)
    
    all_links = []
    
    for json_file in json_files:
        file_path = os.path.join(current_directory, json_file)
        with open(file_path, 'r', encoding='utf-8') as f:
            try:
                data = json.load(f)
                links = extract_links(data)
                all_links.extend(links)
            except json.JSONDecodeError:
                print(f"Файл {json_file} содержит ошибку и не был обработан.")
    
    # Запись ссылок в файл links.txt
    output_file = os.path.join(current_directory, 'links.txt')
    with open(output_file, 'w', encoding='utf-8') as f:
        for link in all_links:
            f.write(link + '\n')
    
    print(f"Ссылки успешно записаны в файл {output_file}")

if __name__ == "__main__":
    main()
