from bs4 import BeautifulSoup
from selenium import webdriver
import requests
import time

##url onde está concentrado o jogos de uma temporada
url = 'https://www.flashscore.com.br/futebol/brasil/serie-a/resultados/'

#inicialização do selenium
options = webdriver.FirefoxOptions()
options.headless = True
driver = webdriver.Firefox(options=options)
driver.get(url)

#retorna o html da página
html = driver.execute_script("return document.documentElement.outerHTML")
driver.quit()

#captura o código das partidas
soup = BeautifulSoup(html, 'html.parser')
codigos = soup.find_all('div', class_="event__match")

#criação do link das partidas
urlBaseJanela = 'https://www.flashscore.com.br/jogo/'
urlBaseJanelaComplemento = '/#resumo-de-jogo'
urlBaseJanelaEstatisticaComplemento = '/#estatisticas-de-jogo;1'
urlBaseJanelaOddsComplemento = '/#comparacao-de-odds;1x2-odds;1-tempo'

linksJogos = []
linksEstatisticasJogos = []
linksOdds = []
for codigo in codigos:
    codigoNovo = (codigo['id'])[4:]
    link = urlBaseJanela + codigoNovo + urlBaseJanelaComplemento
    linkE = urlBaseJanela + codigoNovo + urlBaseJanelaEstatisticaComplemento
    linkO = urlBaseJanela + codigoNovo + urlBaseJanelaOddsComplemento
    linksJogos.append(link)
    linksEstatisticasJogos.append(linkE)
    linksOdds.append(linkO)

#trocar 0 por posicao

#janela dos eventos do jogo
jogo = linksJogos[0]
options = webdriver.FirefoxOptions()
options.headless = True
driver = webdriver.Firefox(options=options)
driver.get(jogo)
time.sleep(2)

html = driver.execute_script("return document.documentElement.outerHTML")
driver.quit()

soup = BeautifulSoup(html, 'html.parser')
eventos = soup.find('div', class_="detailMS")
eventos = eventos.findAll(True, {'class':['detailMS__incidentsHeader', 'detailMS__incidentRow']})

i = 0
#posicao do inicio do segundo tempo
posicao = None
for evento in eventos:
    if 'stage-13' in evento['class']:
        posicao = i
    i += 1

eventosPrimeiroTempo = []
for i in range(1,posicao):
    eventosPrimeiroTempo.append(eventos[i])

eventosMandante = []
eventosVisitante = []
for evento in eventosPrimeiroTempo:
    if 'incidentRow--home' in evento['class']:
        eventosMandante.append(evento)
    else:
        eventosVisitante.append(evento)

##placar do primeiro tempo
##Variáveis de entrada
golsMandante = 0
golsVisitante = 0
##

for evento in eventosMandante:
    info = evento.find('span')
    if ('soccer-ball' or 'soccer-ball-own') in info['class']:
        golsMandante += 1

for evento in eventosVisitante:
    info = evento.find('span')
    if ('soccer-ball' or 'soccer-ball-own') in info['class']:
        golsVisitante += 1

#trocar 0 por posicao

estatisticas = linksEstatisticasJogos[0]
options = webdriver.FirefoxOptions()
options.headless = True
driver = webdriver.Firefox(options=options)
driver.get(estatisticas)
time.sleep(2)

html = driver.execute_script("return document.documentElement.outerHTML")
driver.quit()
soup = BeautifulSoup(html, 'html.parser')

quadro = soup.find('div', id="tab-statistics-1-statistic")
parciais = quadro.find_all('div', class_="statRow")

#Variável
dicionario = {}
for parcial in parciais:
    linha = parcial.find('div', class_="statTextGroup")
    casa = (linha.find('div', class_="statText--homeValue")).text
    estatistica = (linha.find('div', class_="statText--titleValue")).text
    visitante = (linha.find('div', class_="statText--awayValue")).text

    if(estatistica == 'Posse de bola'):
        casa = casa.replace('%', '')
        visitante = visitante.replace('%', '')
    
    dicionario[estatistica] = [casa, visitante]

## Se não existir o atributo Cartões Vermelhos é criado
'''
try:
    verificacao = dicionario['Cartões vermelhos']
except:
    dicionario['Cartões vermelhos'] = ['0','0']
'''


odds = linksOdds[0]
options = webdriver.FirefoxOptions()
options.headless = True
driver = webdriver.Firefox(options=options)
driver.get(odds)
time.sleep(2)

html = driver.execute_script("return document.documentElement.outerHTML")
driver.quit()
soup = BeautifulSoup(html, 'html.parser')

oddsPrimeiroTempo = soup.find('div', id="block-1x2-1hf")
oddsPrimeiroTempo = oddsPrimeiroTempo.find('table', id="odds_1x2")
oddsPrimeiroTempo = oddsPrimeiroTempo.find('tbody')
oddsPrimeiroTempo = oddsPrimeiroTempo.find('tr')
oddsPrimeiroTempo = oddsPrimeiroTempo.find_all('span', class_="odds-wrap")

oddCasa = oddsPrimeiroTempo[0].text
oddEmpate = oddsPrimeiroTempo[1].text
oddVisitante = oddsPrimeiroTempo[2].text

dicionario['Odds'] = [oddCasa, oddEmpate, oddVisitante] 

print(golsMandante)
print(golsVisitante)
print(dicionario)
