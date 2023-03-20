import hikari
import lightbulb
import random

botardo = hikari.GatewayBot("MTAzMjY2OTM4Mjg3NjM0ODQ0Nw.GN8r3p.NFoFWwadjwiyeItYmJvVy8FWQvwnRz4bNkNOtw")
plugin2 = lightbulb.Plugin('Uno')
jugadors = {}
context = []
game = 0
relacio = {}
creador = ''
c_de_partida = ''
cartas_en_mazo = 216
llista = []

mazo = {
    'Bloqueo_azul': 4, 'Bloqueo_rojo': 4, 'Bloqueo_amarillo': 4, 'Bloqueo_verde': 4,
    '0_azul': 4, '0_rojo': 4, '0_amarillo': 4, '0_verde': 4,
    '1_azul': 4, '1_rojo': 4, '1_amarillo': 4, '1_verde': 4,
    '2_azul': 4, '2_rojo': 4, '2_amarillo': 4, '2_verde': 4,
    '3_azul': 4, '3_rojo': 4, '3_amarillo': 4, '3_verde': 4,
    '4_azul': 4, '4_rojo': 4, '4_amarillo': 4, '4_verde': 4,
    '5_azul': 4, '5_rojo': 4, '5_amarillo': 4, '5_verde': 4,
    '6_azul': 4, '6_rojo': 4, '6_amarillo': 4, '6_verde': 4,
    '7_azul': 4, '7_rojo': 4, '7_amarillo': 4, '7_verde': 4,
    '8_azul': 4, '8_rojo': 4, '8_amarillo': 4, '8_verde': 4,
    '9_azul': 4, '9_rojo': 4, '9_amarillo': 4, '9_verde': 4,
    'roba_dos_azul': 4, 'roba_dos_rojo': 4, 'roba_dos_amarillo': 4, 'roba_dos_verde': 4,
    'cambio_de_sentido_azul': 4, 'cambio_de_sentido_rojo': 4, 'cambio_de_sentido_amarillo': 4, 'cambio_de_sentido_verde': 4,
    'cambio_de_color': 4, 'roba_cuatro': 4
    }


# COMANDO /playUno
@plugin2.command
@lightbulb.add_cooldown(60.0, 1, lightbulb.GuildBucket)
@lightbulb.command("playuno", "Empieza una partida de uno.")
@lightbulb.implements(lightbulb.SlashCommand)
async def ini_Uno(ctx):
    if (game != 0):
        await ctx.respond("Ya hay una partida de uno creada.")
        return
    else:
        global creador
        creador = str(ctx.author.id)
        global jugadors
        jugadors = {ctx.author.id:0}
        global c_de_partida
        global context
        context = ctx
        c_de_partida = str(ctx.author)
        await ctx.respond("Partida creada. \n"
                          "Para unirse usad el comando /joinuno.\n"
                          "Pueden jugar hasta 6 personas.\n"
                          "Para empezar la partida, el creador de la partida debe usar el comando /startuno.\n"
                          "Si en 1 minuto no se ha iniciado la partida, se podrá reiniciar el proceso.")

#COMANDO /ready EN DM
@plugin2.command
@lightbulb.app_command_permissions(dm_enabled=True)
@lightbulb.command('ready','Estas listo para juagr')
@lightbulb.implements(lightbulb.SlashCommand)
async def ready(ctx):
    if (ctx.author.id in jugadors.keys()):
        context.append(ctx)
        await ctx.respond("Ya estas listo para jugar")
    else:
        await ctx.respond("No estas en la lista de jugadores")


#COMANDO /joinuno
@plugin2.command
@lightbulb.command('joinuno', 'Unete a la partida.')
@lightbulb.implements(lightbulb.SlashCommand)
async def join_Uno(ctx):
    if (game == 1):
        await ctx.respond("Ya no te puedes unir a la partida.")
        return
    if (creador == ''):
        await ctx.respond("No hay ninguna partida creada.")
        return
    if (len(jugadors) == 6):
        await ctx.respond("La partida esta llena!")
        return
    new_player = ctx.author.id
    if new_player not in jugadors.keys():
        jugadors[new_player] = len(jugadors) - 1
        await ctx.respond("Te has unido a la partida!")
        return
    await ctx.respond("Ya estas registrado en la partida.")

#COMANDO /startuno
@plugin2.command
@lightbulb.command('startuno', 'Empieza la partida.')
@lightbulb.implements(lightbulb.SlashCommand)
async def start_Uno(ctx):
    if (creador == ''):
        await ctx.respond("No hay una partida creada.\n"
                          "Para crear una partida, usa el comando /playuno.")
        return
    if (creador != str(ctx.author.id)):
        await ctx.respond("No eres el creador de esta partida!")
        return
    global game
    if (game == 1):
        await ctx.respond("Ya se está jugando la partida!")
        return
    game = 1

    #inicialitzacio de la partida
    for value in range(1,(7*len(jugadors))+1):
        carta = random.randint(1,cartas_en_mazo)
        global llista
        for key in mazo.keys():
            if (mazo[key]>=carta):
                if(len(llista) != 0):
                    llista.append(key)
                else:
                    llista = [key]
                print (llista)
                --mazo[key]
                if (value%7 == 0):
                    relacio[(value/7)-1] = llista
                    llista = []
                --cartas_en_mazo
                break
            carta -= mazo[key]

    for value in relacio.keys():
        print(relacio[value])


    #final de la inicialitzacio de la partida, es diu qui juga
    resposta = "La partida ha empezado!\n" \
               "Los jugadores son:\n"
    for key in jugadors.keys():
        resposta += ("<@" + str(key) + ">\n")
    await ctx.respond(resposta)


async def persona_ready(event):
    print(event.content)
    print (type(hikari))
    print("\n")
    chan = hikari.channels.TextableChannel
    print (type(chan))
    #await chan.send(event.channel_id,"ja esta ready")
    #await hikari.GatewayBot("MTAzMjY2OTM4Mjg3NjM0ODQ0Nw.GN8r3p.NFoFWwadjwiyeItYmJvVy8FWQvwnRz4bNkNOtw").rest.create_message(event.channel_id,"ready rebut")

def load(bot):
    bot.add_plugin(plugin2)



