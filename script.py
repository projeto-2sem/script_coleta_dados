import psutil
import csv
from datetime import datetime
import time

# MAC ADRESS
hostname = "Lucas"

with open ("./relatorio_monitoramento.csv", "w", newline="") as csv_file:
        csv.writer(csv_file, delimiter=";").writerow(['Usuario', 'Data', 'cpu', 'memoria_total', 'Memoria_disponivel', 'uso_memoria_%'])

for i in range(10):
    time.sleep(1)

    # BYTES PARA GB
    def bytes_para_gb(value):
        return value / (1024 ** 3)

    date_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # PORCENTAGEM CPU
    cpu_percent = psutil.cpu_percent(interval=1)

    # USO DA MEMÓRIA
    memory_total = psutil.virtual_memory().total
    memory_available = psutil.virtual_memory().available
    memory_percent = psutil.virtual_memory().percent

    dados = [
        hostname, date_time, cpu_percent, bytes_para_gb(memory_total), bytes_para_gb(memory_available), memory_percent
    ]

    with open ("./relatorio_monitoramento.csv", "a", newline="") as csv_file:
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

    Memória total: {bytes_para_gb(memory_total):.2f} GB
    Memória disponível: {bytes_para_gb(memory_available):.2f} GB
    Uso da memória: {memory_percent:.1f}%
    """)
