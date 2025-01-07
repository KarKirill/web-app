from django.shortcuts import render # type: ignore
from .models import FileSave
from pathlib import Path

import cv2 
import numpy as np
import matplotlib as plt
import pytesseract 


def index(request):
  file_passport1 = request.FILES.get('file_passport')
  file_snils1 = request.FILES.get('file_snils')
  file_lvplc1 = request.FILES.get('file_lvplc')
  if file_passport1 and file_snils1 and file_lvplc1:
    FileSave.objects.create (
      file_passport = file_passport1,
      file_snils = file_snils1,
      file_lvplc = file_lvplc1
    )
    BASE_DIR = Path(__file__).resolve().parent.parent
    image = cv2.imread(f"{BASE_DIR}\\media\\upldfile\\snils\\{file_snils1}")
    
    snils_ocr(image)

  return render(request, 'blank/index.html')


################################################################################################


pytesseract.pytesseract.tesseract_cmd = "D:\\Nikita\\Tesseract_OSR\\tesseract.exe"
snils = None
surname = None
name = None
middle_name = None
date_of_birth = None
place_of_birth = ""
gender = None

# Перевод изображения в серые тона и выровнить его
def do_grey_img(image):
    # Серый
    image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    _, img_bin = cv2.threshold(image, 128, 255, cv2.THRESH_BINARY_INV)

    return image

# Считывание текста с изображения
def ocr(image):
    text = pytesseract.image_to_string(image, lang='rus')
    return text

def snils_ocr(image):
    global snils
    global surname
    global name
    global middle_name
    global date_of_birth
    global place_of_birth
    global gender
    snils = None
    surname = None
    name = None
    middle_name = None
    date_of_birth = None
    place_of_birth = ""
    gender = None
    image = do_grey_img(image)
    list_snils = ocr(image)
    list_snils = list_snils.strip().splitlines()
    count = 0
    for i in range(len(list_snils)):
        if snils is None and list_snils[i] and list_snils[i][0].isdigit() and count == 0:  # Проверка на цифру в начале и, что item не пустой
            snils = list_snils[i]
            snils = snils.strip()
            count += 1
            
        elif surname is None and " " in list_snils[i] and count == 1: # Проверка на пробел
            space_index = list_snils[i].find(" ")
            surname = list_snils[i][space_index:]
            surname = surname.strip()
            count += 1
        
        elif name is None and count == 2 and list_snils[i]:
            name = list_snils[i]
            name = name.strip()
            count += 1

        elif middle_name is None and count == 3 and list_snils[i]:
            middle_name = list_snils[i]
            middle_name = middle_name.strip()
            count += 1

        elif date_of_birth is None and list_snils[i] and count == 4:
            for j, char in enumerate(list_snils[i]):  # Поиск первой цифры в строке
                if char.isdigit():
                    date_of_birth = list_snils[i][j:]
                    date_of_birth = date_of_birth.strip()
                    count += 1
                    break 
        
        elif count > 4 and count !=6 and list_snils[i]:
            if "Пол" not in list_snils[i]:
                place_of_birth += list_snils[i]
            elif gender is None and " " in list_snils[i]:
                space_index = list_snils[i].find(" ")
                gender = list_snils[i][space_index:]
                gender = gender.strip()
                gender = gender.strip()
                count += 1
    print("---------------------------------------------------------")
    print(snils)
    print(surname)
    print(name)
    print(middle_name)
    print(date_of_birth)
    print(place_of_birth)
    print(gender)
    print("---------------------------------------------------------")

    return

#####################################################################################################