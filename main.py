import json
import re
import disnake
import asyncio
import requests
import datetime
from disnake.ext import commands
no="❌️"

def str_time_to_seconds(str_time, language='ru'):
	conv_dict = {
		'w': 'weeks',
		'week': 'weeks',
		'weeks': 'weeks',
		'н': 'weeks',
		'нед': 'weeks',
		'неделя': 'weeks',
		'недели': 'weeks',
		'недель': 'weeks',
		'неделю': 'weeks',

		'd': 'days',
		'day': 'days',
		'days': 'days',
		'д': 'days',
		'день': 'days',
		'дня': 'days',
		'дней': 'days',

		'h': 'hours',
		'h': 'hours',
		'hour': 'hours',
		'hours': 'hours',
		'ч': 'hours',
		'час': 'hours',
		'часа': 'hours',
		'часов': 'hours',

		'm': 'minutes',
		'min': 'minutes',
		'mins': 'minutes',
		'minute': 'minutes',
		'minutes': 'minutes',
		'мин': 'minutes',
		'минута': 'minutes',
		'минуту': 'minutes',
		'минуты': 'minutes',
		'минут': 'minutes',

		's': 'seconds',
		'sec': 'seconds',
		'secs': 'seconds',
		'second': 'seconds',
		'seconds': 'seconds',
		'сек': 'seconds',
		'секунда': 'seconds',
		'секунду': 'seconds',
		'секунды': 'seconds',
		'секунд': 'seconds'
	}

	pat = r'[0-9]+[w|week|weeks|н|нед|неделя|недели|недель|неделю|d|day|days|д|день|дня|дней|h|hour|hours|ч|час|часа|часов|min|mins|minute|minutes|мин|минута|минуту|минуты|минут|s|sec|secs|second|seconds|c|сек|секунда|секунду|секунды|секунд]{1}'
	def timestr_to_dict(tstr):
		#convert 1d2h3m4s to {"d": 1, "h": 2, "m": 3, "s": 4}
		return {conv_dict[p[-1]]: int(p[:-1]) for p in re.findall(pat, str_time)}

	def timestr_to_seconds(tstr):
		return datetime.timedelta(**timestr_to_dict(tstr)).total_seconds()

	def plural(n, arg):
		days = []
		if language == "ru":
			if arg == 'weeks':
				days = ['неделя', 'недели', 'недель']
			elif arg == 'days':
				days = ['день', 'дня', 'дней']
			elif arg == 'hours':
				days = ['час', 'часа', 'часов']
			elif arg == 'minutes':
				days = ['минута', 'минуты', 'минут']
			elif arg == 'seconds':
				days = ['секунда', 'секунды', 'секунд']
		elif language == "en":
			if arg == 'weeks':
				days = ['week', 'weeks', 'weeks']        
			elif arg == 'days':
				days = ['day', 'day', 'days']
			elif arg == 'hours':
				days = ['hour', 'hour', 'hours']
			elif arg == 'minutes':
				days = ['minute', 'minute', 'minutes']
			elif arg == 'seconds':
				days = ['second', 'second', 'seconds']

		if n % 10 == 1 and n % 100 != 11:
			p = 0
		elif 2 <= n % 10 <= 4 and (n % 100 < 10 or n % 100 >= 20):
			p = 1
		else:
			p = 2
		return str(n) + ' ' + days[p]

	counter_in_str = ""
	for i in timestr_to_dict(str_time).items():
		counter_in_str += f"{plural(i[1], i[0])} "

	return int(timestr_to_seconds(str_time)), counter_in_str

color="0x05fcfa"

client=commands.Bot(command_prefix='TT+', intents=disnake.Intents.all())
client.remove_command( 'help' )

@client.event
async def on_ready():
	print('[LOG] Запуск бота прошел успешно')
	channel = client.get_channel(975256344569450546)
	Embed = disnake.Embed(description = 'Бот запущен!', title = 'Бот запущен', color=0x05fcfa)
	await channel.send(embed=Embed)

@client.slash_command()
async def ping(inter):
	await inter.response.send_message('Pong!') 

@client.slash_command(description="Обычный Say без Embed'a")
async def say_o(inter, message):
	await inter.response.send_message(message)

