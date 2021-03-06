# Требуется Google Chrome
# Установить ChromeDriver соответсвующей версии Google Chrome в C:/Program Files/chromedriver/ 
# В архивах в папке src для каждой OS ChromeDriver версии 86.0.4240.22 

from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.common.keys import Keys

from parsel import Selector

import time
from pathlib import Path
import urllib
import os

options = webdriver.ChromeOptions()
options.add_experimental_option("prefs", {"download.default_directory": os.path.join(os.getcwd(), 'tmp')})
options.add_argument('headless')
options.add_argument('window-size=1920x1080')
# Установить ChromeDriver соответсвующей версии Google Chrome в C:/Program Files/chromedriver/ 
# В архиве ChromeDriver версии 86.0.4240.22 
driver = webdriver.Chrome(executable_path='C:/Program Files/chromedriver/chromedriver.exe', options=options)
sel = Selector(text=driver.page_source)

url = 'https://egrul.nalog.ru/index.html'

def enter():
    global driver, sel, url
    driver.get(url)
    sel = Selector(text=driver.page_source)

def close():
    global driver
    driver.close()

# Стоит оговорится, что если дается имя, то скачивается первый pdf

def paste_id_or_name_and_get_pdf(id_or_name):
    global driver
    driver.find_element_by_id('query').send_keys(id_or_name)
    driver.find_element_by_id('btnSearch').click()
    time.sleep(3)
    driver.find_elements_by_xpath('/html/body//div[3]/button')[0].click()

def get_pdf(id_or_name):
    enter()
    path = os.path.join(os.getcwd(), 'tmp')
    for e in os.listdir(path):
        try:
            os.remove(os.path.join(path, e))
        except Exception:
            raise('Закройте все открытые pdf-ники в папке tmp')
    try:
        paste_id_or_name_and_get_pdf(id_or_name)
    except Exception:
        close()
        return
    time.sleep(3)
    close()
    os.rename(os.path.join(path, os.listdir(path)[0]), os.path.join(path, 'temp.pdf'))

import io
import getpass

from pdfminer.converter import TextConverter
from pdfminer.pdfinterp import PDFPageInterpreter
from pdfminer.pdfinterp import PDFResourceManager
from pdfminer.pdfpage import PDFPage
from pdfminer.layout import LAParams

def extract_text_from_pdf(pdf_path):
    resource_manager = PDFResourceManager()
    fake_file_handle = io.StringIO()
    converter = TextConverter(resource_manager, fake_file_handle)
    page_interpreter = PDFPageInterpreter(resource_manager, converter)

    with open(pdf_path, 'rb') as fh:
        for page in PDFPage.get_pages(fh,
                                      caching=True,
                                      check_extractable=True):
            page_interpreter.process_page(page)

        text = fake_file_handle.getvalue()
        text = text + ' '

    converter.close()
    fake_file_handle.close()
 
    if text:
        return text

def convert_pdf_to_txt(path):
    rsrcmgr = PDFResourceManager()
    retstr = io.StringIO()
    laparams = LAParams()
    device = TextConverter(rsrcmgr, retstr, laparams=laparams)
    fp = open(path, 'rb')
    interpreter = PDFPageInterpreter(rsrcmgr, device)
    password = ""
    maxpages = 0
    caching = True
    pagenos = set()

    for page in PDFPage.get_pages(fp, pagenos, maxpages=maxpages,
                                  password=password,
                                  caching=caching,
                                  check_extractable=True):
        interpreter.process_page(page)

    text = retstr.getvalue()

    fp.close()
    device.close()
    retstr.close()
    path___ = os.path.join(os.getcwd(), 'tmp')
    for e in os.listdir(path___):
        try:
            os.remove(os.path.join(path___, e))
        except Exception:
            raise('Закройте все открытые pdf-ники в папке tmp')
    return text

def from_pdf_to_text():
    # dir_path = os.path.join(os.getcwd(), 'tmp')
    pdf_path = os.path.join(os.getcwd(), 'tmp', 'temp.pdf')
    try:
        res = convert_pdf_to_txt(pdf_path)
    except Exception:
        return ""
    return res

def make_data(text):
    data = {}
    if text == "":
        return data
    sep=''
    text2 = text.split()
    for i in range(0, len(text2)):
        if text2[i] == 'ОГРНИП' and text2[i] not in data:
            data[text2[i]] = sep.join(text2[i + 1: i + 16])
        if text2[i] == 'Сведения' and text2[i + 1] == 'о' and text2[i + 2] == "гражданстве":
            data['Фамилия'] = text2[i - 6].capitalize()
            data['Имя'] = text2[i - 5].capitalize()
            data['Отчество'] = text2[i - 4].capitalize()
            data['Пол'] = text2[i - 3].capitalize()
            data['ГРН'] = text2[i - 2].capitalize()
    data['Деятельности'] = []
    text3 = text.split('\n\n')
    index = 0
    for e in text3:
        if (('деятельность' in e.lower() or 'научные' in e.lower() or 'исследование' in e.lower() or 'исследования' in e.lower() \
            or 'торговля' in e.lower() or 'деятельности' in e.lower() or 'предоставление' in e.lower() or 'предоставления' in e.lower()) \
            and '0' <= e[0] <= '9' and 'грн' not in e.lower() and 'код' not in e.lower()):
            data['Деятельности'] += [' '.join(e.split('\n'))]
        if ('(ИНН)' in e.split(' ')):
            data['ИНН'] = text3[index + 2]
        index += 1
    for i in range(len(data['Деятельности'])):
        e = data['Деятельности'][i].split(' ')
        new_e = {
            'Код' : e[0],
            'Наименование' : ' '.join(e[1:len(e) - 2:1]),
            'ГРН' : e[len(e) - 2],
            'Дата внесения в ЕГРИП' : e[len(e) - 1]
        }
        data['Деятельности'][i] = new_e
    data['Основная деятельность'] = data['Деятельности'][0]
    data['Деятельности'] = data['Деятельности'][1::]
    return data



def get_data(name_or_id):
    get_pdf(name_or_id)
    return make_data(from_pdf_to_text())

def main():
    print(get_data('773370633582'))

if __name__ == '__main__':
    main()