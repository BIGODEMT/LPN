"""Interface principal do projeto P2 - Assistente Virtual.

Esta versão foi refatorada para ser funcional de verdade:
- recebe texto digitado
- escuta o microfone por um botão
- responde falando
- possui botão de sair
- usa o backend modular em modules/assistente_virtual.py
"""

from datetime import datetime
import threading
import tkinter as tk
from tkinter import ttk, scrolledtext

from modules.assistente_virtual import AssistenteVirtual
from modules.voz_assistente import parar_fala_atual


class AppAssistente(tk.Tk):
    """Janela principal do assistente."""

    CORES = {
        'fundo': '#050816',
        'painel': '#0b1120',
        'borda': '#22314d',
        'texto': '#e5eefb',
        'muted': '#8fa3c0',
        'destaque': '#38bdf8',
        'botao': '#0f172a',
        'botao_hover': '#172554',
        'voz': '#0f766e',
        'voz_hover': '#115e59',
        'sair': '#991b1b',
        'sair_hover': '#7f1d1d',
        'chat_usuario': '#14213d',
        'chat_assistente': '#0d1f33',
        'chat_sistema': '#0f2a25',
    }

    def __init__(self):
        super().__init__()
        self.assistente = AssistenteVirtual()
        self._processando_voz = False

        self.title(f'{self.assistente.nome} - Assistente Virtual')
        self.geometry('1100x720')
        self.minsize(940, 640)
        self.configure(bg=self.CORES['fundo'])

        self._configurar_estilo()
        self._construir_interface()

        self._escrever('Sistema', self.assistente.apresentar(), 'sistema')
        self._escrever('Sistema', f'Dupla responsável: {self.assistente.identidade()}', 'sistema')
        self._escrever('Sistema', 'Use texto ou clique em Ouvir voz para falar com o assistente.', 'sistema')

    def _configurar_estilo(self):
        estilo = ttk.Style(self)
        try:
            estilo.theme_use('clam')
        except tk.TclError:
            pass

        estilo.configure('Topo.TFrame', background=self.CORES['painel'])
        estilo.configure('Corpo.TFrame', background=self.CORES['fundo'])
        estilo.configure('Painel.TFrame', background=self.CORES['painel'])
        estilo.configure('Titulo.TLabel', background=self.CORES['painel'], foreground=self.CORES['texto'], font=('Arial', 22, 'bold'))
        estilo.configure('Sub.TLabel', background=self.CORES['painel'], foreground=self.CORES['muted'], font=('Arial', 10))
        estilo.configure('Botao.TButton', padding=(14, 10), background=self.CORES['botao'], foreground=self.CORES['texto'])
        estilo.map('Botao.TButton', background=[('active', self.CORES['botao_hover'])])
        estilo.configure('BotaoVoz.TButton', padding=(14, 10), background=self.CORES['voz'], foreground=self.CORES['texto'])
        estilo.map('BotaoVoz.TButton', background=[('active', self.CORES['voz_hover'])])
        estilo.configure('BotaoSair.TButton', padding=(14, 10), background=self.CORES['sair'], foreground=self.CORES['texto'])
        estilo.map('BotaoSair.TButton', background=[('active', self.CORES['sair_hover'])])

    def _construir_interface(self):
        topo = ttk.Frame(self, style='Topo.TFrame', padding=(24, 20))
        topo.pack(fill='x')

        ttk.Label(topo, text='Assistente Virtual por Voz', style='Titulo.TLabel').pack(anchor='w')
        ttk.Label(
            topo,
            text='Digite comandos ou use o microfone. O assistente responde falando.',
            style='Sub.TLabel',
        ).pack(anchor='w', pady=(6, 0))

        corpo = ttk.Frame(self, style='Corpo.TFrame', padding=20)
        corpo.pack(fill='both', expand=True)

        painel_principal = tk.Frame(
            corpo,
            bg=self.CORES['painel'],
            highlightthickness=1,
            highlightbackground=self.CORES['borda'],
        )
        painel_principal.pack(side='left', fill='both', expand=True, padx=(0, 14))

        informacoes = tk.Frame(painel_principal, bg=self.CORES['painel'])
        informacoes.pack(fill='x', padx=18, pady=(16, 10))

        tk.Label(
            informacoes,
            text='Conversa',
            bg=self.CORES['painel'],
            fg=self.CORES['texto'],
            font=('Arial', 13, 'bold'),
        ).pack(anchor='w')

        tk.Label(
            informacoes,
            text='Comandos: olá, que horas são, pesquisar: assunto, tocar: música, tchau.',
            bg=self.CORES['painel'],
            fg=self.CORES['muted'],
            font=('Arial', 9),
        ).pack(anchor='w', pady=(4, 0))

        self.chat = scrolledtext.ScrolledText(
            painel_principal,
            wrap='word',
            bg='#0a1020',
            fg=self.CORES['texto'],
            insertbackground=self.CORES['texto'],
            relief='flat',
            padx=16,
            pady=16,
            font=('Arial', 10),
        )
        self.chat.pack(fill='both', expand=True, padx=18, pady=(0, 12))
        self.chat.configure(state='disabled')
        self.chat.tag_configure('sistema', foreground='#6ee7b7', background=self.CORES['chat_sistema'], spacing3=8, lmargin1=10, lmargin2=10, rmargin=10)
        self.chat.tag_configure('usuario', foreground='#fbbf24', background=self.CORES['chat_usuario'], spacing3=8, lmargin1=10, lmargin2=10, rmargin=10)
        self.chat.tag_configure('assistente', foreground='#60a5fa', background=self.CORES['chat_assistente'], spacing3=8, lmargin1=10, lmargin2=10, rmargin=10)

        entrada_bloco = tk.Frame(painel_principal, bg=self.CORES['painel'])
        entrada_bloco.pack(fill='x', padx=18, pady=(0, 16))

        self.entrada = tk.Entry(
            entrada_bloco,
            font=('Arial', 11),
            relief='flat',
            bd=0,
            highlightthickness=1,
            highlightbackground=self.CORES['borda'],
            highlightcolor=self.CORES['destaque'],
        )
        self.entrada.pack(side='left', fill='x', expand=True, ipady=10)
        self.entrada.bind('<Return>', self._enviar_texto)

        self.botao_enviar = ttk.Button(entrada_bloco, text='Enviar', style='Botao.TButton', command=self._enviar_texto)
        self.botao_enviar.pack(side='left', padx=(10, 0))

        self.botao_voz = ttk.Button(entrada_bloco, text='Ouvir voz', style='BotaoVoz.TButton', command=self._ouvir_voz)
        self.botao_voz.pack(side='left', padx=(10, 0))

        self.botao_sair = ttk.Button(entrada_bloco, text='Sair', style='BotaoSair.TButton', command=self.destroy)
        self.botao_sair.pack(side='left', padx=(10, 0))

        self.status = tk.Label(
            self,
            text='Pronto.',
            anchor='w',
            bg='#02040b',
            fg=self.CORES['muted'],
            padx=18,
            pady=8,
            font=('Arial', 9),
        )
        self.status.pack(fill='x', side='bottom')

        painel_lateral = tk.Frame(
            corpo,
            bg=self.CORES['painel'],
            width=290,
            highlightthickness=1,
            highlightbackground=self.CORES['borda'],
        )
        painel_lateral.pack(side='right', fill='y')
        painel_lateral.pack_propagate(False)

        tk.Label(
            painel_lateral,
            text='Atalhos',
            bg=self.CORES['painel'],
            fg=self.CORES['texto'],
            font=('Arial', 12, 'bold'),
        ).pack(anchor='w', padx=16, pady=(16, 8))

        atalhos = [
            'olá',
            'que horas são',
            'pesquisar: inteligência artificial',
            'tocar: lo-fi',
            'tchau',
        ]

        for texto in atalhos:
            ttk.Button(
                painel_lateral,
                text=texto,
                style='Botao.TButton',
                command=lambda valor=texto: self._preencher(valor),
            ).pack(fill='x', padx=14, pady=5)

        tk.Label(
            painel_lateral,
            text='Dicas: diga o nome do assistente antes do comando na fala.',
            wraplength=250,
            justify='left',
            bg=self.CORES['painel'],
            fg=self.CORES['muted'],
            font=('Arial', 9),
        ).pack(anchor='w', padx=16, pady=(18, 0))

    def _agora(self):
        return datetime.now().strftime('%H:%M')

    def _escrever(self, autor, mensagem, tag):
        self.chat.configure(state='normal')
        self.chat.insert('end', f'[{self._agora()}] {autor}: {mensagem}\n\n', tag)
        self.chat.see('end')
        self.chat.configure(state='disabled')
        self.status.configure(text=f'Última ação: {self._agora()}')

    def _responder(self, mensagem, falar_resposta=True):
        resposta = self.assistente.executar(mensagem)
        self._escrever(self.assistente.nome, resposta, 'assistente')
        if falar_resposta:
            threading.Thread(target=self.assistente.falar_resposta, args=(resposta,), daemon=True).start()
        # Verifica se o usuário pediu para sair (mais abrangente)
        texto_limpo = mensagem.lower().strip()
        if any(palavra in texto_limpo for palavra in ['sair', 'fechar', 'encerrar', 'tchau', 'adeus', 'desligar']):
            self.after(700, self.destroy)

    def _enviar_texto(self, event=None):
        parar_fala_atual()
        mensagem = self.entrada.get().strip()
        if not mensagem:
            self.status.configure(text='Digite algo antes de enviar.')
            return

        self._escrever('Você', mensagem, 'usuario')
        self.entrada.delete(0, 'end')
        self._responder(mensagem, falar_resposta=True)

    def _preencher(self, valor):
        self.entrada.delete(0, 'end')
        self.entrada.insert(0, valor)
        self.entrada.focus_set()

    def _finalizar_voz(self, texto, arquivo_audio):
        self._processando_voz = False
        self.botao_voz.configure(state='normal')

        if not texto or texto.strip() == '':
            self._escrever('Sistema', f'Não consegui reconhecer a fala. Tente novamente mais claramente.', 'sistema')
            self.status.configure(text='Áudio capturado, mas sem transcrição útil.')
            return

        self._escrever('Você (voz)', texto, 'usuario')
        self._responder(texto, falar_resposta=True)
        self.status.configure(text=f'Áudio reconhecido com sucesso.')

    def _erro_voz(self, erro):
        self._processando_voz = False
        self.botao_voz.configure(state='normal')
        mensagem_erro = str(erro)
        if 'Não consegui entender' in mensagem_erro:
            msg_user = 'Não consegui entender o áudio. Tente falar mais claramente ou espere o final do tempo de gravação.'
        elif 'serviço de reconhecimento' in mensagem_erro or 'conexão' in mensagem_erro.lower():
            msg_user = 'Erro ao conectar ao serviço de reconhecimento. Verifique sua conexão com a internet.'
        else:
            msg_user = f'Falha ao processar áudio: {mensagem_erro}'
        
        self._escrever('Sistema', msg_user, 'sistema')
        self.status.configure(text='Erro ao acessar o microfone ou transcrever a fala.')

    def _capturar_voz(self):
        try:
            texto, arquivo_audio = self.assistente.ouvir_voz(duracao=5)
            self.after(0, lambda: self._finalizar_voz(texto, arquivo_audio))
        except (ValueError, RuntimeError) as erro:
            self.after(0, lambda erro=erro: self._erro_voz(erro))
        except Exception as erro:
            self.after(0, lambda erro=erro: self._erro_voz(f'Erro inesperado: {erro}'))

    def _ouvir_voz(self):
        parar_fala_atual()
        if self._processando_voz:
            return

        self._processando_voz = True
        self.botao_voz.configure(state='disabled')
        self.status.configure(text='Ouvindo por 5 segundos... fale agora.')
        self._escrever('Sistema', 'Capturando áudio do microfone...', 'sistema')
        threading.Thread(target=self._capturar_voz, daemon=True).start()


def main():
    app = AppAssistente()
    app.mainloop()


if __name__ == '__main__':
    main()