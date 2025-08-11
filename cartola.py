import pandas as pd
import requests
import time

RODADA_INICIAL = 1
ULTIMA_RODADA = 18

cartolas = [
    {'nome': 'Clube Pipocada', 'cartola_id': '9092997'},
    {'nome': 'Tra-Thor', 'cartola_id': '15104170'},
    {'nome': 'Fracus FC', 'cartola_id': '10151843'},
    {'nome': 'Plincesa FC', 'cartola_id': '26425845'},
    {'nome': 'Al Bihlau', 'cartola_id': '9064886'},
    {'nome': 'Kika@72fc', 'cartola_id': '7955777'},
]

rodadas = range(RODADA_INICIAL, ULTIMA_RODADA + 1)

posicao = {
    1: 'Goleiro',
    2: 'Lateral',
    3: 'Zagueiro',
    4: 'Meia',
    5: 'Atacante',
    6: 'Técnico',
}

clube = {
    262: 'Flamengo',
    263: 'Botafogo',
    264: 'Corinthians',
    265: 'Bahia',
    266: 'Fluminense',
    267: 'Vasco',
    275: 'Palmeiras',
    276: 'São Paulo',
    277: 'Santos',
    280: 'Bragantino',
    282: 'Atlético-MG',
    283: 'Cruzeiro',
    284: 'Grêmio',
    285: 'Internacional',
    286: 'Juventude',
    287: 'Vitória',
    292: 'Sport',
    354: 'Ceará',
    356: 'Fortaleza',
    2305: 'Mirassol',
}
url_escudo = 'https://raw.githubusercontent.com/victorbarwinski/ligalitopbi/main/Escudos/'
escudo = {
    'Flamengo': 'Flamengo',
    'Botafogo': 'Botafogo',
    'Corinthians': 'Corinthians',
    'Bahia': 'Bahia',
    'Fluminense': 'Fluminense',
    'Vasco': 'Vasco',
    'Palmeiras': 'Palmeiras',
    'São Paulo': 'Sao_Paulo',
    'Santos': 'Santos',
    'Bragantino': 'Red_Bull_Bragantino',
    'Atlético-MG': 'Atletico_Mineiro',
    'Cruzeiro': 'Cruzeiro',
    'Grêmio': 'Gremio',
    'Internacional': 'Internacional',
    'Juventude': 'Juventude',
    'Vitória': 'Vitoria',
    'Sport': 'Sport',
    'Ceará': 'Ceara',
    'Fortaleza': 'Fortaleza',
    'Mirassol': 'Mirassol',
}

def dados_rodada(cartola, rodada):
    while True:
        try:
            url = f'https://api.cartolafc.globo.com/time/id/{cartola["cartola_id"]}/{rodada}'
            resp = requests.get(url)
            dados = resp.json()
            return dados
        except:
            time.sleep(1)
            continue

manutencao = False
df = list()
for cartola in cartolas:
    for rodada in rodadas:
        print(cartola, rodada)
        dados = dados_rodada(cartola, rodada)
        if 'mensagem' in dados:
            print(dados['mensagem'])
            manutencao = True
            break
        for i, atleta in enumerate(dados['atletas']):
            registro = {}
            registro['time_id'] = cartola['cartola_id']
            registro['time_nome'] = cartola['nome']
            registro['rodada'] = rodada
            registro['capitao_id'] = dados['capitao_id']
            registro['reserva_luxo_id'] = dados['reserva_luxo_id']
            registro['pontos'] = round(dados['pontos'], 2)
            registro['esquema_id'] = dados['esquema_id']
            registro['patrimonio'] = round(dados['patrimonio'], 2)

            # Ajuste Zubeldia e Rios
            if atleta['atleta_id'] == 107111:
                atleta['clube_id'] = 275
            if atleta['atleta_id'] == 99366:
                atleta['clube_id'] = 276

            try:
                registro['clube'] = clube[atleta['clube_id']]
                registro['escudo'] = f"{url_escudo}{escudo[registro['clube']]}.png"
            except:
                registro['clube'] = None
                registro['escudo'] = None

            try:
                registro['posicao'] = posicao[atleta['posicao_id']]
            except:
                registro['posicao'] = None

            registro['capitao_time'] = atleta['atleta_id'] == dados['capitao_id']
            registro['reserva_luxo_time'] = atleta['atleta_id'] == dados['reserva_luxo_id']
            if 'scout' in atleta and isinstance(atleta['scout'], dict):
                for key, value in atleta['scout'].items():
                    registro[f'scout_{key}'] = value
            if registro['capitao_time']:
                registro['pontuacao_final'] = round(atleta['pontos_num'] * 1.5, 2)
            else:
                registro['pontuacao_final'] = atleta['pontos_num']
            registro.update(atleta)
            del registro['foto']
            del registro['scout']
            del registro['nome']
            del registro['apelido_abreviado']
            df.append(registro)

if not manutencao:
    cart = pd.DataFrame(df)
    cart = cart.sort_values(['time_nome', 'rodada', 'posicao_id'])
    cart.to_csv('cartola.csv', index=False, sep=';', decimal=',', encoding='latin1')
