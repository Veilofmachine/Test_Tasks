import requests
import pandas as pd
import xml.etree.ElementTree as ET

# Функция для получения описания столбцов из XSD схемы
def get_column_descriptions(xsd_url):
    response = requests.get(xsd_url)
    tree = ET.fromstring(response.content)
    namespaces = {'xs': 'http://www.w3.org/2001/XMLSchema'}
    elements = tree.findall('.//xs:element', namespaces)
    descriptions = {}
    for element in elements:
        name = element.get('name')
        annotation = element.find('.//xs:annotation/xs:documentation', namespaces)
        if annotation is not None:
            descriptions[name] = annotation.text
    return descriptions

# Функция для загрузки и преобразования данных в DataFrame
def fetch_currency_data(xml_url, xsd_url):
    # Получение данных
    response = requests.get(xml_url)
    root = ET.fromstring(response.content)
    
    # Получение описаний столбцов
    descriptions = get_column_descriptions(xsd_url)
    
    # Парсинг данных
    data = []
    for valute in root.findall('.//Valute'):
        entry = {child.tag: child.text for child in valute}
        entry['Date'] = root.get('Date')
        data.append(entry)
    
    # Создание DataFrame
    df = pd.DataFrame(data)
    
    # Фильтрация нужных валют
    currencies = ['USD', 'EUR', 'GBP', 'CNY']
    df = df[df['CharCode'].isin(currencies)]
    
    # Переименование столбцов согласно описаниям из XSD
    df.rename(columns=descriptions, inplace=True)
    
    return df

# URL API и XSD схемы
xml_url = 'http://www.cbr.ru/scripts/XML_daily.asp'
xsd_url = 'https://cbr.ru/StaticHtml/File/92172/ValCurs.xsd'

# Получение и вывод данных
currency_df = fetch_currency_data(xml_url, xsd_url)
print(currency_df)