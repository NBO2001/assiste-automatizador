from tkinter.constants import SEPARATOR
from easygui import diropenbox

import json

from sys import platform

import os
from os import (
    walk,
    getcwd,
    rename
    )

import cv2

from pyzbar.pyzbar import decode 

from PIL import Image

from datetime import datetime

from pathlib import Path

class Assistente:

    def __init__(self):

        
        
        path = (self.separator()).join(((os.getcwd()).split(self.separator()))[:3])
        
        if not self.file_is_exists(f'{path}{self.separator()}LocalScan.json'):
            pdfs = diropenbox()
            self.create_json(f'{path}{self.separator()}LocalScan', {
                "Scan": pdfs
            })

        location = self.reading_json(f'{path}{self.separator()}LocalScan')
        
        self.g_pdfs(location['Scan'])
        pass

        
    def reading_json(self,name):
        with open(f'{name}.json', encoding='utf-8') as fp:
            data = json.load(fp)
        
        return data


    def insert_arq_log(self,texto):
    
        date = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

        if self.file_is_exists("./app.log"):
            file = open("./app.log", 'a')
            file.write(f'{date} : {texto} \n')
            file.close()
        else:
            file = open("./app.log", 'w')
            file.write(f'{date} : {texto} \n')
            file.close()


    def save_file(self,name,list_ims):

        im_one = list_ims[0]

        list_ims.pop(0)

        pdf1_filename = f'{name}.pdf'
        self.insert_arq_log(f'Defini o nome do pdf: {pdf1_filename}')
        im_one.save(pdf1_filename,save_all=True, append_images=list_ims)
        
        self.insert_arq_log(f'Defini o nome salvei')

    def g_pdfs(self,imgs_location):

        ims = list()
        for path, subpath, files in walk(imgs_location):
            for file in files:
                ims.append(file)

        ims.sort()

        pdf_list = list()
        name = ""

        for im in ims:
            self.insert_arq_log(f'Entrei na img: {im}')
            
            img = cv2.imread(f'{imgs_location}/{im}') 

            img_pill = Image.open(f'{imgs_location}/{im}')
            
            detectedBarcodes = decode(img) 
            
            if detectedBarcodes: 

                for barcode in detectedBarcodes:  
                    
                    (x, y, w, h) = barcode.rect 
                    if x > 500 and y > 200 and y < 225 and w > 280 and w < 295 and h > 65 and h < 73:
                        self.insert_arq_log(f'{barcode.rect}')
                        
                        if not len(name) or name == (barcode.data).decode('utf8'):
                            name = (barcode.data).decode('utf8')
                            pdf_list.append(img_pill)
                            self.insert_arq_log(f'Adicionou a lista: {im}')
                        else:
                            
                            self.save_file(name, pdf_list)
                            self.insert_arq_log(f'Adicionou a salvou: {name}')
                            name = (barcode.data).decode('utf8')
                            pdf_list.clear()
                            pdf_list.append(img_pill)
                            self.insert_arq_log(f'Adicionou a lista: {im}')

            else:
                pdf_list.append(img_pill)

    
    def file_is_exists(self,location):
        return Path(location).is_file()
    
    def create_json(self,arq_name,dictionary):
        with open(f'{arq_name}.json', 'w', encoding='utf-8') as fp:
            json.dump(dictionary, fp, ensure_ascii=False, indent=2)

    def separator(self):
        
        if platform.upper() == "LINUX":
            return "/"
        else:
            return "\\"




ass = Assistente()