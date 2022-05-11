from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.firefox import GeckoDriverManager
from bitrix24 import *

from NewCRMcheck import new_CRM_check

"""######################### Подготовка драйвера и сайта для парсинга ###################################"""
url = 'https://reestr.nostroy.ru/reestr'
# Автоматическое получение текущей версии драйвера для браузера Chrome установленного в системе,
# не нужно скачивать и хранить его в проекте
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
# firefox_driver = webdriver.Firefox(service=Service(GeckoDriverManager().install()))
# Во весь экран
driver.maximize_window()
# firefox_driver.maximize_window()
# Время ожидания любого элемента, если переход между страницами тормозит
driver.implicitly_wait(1)
# firefox_driver.implicitly_wait(1)
# Открываем страницу с помощью драйвера
driver.get(url)
# firefox_driver.get(url)
"""#######################*********************************************####################################"""

# Базовый путь для выбора страницы, в дальнейшем строка форматируется с подставлением номера страницы в [text() = '{}']
base_xpath_for_select_page = "//*[@id='members-form']/div[2]/ul//*[text() = '{}']"
# Базовый путь для выбора элемента, в дальнейшем форматируется подставлением строки tr[{}] и столбца td[{}]
base_xpath_for_element = "//*[@id='members']/table/tbody/tr[{}]/td[{}]"
# Полный xpath по которому находится телефонный номер
xpath_number = "//*[text()='Номер контактного телефона:']/following::td[1]"
xpath_ceo = "//*[@id='tabs-1']/table/tbody/tr[15]/td"

# Начальный словарь куда будут сохраняться данные
parse_data = dict(dict())


def get_element_by_column_in_line(current_line: int, column: int) -> str:
    f""" Метод принимающий в себя номер строки и столбца и возвращающий текст элемента по этому пути
    """
    return driver.find_element(By.XPATH, base_xpath_for_element.format(current_line, column)).text.strip()


pop_strings = 0

for page in range(1, 2):
    f"Перебираем диапазон от 1 до 16 страницы(всего страниц)"
    driver.find_element(By.XPATH, base_xpath_for_select_page.format(page)).click()
    for line in range(1, 21):
        f"Перебираем диапазон от 1 до 20 строки(всего на странице)"
        try:
            # Проверяем есть ли текущая строка line на странице (столбец выбран любой, в данном случае 1)
            # Если строка найдена, то наполняем словарь, иначе ничего не делаем
            driver.find_element(By.XPATH, base_xpath_for_element.format(line, 1))
            if not new_CRM_check(get_element_by_column_in_line(line, 3)):
                # В словарь добавляем элемент с номером текущей линии parse_data[line], в которую кладем вложенный
                # словарь с параметрами строки. Строка неизменна, а столбец меняется от 1 до 6. (page-1)*20 учитывает
                # текущую страницу
                parse_data[line + (page - 1) * 20 - pop_strings] = {
                    'full_name': get_element_by_column_in_line(line, 1),
                    'abbreviation': get_element_by_column_in_line(line, 2),
                    'inn': get_element_by_column_in_line(line, 3),
                    'ogrn': get_element_by_column_in_line(line, 4),
                    'status': get_element_by_column_in_line(line, 5),
                    'type': get_element_by_column_in_line(line, 6),
                    'reg_number': get_element_by_column_in_line(line, 7)
                }

                full_company_name = get_element_by_column_in_line(line, 1)
                short_company_name = get_element_by_column_in_line(line, 2)
                company_inn = get_element_by_column_in_line(line, 3)

                # Переходим внутрь строки, чтобы получить номер телефона, кликаем по элементу с текущей строки line
                # и любым номером столбца, в данном случае столбец = 1
                driver.find_element(By.XPATH, base_xpath_for_element.format(line, 1)).click()
                # Добавляем элемент в текущую строку и новым параметром number
                parse_data[line + (page - 1) * 20 - pop_strings]['number'] = driver.find_element(
                    By.XPATH, xpath_number
                ).text
                parse_data[line + (page - 1) * 20 - pop_strings]['ceo'] = driver.find_element(By.XPATH, xpath_ceo).text
                company_phone = driver.find_element(By.XPATH, xpath_number).text
                boss_full_name = driver.find_element(By.XPATH, xpath_ceo).text
                # boss_last_name, boss_first_name, boss_second_name = boss_full_name.split()[1:4]
                assignLead(
                    company_inn=company_inn,
                    boss_full_name=boss_full_name,
                    # boss_last_name=boss_last_name,
                    # boss_first_name=boss_first_name,
                    # boss_second_name=boss_second_name,
                    full_company_name=full_company_name,
                    short_company_name=short_company_name,
                    company_phone=company_phone,
                )
                # Возвращаемся на общую страницу с данными
                driver.back()
            else:
                pop_strings += 1
        except NoSuchElementException:
            pass

# Вывод всех данных
for item in parse_data.items():
    print(item)

# Вывод конкретной спарсенной строки
print(parse_data[1])

# Вывод количества организаций ИНН которых уже было в системе и мы их не записали
print(pop_strings)

# Вывод конкретного параметра из спарсенной строки
print(parse_data[1]['ceo'])

# Закрываем драйвер после выполнения программы
driver.quit()
# firefox_driver.quit()

for string in parse_data.items():
    for item in string:
        print(item)