"""Ferramentas de voz para o assistente virtual."""

import subprocess
import tempfile
from threading import Lock
from pathlib import Path

import numpy as np
import sounddevice as sd
from scipy.io.wavfile import write as wav_write

try:
    import speech_recognition as sr
except ImportError:  # pragma: no cover - fallback defensivo
    sr = None

try:
    import pyttsx3
except ImportError:  # pragma: no cover - fallback defensivo
    pyttsx3 = None

try:
    from gtts import gTTS
except ImportError:  # pragma: no cover - fallback defensivo
    gTTS = None


_fala_lock = Lock()
_motor_fala = None
_parar_fala = False
_processo_ffplay = None


def parar_fala_atual():
    """Sinal global para parar a fala que está em andamento."""
    global _parar_fala, _processo_ffplay
    _parar_fala = True
    
    # Tenta parar o processo ffplay se estiver em execução
    if _processo_ffplay is not None:
        try:
            _processo_ffplay.terminate()
            _processo_ffplay.wait(timeout=1)
        except Exception:
            try:
                _processo_ffplay.kill()
            except Exception:
                pass
        _processo_ffplay = None
    
    # Tenta parar o motor pyttsx3 se estiver em uso
    if _motor_fala is not None:
        try:
            _motor_fala.stop()
        except Exception:
            pass


def _limpar_sinal_parar():
    """Limpa o sinal após usar."""
    global _parar_fala
    _parar_fala = False


def _selecionar_voz_portugues(motor):
    """Seleciona uma voz em portugues quando o sistema oferece essa opcao."""
    try:
        vozes = motor.getProperty('voices')
    except Exception:
        return False

    candidatos_exatos = []
    candidatos = []
    for voz in vozes:
        identificador = str(getattr(voz, 'id', '')).lower()
        nome = str(getattr(voz, 'name', '')).lower()
        idiomas = getattr(voz, 'languages', []) or []
        idiomas_texto = ' '.join(str(item).lower() for item in idiomas)

        if identificador.endswith('roa/pt-br') or identificador.endswith('/pt-br') or 'portuguese (brazil)' in nome:
            candidatos_exatos.append(voz)
        elif 'pt-br' in identificador or 'pt-br' in nome:
            candidatos.insert(0, voz)
        elif 'pt/' in identificador or 'portuguese' in nome or 'pt' in idiomas_texto:
            candidatos.append(voz)

    if candidatos_exatos:
        candidatos = candidatos_exatos + candidatos

    if not candidatos:
        return False

    voz_escolhida = candidatos[0]
    try:
        motor.setProperty('voice', voz_escolhida.id)
        return True
    except Exception:
        return False


def _obter_motor_fala():
    global _motor_fala
    if pyttsx3 is None:
        return None

    if _motor_fala is None:
        try:
            motor = pyttsx3.init()
            motor.setProperty('rate', 178)
            motor.setProperty('volume', 1.0)
            _selecionar_voz_portugues(motor)
            _motor_fala = motor
        except Exception:
            _motor_fala = None

    return _motor_fala


def falar(texto):
    global _parar_fala, _processo_ffplay
    _limpar_sinal_parar()
    
    if gTTS is not None and not _parar_fala:
        with tempfile.NamedTemporaryFile(suffix='.mp3', delete=False) as arquivo_temporario:
            caminho_audio = arquivo_temporario.name

        try:
            audio = gTTS(text=texto, lang='pt')
            audio.save(caminho_audio)
            if not _parar_fala:
                # Usa Popen para poder parar o processo se necessário
                _processo_ffplay = subprocess.Popen(
                    ['ffplay', '-nodisp', '-autoexit', '-loglevel', 'quiet', caminho_audio],
                    stdout=subprocess.DEVNULL,
                    stderr=subprocess.DEVNULL,
                )
                try:
                    _processo_ffplay.wait()
                except Exception:
                    pass
                finally:
                    _processo_ffplay = None
            return True
        except Exception:
            pass
        finally:
            try:
                Path(caminho_audio).unlink(missing_ok=True)
            except Exception:
                pass

    if _parar_fala:
        return False

    motor = _obter_motor_fala()
    if motor is not None:
        with _fala_lock:
            if not _parar_fala:
                motor.say(texto)
                motor.runAndWait()
        return True

    if not _parar_fala:
        print(texto)
    return False


def gravar_audio(caminho_audio=None, duracao=5, taxa_amostragem=16000):
    pasta_padrao = Path(__file__).resolve().parent.parent / 'recordings'
    pasta_padrao.mkdir(parents=True, exist_ok=True)
    arquivo_audio = Path(caminho_audio) if caminho_audio else pasta_padrao / 'speech.wav'

    gravacao = sd.rec(int(duracao * taxa_amostragem), samplerate=taxa_amostragem, channels=1, dtype='int16')
    sd.wait()
    wav_write(str(arquivo_audio), taxa_amostragem, gravacao)
    return arquivo_audio


def transcrever_audio(caminho_audio, idioma='pt-BR'):
    if sr is None:
        raise RuntimeError('SpeechRecognition não está instalado no ambiente.')

    reconhecedor = sr.Recognizer()
    try:
        with sr.AudioFile(str(caminho_audio)) as origem:
            audio = reconhecedor.record(origem)
        return reconhecedor.recognize_google(audio, language=idioma)
    except sr.UnknownValueError:
        raise ValueError('Não consegui entender o áudio. Tente falar mais claramente.')
    except sr.RequestError as e:
        raise RuntimeError(f'Erro ao acessar o serviço de reconhecimento: {e}')
    except Exception as e:
        raise RuntimeError(f'Erro ao transcrever áudio: {e}')


def ouvir_microfone(duracao=5, caminho_audio=None, idioma='pt-BR'):
    try:
        arquivo_audio = gravar_audio(caminho_audio=caminho_audio, duracao=duracao)
        texto = transcrever_audio(arquivo_audio, idioma=idioma)
        return texto, arquivo_audio
    except (ValueError, RuntimeError) as e:
        arquivo_audio = Path(caminho_audio) if caminho_audio else Path(__file__).resolve().parent.parent / 'recordings' / 'speech.wav'
        raise ValueError(str(e))
    except Exception as e:
        arquivo_audio = Path(caminho_audio) if caminho_audio else Path(__file__).resolve().parent.parent / 'recordings' / 'speech.wav'
        raise RuntimeError(f'Erro ao ouvir microfone: {e}')
