import psutil
import csv
from datetime import datetime
import time

# MAC ADRESS
hostname = "Lucas"

with open (f"./{hostname}.csv", "w", newline="") as csv_file:
        csv.writer(csv_file, delimiter=";").writerow(['Usuario', 'Data', 'cpu', 'disco_livre', 'Memoria_disponivel', 'uso_memoria_%'])

for i in range(10):
    time.sleep(1)

    # BYTES PARA GB
    def bytes_para_gb(value):
        return value / (1024 ** 3)

    date_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # PORCENTAGEM CPU
    cpu_percent = psutil.cpu_percent(interval=1)

    # USO DA MEMÓRIA
    memory_available = psutil.virtual_memory().available
    memory_percent = psutil.virtual_memory().percent

    #Uso do disco
    disco = psutil.disk_usage(path= "/").free
    dados = [
        hostname, date_time, cpu_percent, bytes_para_gb(disco), bytes_para_gb(memory_available), memory_percent
    ]

    with open (f"./{hostname}.csv", "a", newline="") as csv_file:
        csv.writer(csv_file, delimiter=";").writerow(dados)
    # ==============================
    # RELATÓRIO
    # ==============================
    print(f"""
    BEM VINDO AO SENTRY, SEU MELHOR MONITORAMENTO DO SISTEMA SCADA

    Horário do monitoramento: {date_time}

    INFORMAÇÕES DA CPU
    Uso da CPU: {cpu_percent:.1f}%

    INFORMAÇÕES DA MEMÓRIA RAM

    Disco livre: {disco:.2f} GB
    Memória disponível: {bytes_para_gb(memory_available):.2f} GB
    Uso da memória: {memory_percent:.1f}%
    """)
