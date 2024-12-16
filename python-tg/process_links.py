import subprocess
import csv

def process_link(link):
    try:
        # Запускаем xeuledoc
        result = subprocess.run(['xeuledoc', link], capture_output=True, text=True)
        output = result.stdout
        error_output = result.stderr

        info = {'Link': link}

        # Проверка на ошибки
        if result.returncode != 0:
            info['Status'] = 'Error'
            info['Error'] = error_output.strip()
            return info

        # Парсим вывод
        lines = output.strip().split('\n')
        for line in lines:
            line = line.strip()
            if 'Document ID :' in line:
                info['Document ID'] = line.split(':', 1)[1].strip()
            elif 'Creation date :' in line:
                info['Creation Time'] = line.split(':', 1)[1].strip()
            elif 'Last edit date :' in line:
                info['Last Modification'] = line.split(':', 1)[1].strip()
            elif 'Public permissions :' in line:
                info['Public Access'] = 'Yes' if 'reader' in line.lower() else 'No'
            elif 'Name :' in line:
                info['Owner Name'] = line.split(':', 1)[1].strip()
            elif 'Email :' in line:
                info['Owner Email'] = line.split(':', 1)[1].strip()
        
        # Статус документа
        if 'Public Access' not in info:
            info['Public Access'] = 'No'
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

    # Запись в CSV
    with open('results.csv', 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for result in results:
            writer.writerow(result)

    print('Обработка завершена. Результаты сохранены в файле results.csv')

if __name__ == '__main__':
    main()
