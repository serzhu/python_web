import re
from threading import Thread, Semaphore
import logging
import argparse
from  shutil import unpack_archive, move, copyfile
from pathlib import Path

folders = {'archives':{'ZIP', 'GZ', 'TAR'},
           'video':{'AVI', 'MP4', 'MOV', 'MKV'},
           'audio':{'MP3', 'OGG', 'WAV', 'AMR'}, 
           'documents':{'DOC', 'DOCX', 'TXT', 'PDF', 'XLSX', 'XLS', 'DJVU'}, 
           'images':{'JPEG', 'PNG', 'JPG', 'SVG', 'BMP'},
           'scripts':{'SH', 'BAT'},
           'unknown':{}
           }

parser = argparse.ArgumentParser(description="Sorting folder")
parser.add_argument("--source", "-s", help="Source folder", required=True)

args = vars(parser.parse_args())

source = Path(args.get("source"))

file_list = []
folders_list = []
ext_list = [ext for item in list(folders.values()) for ext in item]

def make_file_list(path: Path):
    folders_list.append(source)
    for el in path.glob('**/*'):
        if el.is_file(): 
            file_list.append(el)
        elif el.is_dir():
            folders_list.append(el)
#    print(file_list, folders_list)

def normalize(old_name: str) -> str:
    ru = ('а', 'б', 'в', 'г', 'д', 'е', 'ё', 'ж', 'з', 'и', 'й', 'к', 'л', 'м', 'н', 'о', 'п',
          'р', 'с', 'т', 'у', 'ф', 'х', 'ц', 'ч', 'ш', 'щ', 'ъ', 'ы', 'ь', 'э', 'ю', 'я')
    en = ('a', 'b', 'v', 'g', 'd', 'e', 'e', 'zh','z', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p',
          'r', 's', 't', 'u', 'f', 'h', 'ts','ch','sh','sch','\'','y','\'','e', 'ju', 'ya')
    dict = {}
    for r, e in zip(ru, en):
        dict[ord(r)] = e
        dict[ord(r.upper())] = e.upper()
    new_name = re.sub(r'[^A-Za-z0-9.!]', '_', old_name.translate(dict))  # tranlslit names and substitute symbols except ! and . to _ 
    return new_name

def extract_archive(path: Path):
    unpack_archive(path, source / 'archives')
    logging.debug(f'{path.name} unpacked to {source}/archives/{path.stem}')
    path.unlink()                

def sort_files(path: Path, condition):
    with condition:
        for item in path.iterdir():
            if item.is_file():
                extention = item.suffix.lstrip('.').upper()     # get file extention
                if extention not in ext_list:
                    try:
                        dst = source / 'unknown'
                        dst.mkdir(exist_ok=True, parents=True)
                        logging.debug(f'start moving  {item.name}')
                        #copyfile(item, dst / f'{normalize(item.stem) + item.suffix}')
                        logging.debug(f'stop moving  {item.name}\n')
                        move(item, dst / f'{normalize(item.stem) + item.suffix}')
                    except OSError as err:
                        logging.error(err)                
                else:
                    for fold,ext in folders.items():
                        if extention in ext:
                            try:
                                dst = source / fold
                                dst.mkdir(exist_ok=True, parents=True)
                                logging.debug(f'start moving  {item.name}')
                                #copyfile(item, dst / f'{normalize(item.stem) + item.suffix}')
                                logging.debug(f'stop moving  {item.name}\n')
                                move(item, dst / f'{normalize(item.stem) + item.suffix}')
                            except OSError as err:
                                logging.error(err)

#remove empty folders
def rm_empty_dirs(path: Path):
    for item in path.iterdir():
        if item.is_dir(): 
            if any(item.iterdir()):
                rm_empty_dirs(item)
            else:
                item.rmdir()
                logging.debug(f'Deleting ITEM: {item}')
    try:
        path.rmdir()
        logging.debug(f'Deleting ROOT: {path}')
    except OSError:
        pass
            

if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG, format="%(threadName)s:  %(message)s")

    make_file_list(source)

# Sort files by moving to extention folders using threads
    threads = []
    pool = Semaphore(3)
    for folder in folders_list:
        th = Thread(target=sort_files, args=(folder, pool,))
        th.start()
        threads.append(th)
    [th.join() for th in threads]

# Unpack archives using threads
    for arc in (source / 'archives').iterdir():
        th = Thread(name=f'Thread for arc {arc}', target=extract_archive, args=(arc,))
        th.start()
        threads.append(th)
    [th.join() for th in threads]

# Remove empty directories
    rm_empty_dirs(source)
