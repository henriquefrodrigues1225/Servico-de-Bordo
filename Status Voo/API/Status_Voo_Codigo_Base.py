from datetime import datetime
voos = [
    # Voos já existentes
    {
        "codigo_voo": "AD4070", "origem": "VCP (Campinas)", "destino": "SDU (Rio de Janeiro)", 
        "voo": "Nacional", "dia_partida": "21/10/2025", "partida_programada": "09:00", "chegada_programada": "10:05", 
        "status": None, "nova_partida": None, "nova_chegada": None, # Decolado (Passou da hora atual 23:22)
    },
    {
        "codigo_voo": "AD2550", "origem": "CNF (Belo Horizonte)", "destino": "SSA (Salvador)", 
        "voo": "Nacional", "dia_partida": "22/10/2025", "partida_programada": "10:15", "chegada_programada": "12:00", 
        "status": None, "nova_partida": None, "nova_chegada": None, # Programado (Data futura)
    },
    {
        "codigo_voo": "AD5001", "origem": "REC (Recife)", "destino": "FOR (Fortaleza)", 
        "voo": "Nacional", "dia_partida": "18/10/2025", "partida_programada": "11:40", "chegada_programada": "12:50", 
        "status": "Adiado", "nova_partida": "22:40", "nova_chegada": "23:50", # Aterrissando (Passou das 22:40 e a chegada 23:50 está próxima)
    },
    {
        "codigo_voo": "AD4130", "origem": "VCP (Campinas)", "destino": "CWB (Curitiba)", 
        "voo": "Nacional", "dia_partida": "21/10/2025", "partida_programada": "12:00", "chegada_programada": "13:00", 
        "status": "Cancelado", "nova_partida": None, "nova_chegada": None, # Cancelado (Status Fixo)
    },
    
    # --- NOVOS VOOS INSERIDOS ---
    
    # Voo que Aterrisou (Chegada programada já passou há muito tempo no dia 17)
    {
        "codigo_voo": "AD8720", "origem": "VCP (Campinas)", "destino": "MIA (Miami)", 
        "voo": "Internacional", "dia_partida": "18/10/2025", "partida_programada": "08:30", "chegada_programada": "17:00", 
        "status": None, "nova_partida": None, "nova_chegada": None, # Aterrissado
    },
    # Voo de data futura (Programado)
    {
        "codigo_voo": "AD8705", "origem": "SSA (Salvador)", "destino": "LIS (Lisboa)", 
        "voo": "Internacional", "dia_partida": "25/10/2025", "partida_programada": "23:59", "chegada_programada": "10:00", 
        "status": None, "nova_partida": None, "nova_chegada": None, # Programado
    },
    # Voo do dia de hoje, mas com partida MUITO próxima da hora atual (Embarcando)
    {
        "codigo_voo": "AD4400", "origem": "CNF (Belo Horizonte)", "destino": "BSB (Brasília)", 
        "voo": "Nacional", "dia_partida": "18/10/2025", "partida_programada": "23:50", "chegada_programada": "01:00", 
        "status": None, "nova_partida": None, "nova_chegada": None, # Embarcando (23:50 - 23:22 = 28 min)
    },
    # Voo do dia de hoje, mas com partida já ultrapassada e longa duração (Decolado)
    {
        "codigo_voo": "AD8780", "origem": "GRU (Guarulhos)", "destino": "PTY (Panamá)", 
        "voo": "Internacional", "dia_partida": "18/10/2025", "partida_programada": "21:00", "chegada_programada": "02:00", 
        "status": None, "nova_partida": None, "nova_chegada": None, # Decolado
    },
    # Voo Cancelado (Status Fixo)
    {
        "codigo_voo": "AD4001", "origem": "REC (Recife)", "destino": "VCP (Campinas)", 
        "voo": "Nacional", "dia_partida": "18/10/2025", "partida_programada": "06:00", "chegada_programada": "09:00", 
        "status": "Cancelado", "nova_partida": None, "nova_chegada": None, # Cancelado
    },
    # Voo Adiado com nova partida para amanhã (18/10)
    {
        "codigo_voo": "AD2523", "origem": "VCP (Campinas)", "destino": "PVH (Porto Velho)", 
        "voo": "Nacional", "dia_partida": "17/10/2025", "partida_programada": "23:00", "chegada_programada": "03:30", 
        "status": "Adiado", "nova_partida": "08:00", "nova_chegada": "12:30", # Adiado - Programado (Partida amanhã 08:00)
    },
]


def converter(hora):
    h, m = map(int, hora.split(':'))
    return h * 60 + m

def converterdata(data, txt):
    d, m, a = map(int, data.split('/'))
    if txt == "d":
        return d
    elif txt == "m":
        return m
    else: 
        return a

def encontrar(codigo):
    for voo in voos:
        if codigo == voo["codigo_voo"]:
            return voo
    return None

def det_status(voo):
    atraso = False
    if voo["status"]:
        if voo["status"] == "Adiado":
            retorno = voo["status"] + ' - '
            atraso = True
            n_part = converter(voo["nova_partida"])
            n_cheg = converter(voo["nova_chegada"])
        else:
            return voo["status"]
    else:
        retorno = ''
    
    dia = datetime.now().day
    mes = datetime.now().month
    ano = datetime.now().year
    min = datetime.now().hour * 60 + datetime.now().minute
    part_min = converter(voo["partida_programada"])
    cheg_min = converter(voo["chegada_programada"])
    if atraso:
        diff = n_part - min
    else:
        diff = part_min - min 
    if atraso:
        if min > n_cheg:
            difer = min - n_cheg
        else:
            difer = n_cheg - min
    else: 
        if min > cheg_min:
            difer = min - cheg_min
        else:
            difer = cheg_min - min
    part_d = converterdata(voo["dia_partida"], "d")
    part_m = converterdata(voo["dia_partida"], "m")
    part_a = converterdata(voo["dia_partida"], "a")
    
    print(difer)
    print(diff)
    if part_a <= ano and part_m <= mes and part_d <= dia and part_min <= min:
        if difer > 0 and difer < 30 and difer > diff:
            return retorno + "Aterrissando"
        elif difer > 30 and difer > diff:
            return retorno + "Aterrissado"
        else:
            return retorno + "Decolado"
    elif part_a == ano and part_m == mes and part_d == dia and part_min < min and diff <= 30:
        return retorno + "Embarcando"
    else:
        return retorno + "Programado"
    
def buscar_voo():
    while True:
        cod_voo = input('\nCódigo do voo (ou "sair") - ').upper()
        if cod_voo == "SAIR":
            break
        voo_exibido = encontrar(cod_voo)
        if voo_exibido == None:
            print('Código Inválido, tente novamente')
        else:
            status = det_status(voo_exibido)
            print(f'\nCódigo do voo - {voo_exibido["codigo_voo"]}\nOrigem - {voo_exibido["origem"]}\nDestino - {voo_exibido["destino"]}\nData Programada - {voo_exibido["dia_partida"]}\nPartida Programada - {voo_exibido["partida_programada"]}\nChegada Programada - {voo_exibido["chegada_programada"]}\nStatus - {status}')
            if voo_exibido["status"] == "Adiado":
                print(f'Nova Partida - {voo_exibido["nova_partida"]}\nNova Chegada - {voo_exibido["nova_chegada"]}')
        
if __name__ == '__main__':
    buscar_voo()
    