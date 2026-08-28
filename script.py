import psutil
from getmac import get_mac_address
import socket
import csv
from datetime import datetime

# MAC ADRESS
def info_machine():
    return{
    "mac": get_mac_address(),
    "hostname": socket.gethostname()
}


# TUDO SOBRE CPU 
def cpu_functions():
    # PORCENTAGEM CPU

    # TEMPO DA CPU
    cpu_percent = psutil.cpu_percent(interval=1)
    cpu_time = psutil.cpu_times()
    
    return { 
    "cpu_percent": cpu_percent,
    "cpu_user": cpu_time.user,
    "cpu_system": cpu_time.system,
    "cpu_idle": cpu_time.idle, # tempo ocioso / sem fazer nada

    # funções linux
    #"cpu_nice": cpu_time.nice, # tarfa de nível baixo
    #"cpu_iowait": cpu_time.iowait, # tempo de aguardo de uma operação de entrada e saída
    #"cpu_irq": cpu_time.irq, # interrupt quest, quando um hardware chama a cpu
    #"cpu_softirq": cpu_time.softirq, # interrupção de software, precido com o de cima, mas nivel software


    # CONTAS DA CPU
    "cpu_cores" : psutil.cpu_count(logical=False),
    "cpu_threads": psutil.cpu_count(logical=True)
    }

# MÉDIA DE NÚCLEOS POR 1 MIN 10 MIN 15 MIN
# função linux para indicar a quantidade média de trabalho/processos aguardando ou utilizando CPU
#def loadavg_function():
#    loadavg = psutil.getloadavg()
 #   return{
  #     "loadavg_1min": loadavg[0],
   #     "loadavg_5min": loadavg[1],
    #    "loadavg_15min": loadavg[2]
    #}

# BYTES PARA GB
def bytes_para_gb(value):
    return value / (1024 ** 3)

# TUDO SOBRE MEMÓRIA RAM
def memory_functions():
    # USO DA MEMÓRIA
    memory = psutil.virtual_memory()
    swap = psutil.swap_memory()

    return {
    "memory_total_gb": bytes_para_gb(memory.total),
    "memory_available": bytes_para_gb(memory.available),
    "memory_used": bytes_para_gb(memory.used),
    "memory_percent": memory.percent,
    # TUDO SOBRE MEMÓRIA SWAP
    # MEMÓRIA SWAP EM USO
    "swap_used": bytes_para_gb(swap.used),
    "swap_percent": swap.percent
    }



# TUDO SOBRE DISCO
def disk_functions():
    # DESEMPENHO DO DISCO
    disk = psutil.disk_io_counters()

    return{
    "disk_write_time": disk.write_time,
    "disk_read_time": disk.read_time,
    "disk_read_bytes": bytes_para_gb(disk.read_bytes),
    "disk_write_bytes": bytes_para_gb(disk.write_bytes),
    "disk_read_count": disk.read_count,
    "disk_write_count": disk.write_count
    }
    

# TUDO SOBRE REDE
def network_functions():
    # Recebimento e envio de bytes na rede
    network = psutil.net_io_counters()

    return{
    "net_bytes_recv": bytes_para_gb(network.bytes_recv),
    "net_bytes_sent": bytes_para_gb(network.bytes_sent),
    # Erros de informações saindo e chegando
    "net_errors_in": network.errin,
    "net_errors_out": network.errout,
     # Informações que foram dropadas (descartadas) na rede na entrada e saída
    "net_drops_in": network.dropin,
    "net_drops_out": network.dropout
    }
    
    

# temperatura, apenas no linux
#def temperature_measure():
 #   return psutil.sensors_temperatures()



#loadavg = loadavg_function()
cpu = cpu_functions()
memory = memory_functions()
disk = disk_functions()
network = network_functions()
#temperature = temperature_measure()
machine = info_machine()
date_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

# ** significa dicionary unpacking, para juntar os dicionários
dados = {
    "timestamp": date_time,
    **machine,
    **cpu,
    **memory,
    **disk,
    **network
}

with open ("./relatorio_monitoramento.csv", "a") as csv_file:
    writer = csv.DictWriter(
        csv_file,
        fieldnames=dados.keys(),
        delimiter=";"
    )

    writer.writerow(dados)

# ==============================
# RELATÓRIO
# ==============================

print(f"""
BEM VINDO AO SENTRY, SEU MELHOR MONITORAMENTO DO SISTEMA SCADA

Horário do monitoramento: {date_time}

INFORMAÇÕES DO COMPUTADOR
mac: {machine["mac"]}
hostname: {machine["hostname"]}

INFORMAÇÕES DA CPU
Uso da CPU: {cpu["cpu_percent"]:.1f}%
Núcleos físicos: {cpu["cpu_cores"]}
Threads lógicas: {cpu["cpu_threads"]}

Tempo de CPU:
User: {cpu["cpu_user"]:.2f} segundos
System: {cpu["cpu_system"]:.2f} segundos
Idle: {cpu["cpu_idle"]:.2f} segundos


INFORMAÇÕES DA MEMÓRIA RAM

Memória total: {memory["memory_total_gb"]:.2f} GB
Memória disponível: {memory["memory_available"]:.2f} GB
Memória usada: {memory["memory_used"]:.2f} GB
Uso da memória: {memory["memory_percent"]:.1f}%

INFORMAÇÕES DA MEMÓRIA SWAP
Swap usada: {memory["swap_used"]:.2f} GB
Uso da Swap: {memory["swap_percent"]:.1f}%

INFORMAÇÕES DO DISCO
Tempo de escrita: {disk["disk_write_time"]} ms
Tempo de leitura: {disk["disk_read_time"]} ms

Dados lidos: {disk["disk_read_bytes"]:.2f} GB
Dados escritos: {disk["disk_write_bytes"]:.2f} GB

Operações de leitura:  {disk["disk_read_count"]}
Operações de escrita:  {disk["disk_write_count"]}

INFORMAÇÕES DA REDE
GB recebidos: {network["net_bytes_recv"]:.2f} GB
GB enviados: {network["net_bytes_sent"]:.2f} GB

Erros de entrada: {network["net_errors_in"]}
Erros de saída: {network["net_errors_out"]}

Pacotes descartados na entrada: {network["net_drops_in"]}
Pacotes descartados na saída: {network["net_drops_out"]}

""")
