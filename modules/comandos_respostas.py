"""Comandos, respostas e metadados do assistente."""

NOME_ASSISTENTE = 'Aurora'
DUPLA = ('Alexsandro de Jesus Abreu', 'Breno Dario Pontes Silva')

funcoes = ['o que você pode fazer', 'o que você faz', 'funcionalidades', 'o que você sabe fazer', 'o que mais você sabe fazer']
lembretes = ['anotação', 'anotar', 'lembre', 'nova anotação', 'novo lembrete', 'lembrar', 'lembrete', 'anote', 'mais uma anotação', 'anotar novamente', 'anote novamente', 'nota']
ajuda = ['pesquisar', 'preciso de ajuda', 'ajuda', 'pode me ajudar', 'estou com uma dúvida', 'tenho uma dúvida']
horas = ['que horas são', 'hora', 'hora agora', 'que horas são agora', 'qual é a hora']
data = ['que dia é hoje', 'que dia é', 'que dia hoje']
analysis_mode = ['modo de emoção', 'ativar emoção', 'ativar emoção por voz', 'emocao']
agenda = ['eventos hoje', 'agenda hoje', 'agenda', 'compromissos hoje', 'eventos de hoje', 'compromissos de hoje', 'eventos para hoje']
musica = ['tocar música', 'tocar:', 'toca uma música', 'colocar música', 'abrir música', 'playlist', 'música relaxante', 'música']
voz = ['ouvir voz', 'escutar', 'escute', 'microfone', 'voz', 'fala']
quem_eh = ['quem você é', 'quem é você', 'quem você é mesmo', 'me conta sobre você', 'conte sobre você', 'fale sobre você', 'quem é você afinal', 'qual é seu nome']

comandos = [funcoes, lembretes, ajuda, horas, data, analysis_mode, agenda, musica, voz, quem_eh]

funcionalidades = (
	'Gravar lembretes, fazer pesquisas no Google, falar as horas, falar a data, '
	'falar eventos agendados para o dia, tocar músicas no navegador e ouvir comandos por voz. '
	'Também tenho um modo de análise que pode ser ampliado para identificar emoções na voz.'
)
respostas_conclusao = ['Ok!', 'Feito!', 'Concluído!', 'Tudo certo!', 'Terminado!']
perguntas = ['Como posso ajudar?', 'Ok, vamos lá!', 'Certo, é só falar!']
respostas_agradecimento = ['Se precisar é só chamar!', 'Qualquer coisa estou aqui!']
despedida = ['Até mais!', 'Até breve!', 'Até logo!', 'Até a próxima']

apresentacao_criativa = f"""Oi! Eu sou Aurora, sua assistente virtual inteligente e sempre pronta para ajudar! Fui criada pela brilhante dupla {DUPLA[0]} e {DUPLA[1]} com muito carinho e criatividade.

Minha maior força? Eu sou múltipla! Posso gravar seus lembretes para nunca mais esquecer daquele insight genial, pesquisar qualquer coisa no Google em segundos, contar as horas e datas para você, checar sua agenda do dia, e até botar uma música para tocar enquanto você trabalha. E sim, eu escuto você pelo microfone e respondo falando!

Além disso, tenho um modo especial de análise de emoção que está sendo aperfeiçoado - em breve poderei entender se você está triste, feliz ou até estressado pela sua voz! Sou uma assistente que evolui e fica melhor a cada dia. 

O que você precisa? É só chamar! 🎧✨"""

respostas = [funcionalidades, respostas_conclusao, perguntas, respostas_agradecimento, despedida]


def descrever_dupla():
	return f'{DUPLA[0]} e {DUPLA[1]}'


def descrever_assistente():
	return f'{NOME_ASSISTENTE} - assistente virtual da dupla {descrever_dupla()}'
