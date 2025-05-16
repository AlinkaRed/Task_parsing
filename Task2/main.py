import os
import json
import sys
from collections import defaultdict


def main(folder_path: str, output_file: str):
    """
    Функция собирает информацию о PNG-файлах из заданной директории и сохраняет ее в структурированном формате JSON.
    folder_path: строка, представляющая путь к папке, в которой будут искаться файлы PNG.
    output_file: строка, представляющая путь к выходному JSON-файлу, в который будет сохранена собранная информация.
    """
    data = defaultdict(lambda: {
        'id': None,
        'paths': [],
        'name': None,
        'weights': []
    })

    if os.path.exists(output_file):
        with open(output_file, 'r', encoding='utf-8') as f:
            existing_data = json.load(f)
        existing_data = {i['id']: i for i in existing_data}
        data.update(existing_data)
            
    for dirpath, _, filenames in os.walk(folder_path):
        for filename in filenames:
            if filename.endswith('.png'):
                parts = filename[:-4].split('_')
                if len(parts) < 4:
                    continue

                id1 = parts[0]
                n1 = int(parts[1])
                n2 = int(parts[2])
                nameId = str(parts[3])

                data[id1]['id'] = id1
                data[id1]['paths'].append(os.path.join(dirpath, filename))
                data[id1]['name'] = nameId
                data[id1]['weights'].append([n1, n2])

    result = list(data.values())

    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(result, f, ensure_ascii=False, indent=4)


if __name__ == "__main__":
    if len(sys.argv) != 3:
         sys.exit(1)

    folder_path = sys.argv[1]
    output_file = sys.argv[2]

    main(folder_path, output_file)
    print(f"Данные успешно сохранены в файл: {output_file}")
