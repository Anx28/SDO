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
            elif 'Name :' in line:
                info['Owner Name'] = line.split(':', 1)[1].strip()
            elif 'Email :' in line:
                info['Owner Email'] = line.split(':', 1)[1].strip()
        
        # Статус документа
        info['Status'] = 'OK'
        return info

    except Exception as e:
        return {'Link': link, 'Status': 'Exception', 'Error': str(e)}

def main():
    # Читаем ссылки из файла
    with open('links.txt', 'r', encoding='utf-8') as f:
        all_links = [line.strip() for line in f if line.strip()]
    
    # Удаляем дубликаты
    unique_links = list(set(all_links))
    print(f'Обнаружено {len(all_links)} ссылок. Уникальных ссылок: {len(unique_links)}.')

    # Обрабатываем каждую уникальную ссылку
    results = []
    for link in unique_links:
        info = process_link(link)
        # Удаляем Public Access из словаря
        info.pop('Public Access', None)
        results.append(info)

    # Определяем порядок столбцов
    ordered_columns = ['Link', 'Owner Email', 'Creation Time', 'Last Modification']
    # Добавляем остальные колонки
    all_columns = set().union(*results)
    for col in all_columns:
        if col not in ordered_columns:
            ordered_columns.append(col)

    # Запись в CSV
    with open('results.csv', 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=ordered_columns)
        writer.writeheader()
        for result in results:
            writer.writerow(result)

    print('Обработка завершена. Результаты сохранены в файле results.csv')

if __name__ == '__main__':
    main()