@client.slash_command(description='Команда бана')
async def ban(ctx, member: disnake.Member=None, time1: str=None, *, reason=None):
	if not ctx.author.guild_permissions.ban_members:
		Embed = disnake.Embed(description = '❌️ **Ошибка! У вас недостаточно прав**', color=0x05fcfa)
		await ctx.send(embed = Embed)
		return
	if member == ctx.author:
		Embed = disnake.Embed(description = '❌️ **Ошибка! Вы не можете забанить себя**', color=0x05fcfa)
		await ctx.send(embed = Embed)
		return
	if member == ctx.guild.owner:
		Embed = disnake.Embed(description = '❌️ **Ошибка! Вы не можете забанить владельца сервера**', color=0x05fcfa)
		await ctx.send(embed = Embed)
		return
	if member.top_role >= ctx.author.top_role:
		Embed = disnake.Embed(description = '❌️ **Ошибка! Вы не можете забанить участника с более высокой ролью**', color=0x05fcfa)
		await ctx.send(embed = Embed)
		return
	if member.top_role >= ctx.me.top_role:
		Embed = disnake.Embed(description = '❌️ **Ошибка! Я не могу забанить участника выше или на равне со мной**', color=0x05fcfa)
		await ctx.send(embed = Embed)
		return
	try:
		channel = client.get_channel(941283209457569792)
		owner = ctx.guild.owner
		if time1 == None:
			await member.ban(reason=reason)
			embed = disnake.Embed(title=f"✅|{member} был забанен", color = 0x05fcfa)
			embed.add_field(name = "Модератор", value = ctx.author)
			embed.add_field(name = "Причина", value = 'Отсутствует')
			embed.add_field(name = "Время", value = 'Навсегда')
			embed.add_field(name = "ID забаненного участника:", value = member.id)
			await ctx.send(embed=embed)

			embed = disnake.Embed(title=f"Вы были забанены на сервере {ctx.guild.name}", color = 0x05fcfa)
			embed.add_field(name = "Модератор", value = ctx.author)
			embed.add_field(name = "Причина", value = 'Отсутствует')
			embed.add_field(name = "Время", value = 'Навсегда')
			await member.send(embed=embed)

			embed = disnake.Embed(title=f"{ctx.author} забанил пользователя {member} на сервере {ctx.guild.name}", color = 0x05fcfa)
			embed.add_field(name = "ID сервера:", value = ctx.guild.id)
			embed.add_field(name = "ID забаненного участника:", value = member.id)
			embed.add_field(name = "Владелец", value = ctx.guild.owner.mention)
			embed.add_field(name = "ID Владельца", value = ctx.guild.owner_id)
			embed.add_field(name="Причина:", value='Отсутствует')
			embed.add_field(name = "Время", value = 'Навсегда')
			await channel.send(embed=embed)

			embed = disnake.Embed(title=f"{ctx.author} забанил пользователя {member} на вашем сервере с именем {ctx.guild.name}", color = 0x05fcfa)
			embed.add_field(name = "ID сервера:", value = ctx.guild.id)
			embed.add_field(name = "ID забаненного участника:", value = member.id)
			embed.add_field(name="Причина:", value='Отсутствует')
			embed.add_field(name = "Время", value = 'Навсегда')
			await owner.send(embed=embed)
			return
		seconds, str_time = str_time_to_seconds(time1)
		if seconds <1:
			str_time = reason
			str_time=None
			reason1 = time1
			await member.ban(reason=reason1)
			embed = disnake.Embed(title=f"✅|{member} был забанен", color = 0x05fcfa)
			embed.add_field(name = "Модератор", value = ctx.author)
			embed.add_field(name = "Причина", value = reason1)
			embed.add_field(name = "Время", value = 'Навсегда')
			embed.add_field(name = "ID забаненного участника:", value = member.id)
			await ctx.send(embed=embed)

			embed = disnake.Embed(title=f"Вы были забанены на сервере {ctx.guild.name}", color = 0x05fcfa)
			embed.add_field(name = "Модератор", value = ctx.author)
			embed.add_field(name = "Причина", value = reason1)
			embed.add_field(name = "Время", value = 'Навсегда')
			await member.send(embed=embed)

			embed = disnake.Embed(title=f"{ctx.author} забанил пользователя {member} на сервере {ctx.guild.name}", color = 0x05fcfa)
			embed.add_field(name = "ID сервера:", value = ctx.guild.id)
			embed.add_field(name = "ID забаненного участника:", value = member.id)
			embed.add_field(name = "Владелец", value = ctx.guild.owner.mention)
			embed.add_field(name = "ID Владельца", value = ctx.guild.owner_id)
			embed.add_field(name="Причина:", value=reason1)
			embed.add_field(name = "Время", value = 'Навсегда')
			await channel.send(embed=embed)

			embed = disnake.Embed(title=f"{ctx.author} забанил пользователя {member} на вашем сервере с именем {ctx.guild.name}", color = 0x05fcfa)
			embed.add_field(name = "ID сервера:", value = ctx.guild.id)
			embed.add_field(name = "ID забаненного участника:", value = member.id)
			embed.add_field(name="Причина:", value=reason1)
			embed.add_field(name = "Время", value = 'Навсегда')
			await owner.send(embed=embed)
			return
		else:
			seconds, str_time = str_time_to_seconds(time1)
			await member.ban(reason=f'"{reason}"')
			embed = disnake.Embed(title=f"✅|{member} был забанен", color = 0x05fcfa)
			embed.add_field(name = "Модератор", value = ctx.author)
			embed.add_field(name = "Причина", value = reason)
			embed.add_field(name = "Время", value = time1)
			embed.add_field(name = "ID забаненного участника:", value = member.id)
			await ctx.send(embed=embed)

			embed = disnake.Embed(title=f"Вы были забанены на сервере {ctx.guild.name}", color = 0x05fcfa)
			embed.add_field(name = "Модератор", value = ctx.author)
			embed.add_field(name = "Причина", value = reason)
			embed.add_field(name = "Время", value = time1)
			await member.send(embed=embed)
		
			embed = disnake.Embed(title=f"{ctx.author} забанил пользователя {member} на сервере {ctx.guild.name}", color = 0x05fcfa)
			embed.add_field(name = "ID сервера:", value = ctx.guild.id)
			embed.add_field(name = "ID забаненного участника:", value = member.id)
			embed.add_field(name = "Владелец", value = ctx.guild.owner.mention)
			embed.add_field(name = "ID Владельца", value = ctx.guild.owner_id)
			embed.add_field(name="Причина:", value=reason)
			embed.add_field(name = "Время", value = time1)
			await channel.send(embed=embed)

			embed = disnake.Embed(title=f"{ctx.author} забанил пользователя {member} на вашем сервере с именем {ctx.guild.name}", color = 0x05fcfa)
			embed.add_field(name = "ID сервера:", value = ctx.guild.id)
			embed.add_field(name = "ID забаненного участника:", value = member.id)
			embed.add_field(name="Причина:", value=reason)
			embed.add_field(name = "Время", value = time1)
			await owner.send(embed=embed)
			await asyncio.sleep(seconds)
			await member.unban()
			link = await ctx.channel.create_invite(max_age=300)
			Embed = disnake.Embed(description = f'У тебя закончился бан на сервере "{ctx.guild.name}"!Заходи по ссылке: {link}', color = 0x05fcfa)
			await member.send(embed = Embed)
	except disnake.Forbidden:
		return
	except disnake.HTTPException:
		return
