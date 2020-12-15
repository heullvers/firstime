from bs4 import BeautifulSoup
from selenium import webdriver
import requests
import time
from Partida import Partida
import csv


nomeArquivo = 'coletaOficial.csv'
with open(nomeArquivo, 'a+', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(['odd_mandante', 'odd_empate', 'odd_visitante', 'posse_bolaM', 'posse_bolaV',
       'finalizacoesM', 'finalizacoesV', 'chutes_foraM', 'chutes_foraV', 'escanteiosM', 'escanteiosV', 'impedimentosM', 'impedimentosV',
       'cartoes_vermelhosM', 'cartoes_vermelhosV', 'placar_atual'])

    jogo = 'https://www.flashscore.com.br/jogo/QgE7PMPo/#resumo-de-jogo'
    estatisticas = 'https://www.flashscore.com.br/jogo/QgE7PMPo/#estatisticas-de-jogo;0'
    odds = 'https://www.flashscore.com.br/jogo/QgE7PMPo/#comparacao-de-odds;1x2-odds;tempo-regulamentar'

    options = webdriver.FirefoxOptions()
    options.headless = True
    driver = webdriver.Firefox(options=options)
    driver.get(jogo)
    time.sleep(2)

    html = driver.execute_script("return document.documentElement.outerHTML")
    driver.quit()

    soup = BeautifulSoup(html, 'html.parser')



    placar = soup.find('div', class_="match-info")
    placar = placar.find_all('span', class_="scoreboard")

    ##Descobrir o placar atual do jogo
    golsMandante = placar[0].text
    golsVisitante = placar[1].text

    #Variável
    placarAtual = None

    if(golsMandante == golsVisitante):
        placarAtual = 'E'
    elif(golsMandante > golsVisitante):
        placarAtual = 'V'
    else:
        placarAtual = 'D'


    ##Descobrir as estatísticas
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


    ##Variáveis
    if('Posse de bola' in dicionario):
        posseDebolaM = dicionario['Posse de bola'][0]
        posseDebolaV = dicionario['Posse de bola'][1]
    else:
        posseDebolaM = None
        posseDebolaV = None

    if('Finalizações' in dicionario):
        finalizacoesM = dicionario['Finalizações'][0]
        finalizacoesV = dicionario['Finalizações'][1]
    else:
        finalizacoesM = None
        finalizacoesV = None

    if('Chutes fora' in dicionario):
        chutesForaM = dicionario['Chutes fora'][0]
        chutesForaV = dicionario['Chutes fora'][1]
    else:
        chutesForaM = None
        chutesForaV = None

    if('Escanteios' in dicionario):
        escanteiosM = dicionario['Escanteios'][0]
        escanteiosV = dicionario['Escanteios'][1]
    else:
        escanteiosM = None
        escanteiosV = None

    if('Impedimentos' in dicionario):
        impedimentosM = dicionario['Impedimentos'][0]
        impedimentosV = dicionario['Impedimentos'][1]
    else:
        impedimentosM = None
        impedimentosV = None

    if('Cartões vermelhos' not in dicionario):
        dicionario['Cartões vermelhos'] = ['0','0']
        cartoesVermelhosM = dicionario['Cartões vermelhos'][0]
        cartoesVermelhosV = dicionario['Cartões vermelhos'][1]
    else:
        cartoesVermelhosM = dicionario['Cartões vermelhos'][0]
        cartoesVermelhosV = dicionario['Cartões vermelhos'][1]

    ##Descobrir as odds

    options = webdriver.FirefoxOptions()
    options.headless = True
    driver = webdriver.Firefox(options=options)
    driver.get(odds)
    time.sleep(2)

    html = driver.execute_script("return document.documentElement.outerHTML")
    driver.quit()
    soup = BeautifulSoup(html, 'html.parser')

    oddsPrimeiroTempo = soup.find('div', id="block-1x2")
    oddsPrimeiroTempo = oddsPrimeiroTempo.find('table', id="odds_1x2")
    oddsPrimeiroTempo = oddsPrimeiroTempo.find('tbody')
    oddsPrimeiroTempo = oddsPrimeiroTempo.find('tr')
    oddsPrimeiroTempo = oddsPrimeiroTempo.find_all('span', class_="odds-wrap")

    ##Variáveis
    oddCasa = oddsPrimeiroTempo[0].text
    oddEmpate = oddsPrimeiroTempo[1].text
    oddVisitante = oddsPrimeiroTempo[2].text

    writer.writerow([oddCasa, oddEmpate, oddVisitante, posseDebolaM, posseDebolaV, finalizacoesM, finalizacoesV,
    chutesForaM, chutesForaV, escanteiosM, escanteiosV, impedimentosM, impedimentosV, cartoesVermelhosM, cartoesVermelhosV,
    placarAtual])