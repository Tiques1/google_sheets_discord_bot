#!/usr/bin/python3

import discord
import sheet_api
import configparser
import threading
from discord.ext import commands

config = configparser.ConfigParser()
config.read('apikeys.cfg.txt')

apikey = configparser.ConfigParser()
apikey.read('api_keys.cfg.txt')

client = commands.Bot(command_prefix='>', intents=discord.Intents.all())
intents = discord.Intents.all()
intents.members = True


@client.event
async def on_ready():
    print("I'm ready")
    print("----------")
    sometimes_update()


def sometimes_update():
    for i in config.sections():
        guild = client.get_guild(int(i))
        members = [["id", "Имя", "id имени", "Ник на сервере", "Бот"]]
        for j in range(0, len(guild.members)):
            gm = guild.members
            members.append([str(gm[j].id),
                            str(gm[j].name),
                            str(gm[j].discriminator),
                            str(gm[j].nick),
                            str(gm[j].bot)])
        sheet_api.file_update(members, i)
    try:
        threading.Timer(10, sometimes_update).start()
    except():
        return


@client.event
async def on_member_join(member):
    sheet_api.append([str(member.id), member.name, str(member.discriminator), str(member.nick), str(member.bot)],
                     str(member.guild.id))


@client.event
async def on_member_remove(member):
    sheet_api.delete(str(member.id), str(member.guild.id))


@client.command(name="start", help = "Создает конфиг сервера")
async def start(ctx):
    config[str(ctx.guild.id)] = {}
    await reset_variables(ctx)
    await ctx.send("Для начала пользования ботом вам нужно создать документ в google sheets.\n"
                   "Затем предоставьте доступ этому аккаунту с возможностью редактирования:\n"
                   "tiques@centered-osprey-384615.iam.gserviceaccount.com\n"
                   "После чего используйте команду change_value sheeturl и укажите ссылку на документ\n"
                   "И наконец, используя команду change_value user_name укажите имя листа, "
                   "где будет вестись список участников.\n"
                   "Чтобы список появился, обнулите его с помощью команды reset")


@client.command(name="reset_variables", help = "Обнуляет все переменные")
async def reset_variables(ctx):
    try:
        config[str(ctx.guild.id)]['user_name'] = ''
        config[str(ctx.guild.id)]['sheeturl'] = ''
        with open('apikeys.cfg.txt', 'w') as configfile:
            config.write(configfile)
        config.read('apikeys.cfg.txt')
    except KeyError:
        await ctx.send("Переменные не найдены. Проверьте правильность написания."
                       " Для создания переменных используйте команду >start")


@client.command(name="change_value", help = "Изменяет значение переменной")
async def change_value(ctx, value: str = commands.parameter(description="Возможные переменные: sheeturl, user_name"),
                       user_name: str = commands.parameter(description="")):
    try:
        config.set(str(ctx.guild.id), value, user_name)
        with open('apikeys.cfg.txt', 'w') as configfile:
            config.write(configfile)
    except configparser.NoSectionError:
        await ctx.send("Переменная не найдена. Проверьте правильность написания."
                       " Для создания переменной используйте команду >start")


@client.command(name="reset", help = "Обновляет список участников сервера")
async def reset(member):
    members = [["id", "Имя", "id имени", "Ник на сервере", "Бот"]]
    for i in range(0, len(member.guild.members)):
        members.append([str(member.guild.members[i].id), member.guild.members[i].name,
                        member.guild.members[i].discriminator,
                        str(member.guild.members[i].nick), str(member.guild.members[i].bot)])

    sheet_api.file_update(members, str(member.guild.id))


@client.event
async def on_message(message):
    if str(message.author.id) == str(apikey['api']['punishment_bot']) and str(message.channel.id) == str(apikey['api']['punishment_channel']):
        s = message.embeds[0].to_dict()
        line1 = []
        kind = ''
        i = s['author']['name'].index('|')

        while True:
            i += 1
            if s['author']['name'][i] == '|':
                break
            kind += s['author']['name'][i]

        line = dict(type=kind, User='', Moderator='', Length='', Reason='', time=s['timestamp'])

        for j in s['fields']:
            if j['name'] in line:
                line[j['name']] = j['value']

        for l in line.values():
            line1.append(l)

        sheet_api.punishment_history(line1, str(message.guild.id))


