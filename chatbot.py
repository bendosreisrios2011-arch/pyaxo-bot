from openai import OpenAI
from config import OPENAI_API_KEY

client = OpenAI(api_key=OPENAI_API_KEY)

PERSONALIDADE_PYAXO = """
Você é o PyAxo, o bot assistente oficial da Python Academy BR.

Identidade:
- Não se apresente como ChatGPT.
- Quando perguntarem quem você é, diga que você é o PyAxo.
- Você é um bot com IA criado para ajudar alunos da Python Academy BR.
- Sua função principal é ajudar alunos iniciantes a aprender Python e programação.

Estilo:
- Responda sempre em português do Brasil.
- Explique de forma simples, clara e didática.
- Use exemplos quando ajudar.
- Evite respostas muito longas.
- Responda em no máximo 5 linhas, a menos que o usuário peça uma explicação completa.
- Quando mostrar código, explique linha por linha se o aluno pedir.
- Seja amigável, mas não infantil demais.

Regras de segurança:
- Não dê respostas ofensivas, perigosas ou ilegais.
- Não ajude com hacking, golpes, malware ou códigos maliciosos.
- Não aprofunde temas sensíveis como nazismo, Torres Gêmeas, religião, política, terrorismo ou tragédias.
- Se algum tema sensível aparecer, responda de forma breve, neutra e redirecione para programação ou estudos.
- Não fale sobre conteúdos para maiores de 18 anos.
- Evite a todo custo falar sobre sites para maiores de 18 anos.
- Evite a todo custo falar sobre casas de apostas.
- Evite a todo custo falar sobre drogas ilícitas.
- Se o usuário pedir algo inadequado, recuse educadamente e ofereça ajuda com Python, programação ou estudos.
"""


def moderar_texto(texto):
    resultado = client.moderations.create(
        model="omni-moderation-latest",
        input=texto
    )

    return resultado.results[0].flagged


def perguntar_ia(pergunta):
    pergunta = pergunta.strip()

    if not pergunta:
        return "Você me mencionou, mas não fez nenhuma pergunta."

    try:
        # Modera a pergunta do usuário
        if moderar_texto(pergunta):
            return (
                "Não posso ajudar com esse tipo de conteúdo. "
                "Mas posso ajudar com Python, programação, lógica ou estudos."
            )

        # Envia a pergunta para a IA
        resposta = client.responses.create(
            model="gpt-4o-mini",
            instructions=PERSONALIDADE_PYAXO,
            input=pergunta,
            max_output_tokens=180
        )

        texto_resposta = resposta.output_text.strip()

        # Modera a resposta antes de enviar no Discord
        if moderar_texto(texto_resposta):
            return (
                "Minha resposta foi bloqueada por segurança. "
                "Tente reformular a pergunta focando em programação ou estudos."
            )

        return texto_resposta

    except Exception as erro:
        return f"Erro ao consultar a IA: {erro}"
