"""Núcleo do assistente virtual."""

from datetime import datetime
from pathlib import Path
from urllib.parse import quote_plus
import random
import webbrowser

from modules.carrega_agenda import carrega_agenda
from modules.comandos_respostas import (
    DUPLA,
    NOME_ASSISTENTE,
    ajuda,
    analysis_mode,
    agenda,
    comandos,
    despedida,
    funcoes,
    horas,
    data,
    lembretes,
    musica,
    perguntas,
    respostas,
    respostas_agradecimento,
    respostas_conclusao,
    descrever_assistente,
    descrever_dupla,
    quem_eh,
    apresentacao_criativa,
)
from modules.voz_assistente import falar, ouvir_microfone


class AssistenteVirtual:
    def __init__(self, nome=None, dupla=None, arquivo_anotacao=None, caminho_agenda=None):
        self.nome = nome or NOME_ASSISTENTE
        self.dupla = dupla or DUPLA
        self.arquivo_anotacao = Path(arquivo_anotacao) if arquivo_anotacao else Path(__file__).resolve().parent.parent / 'anotacao.txt'
        self.caminho_agenda = caminho_agenda
        self.raiz_projeto = Path(__file__).resolve().parent.parent
        self.modelo_emocao = self.raiz_projeto / 'models' / 'speech_emotion_recognition.hdf5'
        self.pasta_gravacoes = self.raiz_projeto / 'recordings'

    def identidade(self):
        return descrever_assistente()

    def apresentar(self):
        return f'Olá! Eu sou {self.nome}, criado pela dupla {descrever_dupla()}.'

    def recursos_projeto(self):
        return {
            'anotacoes': str(self.arquivo_anotacao),
            'agenda': str(self.caminho_agenda or (self.raiz_projeto / 'agenda.xlsx')),
            'gravacoes': str(self.pasta_gravacoes),
            'modelo_emocao': str(self.modelo_emocao),
        }

    def listar_funcionalidades(self):
        return respostas[0]

    def registrar_lembrete(self, texto):
        texto = texto.strip()
        if not texto:
            return 'Não recebi o texto da anotação.'

        self.arquivo_anotacao.parent.mkdir(parents=True, exist_ok=True)
        with self.arquivo_anotacao.open('a', encoding='utf-8') as arquivo:
            arquivo.write(f'{texto}\n')

        return random.choice(respostas_conclusao)

    def listar_lembretes(self):
        if not self.arquivo_anotacao.exists():
            return 'Ainda não há anotações salvas.'

        conteudo = self.arquivo_anotacao.read_text(encoding='utf-8').strip()
        if not conteudo:
            return 'Ainda não há anotações salvas.'

        return conteudo

    def consultar_agenda(self):
        eventos = carrega_agenda(self.caminho_agenda)
        if not eventos:
            return 'Não encontrei eventos para hoje.'

        descricao, responsavel, hora_agenda = eventos
        linhas = ['Eventos de hoje:']
        for desc, resp, hora in zip(descricao, responsavel, hora_agenda):
            linhas.append(f'- {hora} | {desc} | {resp}')
        return '\n'.join(linhas)

    def tocar_musica(self, consulta='lofi relaxante'):
        consulta = (consulta or 'lofi relaxante').strip()
        url = f'https://www.youtube.com/results?search_query={quote_plus(consulta)}'
        webbrowser.open(url)
        return f'Abrindo busca de música para "{consulta}" no navegador.'

    def ouvir_voz(self, duracao=5):
        texto, arquivo_audio = ouvir_microfone(duracao=duracao, caminho_audio=self.pasta_gravacoes / 'speech.wav')
        return texto, arquivo_audio

    def falar_resposta(self, texto):
        return falar(texto)

    def pesquisar(self, consulta):
        consulta = consulta.strip()
        if not consulta:
            return 'Informe um termo para pesquisar.'

        url = f'https://www.google.com/search?q={quote_plus(consulta)}'
        webbrowser.open(url)
        return f'Pesquisando "{consulta}" no Google.'

    def mostrar_data_hora(self):
        agora = datetime.now()
        return agora.strftime('Agora são %H:%M de %d/%m/%Y.')

    def executar(self, mensagem):
        texto = mensagem.strip().lower()
        if not texto:
            return 'Digite um comando para começar.'

        if any(palavra in texto for palavra in funcoes):
            return self.listar_funcionalidades()

        if any(palavra in texto for palavra in quem_eh):
            return apresentacao_criativa

        if any(palavra in texto for palavra in lembretes):
            anotacao = ''
            if ':' in mensagem:
                anotacao = mensagem.split(':', 1)[1].strip()
            else:
                palabras_ordenadas = sorted(lembretes, key=len, reverse=True)
                for pw in palabras_ordenadas:
                    if pw in texto:
                        idx = texto.find(pw)
                        anotacao = mensagem[idx + len(pw):].strip()
                        if anotacao.startswith(':'):
                            anotacao = anotacao[1:].strip()
                        break
            if anotacao:
                return self.registrar_lembrete(anotacao)
            return 'Digite "anotar: sua mensagem" ou diga "anotar [sua mensagem]" para salvar um lembrete.'

        if any(palavra in texto for palavra in ajuda):
            consulta = ''
            if ':' in mensagem:
                consulta = mensagem.split(':', 1)[1].strip()
            else:
                palabras_ordenadas = sorted(ajuda, key=len, reverse=True)
                for pw in palabras_ordenadas:
                    if pw in texto:
                        idx = texto.find(pw)
                        consulta = mensagem[idx + len(pw):].strip()
                        if consulta.startswith(':'):
                            consulta = consulta[1:].strip()
                        break
            if consulta:
                return self.pesquisar(consulta)
            return 'Digite "pesquisar: assunto" ou diga "pesquisar [assunto]" para abrir uma busca no Google.'

        if any(palavra in texto for palavra in horas):
            agora = datetime.now()
            return agora.strftime('Agora são %H:%M')

        if any(palavra in texto for palavra in data):
            # Meses em português
            meses = {
                1: 'janeiro', 2: 'fevereiro', 3: 'março', 4: 'abril',
                5: 'maio', 6: 'junho', 7: 'julho', 8: 'agosto',
                9: 'setembro', 10: 'outubro', 11: 'novembro', 12: 'dezembro'
            }
            agora = datetime.now()
            dia = agora.day
            mes = meses[agora.month]
            ano = agora.year
            return f'Hoje é {dia} de {mes} de {ano}.'

        if any(palavra in texto for palavra in analysis_mode):
            return 'O modo de emoção está reservado para a próxima etapa do projeto.'

        if any(palavra in texto for palavra in agenda):
            return self.consultar_agenda()

        if any(palavra in texto for palavra in musica):
            consulta = ''
            if ':' in mensagem:
                consulta = mensagem.split(':', 1)[1].strip()
            else:
                palabras_ordenadas = sorted(musica, key=len, reverse=True)
                for pw in palabras_ordenadas:
                    pw_clean = pw.rstrip(':').strip()
                    if pw_clean and pw_clean in texto:
                        idx = texto.find(pw_clean)
                        consulta = mensagem[idx + len(pw_clean):].strip()
                        if consulta.startswith(':'):
                            consulta = consulta[1:].strip()
                        break
                if not consulta:
                    consulta = 'música relaxante'
            return self.tocar_musica(consulta)

        if texto in {'oi', 'olá', 'ola', 'bom dia', 'boa tarde', 'boa noite'}:
            return random.choice(perguntas)

        if texto in {'obrigado', 'obrigada', 'valeu', 'grato', 'grata'}:
            return random.choice(respostas_agradecimento)

        if any(palavra in texto for palavra in {'sair', 'fechar', 'encerrar', 'tchau', 'adeus', 'desligar'}):
            return random.choice(despedida)

        return 'Não entendi. Tente: funcionalidades, anotar: texto, pesquisar: assunto, agenda, música: nome, horas ou data.'