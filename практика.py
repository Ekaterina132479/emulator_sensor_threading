import random      #���������� ��� ��������� ��������� ��������
import datetime    #���������� ��� ������ � ����� � ��������
import time        #���������� ��� �������� �������
import threading   #���������� ��� ������ � ��������

#������� sensor_emulator ��������� �� ���� �������� �������, �������� �������� ��� ��������� � ������� ���������
def sensor_emulator(metric_name, metric_range, metric_unit):
    #����� ������ ������ ���������
    start_time = datetime.datetime.now()     
    #����� ��������� ������ ���������
    end_time = start_time + datetime.timedelta(minutes=3)    

    #�������� ������ ����� ��� ������ ������
    with open("sensor_data.txt", "a") as file:
        #�������� ���������� ��� ����������� ������� � �����
        lock = threading.Lock()
        
        #���� �����������, ���� ������� ����� ������ ������� ��������� 
        while datetime.datetime.now() < end_time:
            #�������� ������� ������
            sensor_values = []
            #��������� 60 ��������� �������� � �� ������ � ������
            for _ in range(60):
                #��������� ��������� �������� � �������� ����������
                value = random.uniform(metric_range[0], metric_range[1])
                #������ �������� � ������
                sensor_values.append(value)
                time.sleep(1)

            # ���������� �������� �������� ������� �� 1 ������
            avg_value = sum(sensor_values) / 60
            # ����� ��������� ������ ���������
            current_time = datetime.datetime.now()
            
            # ���������� ������� � �����
            with lock:
                # ������ � ���� ������� ��������� ������ ���������, ����� �������, �������� � ������� ���������
                file.write(f"{current_time}, {metric_name}, {avg_value:.2f} {metric_unit}\n")
    
    print(f" sensor '{metric_name}' done")
    
# �������� � ������ ���������� ������� ��� �������� ������ ��������
threads = []
for metric in ["temperature", "humidity", "air_quality"]:
    thread = threading.Thread(target=sensor_emulator, args=(metric, (-20, 40), "�C" if metric == "temperature" else ("%" if metric == "humidity" else "ppm")))
    threads.append(thread)
    thread.start()

# �������� ���������� ������ ���� �������
for thread in threads:
    thread.join()