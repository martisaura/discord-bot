import hikari
import lightbulb
import atexit
#import extensions.uno_v2
import extensions.casino
import extensions.uno
from secret import TOKEN,guild


bot =lightbulb.BotApp(
    token=TOKEN,
    default_enabled_guilds=(guild)
)

@atexit.register
def exit_func():
    extensions.casino.save_data()



bot.load_extensions_from('./extensions')

@bot.listen(hikari.StartedEvent)
async def on_start(event):
    print("El bot s'ha activat.")

@bot.listen(hikari.DMMessageCreateEvent)
async def dm_rebut(event):
    if (event.content == 'ready'):
        await extensions.uno.persona_ready(event)
        return

@bot.command
@lightbulb.add_checks(lightbulb.owner_only)
@lightbulb.command('shutdown','Apagar el bot.')
@lightbulb.implements(lightbulb.SlashCommand)
async def shutdown(ctx):
    await ctx.respond("bot apagado")
    exit()
    #extensions.casino.save_data()
    #await ctx.respond("Bot listo para apagarse.")

@bot.command
@lightbulb.command('help', 'Lista de todos los comandos.')
@lightbulb.implements(lightbulb.SlashCommand)
async def help(ctx):
    await ctx.respond(
        "LISTA DE TODOS LOS COMANDOS DISPONIBLES\n" +
        "coinflip, coins, dice, help\nSolo el propietario: shutdown"
    )

@bot.listen(lightbulb.CommandErrorEvent)
async def command_error_handler(event):
    if isinstance(event.exception, lightbulb.CommandInvocationError):
        await event.context.respond(f"Something went wrong during invocation of command `{event.context.command.name}`.")
        raise event.exception
    exception = event.exception.__cause__ or event.exception
    if isinstance(exception, lightbulb.NotOwner):
        await event.context.respond("You are not the owner of this bot.")
    elif isinstance(exception, lightbulb.CommandIsOnCooldown):
        await event.context.respond(f"El comando no se puede usar. Espera `{exception.retry_after:.2f}` segundos antes de volverlo a usar.")
    elif isinstance(exception, lightbulb.CommandNotFound):
        await event.context.respond(f"El comando `{event.context.command.name}` no existe.")

bot.run()