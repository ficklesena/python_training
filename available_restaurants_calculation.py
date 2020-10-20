# Добавляем необходимые модули: csv (для работы с файлами csv) и
# shapely (для проверки входит ли клиент в зону доставки)
import csv
from shapely.geometry import Point, Polygon

# Объявляем переменные для вычисления зоны доставки и
# количества ресторанов доступных клиенту
rest_deliv_coord=[]
rest_counter=0

# Создаем файл для записи результатов и вводим в него
# поля-идентификаторы
with open('places_available.csv', 'w', newline='') as place_avail:
    place_avail = csv.writer(place_avail)
    place_avail.writerow(['id', 'number_of_places_available'])
    # Открываем файл с координатами клиентов
    with open('user_coordinates.csv') as user_coord:
        user_coord = csv.reader(user_coord, delimiter=',')
        next(user_coord)
        # Запускаем цикл по клиентам и их координатам
        for user_line in user_coord:
            # Назначаем точке координаты клиента
            client=Point(float(user_line[1]), float(user_line[2]))
            # Открываем файл с координатами ресторанов
            with open('place_zone_coordinates.csv') as place_coord:
                place_coord = csv.reader(place_coord, delimiter=',')
                next(place_coord)
                # Запускаем цикл по ресторанам и их координатам
                for place_line in place_coord:
                    # Проверяем считывается ли последняя вершина зоны
                    # доставки ресторана
                    if int(place_line[3]) == 3:
                        # Прибавляем к координатам новую вершину
                        rest_deliv_coord += [(float(place_line[1]),
                                              float(place_line[2]))]
                        # Объединяем координаты классом Polygon
                        rest_deliv_zone = Polygon(rest_deliv_coord)
                        # Проверяем если точка с координатами клиента
                        # входит в зону доставки ресторана
                        if client.within(rest_deliv_zone):
                            rest_counter += 1
                        # Обнуляем координаты для координатов следующего
                        # ресторана
                        rest_deliv_coord = []
                    # Если считываются точки, кроме последней -
                    # прибавляем к координатам новую вершину
                    else:
                        rest_deliv_coord += [(float(place_line[1]),
                                              float(place_line[2]))]
            # Записываем в файл для записи результатов id клиента и
            # доступное ему количество ресторанов
            place_avail.writerow([user_line[0], rest_counter])
            # Обнуляем счетчик ресторанов для следующего клиента
            rest_counter = 0