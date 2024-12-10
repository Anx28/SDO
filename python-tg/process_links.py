import subprocess
import csv
import re

def process_link(link):
    try:
        # Запускаем xeuledoc с передачей ссылки
        result = subprocess.run(['xeuledoc', link], capture_output=True, text=True)
        output = result.stdout
        error_output = result.stderr

        info = {'Link': link}

        # Проверяем, есть ли ошибки
        if result.returncode != 0:
            info['Status'] = 'Error'
            info['Error'] = error_output.strip()
            return info

        # Парсим вывод xeuledoc
        lines = output.strip().split('\n')
        for line in lines:
            line = line.strip()
            if 'Document ID :' in line:
                info['Document ID'] = line.split('Document ID :',1)[1].strip()
            elif 'Title :' in line:
                info['Title'] = line.split('Title :',1)[1].strip()
            elif 'Author :' in line:
                info['Author'] = line.split('Author :',1)[1].strip()
            elif 'Creation Time :' in line:
                info['Creation Time'] = line.split('Creation Time :',1)[1].strip()
            elif 'Last Modification :' in line:
                info['Last Modification'] = line.split('Last Modification :',1)[1].strip()
            elif '[-]' in line:
                info['Status'] = 'Error'
                info['Error'] = line.strip('[-] ').strip()
        # Если не было ошибок, статус OK
        if 'Status' not in info:
            info['Status'] = 'OK'
        return info
    except Exception as e:
        return {'Link': link, 'Status': 'Exception', 'Error': str(e)}

def main():
    # Читаем ссылки из файла
    with open('links.txt', 'r', encoding='utf-8') as f:
        links = [line.strip() for line in f if line.strip()]

    # Обрабатываем каждую ссылку
    results = []
    for link in links:
        info = process_link(link)
        results.append(info)

    # Определяем заголовки для CSV-файла
    fieldnames = set()
    for result in results:
        fieldnames.update(result.keys())
    fieldnames = list(fieldnames)

    # Сохраняем результаты в CSV-файл
    with open('results.csv', 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for result in results:
            writer.writerow(result)

    print('Обработка завершена. Результаты сохранены в файле results.csv')

if __name__ == '__main__':
    main()