@client.slash_command()
async def say(ctx, *, text:str=None):
	if text == None:
		Embed = disnake.Embed(description = 'Нету текста', color=0x05fcfa)
		await ctx.send(embed = Embed)
	else:
		Embed = disnake.Embed(description = text, color=0x05fcfa)
		await ctx.send(embed = Embed)

@client.slash_command()
async def kick(ctx, *, member):
	if not member:
		Embed = disnake.Embed(description = '❌️ **Ошибка! Вы не указали пользователя**\n**Аргументы данной команды**\n**[] обязательный аргумент, () необязательный аргумент**\n\n**/kick [участник] (причина)**', color=0x05fcfa)
		await ctx.send(embed = Embed) 
		return
	if member == ctx.author:
		Embed = disnake.Embed(description = '❌️ **Ошибка! Вы не можете кикнуть себя**', color=0x05fcfa)
		await ctx.send(embed = Embed)
		return
	if member.top_role >= ctx.author.top_role:
		Embed = disnake.Embed(description = '❌️ **Ошибка! Вы не можете кикнуть участника с более высокой ролью**', color=0x05fcfa)
		await ctx.send(embed = Embed)
		return
	if not ctx.author.guild_permissions.kick_members:
		Embed = disnake.Embed(description = '❌️ **Ошибка! У вас недостаточно прав**', color=0x05fcfa)
		await ctx.send(embed = Embed)
		return
	try:
		channel = client.get_channel(941283209457569792)
		owner = ctx.guild.owner
		await member.kick(reason=reason)

		embed = disnake.Embed(title=f"✅|{member} был кикнут", color = 0x05fcfa)
		embed.add_field(name = "Модератор", value = ctx.author)
		embed.add_field(name = "Причина", value = reason)
		embed.add_field(name = "ID забаненного участника:", value = member.id)
		await ctx.send(embed=embed)

		embed = disnake.Embed(title=f"Вы были кикнуты с сервера {ctx.guild.name}", color = 0x05fcfa)
		embed.add_field(name = "Модератор", value = ctx.author)
		embed.add_field(name = "Причина", value = reason)
		await member.send(embed=embed)
		
		embed = disnake.Embed(title=f"{ctx.author} кикнул пользователя {member} на сервере {ctx.guild.name}", color = 0x05fcfa)
		embed.add_field(name = "ID сервера:", value = ctx.guild.id)
		embed.add_field(name = "ID кикнутого участника:", value = member.id)
		embed.add_field(name = "Владелец", value = ctx.guild.owner.mention)
		embed.add_field(name = "ID Владельца", value = ctx.guild.owner_id)
		embed.add_field(name="Причина:", value=reason)
		await channel.send(embed=embed)

		embed = disnake.Embed(title=f"{ctx.author} кикнул пользователя {member} на вашем сервере с именем {ctx.guild.name}", color = 0x05fcfa)
		embed.add_field(name = "ID сервера:", value = ctx.guild.id)
		embed.add_field(name = "ID кикнутого участника:", value = member.id)
		embed.add_field(name="Причина:", value=reason)
		await owner.send(embed=embed)

	except disnake.Forbidden:
		return
	except disnake.HTTPException:
		return

