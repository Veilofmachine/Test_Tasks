import requests
from bs4 import BeautifulSoup
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.image as mpimg

# URL страницы
url = "https://www.cbr.ru/hd_base/mkr/mkr_base/?UniDbQuery.Posted=True&UniDbQuery.From=01.01.2023&UniDbQuery.To=30.06.2024&UniDbQuery.st=HR&UniDbQuery.st=MB&UniDbQuery.ob=OB_MIACR_IG&UniDbQuery.ob=OB_MIACR_B&UniDbQuery.Currency=-1&UniDbQuery.sk=Dd1_&UniDbQuery.sk=Dd7&UniDbQuery.sk=Dd30&UniDbQuery.sk=Dd90&UniDbQuery.sk=Dd180&UniDbQuery.sk=Dd360"

# Отправляем HTTP-запрос GET
response = requests.get(url)


if response.status_code == 200:
    # Создаем объект BeautifulSoup
    soup = BeautifulSoup(response.text, 'html.parser')
    
    # Находим данные, предполагаем, что они находятся в таблице
    table = soup.find('table')
    if table:
        # Используем pandas для чтения таблицы непосредственно из HTML
        df = pd.read_html(str(table))[0]
        # Предполагаем, что первый столбец содержит даты
        df['Дата'] = pd.to_datetime(df.iloc[:, 0])  # Преобразуем столбец с датами
        df.set_index('Дата', inplace=True)  # Устанавливаем дату как индекс DataFrame
        df.rename(columns={'1 день': 'Ежедневное изменение'}, inplace=True)
        # Сохраняем данные в CSV файл
        df.to_csv('interbank_rates.csv', index=True)
        
        # Построение графика
        df.plot(kind='line')
        plt.title('Изменение межбанковских ставок с 01.01.2023 по 30.06.2024')
        plt.xlabel('Дата')
        plt.ylabel('Ставка')
        plt.xticks(rotation=45)
        plt.tight_layout()
        plt.savefig('fig_2.png')
        plt.show()
    else:
        print("Таблица с данными не найдена.")
else:
    print("Ошибка при запросе данных:", response.status_code)



# Создание фигуры и осей с двумя подграфиками
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(20, 10))

# Загрузка и отображение первого графика
img1 = mpimg.imread('fig_1.png')
ax1.imshow(img1)
ax1.axis('off')  # Отключаем оси для изображения
ax1.set_title('График 1')

# Загрузка и отображение второго графика
img2 = mpimg.imread('fig_2.png')
ax2.imshow(img2)
ax2.axis('off')
ax2.set_title('График 2')

# Показать фигуру с подграфиками
plt.tight_layout()
plt.savefig('fig_final.png')
plt.show()