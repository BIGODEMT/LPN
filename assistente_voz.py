"""Assistente virtual por voz para projeto academico.

Fluxo principal:
1. O assistente escuta um trecho de audio do microfone.
2. O texto reconhecido e analisado em busca do nome do assistente.
3. Se o nome for pronunciado, o comando e processado.
4. O assistente responde falando em voz alta.

O codigo foi dividido em funcoes pequenas para facilitar manutencao,
apresentacao em aula e expansao futura.
"""

from __future__ import annotations

from datetime import datetime
from pathlib import Path
from urllib.parse import quote_plus
import webbrowser

import numpy as np
import sounddevice as sd
from scipy.io.wavfile import write as wav_write
import speech_recognition as sr
import pyttsx3
import wikipedia


# Nome do assistente configuravel. O assistente reage quando esse nome aparece
# no comando, por exemplo: "Jarvis, que horas sao?"
nome_assistente = "Aurora"

# Pasta do projeto usada para gravacoes temporarias.
BASE_DIR = Path(__file__).resolve().parent
PASTA_GRAVACOES = BASE_DIR / "recordings"
PASTA_GRAVACOES.mkdir(parents=True, exist_ok=True)

# Arquivo temporario de audio gravado.
ARQUIVO_AUDIO = PASTA_GRAVACOES / "comando_voz.wav"


def configurar_motor_voz():
    """Cria e configura o sintetizador de voz."""
    motor = pyttsx3.init()
    motor.setProperty("rate", 175)
    motor.setProperty("volume", 1.0)
    return motor


def falar(texto, motor):
    """Fala um texto em voz alta e tambem mostra no terminal."""
    print(f"{nome_assistente}: {texto}")
    motor.say(texto)
    motor.runAndWait()


def ouvir_microfone(duracao=5, taxa_amostragem=16000):
    """Grava alguns segundos do microfone e salva em WAV.

    Esta abordagem evita depender de PyAudio e continua usando
    SpeechRecognition para a transcricao.
    """
    print("Ouvindo... fale agora.")
    gravacao = sd.rec(
        int(duracao * taxa_amostragem),
        samplerate=taxa_amostragem,
        channels=1,
        dtype=np.int16,
    )
    sd.wait()
    wav_write(str(ARQUIVO_AUDIO), taxa_amostragem, gravacao)
    return ARQUIVO_AUDIO


def transcrever_audio(caminho_audio):
    """Transcreve o audio gravado usando a API do Google via SpeechRecognition."""
    reconhecedor = sr.Recognizer()
    with sr.AudioFile(str(caminho_audio)) as origem:
        audio = reconhecedor.record(origem)

    try:
        return reconhecedor.recognize_google(audio, language="pt-BR")
    except sr.UnknownValueError:
        return ""
    except sr.RequestError as erro:
        print(f"Erro ao transcrever audio: {erro}")
        return ""


def remover_nome_assistente(texto):
    """Remove o nome do assistente do texto para facilitar o processamento."""
    texto_limpo = texto.lower().replace(nome_assistente.lower(), "")
    return texto_limpo.replace(",", " ").replace("  ", " ").strip()


def saudacao_atual():
    """Escolhe uma saudacao adequada ao horario."""
    hora = datetime.now().hour
    if hora < 12:
        return "Bom dia!"
    if hora < 18:
        return "Boa tarde!"
    return "Boa noite!"


def dizer_hora():
    """Retorna a hora atual em formato amigavel."""
    return datetime.now().strftime("Agora sao %H horas e %M minutos.")


def pesquisar_informacao(termo):
    """Busca um resumo rapido na Wikipedia.

    Se a busca falhar, abre uma pesquisa no navegador.
    """
    termo = termo.strip()
    if not termo:
        return "Voce precisa informar o assunto da pesquisa."

    wikipedia.set_lang("pt")
    try:
        resumo = wikipedia.summary(termo, sentences=2, auto_suggest=True, redirect=True)
        return resumo
    except Exception:
        url = f"https://www.google.com/search?q={quote_plus(termo)}"
        webbrowser.open(url)
        return f"Nao encontrei resumo direto. Abri a busca por {termo}."


def tocar_midia_youtube(termo):
    """Abre uma busca no YouTube para tocar musica ou video."""
    termo = termo.strip()
    if not termo:
        termo = "musica relaxante"

    url = f"https://www.youtube.com/results?search_query={quote_plus(termo)}"
    webbrowser.open(url)
    return f"Abrindo o YouTube para {termo}."


def processar_comando(comando):
    """Analisa o comando e devolve a resposta correspondente."""
    texto = comando.lower().strip()

    if not texto:
        return "Nao consegui entender. Fale novamente, por favor."

    # Saudacoes.
    if any(palavra in texto for palavra in ["ola", "olá", "bom dia", "boa tarde", "boa noite", "oi"]):
        return saudacao_atual() + f" Eu sou {nome_assistente}."

    # Hora atual.
    if any(palavra in texto for palavra in ["hora", "horas", "que horas sao", "que horas são"]):
        return dizer_hora()

    # Busca rapida na internet.
    if texto.startswith("pesquisar") or texto.startswith("buscar"):
        partes = texto.split(":", 1)
        termo = partes[1] if len(partes) > 1 else texto.replace("pesquisar", "").replace("buscar", "")
        return pesquisar_informacao(termo)

    # Tocar musica ou video no YouTube.
    if texto.startswith("tocar") or texto.startswith("musica") or texto.startswith("música"):
        partes = texto.split(":", 1)
        termo = partes[1] if len(partes) > 1 else texto.replace("tocar", "").replace("musica", "").replace("música", "")
        return tocar_midia_youtube(termo)

    # Encerrar o programa.
    if any(palavra in texto for palavra in ["tchau", "desligar", "sair", "encerrar", "fechar"]):
        return "encerrando"

    return "Nao entendi o comando. Tente dizer hora, pesquisar, tocar ou tchau."


def deve_ativar_assistente(texto):
    """Verifica se o nome do assistente foi pronunciado.

    Se o nome nao aparecer, o assistente fica em modo passivo.
    """
    texto_normalizado = texto.lower()
    return nome_assistente.lower() in texto_normalizado or texto_normalizado.startswith("assistente")


def executar_assistente():
    """Loop principal do assistente virtual."""
    motor = configurar_motor_voz()

    falar(f"{saudacao_atual()} Eu sou {nome_assistente}. Diga meu nome para me ativar.", motor)

    while True:
        try:
            arquivo_audio = ouvir_microfone(duracao=5)
            texto = transcrever_audio(arquivo_audio)

            if not texto:
                print("Nao foi possivel reconhecer a fala.")
                continue

            print(f"Usuario: {texto}")

            if not deve_ativar_assistente(texto):
                print("Nome do assistente nao foi detectado. Aguardando ativacao...")
                continue

            comando = remover_nome_assistente(texto)
            resposta = processar_comando(comando)

            if resposta == "encerrando":
                falar("Tudo bem, encerrando o assistente. Ate mais!", motor)
                break

            falar(resposta, motor)

        except KeyboardInterrupt:
            falar("Encerrando por interrupcao do teclado.", motor)
            break
        except Exception as erro:
            print(f"Erro inesperado: {erro}")
            falar("Ocorreu um erro ao processar o comando.", motor)


if __name__ == "__main__":
    executar_assistente()