@client.slash_command(description='Рандомная лиса')
async def fox(ctx):
	response = requests.get('https://some-random-api.ml/img/fox') # Get-запрос
	json_data = json.loads(response.text) # Извлекаем JSON

	embed = disnake.Embed(color = 0x05fcfa, title = 'Лиса') # Создание Embed'a
	embed.set_image(url = json_data['link']) # Устанавливаем картинку Embed'a
	await ctx.send(embed = embed) # Отправляем Embed
@client.slash_command(description='Рандомная собака')
async def dog(ctx):
	response = requests.get('https://some-random-api.ml/img/dog') # Get-запрос
	json_data = json.loads(response.text) # Извлекаем JSON

	embed = disnake.Embed(color = 0x05fcfa, title = 'Собака') # Создание Embed'a
	embed.set_image(url = json_data['link']) # Устанавливаем картинку Embed'a
	await ctx.send(embed = embed) # Отправляем E
@client.slash_command(description='Рандомная панда')
async def cat(ctx):
	response = requests.get('https://some-random-api.ml/img/cat') # Get-запрос
	json_data = json.loads(response.text) # Извлекаем JSON

	embed = disnake.Embed(color = 0x05fcfa, title = 'Кот') # Создание Embed'a
	embed.set_image(url = json_data['link']) # Устанавливаем картинку Embed'a
	await ctx.send(embed = embed) # Отправляем Embed
@client.slash_command(description='Рандомная панда')
async def panda(ctx):
	response = requests.get('https://some-random-api.ml/img/panda') # Get-запрос
	json_data = json.loads(response.text) # Извлекаем JSON

	embed = disnake.Embed(color = 0x05fcfa, title = 'Панда') # Создание Embed'a
	embed.set_image(url = json_data['link']) # Устанавливаем картинку Embed'a
	await ctx.send(embed = embed) # Отправляем Embed

