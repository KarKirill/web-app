from django.shortcuts import render # type: ignore
from .models import FileSave
from pathlib import Path

import cv2 
import pytesseract
import re

from docxtpl import DocxTemplate
from alfora.settings import MEDIA_ROOT

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
    passport(cv2.imread(f"{BASE_DIR}\\media\\upldfile\\passport\\{file_passport1}"))
    snils_ocr(cv2.imread(f"{BASE_DIR}\\media\\upldfile\\snils\\{file_snils1}"))
  context = {'name':'Kirill'}
  base_url = f"{MEDIA_ROOT}\\upldfile\\docx\\"
  asset_url = base_url + 'temp.docx'
  print(asset_url)
  tpl = DocxTemplate(asset_url)
  tpl.render(context)
  tpl.save(base_url + 'test.docx')
  return render(request, 'blank/index.html')


################################################################################################


pytesseract.pytesseract.tesseract_cmd = "D:\\tesseract\\tesseract.exe"
snils = None
surname = None
name = None
middle_name = None
date_of_birth = None
place_of_birth = ""
gender = None

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
    image = get_grayscale(image)
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

#обработка паспорта (первые страницы)

# получение серого изображения
def get_grayscale(image):
    return cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

def turn(image):
    (h, w) = image.shape[:2]
    center = (w // 2, h // 2)
    matrix = cv2.getRotationMatrix2D(center, 90, 1.0)
    rotated = cv2.warpAffine(image, matrix, (h, w))
    return rotated

# обрезаем изображение
def crop_center(img, crop_width, crop_height):
    height, width = img.shape[:2]
    
    start_x = width // 2 - crop_width // 2
    start_y = height // 2 - crop_height // 2

    end_x = start_x + crop_width
    end_y = start_y + crop_height

    cropped_img = img[start_y:end_y, start_x:end_x]

    return cropped_img



# обработка главной страницы паспорта
def passport(image):
    lst = []
    lst_help = []
    img_passport = image
    img_passport_2 = get_grayscale(img_passport) # изображение для остальной части паспорта
    img_passport = turn(img_passport)
    img_passport_1 = get_grayscale(img_passport) # изображение для серии и номера

    # обрезаем изображение
    crop_width = 600
    crop_height = 500
    img_passport_1 = crop_center(img_passport_1, crop_width, crop_height)

    # считывание серии и номера
    config = r'--oem 3 --psm 6'
    text_series_number = pytesseract.image_to_string(img_passport_1, lang='rus', config=config)
    pattern = r"(\d{2})\s(\d{2})\s(\d{6})"
    match = re.search(pattern, text_series_number)
    try:
      lst_help.append(match.group(1))
      lst_help.append(match.group(2))
      lst_help.append(match.group(3))
      series_number = "".join(lst_help)
      lst.append(series_number)
    except Exception as e:
        print(f"Некачественное изображение паспорта: {e}")
        return None
    
    text_other = pytesseract.image_to_string(img_passport_2, lang='rus', config=config)
    print(text_other)

    for i in lst:
        print(i)