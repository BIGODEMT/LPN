# Projeto P2 - Assistente Virtual

## Identificação
- Nome do assistente: Aurora
- Dupla: Alexsandro de Jesus Abreu   e  Breno Dario Pontes Silva

## Funcionalidades
- Responder quais comandos o assistente sabe executar.
- Registrar anotações em `anotacao.txt`.
- Consultar data e hora.
- Consultar eventos do dia na agenda.
- Pesquisar no Google.
- Abrir busca de músicas no navegador.
- Preparar o projeto para evolução do modo de análise de emoção.
- Executar um assistente por voz em `assistente_voz.py`.

## Interface
- A aplicação principal é `app.py`.
- A interface foi organizada com Tkinter e inclui atalhos rápidos para facilitar a demonstração.

## Assistente por Voz
- O script principal para a versão de voz é `assistente_voz.py`.
- O nome do assistente pode ser alterado na variável `nome_assistente` no topo do arquivo.
- O assistente grava o microfone em `recordings/`, transcreve o audio e responde falando.

## Execução
1. Abra um terminal na pasta do projeto.
2. Ative a venv do projeto:

```bash
source .venv/bin/activate
```

3. Instale as bibliotecas necessárias dentro da venv:

```bash
pip install speechrecognition pyttsx3 sounddevice scipy numpy wikipedia pandas openpyxl gTTS
```

4. No Linux, instale também o sintetizador de voz do sistema para o `pyttsx3` funcionar corretamente:

```bash
sudo apt-get install espeak-ng
```

5. Para abrir a interface visual principal, execute:

```bash
python app.py
```

Na interface visual, o assistente também responde falando quando você envia um comando pelo teclado ou pelo botão de voz.

6. Para executar a versão por voz, execute:

```bash
python assistente_voz.py
```

Na versão por voz, ele escuta o microfone e fala a resposta em voz alta.

7. Para ativar o assistente por voz, diga o nome definido em `nome_assistente` antes do comando.

8. Exemplos de comandos:
   - `Aurora, bom dia`
   - `Aurora, que horas são?`
   - `Aurora, pesquisar: inteligência artificial`
   - `Aurora, tocar: lo-fi`
   - `Aurora, tchau`

9. Se preferir, também é possível executar sem ativar a venv usando o interpretador direto:

```bash
.venv/bin/python app.py
.venv/bin/python assistente_voz.py
```

## Observação
- O nome do assistente e a dupla podem ser alterados em `modules/comandos_respostas.py`.

## Bibliotecas para instalar
Instale com `pip` dentro do ambiente virtual:

```bash
pip install speechrecognition pyttsx3 sounddevice scipy numpy wikipedia pandas openpyxl gTTS
```

Se quiser abrir vídeos ou músicas no YouTube de forma automatizada com outra biblioteca, você pode adicionar `pywhatkit`.

## Observações importantes
- O app principal com interface visual está em [app.py](app.py).
- A versão por voz está em [assistente_voz.py](assistente_voz.py).
- As pastas `models/` e `recordings/` já fazem parte da integração do projeto.
- Se o assistente não falar, verifique se `espeak-ng` está instalado no sistema e se você está rodando dentro da venv.