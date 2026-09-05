import csv
from datetime import datetime, timedelta
import time

def bytes_para_mb(value):
    return value / (1024 ** 2)

def converterData(data):
    data = datetime.strptime(data, "%Y-%m-%d %H:%M:%S")
    return data

def converterFloat(numero):
    numero = float(numero)
    return numero

servidores = []
dadosCsv = []

with open('./relatorio_monitoramento.csv') as csvfile:
    reader = csv.reader(csvfile, delimiter=';')
    next(reader)
    
    for linha in reader:
        linha[0] = converterData(linha[0])
        linha[3] = converterFloat(linha[3])
        linha[12] = converterFloat(linha[12])
        linha[17] = converterFloat(linha[17])
        linha[18] = converterFloat(linha[18])
        linha[21] = converterFloat(linha[21])
        linha[22] = converterFloat(linha[22])
        
        
        dadosCsv.append(linha)
        
        if(linha[2] not in servidores):
            servidores.append(linha[2])
            
    print(20*"="+" Métricas individuais dos últimos 10 minutos"+"="*20)
    
    for servidor in servidores:        
        dadosServer = []
        for dados in dadosCsv:
            if dados[2] == servidor:
                dadosServer.append(dados)
                        
        print(f"""
=====================================
Servidor: {servidor}
=====================================""")
        maxCpu = [0, '']
        minCpu = [100, '']
        maxRam = [0, '']
        minRam = [100, '']

        
        dataFinal = dadosServer[-1][0]
        dataInicial = dataFinal - timedelta(minutes=10)

        dadosUltimos10 = []
        for dado in dadosServer:
                    if dataInicial <= dado[0] <= dataFinal:
                        dadosUltimos10.append(dado)
                      
                      
        if len(dadosUltimos10) == 0:
                    print("Não existem dados nos últimos 10 minutos.")
                    continue
                          
        for dado in dadosUltimos10:
            if dado[3] > maxCpu[0]:
                maxCpu[0] = dado[3]
                maxCpu[1] = dado[0]
                
            if dado[3] < minCpu[0]:
                minCpu[0] = dado[3]
                minCpu[1] = dado[0]
                
            if dado[12] > maxRam[0]:
                maxRam[0] = dado[12]
                maxRam[1] = dado[0]
                
            if dado[12] < minRam[0]:
                minRam[0] = dado[12]
                minRam[1] = dado[0]
                
        
        
        mediaCpu = sum(dado[3] for dado in dadosUltimos10) / len(dadosUltimos10)
        mediaRam = sum(dado[12] for dado in dadosUltimos10) / len(dadosUltimos10)
        
        redeRecebida = bytes_para_mb(dadosUltimos10[-1][21] - dadosUltimos10[0][21])
        redeEnviada = bytes_para_mb(dadosUltimos10[-1][22] - dadosUltimos10[0][22])
        discoLido = bytes_para_mb(dadosUltimos10[-1][17] - dadosUltimos10[0][17])
        discoEscrito = bytes_para_mb(dadosUltimos10[-1][18] - dadosUltimos10[0][18])
        
        print(f'''
QUantidade de dados capturados: {len(dadosUltimos10)}

Média de uso da CPU: {round(mediaCpu, 2)}%
Pico da CPU: {round(maxCpu[0],2)}% - {maxCpu[1]}
Mínimo de CPU: {round(minCpu[0],2)}% - {minCpu[1]}

Média de uso da RAM: {round(mediaRam, 2)}%
Pico da RAM: {round(maxRam[0], 2)}% - {maxRam[1]}
Mínimo de RAM: {round(minRam[0], 2)}% - {minRam[1]}

Rede recebida: {round(redeRecebida, 2)}MB
Rede enviada: {round(redeEnviada,2)}MB

Disco lido: {round(discoLido, 2)}MB
Disco escrito: {round(discoEscrito, 2)}MB
''')