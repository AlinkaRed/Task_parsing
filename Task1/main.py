import os
import pymupdf
import sys


def main(folder_path: str, output_path: str):
    """
    Функция позволяет пройтись по всем PDF-файлам в указанной папке и её подпапках, 
    конвертировать каждую страницу каждого PDF в отдельное PNG-изображение,
    сохранить полученные изображения в выходной папке с сохранением исходной структуры каталогов.
    
    folder_path: строка, представляющая путь к папке, в которой будут искаться файлы PDF.
    output_path: строка, представляющая путь к выходной папке, в которой будут храниться результаты. 
    """
    
    for dirpath, _, filenames in os.walk(folder_path):
        for filename in filenames:
            if filename.endswith('.pdf'):
                full_path = os.path.join(dirpath, filename)
                
                relative_path = os.path.relpath(full_path, folder_path)
                relative_path = relative_path.replace('\\', '/')
                
                doc = pymupdf.open(full_path)
                
                for page in doc:
                    if page.rect[2] < page.rect[3]:
                        page.set_rotation(270)
                    pix = page.get_pixmap()
                    
                    output_dir = os.path.join(output_path, os.path.dirname(relative_path))
                    os.makedirs(output_dir, exist_ok=True)
                    
                    pix.save(os.path.join(output_dir, f'{os.path.splitext(filename)[0]}_page_{page.number + 1}.png'))


if __name__ == "__main__":
    if len(sys.argv) != 3:
         sys.exit(1)

    folder_path = sys.argv[1]
    output_path = sys.argv[2]

    main(folder_path, output_path)
    print(f"Данные успешно сохранены в папку: {output_path}")
