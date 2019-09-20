import pandas as pd
import sys, os
from susep import SUSEP

if not os.path.isfile('ControleOperacoesMPME.xlsx'):
    print('Não foi possível encontrar o arquivo ControleOperacoesMPME.xlsx')
    sys.exit()

dados = pd.read_excel('ControleOperacoesMPME.xlsx', sheet_name="378")

resultado = ''
i = 0

susep = SUSEP()

for index, col in dados.iterrows():
    susep.ESPSEQ = col['ESPSEQ']
    # susep.ENTCODIGO = col['ENTCODIGO']
    susep.MRFMESANO = col['MRFMESANO']
    # susep.QUAID = col['QUAID']
    susep.TPMOID = col['TPMOID']
    susep.CMPID = col['CMPID']
    # susep.RAMCODIGO = col['RAMCODIGO']
    susep.ESPDATAINICIORO = col['ESPDATAINICIORO']
    susep.ESPDATAFIMRO = col['ESPDATAFIMRO']
    susep.ESPDATAEMISSRD = col['ESPDATAEMISSRD']
    susep.ESPDATAEMISSRO = col['ESPDATAEMISSRO']
    susep.ESPDATAINICIORD = col['ESPDATAINICIORD']
    susep.ESPDATAFIMRD = col['ESPDATAFIMRD']
    susep.ESPDATAEMISSRD = col['ESPDATAEMISSRD']
    susep.ESPVALORMOVRD = col['ESPVALORMOVRD']
    # susep.ESPCODCESS = col['ESPCODCESS']
    susep.ESPFREQ = col['ESPFREQ']
    susep.ESPVARCARO = col['ESPVARCARO']
    susep.ESPVALORCARD = col['ESPVALORCARD']
    susep.ESPVALORCIRO = col['ESPVALORCIRO']
    susep.ESPVALORCIRD = col['ESPVALORCIRD']
    susep.ESPMOEDA = col['ESPMOEDA']

    resultado += susep._arquivo_quadro_378()

    if susep._arquivo_quadro_378() == 'erro':
        i += 1

if i == 0:
    arquivo = open('susep_quadro_378.txt', 'w+')
    arquivo.write(resultado)
    arquivo.close()