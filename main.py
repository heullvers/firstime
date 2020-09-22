from bs4 import BeautifulSoup
from selenium import webdriver
import requests
import time
from Partida import Partida
import csv

nomeArquivo = 'brasileiro-seriea-2020'
with open(nomeArquivo, 'w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(['País','Campeonato','timeMandante','timeVisitante','Posse de bolaM', 'Posse de bolaV', 'Tentativas de golM', 'Tentativas de golV', 'FinalizaçõesM', 'FinalizaçõesV',
    'Chutes foraM', 'Chutes foraV', 'Chutes bloqueadosM', 'Chutes bloqueadosV', 'Faltas cobradasM', 'Faltas cobradasV',
    'EscanteiosM', 'EscanteiosV', 'ImpedimentosM', 'ImpedimentosV', 'Defesas do goleiroM', 'Defesas do goleiroV', 'FaltasM', 'FaltasV',
    'Cartões amarelosM', 'Cartões amarelosV', 'Cartões VermelhosM', 'Cartões VermelhosV', 'Total de passesM', 'Total de passesV',
    'DesarmesM', 'DesarmesV', 'AtaquesM', 'AtaquesV', 'Ataques PerigososM', 'Ataques PerigososV', 'OddM', 'OddE', 'OddV', 
    'DiferencaGols','PlacarPrimeiroTempo', 'PlacarFinal'])

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
    ##Variáveis
    pais = (soup.find('span', class_="event__title--type")).text
    campeonato = (soup.find('span', class_="event__title--name")).text
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

    pos = 0
    for match in linksJogos:
        #janela dos eventos do jogo
        jogo = linksJogos[pos]
        print(pos)
        print(jogo)
        options = webdriver.FirefoxOptions()
        options.headless = True
        driver = webdriver.Firefox(options=options)
        driver.get(jogo)
        time.sleep(2)

        html = driver.execute_script("return document.documentElement.outerHTML")
        driver.quit()

        soup = BeautifulSoup(html, 'html.parser')

        times = soup.find_all('div', class_="tname__text")
        listaTimes = []
        for linha in times:
            team = (linha.find('a')).text
            listaTimes.append(team)

        #Variáveis
        timeMandante = listaTimes[0]
        timeVisitante = listaTimes[1]

        print(timeMandante, ' x ', timeVisitante)

        placar = soup.find('div', class_="match-info")
        placar = placar.find_all('span', class_="scoreboard")

        golsMandanteFinal = placar[0].text
        golsVisitanteFinal = placar[1].text

        placarFinal = None

        if(golsMandanteFinal == golsVisitanteFinal):
            placarFinal = 'E'
        elif(golsMandanteFinal > golsVisitanteFinal):
            placarFinal = 'V'
        else:
            placarFinal = 'D'

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

        placarPrimeiroTempo = None
        if(golsMandante == golsVisitante):
            placarPrimeiroTempo = 'E'
        elif(golsMandante > golsVisitante):
            placarPrimeiroTempo = 'V'
        else:
            placarPrimeiroTempo = 'D'

        estatisticas = linksEstatisticasJogos[pos]
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
        ##estatisticas do jogo
        for parcial in parciais:
            linha = parcial.find('div', class_="statTextGroup")
            casa = (linha.find('div', class_="statText--homeValue")).text
            estatistica = (linha.find('div', class_="statText--titleValue")).text
            visitante = (linha.find('div', class_="statText--awayValue")).text

            if(estatistica == 'Posse de bola'):
                casa = casa.replace('%', '')
                visitante = visitante.replace('%', '')
            
            dicionario[estatistica] = [casa, visitante]

        odds = linksOdds[pos]
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
        dicionario['PlacarPrimeiroTempo'] =  placarPrimeiroTempo
        dicionario['PlacarFinal'] = placarFinal
        dicionario['DiferencaGols'] = golsMandante - golsVisitante

        try:
            posseDeBolaM = dicionario['Posse de bola'][0]
            posseDeBolaV = dicionario['Posse de bola'][1]
        except:
            posseDeBolaM = None
            posseDeBolaV = None

        try:
            tentativasDeGolM = dicionario['Tentativas de gol'][0]
            tentativasDeGolV = dicionario['Tentativas de gol'][1]
        except:
            tentativasDeGolM = None
            tentativasDeGolV = None

        try:
            finalizacoesM = dicionario['Finalizações'][0]
            finalizacoesV = dicionario['Finalizações'][1]
        except:
            finalizacoesM = None
            finalizacoesV = None

        try:
            chutesForaM = dicionario['Chutes fora'][0]
            chutesForaV = dicionario['Chutes fora'][1]
        except:
            chutesForaM = None
            chutesForaV = None

        try:
            chutesBloqueadosM = dicionario['Chutes bloqueados'][0]
            chutesBloqueadosV = dicionario['Chutes bloqueados'][1]
        except:
            chutesBloqueadosM = None
            chutesBloqueadosV = None

        try:
            faltasCobradasM = dicionario['Faltas cobradas'][0]
            faltasCobradasV = dicionario['Faltas cobradas'][1]
        except:
            faltasCobradasM = None
            faltasCobradasV = None

        try:
            escanteiosM = dicionario['Escanteios'][0]
            escanteiosV = dicionario['Escanteios'][1]
        except:
            escanteiosM = None
            escanteiosV = None

        try:
            impedimentosM = dicionario['Impedimentos'][0]
            impedimentosV = dicionario['Impedimentos'][1]
        except:
            impedimentosM = None
            impedimentosV = None

        try:
            defesasDoGoleiroM = dicionario['Defesas do goleiro'][0]
            defesasDoGoleiroV = dicionario['Defesas do goleiro'][1]
        except:
            defesasDoGoleiroM = None
            defesasDoGoleiroV = None

        try:
            faltasM = dicionario['Faltas'][0]
            faltasV = dicionario['Faltas'][1]
        except:
            faltasM = None
            faltasV = None

        try:
            cartoesAmarelosM = dicionario['Cartões amarelos'][0]
            cartoesAmarelosV = dicionario['Cartões amarelos'][1]
        except:
            cartoesAmarelosM = '0'
            cartoesAmarelosV = '0'

        try:
            cartoesVermelhosM = dicionario['Cartões vermelhos'][0]
            cartoesVermelhosV = dicionario['Cartões vermelhos'][1]
        except:
            cartoesVermelhosM = '0'
            cartoesVermelhosV = '0'

        try:
            totalDePassesM = dicionario['Total de passes'][0]
            totalDePassesV = dicionario['Total de passes'][1]
        except:
            totalDePassesM = None
            totalDePassesV = None

        try:
            desarmesM = dicionario['Tackles'][0]
            desarmesV = dicionario['Tackles'][1]
        except:
            desarmesM = None
            desarmesV = None

        try:
            ataquesM = dicionario['Ataques'][0]
            ataquesV = dicionario['Ataques'][1]
        except:
            ataquesM = None
            ataquesV = None

        try:
            ataquesPerigososM = dicionario['Ataques Perigosos'][0]
            ataquesPerigososV = dicionario['Ataques Perigosos'][1]
        except:
            ataquesPerigososM = None
            ataquesPerigososV = None

        try:
            oddsM = dicionario['Odds'][0]
            oddsE = dicionario['Odds'][1]
            oddsV = dicionario['Odds'][2]
        except:
            oddsM = None
            oddsE = None
            oddsV = None

        try:
            diferencaGols = dicionario['DiferencaGols']
        except:
            diferencaGols = None

        try:
            placarPrimeiroTempo = dicionario['PlacarPrimeiroTempo']
        except:
            placarPrimeiroTempo = None

        try:
            placarFinal = dicionario['PlacarFinal']
        except:
            placarFinal = None

        pos += 1

        partidaAnalisada = Partida(pais,campeonato,timeMandante,timeVisitante,posseDeBolaM, posseDeBolaV,tentativasDeGolM, tentativasDeGolV, 
        finalizacoesM,finalizacoesV ,chutesForaM, chutesForaV, chutesBloqueadosM, chutesBloqueadosV,
        faltasCobradasM, faltasCobradasV,escanteiosM, escanteiosV, impedimentosM, impedimentosV,defesasDoGoleiroM, defesasDoGoleiroV,
        faltasM, faltasV,cartoesAmarelosM, cartoesAmarelosV, cartoesVermelhosM, cartoesVermelhosV, 
        totalDePassesM, totalDePassesV, desarmesM, desarmesV, ataquesM, ataquesV, ataquesPerigososM,ataquesPerigososV, 
        oddsM, oddsE, oddsV, diferencaGols,placarPrimeiroTempo,placarFinal)

        writer.writerow([partidaAnalisada.Pais,partidaAnalisada.Campeonato, partidaAnalisada.TimeMandante, partidaAnalisada.TimeVisitante,
        partidaAnalisada.PosseDeBolaM,partidaAnalisada.PosseDeBolaV,partidaAnalisada.TentativasDeGolM ,
        partidaAnalisada.TentativasDeGolV,partidaAnalisada.FinalizacoesM ,partidaAnalisada.FinalizacoesV ,partidaAnalisada.ChutesForaM ,
        partidaAnalisada.ChutesForaV ,partidaAnalisada.ChutesBloqueadosM ,partidaAnalisada.ChutesBloqueadosV, partidaAnalisada.FaltasCobradasM ,
        partidaAnalisada.FaltasCobradasV ,partidaAnalisada.EscanteiosM ,partidaAnalisada.EscanteiosV ,partidaAnalisada.ImpedimentosM ,
        partidaAnalisada.ImpedimentosV ,partidaAnalisada.DefesasDoGoleiroM ,partidaAnalisada.DefesasDoGoleiroV ,partidaAnalisada.FaltasM ,
        partidaAnalisada.FaltasV ,partidaAnalisada.CartoesAmarelosM ,partidaAnalisada.CartoesAmarelosV ,partidaAnalisada.CartoesVermelhosM ,
        partidaAnalisada.CartoesVermelhosV ,partidaAnalisada.TotalDePassesM, partidaAnalisada.TotalDePassesV,partidaAnalisada.DesarmesM ,
        partidaAnalisada.DesarmesV ,partidaAnalisada.AtaquesM ,partidaAnalisada.AtaquesV ,partidaAnalisada.AtaquesPerigososM ,partidaAnalisada.AtaquesPerigososV ,
        partidaAnalisada.OddM ,partidaAnalisada.OddE ,partidaAnalisada.OddV ,partidaAnalisada.DiferencaGols,partidaAnalisada.PlacarPrimeiroTempo ,
        partidaAnalisada.PlacarFinal])