@client.slash_command(description='Рандомный мем')
async def meme(ctx):
	response = requests.get('https://some-random-api.ml/meme') # Get-запрос
	json_data = json.loads(response.text) # Извлекаем JSON
	embed = disnake.Embed(color = 0x05fcfa, title = 'Мемы!', description = json_data['caption']) # Создание Embed'a
	embed.set_image(url = json_data['image']) # Устанавливаем картинку Embed'a
	await ctx.send(embed = embed)

@client.slash_command(description='Статистика бот')
async def stat(ctx):
	embed = disnake.Embed(title="Статистика TicTacBOT", color = 0x05fcfa)
	embed.add_field(name = "Серверов", value = len(client.guilds))
	embed.add_field(name = "Пользователей", value = len(set(client.get_all_members())))
	embed.add_field(name = "Каналов", value = len(set(client.get_all_channels())))
	embed.add_field(name = "Голосовых соединений", value = len(client.voice_clients))
	embed.add_field(name = "Задержка", value = f"{(round(client.latency, 2))} секунд")
	embed.set_thumbnail(url = "https://cdn.discordapp.com/app-icons/975086040266190849/7c378abd20606a7b53bfd634ee5a062a.png?size=256")
	await ctx.send(embed=embed)


@client.slash_command(description='Голубой аватар дискорд')
async def blue_avatar( ctx ):
  embed = disnake.Embed(title="Голубая аватарка Discord", color = 0x05fcfa)
  embed.set_image(url = 'https://cdn.discordapp.com/attachments/936681962255548437/940197366533857300/blue.png')
  await ctx.send(embed=embed)


@client.slash_command(description='Зеленый аватар дискорд')
async def green_avatar( ctx ):
  embed = disnake.Embed(title="Зеленая аватарка Discord", color = 0x05fcfa)
  embed.set_image(url = 'https://cdn.discordapp.com/attachments/936681962255548437/940201969929293844/green.png')
  await ctx.send(embed=embed)

@client.slash_command(description='Серая аватарка дискорд')
async def gray_avatar( ctx ):
  embed = disnake.Embed(title="Серая аватарка Discord", color = 0x05fcfa)
  embed.set_image(url = 'https://cdn.discordapp.com/attachments/936681962255548437/940201970160009256/gray.png')
  await ctx.send(embed=embed)

@client.slash_command(description='Серая аватарка дискорд')
async def red_avatar( ctx ):
  embed = disnake.Embed(title="Красная аватарка Discord", color = 0x05fcfa)
  embed.set_image(url = 'https://cdn.discordapp.com/attachments/936681962255548437/940201970348744745/red.png')
  await ctx.send(embed=embed)



@client.slash_command(description='Розовая аватарка')
async def pink_avatar( ctx ):
  embed = disnake.Embed(title="Розовая аватарка Discord", color = 0x05fcfa)
  embed.set_image(url = 'https://cdn.discordapp.com/attachments/936681962255548437/940201970600378428/pink.png')
  await ctx.send(embed=embed)


@client.slash_command(description='Желтая аватарка дискорд')
async def yellow_avatar( ctx ):
  embed = disnake.Embed(title="Желтая аватарка Discord", color = 0x05fcfa)
  embed.set_image(url = 'https://cdn.discordapp.com/attachments/936681962255548437/940201970864631828/yellow.png')
  await ctx.send(embed=embed)


@client.slash_command(description='Разноцветная аватарка дискорд')
async def multi_avatar( ctx ):
  embed = disnake.Embed(title="Разноцветная аватарка Discord", color = 0x05fcfa)
  embed.set_image(url = 'https://cdn.discordapp.com/attachments/936681962255548437/940196944322658374/multi.gif')
  await ctx.send(embed=embed)

