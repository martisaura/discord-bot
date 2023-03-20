import hikari
import lightbulb
import random

plugin = lightbulb.Plugin('Casino')

monedes_reg = {}

with open('data/monedes.txt', 'r') as f:
    for line in f:
        id='0'
        val = 0
        pos = 0
        for word in line.split(" "):
            if (pos == 1):
                val = int(word)
                pos = 0
            else:
                if (word != 'a\n'):
                    pos = 1
                    id = word
        monedes_reg[id] = val



# COMANDO /dice
@plugin.command
@lightbulb.add_cooldown(10.0, 1, lightbulb.UserBucket)
@lightbulb.option('apuesta', 'Cantidad de monedas que apuestas', type=int)
@lightbulb.option('resultado','Un numero entre 1 y 6', type=int, min_value=1, max_value=6)
@lightbulb.command('dice', 'Acierta el numero y gana monedas!')
@lightbulb.implements(lightbulb.SlashCommand)
async def dice(ctx):
    ident = str(ctx.author.id)

    if not (ident in monedes_reg.keys()):
        monedes_reg[ident] = 100

    res = random.randint(1, 6)
    res_str = str(res)

    if (ctx.options.apuesta < 1):
        await ctx.respond("dadle las gracias a @Niltrio")
        return

    if (monedes_reg[ident] < ctx.options.apuesta):
        mon_str = str(monedes_reg[ident])
        await ctx.respond("No tienes suficientes monedas (" + mon_str + ").")

    else:
        if (res == ctx.options.resultado):
             monedes_reg[ident] += (ctx.options.apuesta * 5)
             mon_str = str(monedes_reg[ident])
             await ctx.respond("El numero era " + res_str + ". Has acertado. Tienes " + mon_str + " monedas.")

        else:
            monedes_reg[ident] = monedes_reg[ident] - ctx.options.apuesta
            mon_str = str(monedes_reg[ident])
            await ctx.respond("El numero era " + res_str +  ". Has fallado. Tienes " + mon_str + " monedas.")

#COMANDO /daily
@plugin.command
@lightbulb.add_cooldown(86400.0,1,lightbulb.UserBucket)
@lightbulb.command('daily','Daily coins.')
@lightbulb.implements(lightbulb.SlashCommand)
async def daily(ctx):
    iden = str(ctx.author.id)

    if not (iden in monedes_reg.keys()):
        monedes_reg[iden] = 110
    else:
        monedes_reg[iden] += 10
    resposta = "Tienes " + str(monedes_reg[iden]) + " monedas."
    await ctx.respond(resposta)

#COMANDO /coins
@plugin.command
@lightbulb.command('coins','La cantidad de monedas que tienes.')
@lightbulb.implements(lightbulb.SlashCommand)
async def coins(ctx):
    iden = str(ctx.author.id)
    if not (iden in monedes_reg.keys()):
        monedes_reg[iden] = 100
    resposta = "Tienes " + str(monedes_reg[iden]) + " monedas."
    await ctx.respond(resposta)

#COMANDO /coinflip
@plugin.command
@lightbulb.add_cooldown(10.0,1,lightbulb.UserBucket)
@lightbulb.option('apuesta', 'Cantidad que quieres apostar.',type=int)
@lightbulb.option('res', 'Resultado de tirar la moneda.', type=str, choices=('cara','cruz'))
@lightbulb.command('coinflip', 'Acierta el resultado para duplicar tus monedas.')
@lightbulb.implements(lightbulb.SlashCommand)
async def coinflip(ctx):
    iden = str(ctx.author.id)
    if not (iden in monedes_reg.keys()):
        monedes_reg[iden] = 100
    resposta = ""
    encert = (0==0)

    if (ctx.options.apuesta < 1):
        await ctx.respond("dadle las gracias a @Niltrio")
        return

    if (ctx.options.apuesta > monedes_reg[iden]):
        resposta = "No tienes monedas suficientes (" + str(monedes_reg[iden]) + ")."
        await ctx.respond(resposta)
        return
    else:
        res = random.randint(1,100)
        if ((res%2) == 0):
            encert = (str(ctx.options.res) == 'cara')
        else:
            encert = (str(ctx.options.res) == 'cruz')
    if encert:
        monedes_reg[iden] += ctx.options.apuesta
        resposta = "Has acertado! Ahora tienes " + str(monedes_reg[iden]) + " monedas."
    else:
        monedes_reg[iden] -= ctx.options.apuesta
        resposta = "Has fallado! Ahora tienes " + str(monedes_reg[iden]) + " monedas."
    print(ctx.options.res)
    await ctx.respond(resposta)


def load(bot):
    bot.add_plugin(plugin)

#PER GUARDAR LES DADES ABANS D'APAGAR EL BOT
def save_data():
    with open('data/monedes.txt', 'w') as f:
        for key in monedes_reg.keys():
            val = monedes_reg[key]
            escriure = key + ' '  + str(val) + ' a\n'
            f.write(escriure)


