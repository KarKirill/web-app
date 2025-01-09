from django.shortcuts import render # type: ignore
from .models import FileSave, Clinic
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
    passport_ocr(cv2.imread(f"{BASE_DIR}\\media\\upldfile\\passport\\{file_passport1}"))
    snils_ocr(cv2.imread(f"{BASE_DIR}\\media\\upldfile\\snils\\{file_snils1}"))
    passport_home_ocr(cv2.imread(f"{BASE_DIR}\\media\\upldfile\\live_place\\{file_lvplc1}"))

    context = {'surname':f'{surname}', 'name':f'{name}', 'middle_name':f'{middle_name}', 'gender':f'{gender}',
                'date_of_birth':f'{date_of_birth}', 'passport_date':f'{passport_date}', 'passport_place':f'{passport_place}',
                'departament_code':f'{departament_code}', 'place_of_residence':f'{place_of_residense}',
                'snils':f'{snils}', 'passport':f'{passport}', 'place_of_birth':f'{place_of_birth}'}
    base_url = f"{MEDIA_ROOT}\\upldfile\\docx\\"
    asset_url = base_url + 'temp.docx'
    print(asset_url)
    tpl = DocxTemplate(asset_url)
    tpl.render(context)
    tpl.save(base_url + 'test.docx')

    Clinic.objects.create (
        surname = surname,
        name = name,
        middle_name = middle_name,
        gender = gender,
        date_of_birth = date_of_birth,
        passport_date = passport_date,
        passport_place = passport_place,
        departament_code = departament_code,
        place_of_residence = place_of_residense,
        snils = snils,
        passport = passport,
        place_of_birth = place_of_birth
    )

  man = Clinic.objects.all()
  return render(request, 'blank/index.html', {'man': man})


################################################# ФУНКЦИИ ###################################################

# pytesseract.pytesseract.tesseract_cmd = "D:\\Nikita\\Tesseract_osr\\tesseract.exe"
# pytesseract.pytesseract.tesseract_cmd = "D:\\Programming\\Tesseract\\tesseract.exe"
pytesseract.pytesseract.tesseract_cmd = "D:\\tesseract\\tesseract.exe"
snils = None
surname = None
name = None
middle_name = None
date_of_birth = None
place_of_birth = ""
place_of_residense = ""
gender = None
passport = ""
passport_place = ""
passport_date = ""
departament_code = ""


# Считывание текста с изображения
def ocr(image):
    text = pytesseract.image_to_string(image, lang='rus')
    return text

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

# для применения порога
def thresholding(image):
    return cv2.adaptiveThreshold(image, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 1201, 110)


############################################## СНИЛС ##################################################

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

############################################# ПАСПОРТ ########################################################

def passport_ocr(image):
    global passport
    global passport_place
    global passport_date
    global departament_code
    passport = ""
    passport_place = ""
    passport_date = ""
    departament_code = ""

    lst_help = []
    img_passport = image
    img_passport_2 = get_grayscale(img_passport) # изображение для остальной части паспорта
    img_passport = turn(img_passport)
    img_passport_1 = get_grayscale(img_passport) # изображение для серии и номера
    img_passport_2 = thresholding(img_passport_2)
    height, width = img_passport_2.shape[:2]
    img_passport_2 = img_passport_2[0:int(height/2), 0:int(width/1.1)]

    # обрезаем изображение
    crop_width = 600
    crop_height = 500
    img_passport_1 = crop_center(img_passport_1, crop_width, crop_height)

    # считывание серии и номера
    config = r'--oem 3 --psm 6'
    text_series_number = pytesseract.image_to_string(img_passport_1, lang='rus', config=config)
    pattern = r"(\d{2})\s(\d{2})\s(\d{6})"
    match = re.search(pattern, text_series_number)
    lst_help.append(match.group(1))
    lst_help.append(match.group(2))
    lst_help.append(match.group(3))
    series_number = "".join(lst_help)
    passport = series_number

    # считывание всего остального   
    text_other = pytesseract.image_to_string(img_passport_2, lang='rus', config=config)

    try:
        # считывание кем выдан
        pattern_who = r"([А-Я\s]+)"
        match_who = re.search(pattern_who, text_other)
        passport_place = match_who.group(0).strip()  
    except Exception as e:
        print(f"Некачественное изображение кем выдан: {e}")
        return None
    
    try:
        # считывание даты выдачи
        pattern_date = r"(\d{2})\.(\d{2})\.(\d{4})"
        match_date = re.search(pattern_date, text_other)
        passport_date = match_date.group(0)
    except Exception as e:
        print(f"Некачественное изображение даты: {e}")
        return None
    
    
    # считывание кода подразделения
    pattern_kod = r"\d{3}-\d{3}"
    match_kod = re.search(pattern_kod, text_other)
    departament_code = match_kod.group(0)

    # вывод всех считанных данных
    print(passport)
    print(passport_place)
    print(passport_date)
    print(departament_code)




############################################# МЕСТО ЖИТЕЛЬСТВА ##################################################

def passport_home_ocr(image):
    global place_of_residense
    place_of_residense = ""

    height, width = image.shape[:2]
    image = image[0:int(height/2), 0:width]

    image = get_grayscale(image)
    list_passport_home = ocr(image)
    list_passport_home = list_passport_home.strip().splitlines()

    count = 0
    for i in range(len(list_passport_home)):
        if count == 0 and "ОБЛ" in list_passport_home[i]:
            list_home = list_passport_home[i]
            list_home = list_home.strip()

            space_index = list_home.find(" ")
            element_place = list_home[space_index:]
            element_place = element_place.strip()

            place_of_residense += "ОБЛ. "
            place_of_residense += element_place
            count += 1
        elif count == 1 and "Р-Н" in list_passport_home[i]:
            list_home = list_passport_home[i]
            list_home = list_home.strip()

            space_index = list_home.find(" ")
            element_place = list_home[space_index:]
            element_place = element_place.strip()
            
            place_of_residense += ", Р-Н. "
            place_of_residense += element_place
            count += 1

        elif count == 2 and "Г" in list_passport_home[i]:
            list_home = list_passport_home[i]
            list_home = list_home.strip()

            space_index = list_home.find(" ")
            element_place = list_home[space_index:]
            element_place = element_place.strip()
            
            place_of_residense += ", Г. "
            place_of_residense += element_place
            count += 1

        elif count == 3 and "УЛ" in list_passport_home[i]:
            list_home = list_passport_home[i]
            list_home = list_home.strip()

            space_index = list_home.find(". ")
            element_place = list_home[space_index+2:]
            element_place = element_place.strip()
            
            place_of_residense += ", УЛ. "
            place_of_residense += element_place
            count += 1

        elif count == 4 and list_passport_home[i]:
            place_of_residense += " "
            place_of_residense += list_passport_home[i].strip()
            count += 1

    print("--------------------------------------")
    print(place_of_residense)
    print("--------------------------------------")

    return