@client.slash_command(description='Все аватарки дискорд')
async def all_avatar( ctx ):
  embed = disnake.Embed(title="Голубая аватарка Discord", color = 0x05fcfa)
  embed.set_image(url = 'https://cdn.discordapp.com/attachments/936681962255548437/940197366533857300/blue.png')
  await ctx.send(embed=embed)
  embed = disnake.Embed(title="Разноцветная аватарка Discord", color = 0x05fcfa)
  embed.set_image(url = 'https://cdn.discordapp.com/attachments/936681962255548437/940196944322658374/multi.gif')
  await ctx.send(embed=embed)
  embed = disnake.Embed(title="Желтая аватарка Discord", color = 0x05fcfa)
  embed.set_image(url = 'https://cdn.discordapp.com/attachments/936681962255548437/940201970864631828/yellow.png')
  await ctx.send(embed=embed)
  embed = disnake.Embed(title="Розовая аватарка Discord", color = 0x05fcfa)
  embed.set_image(url = 'https://cdn.discordapp.com/attachments/936681962255548437/940201970600378428/pink.png')
  await ctx.send(embed=embed)
  embed = disnake.Embed(title="Красная аватарка Discord", color = 0x05fcfa)
  embed.set_image(url = 'https://cdn.discordapp.com/attachments/936681962255548437/940201970348744745/red.png')
  await ctx.send(embed=embed)
  embed = disnake.Embed(title="Серая аватарка Discord", color = 0x05fcfa)
  embed.set_image(url = 'https://cdn.discordapp.com/attachments/936681962255548437/940201970160009256/gray.png')
  await ctx.send(embed=embed)
  embed = disnake.Embed(title="Зеленая аватарка Discord", color = 0x05fcfa)
  embed.set_image(url = 'https://cdn.discordapp.com/attachments/936681962255548437/940201969929293844/green.png')
  await ctx.send(embed=embed)

@client.command(name='unban')
async def unban(ctx, *, user_id=None):
	if not ctx.author.guild_permissions.ban_members:
		await ctx.message.add_reaction("<:error:925385765188419604>")
		Embed = discord.Embed(description = ':x: **Ошибка! У вас недостаточно прав**', color=0x00008b)
		await ctx.send(embed = Embed)
		return
	if not user_id:
		await ctx.message.add_reaction("<:error:925385765188419604>")
		Embed = discord.Embed(description = ':x: **Ошибка! Вы не указали ID пользователя**\n**Аргументы данной команды**\n**[] обязательный аргумент**\n\n**Gides!unban [ID участника]**', color=0x00008b)
		await ctx.send(embed = Embed)
		return
	try:
		channel = client.get_channel(941283209457569792)
		owner = ctx.guild.owner
		user = await client.fetch_user(user_id=user_id)

		await ctx.guild.unban(user)
		await ctx.message.add_reaction("<:succesfully:925385120280612864>")

		embed = discord.Embed(title=f"✅|{user} был разбанен", color = 0x00008b)
		embed.add_field(name = "Модератор", value = ctx.author)
		embed.add_field(name = "ID разбаненного участника:", value = user.id)
		await ctx.send(embed=embed)

		embed = discord.Embed(title=f"Вы были разбанены на сервере {ctx.guild.name}", color = 0x00008b)
		embed.add_field(name = "Модератор", value = ctx.author)
		await user.send(embed=embed)
		
		embed = discord.Embed(title=f"{ctx.author} разбанил пользователя {user} на сервере {ctx.guild.name}", color = 0x00008b)
		embed.add_field(name = "ID сервера:", value = ctx.guild.id)
		embed.add_field(name = "ID разбаненного участника:", value = user.id)
		embed.add_field(name = "Владелец", value = ctx.guild.owner.mention)
		embed.add_field(name = "ID Владельца", value = ctx.guild.owner_id)
		await channel.send(embed=embed)

		embed = discord.Embed(title=f"{ctx.author} разбанил пользователя {user} на вашем сервере с именем {ctx.guild.name}", color = 0x00008b)
		embed.add_field(name = "ID сервера:", value = ctx.guild.id)
		embed.add_field(name = "ID разбаненного участника:", value = user.id)
		await owner.send(embed=embed)

	except discord.DiscordException:
		embed = discord.Embed(f"{user} не забанен")
		await ctx.send(embed=embed)
	except discord.Forbidden:
		return
	except discord.HTTPException:
		return

client.run(os.environ["DISCORD_TOKEN"]) 
