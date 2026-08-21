import psutil
from getmac import get_mac_address
import socket
import csv
from datetime import datetime

# MAC ADRESS
mac = get_mac_address()
hostname = socket.gethostname()


# TUDO SOBRE CPU 

# PORCENTAGEM CPU
cpu_percent = psutil.cpu_percent(interval=1)

# TEMPO DA CPU
cpu_user = psutil.cpu_times().user 
cpu_system = psutil.cpu_times().system #quanto a cpu esta usando no sistema
cpu_idle = psutil.cpu_times().idle # tempo ocioso / sem fazer nada


# CONTAS DA CPU
cpu_cores = psutil.cpu_count(logical=False)
cpu_threads = psutil.cpu_count(logical=True)


# MÉDIA DE NÚCLEOS POR 1 MIN 10 MIN 15 MIN
loadavg = psutil.getloadavg()


# TUDO SOBRE MEMÓRIA RAM

# USO DA MEMÓRIA
memory_total = psutil.virtual_memory().total #memória total
memory_available = psutil.virtual_memory().available #quanto está disponível p usar
memory_used = psutil.virtual_memory().used #quantos gb já foram usados
memory_percent = psutil.virtual_memory().percent #percentual do used


# TUDO SOBRE MEMÓRIA SWAP

# MEMÓRIA SWAP EM USO
swap_used = psutil.swap_memory().used
swap_percent = psutil.swap_memory().percent


# TUDO SOBRE DISCO

# DESEMPENHO DO DISCO
disk_write_time = psutil.disk_io_counters().write_time #tempo que o disco demora p ser totalment escrito
disk_read_time = psutil.disk_io_counters().read_time #tempo que o disco demora p ser lido


# TUDO SOBRE REDE

# Recebimento e envio de bytes na rede
net_bytes_recv = psutil.net_io_counters().bytes_recv #dados recebidos da rede
net_bytes_sent = psutil.net_io_counters().bytes_sent #dados enviados p fora da rede

# Erros de informações saindo e chegando
net_errors_in = psutil.net_io_counters().errin #quando se entrada de rede da errado
net_errors_out = psutil.net_io_counters().errout #quanto de saída da errado

# Informações que foram dropadas (descartadas) na rede na entrada e saída
net_drops_in = psutil.net_io_counters().dropin 
net_drops_out = psutil.net_io_counters().dropout



# BYTES PARA GB
def bytes_para_gb(value):
    return value / (1024 ** 3)


date_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

dados = [
    date_time, mac, hostname, cpu_percent, cpu_cores, cpu_threads, cpu_user, cpu_system, cpu_idle, loadavg[0], loadavg[1], loadavg[2], bytes_para_gb(memory_total), bytes_para_gb(memory_available), bytes_para_gb(memory_used), memory_percent, bytes_para_gb(swap_used), swap_percent, disk_write_time, disk_read_time, bytes_para_gb(net_bytes_recv), bytes_para_gb(net_bytes_sent), net_errors_in, net_errors_out, net_drops_in, net_drops_out
]

with open ("./relatorio_monitoramento.csv", "a") as csv_file:
    csv.writer(csv_file, delimiter=";").writerow(dados)


# ==============================
# RELATÓRIO
# ==============================

print(f"""
BEM VINDO AO SENTRY, SEU MELHOR MONITORAMENTO DO SISTEMA SCADA

Horário do monitoramento: {date_time}

INFORMAÇÕES DO COMPUTADOR
mac: {mac}
hostname: {hostname}

INFORMAÇÕES DA CPU
Uso da CPU: {cpu_percent:.1f}%
Núcleos físicos: {cpu_cores}
Threads lógicas: {cpu_threads}

Tempo de CPU:
User: {cpu_user:.2f} segundos
System: {cpu_system:.2f} segundos

Load Average:
1 minuto: {loadavg[0]:.2f}
5 minutos: {loadavg[1]:.2f}
15 minutos: {loadavg[2]:.2f}


INFORMAÇÕES DA MEMÓRIA RAM

Memória total: {bytes_para_gb(memory_total):.2f} GB
Memória disponível: {bytes_para_gb(memory_available):.2f} GB
Memória usada: {bytes_para_gb(memory_used):.2f} GB
Uso da memória: {memory_percent:.1f}%

INFORMAÇÕES DA MEMÓRIA SWAP
Swap usada: {bytes_para_gb(swap_used):.2f} GB
Uso da Swap: {swap_percent:.1f}%

INFORMAÇÕES DO DISCO
Tempo de escrita: {disk_write_time} ms
Tempo de leitura: {disk_read_time} ms

INFORMAÇÕES DA REDE
GB recebidos: {bytes_para_gb(net_bytes_recv):.2f} GB
GB enviados: {bytes_para_gb(net_bytes_sent):.2f} GB

Erros de entrada: {net_errors_in}
Erros de saída: {net_errors_out}

Pacotes descartados na entrada: {net_drops_in}
Pacotes descartados na saída: {net_drops_out}

""")