import discord
from discord.ext import commands
import asyncio

from config import DISCORD_TOKEN
from chatbot import perguntar_ia


rules = """📜 **Regras da Python Academy BR**

>>> 1. Respeite todos os membros da comunidade.

2. Não faça spam, flood ou divulgação sem permissão.

3. Não ridicularize dúvidas de iniciantes.

4. Não envie conteúdo ofensivo, discriminatório ou inadequado.

5. Não compartilhe vírus, malware ou códigos maliciosos.

6. Use os canais corretos para cada assunto.

7. Não copie respostas sem tentar entender o código.

8. Ajude outros alunos sempre que possível.

9. Discussões são permitidas, mas mantenha o respeito.

10. O objetivo principal deste servidor é aprender Python e programação 😁
"""


intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix="!", intents=intents)


@bot.event
async def on_ready():
    print(f"PyAxo conectado como {bot.user}")


@bot.command()
async def ping(ctx):
    await ctx.send("🟢 **Status: ONLINE**\nO sistema está pronto para receber comandos.")


@bot.command()
async def regras(ctx):
    await ctx.send("Eis as regras:")
    await ctx.send(rules)


@bot.event
async def on_message(message):
    # Ignora mensagens de bots
    if message.author.bot:
        return

    # Verifica se o PyAxo foi mencionado
    if bot.user in message.mentions:
        pergunta = message.content

        # Remove a menção do bot da pergunta
        pergunta = pergunta.replace(f"<@{bot.user.id}>", "")
        pergunta = pergunta.replace(f"<@!{bot.user.id}>", "")
        pergunta = pergunta.strip()

        if not pergunta:
            await message.channel.send(
                "O conhecedor de tudo está ao seu dispor! Faça sua pergunta."
            )
        else:
            await message.channel.send("Pensando... 🧠")

            resposta = await asyncio.to_thread(perguntar_ia, pergunta)

            # Limite de caracteres do Discord
            if len(resposta) > 1900:
                resposta = resposta[:1900] + "\n\n...resposta cortada para caber no Discord."

            await message.channel.send(resposta)

    # Mantém comandos como !ping e !regras funcionando
    await bot.process_commands(message)


bot.run(DISCORD_TOKEN)