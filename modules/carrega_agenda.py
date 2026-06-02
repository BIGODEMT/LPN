"""Carregamento dos eventos da agenda do dia."""

from datetime import datetime, date, time
from pathlib import Path

import pandas as pd


def _normaliza_hora(valor):
    if pd.isna(valor):
        return None
    if isinstance(valor, time):
        return valor
    if isinstance(valor, datetime):
        return valor.time()

    texto = str(valor).strip()
    for formato in ('%H:%M:%S', '%H:%M'):
        try:
            return datetime.strptime(texto, formato).time()
        except ValueError:
            continue

    convertido = pd.to_datetime(texto, errors='coerce')
    if pd.isna(convertido):
        return None
    return convertido.time()


def carrega_agenda(caminho_planilha=None, data_referencia=None):
    caminho_padrao = Path(__file__).resolve().parent.parent / 'agenda.xlsx'
    caminho = Path(caminho_planilha) if caminho_planilha else caminho_padrao

    if not caminho.exists():
        return False

    agenda = pd.read_excel(caminho)
    if agenda.empty:
        return False

    data_atual = data_referencia or date.today()
    hora_atual = datetime.now().time()

    descricao, responsavel, hora_agenda = [], [], []

    for _, row in agenda.iterrows():
        data_evento = pd.to_datetime(row.get('data'), errors='coerce')
        hora_evento = _normaliza_hora(row.get('hora'))

        if pd.isna(data_evento) or hora_evento is None:
            continue

        if data_evento.date() == data_atual and hora_evento >= hora_atual:
            descricao.append(row.get('descricao', 'Sem descrição'))
            responsavel.append(row.get('responsavel', 'Sem responsável'))
            hora_agenda.append(hora_evento.strftime('%H:%M'))

    if descricao:
        return descricao, responsavel, hora_agenda

    return False




















