from zeep import Client
import matplotlib.pyplot as plt
import pandas as pd

# URL WSDL для SOAP сервиса ЦБ РФ
wsdl_url = 'http://www.cbr.ru/DailyInfoWebServ/DailyInfo.asmx?WSDL'

# Создание клиента SOAP
client = Client(wsdl_url)

# Даты для запроса
start_date = '2023-01-01'
end_date = '2024-06-30'

# Выполнение запроса к SOAP сервису
response = client.service.KeyRate(fromDate=start_date, ToDate=end_date)

# Парсинг данных
data = []
for item in response._value_1._value_1:
    date = item['KR']['DT']  # Изменено для доступа к дате
    rate = item['KR']['Rate']  # Уже правильно для доступа к ставке
    data.append({'Date': date, 'Rate': rate})

# Создание DataFrame
df = pd.DataFrame(data)

# Преобразование типов с преобразованием в UTC
#df['Date'] = pd.to_datetime(df['Date']).dt.tz_convert('UTC').dt.tz_localize(None)
df['Date'] = pd.to_datetime(df['Date'], utc=True)
df['Rate'] = pd.to_numeric(df['Rate'])

# Построение графика
plt.figure(figsize=(10, 5))
plt.plot(df['Date'], df['Rate'], marker='o', linestyle='-', color='b')
plt.title('Изменение ключевой ставки ЦБ РФ с 1 января 2023 по 30 июня 2024')
plt.xlabel('Дата')
plt.ylabel('Ключевая ставка (%)')
plt.grid(True)
plt.savefig('fig_1.png')
plt.show()