# members:
# SequenceProxy(dict_values([<Member id=155149108183695360 name='Dyno' discriminator='3861' bot=True nick=None
# guild=<Guild id=1090216132868317257 name='Test' shard_id=0 chunked=True member_count=22>>,
# <Member id=159985870458322944 name='MEE6' discriminator='4876' bot=True nick=None
# guild=<Guild id=1090216132868317257 name='Test' shard_id=0 chunked=True member_count=22>>, <Member id=184405311681986560 name='FredBoat♪♪' discriminator='7284' bot=True nick=None guild=<Guild id=1090216132868317257 name='Test' shard_id=0 chunked=True member_count=22>>, <Member id=321046928391667712 name='April' discriminator='4100' bot=True nick=None guild=<Guild id=1090216132868317257 name='Test' shard_id=0 chunked=True member_count=22>>, <Member id=360081866461806595 name='Translator' discriminator='2653' bot=True nick=None guild=<Guild id=1090216132868317257 name='Test' shard_id=0 chunked=True member_count=22>>, <Member id=372022813839851520 name='AltDentifier' discriminator='5594' bot=True nick=None guild=<Guild id=1090216132868317257 name='Test' shard_id=0 chunked=True member_count=22>>, <Member id=458276816071950337 name='ServerStats' discriminator='0197' bot=True nick=None guild=<Guild id=1090216132868317257 name='Test' shard_id=0 chunked=True member_count=22>>, <Member id=460017141207531520 name='Crepqyc' discriminator='7527' bot=False nick=None guild=<Guild id=1090216132868317257 name='Test' shard_id=0 chunked=True member_count=22>>, <Member id=500658624109084682 name='Emoji.gg' discriminator='7083' bot=True nick=None guild=<Guild id=1090216132868317257 name='Test' shard_id=0 chunked=True member_count=22>>, <Member id=512925108499906561 name='zixjnenwj' discriminator='8387' bot=False nick=None guild=<Guild id=1090216132868317257 name='Test' shard_id=0 chunked=True member_count=22>>, <Member id=628213411813130262 name='Tiques' discriminator='9959' bot=False nick=None guild=<Guild id=1090216132868317257 name='Test' shard_id=0 chunked=True member_count=22>>, <Member id=674885857458651161 name='MemberList' discriminator='4997' bot=True nick=None guild=<Guild id=1090216132868317257 name='Test' shard_id=0 chunked=True member_count=22>>, <Member id=713579531935416331 name='Crypto Checker' discriminator='4052' bot=True nick=None guild=<Guild id=1090216132868317257 name='Test' shard_id=0 chunked=True member_count=22>>, <Member id=830530156048285716 name='Lofi Radio' discriminator='1753' bot=True nick=None guild=<Guild id=1090216132868317257 name='Test' shard_id=0 chunked=True member_count=22>>, <Member id=842425623754702868 name='Desure' discriminator='9967' bot=True nick='радикальный гедонизм' guild=<Guild id=1090216132868317257 name='Test' shard_id=0 chunked=True member_count=22>>, <Member id=889098512564899870 name='Roles' discriminator='6006' bot=True nick=None guild=<Guild id=1090216132868317257 name='Test' shard_id=0 chunked=True member_count=22>>, <Member id=920797097270333480 name='Donate' discriminator='9669' bot=True nick=None guild=<Guild id=1090216132868317257 name='Test' shard_id=0 chunked=True member_count=22>>, <Member id=936929561302675456 name='Midjourney Bot' discriminator='9282' bot=True nick=None guild=<Guild id=1090216132868317257 name='Test' shard_id=0 chunked=True member_count=22>>, <Member id=1053015370115588147 name='ChatGPT' discriminator='3799' bot=True nick=None guild=<Guild id=1090216132868317257 name='Test' shard_id=0 chunked=True member_count=22>>, <Member id=1055196262896500776 name='ChatGPT' discriminator='2931' bot=True nick=None guild=<Guild id=1090216132868317257 name='Test' shard_id=0 chunked=True member_count=22>>, <Member id=1090211566764429352 name='Искин' discriminator='9346' bot=True nick=None guild=<Guild id=1090216132868317257 name='Test' shard_id=0 chunked=True member_count=22>>, <Member id=1016775687543205918 name='sihihgidv' discriminator='9213' bot=False nick=None guild=<Guild id=1090216132868317257 name='Test' shard_id=0 chunked=True member_count=22>>]))


# {'color': 4437377, 'type': 'rich', 'description': ':dynoSuccess: sihihgidv#9213 has been warned. || 1'}
# embed message example
# {'footer': {'text': 'ID: 1016775687543205918'},
# 'author': {'name': 'Case 24 | Warn | sihihgidv#9213'},
#  'fields': [{'value': '@sihihgidv', 'name': 'User', 'inline': True},
# {'value': '@Tiques', 'name': 'Moderator', 'inline': True}, {'value': '1', 'name': 'Reason', 'inline': True}],
#  'color': 16439902, 'timestamp': '2023-04-23T13:49:51.843000+00:00', 'type': 'rich'}


client.run(apikey['api']['bottoken'])
