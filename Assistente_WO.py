try:

    import json
    import os
    from datetime import datetime
    from os import getcwd, rename, walk
    from pathlib import Path
    from sys import platform

    import cv2
    from easygui import diropenbox
    from PIL import Image
    from pyzbar.pyzbar import decode
except Exception as e:

    print(f'I need {e}')


def file_is_exists(location):
    return Path(location).is_file()


def create_json(arq_name, dictionary):
    with open(f'{arq_name}.json', 'w', encoding='utf-8') as fp:
        json.dump(dictionary, fp, ensure_ascii=False, indent=2)


def separator():

    if platform.upper() == 'LINUX':
        return '/'
    else:
        return '\\'


def having_code(image_location):

    img_pill = Image.open(f'{image_location}')

    detectedBarcodes = decode(img_pill)

    if detectedBarcodes:
        for barcode in detectedBarcodes:

            (position_x, position_y, position_w, position_h) = barcode.rect

            if (
                position_x > 1000
                and 340 >= position_y >= 200
                and 440 >= position_w >= 280
                and 108 >= position_h >= 90
            ):
                return (True, (barcode.data).decode('utf8'))

        return (False, '')

    else:
        return (False, '')


def remove_no_code(lista_imgs):

    new_list_code = []

    if len(lista_imgs) <= 1:
        return lista_imgs

    new_list_code.append(lista_imgs[0])

    for index_code in range(1,len(lista_imgs)):

        if lista_imgs[index_code][1] == False:
            new_list_code.append(
                (
                    lista_imgs[index_code][0],
                    lista_imgs[index_code][1],
                    lista_imgs[index_code - 1][2],
                )
            )
        else:
            new_list_code.append(lista_imgs[index_code])

    return new_list_code


def insert_arq_log(texto):

    date = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    if file_is_exists('./app.log'):
        file = open('./app.log', 'a')
        file.write(f'{date} : {texto} \n')
        file.close()
    else:
        file = open('./app.log', 'w')
        file.write(f'{date} : {texto} \n')


def save_file(name, list_ims):

    im_one = list_ims[0]

    list_ims.pop(0)

    pdf1_filename = f'{name} WO.pdf'
    insert_arq_log(f'Defini o nome do pdf: {pdf1_filename}')
    im_one.save(pdf1_filename, save_all=True, append_images=list_ims)

    insert_arq_log(f'Defini o nome salvei')


def list_imgs_pil(location, list_name_imgs):

    return [Image.open(f'{location}/{img}') for img in list_name_imgs]


def app(location):

    try:
        name_imagens = tuple(walk(location))[0][2]

        name_imagens.sort()

        detect_code = remove_no_code(
            [
                (name_only_img,) + having_code(f'{location}/{name_only_img}')
                for name_only_img in name_imagens
            ]
        )

        files_dic = {detc[2]: [] for detc in detect_code}

        for code_values in detect_code:

            if len(code_values) == 0: insert_arq_log(f'Arquivos com indice vazios: {[code_values[0]]}')

            files_dic[code_values[2]] += [code_values[0]]

        for index_dic in files_dic:
            save_file(index_dic, list_imgs_pil(location, files_dic[index_dic]))

        return True
    except Exception as e:
        insert_arq_log(f'Error: {e}')
        return False


app(diropenbox())
