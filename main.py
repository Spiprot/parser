from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager

url = 'https://reestr.nostroy.ru'
# Автоматическое получение текущей версии драйвера для браузера Chrome установленного в системе,
# не нужно скачивать и хранить его в проекте
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
# Открываем страницу с помощью драйвера
driver.get(url)


# Базовый путь для выбора страницы, в дальнейшем строка форматируется с подставлением номера страницы в [text() = '{}']
base_xpath_for_select_page = "//*[@id='members-form']/div[2]/ul//*[text() = '{}']"
# Базовый путь для выбора элемента, в дальнейшем форматируется подставлением строки tr[{}] и столбца td[{}]
base_xpath_for_element = "//*[@id='members']/table/tbody/tr[{}]/td[{}]"
# Полный xpath по которому находится телефонный номер
xpath_number = "//*[@id='block-content-open-client']/div/div[1]/div[8]/div[2]"
# Начальный словарь куда будут сохраняться данные
parse_data = dict(dict())


def get_element_by_column_in_line(current_line: int, column: int) -> str:
    try:
        element_text = driver.find_element(By.XPATH, base_xpath_for_element.format(current_line, column)).text
    except NoSuchElementException:
        pass
    return element_text


for page in range(1, 3):
    f"Перебираем диапазон от 1 до 16 страницы"
    driver.find_element(By.XPATH, base_xpath_for_select_page.format(page)).click()
    for line in range(1, 21):
        f"Перебираем диапазон от 1 до 20 строки(всего на странице)"

        # В словарь добавляем элемент с номером текущей линии parse_data[line], в которую кладем вложенный словарь с
        # параметрами строки. Строка неизменна, а столбец меняется от 1 до 6
        parse_data[line] = {
            'reg_number': get_element_by_column_in_line(line, 1),
            'full_and_abbreviation': get_element_by_column_in_line(line, 2),
            'address': get_element_by_column_in_line(line, 3),
            'subject': get_element_by_column_in_line(line, 4),
            'federal_district': get_element_by_column_in_line(line, 5),
            'status': get_element_by_column_in_line(line, 6)
        }
        # Переходим внутрь строки, чтобы получить номер телефона, кликаем по элементу с текущей строки line
        # и любым номером столбца, в данном случае столбец = 1
        driver.find_element(By.XPATH, base_xpath_for_element.format(line, 1)).click()
        # Добавляем элемент в текущую строку и новым параметром number
        parse_data[line] = {'number': driver.find_element(By.XPATH, xpath_number).text}
        # Возвращаемся на общую страницу с данными
        driver.back()

print(len(parse_data))
for item in parse_data.items():
    print(item)
