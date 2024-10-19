import random      #библиотека для генерации случайных значений
import datetime    #библиотека для работы с датой и временем
import time        #библиотека для задержки времени
import threading   #библиотека для работы с потоками

#функция sensor_emulator принимает на вход название метрики, диапазон значений для генерации и единицу измерения
def sensor_emulator(metric_name, metric_range, metric_unit):
    #время начала работы эмулятора
    start_time = datetime.datetime.now()     
    #время окончания работы эмулятора
    end_time = start_time + datetime.timedelta(minutes=3)    

    #создание общего файла для записи данных
    with open("sensor_data.txt", "a") as file:
        #создание блокировки для безопасного доступа к файлу
        lock = threading.Lock()
        
        #цикл выполняется, пока текущее время меньше времени окончания 
        while datetime.datetime.now() < end_time:
            #создание пустого списка
            sensor_values = []
            #генерация 60 случайных значений и их запись в список
            for _ in range(60):
                #генерация случайных значений в заданном промежутке
                value = random.uniform(metric_range[0], metric_range[1])
                #запись значения в список
                sensor_values.append(value)
                time.sleep(1)

            # Вычисление среднего значения метрики за 1 минуту
            avg_value = sum(sensor_values) / 60
            # Время окончания работы эмулятора
            current_time = datetime.datetime.now()
            
            # Блокировка доступа к файлу
            with lock:
                # Запись в файл времени окончания работы эмулятора, имени метрики, значения и единицы измерения
                file.write(f"{current_time}, {metric_name}, {avg_value:.2f} {metric_unit}\n")
    
    print(f" sensor '{metric_name}' done")
    
# Создание и запуск нескольких потоков для эмуляции разных датчиков
threads = []
for metric in ["temperature", "humidity", "air_quality"]:
    thread = threading.Thread(target=sensor_emulator, args=(metric, (-20, 40), "°C" if metric == "temperature" else ("%" if metric == "humidity" else "ppm")))
    threads.append(thread)
    thread.start()

# Ожидание завершения работы всех потоков
for thread in threads:
    thread.join()