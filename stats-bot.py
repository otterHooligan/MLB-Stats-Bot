import statsapi
import discord
import random
from discord import Colour, Embed
from discord.ext import commands

#------------------------------------------------------------------------------
# Bot Setup
#------------------------------------------------------------------------------

prefix = '.'
bot = commands.Bot(command_prefix=prefix,description='MLB Stats Bot')
token = ''

#------------------------------------------------------------------------------
# Commands
#------------------------------------------------------------------------------

@bot.command()
async def stats(ctx,*,args):
	players = statsapi.lookup_player(args)
	if(len(players)) == 0:
		await ctx.send("I couldn't find anyone with that name.")
	elif(len(players)) > 1:
		allPlayers = "Found %s players\n" % (len(players))
		for x in players:
			allPlayers = allPlayers + (x['fullName']) + "\n"
		await ctx.send(allPlayers)
	else:
		player = players[0]
		title = "%s | %s - %s" %(player['primaryNumber'],player['fullName'],player['primaryPosition']['abbreviation'])
		playerStats = statsapi.player_stat_data(player['id'], group="[hitting]", type="season")
		team = playerStats['current_team']
		stats = playerStats['stats']
		if(len(stats)) == 0:
			await ctx.send("I don't have any data for that player.")
		else:
			print(stats)
			stats = stats[0]['stats']
			embed = createEmbed(title,team)
			embed.add_field(name="AVG/OBP/SLG/OPS",value=("%s/%s/%s/%s" % (stats['avg'],stats['obp'],stats['slg'],stats['ops'])),inline=False)
			embed.add_field(name="Games Played",value=stats['gamesPlayed'],inline=True)
			embed.add_field(name="Runs",value=stats['runs'],inline=True)
			embed.add_field(name="RBIs",value=stats['rbi'],inline=True)
			embed.add_field(name="BABIP",value=stats['babip'],inline=True)
			embed.add_field(name="ABs",value=stats['atBats'],inline=True)
			embed.add_field(name="PAs",value=stats['plateAppearances'],inline=True)
			embed.add_field(name="Hits",value=stats['hits'],inline=True)
			embed.add_field(name="BB",value=stats['baseOnBalls'],inline=True)
			embed.add_field(name="HRs",value=stats['homeRuns'],inline=True)
			embed.add_field(name="Triples",value=stats['triples'],inline=True)
			embed.add_field(name="Doubles",value=stats['doubles'],inline=True)
			embed.add_field(name="IBB",value=stats['intentionalWalks'],inline=True)
			embed.add_field(name="HBP",value=stats['hitByPitch'],inline=True)
			embed.add_field(name="Total Bases",value=stats['totalBases'],inline=True)
			embed.add_field(name="Strikeouts",value=stats['strikeOuts'],inline=True)
			embed.add_field(name="LOB",value=stats['leftOnBase'],inline=True)
			embed.add_field(name="Stolen Bases",value=stats['stolenBases'],inline=True)
			embed.add_field(name="SB %",value=stats['stolenBasePercentage'],inline=True)
			await ctx.send(embed=embed)

@bot.command()
async def pstats(ctx,*,args):
	players = statsapi.lookup_player(args)
	if(len(players)) == 0:
		await ctx.send("I couldn't find anyone with that name.")
	elif(len(players)) > 1:
		allPlayers = "Found %s players\n" % (len(players))
		for x in players:
			allPlayers = allPlayers + (x['fullName']) + "\n"
		await ctx.send(allPlayers)
	else:
		player = players[0]
		title = "%s | %s - %s" %(player['primaryNumber'],player['fullName'],player['primaryPosition']['abbreviation'])
		playerStats = statsapi.player_stat_data(player['id'], group="[pitching]", type="season")
		team = playerStats['current_team']
		stats = playerStats['stats']
		if(len(stats)) == 0:
			await ctx.send("I don't have any data for that player.")
		else:
			stats = stats[0]['stats']
			record = "%s - %s (%s)" % (stats['wins'],stats['losses'],stats['saves'])
			embed = createEmbed(title,team)
			embed.add_field(name="Record",value=record,inline=True)
			embed.add_field(name="ERA",value=stats['era'],inline=True)
			embed.add_field(name="WHIP",value=stats['whip'],inline=True)
			embed.add_field(name="Opp. Batting",value=("%s/%s/%s/%s" % (stats['avg'],stats['obp'],stats['slg'],stats['ops'])),inline=True)
			embed.add_field(name="Earned Runs",value=stats['earnedRuns'],inline=True)
			embed.add_field(name="Innings Pitched",value=stats['inningsPitched'],inline=True)
			embed.add_field(name="Hits",value=stats['hits'],inline=True)
			embed.add_field(name="Walks",value=stats['baseOnBalls'],inline=True)
			embed.add_field(name="Homeruns",value=stats['homeRuns'],inline=True)
			embed.add_field(name="Strikeouts",value=stats['strikeOuts'],inline=True)
			embed.add_field(name="Strike %",value=stats['strikePercentage'],inline=True)
			embed.add_field(name="Pitches/Inning",value=stats['pitchesPerInning'],inline=True)
			embed.add_field(name="K/BB Ratio",value=stats['strikeoutWalkRatio'],inline=True)
			embed.add_field(name="K/9",value=stats['strikeoutsPer9Inn'],inline=True)
			embed.add_field(name="BB/9",value=stats['walksPer9Inn'],inline=True)
			embed.add_field(name="Hits/9",value=stats['hitsPer9Inn'],inline=True)
			embed.add_field(name="HR/9",value=stats['homeRunsPer9'],inline=True)
			await ctx.send(embed=embed)

@bot.command()
async def otter(ctx):
	otters = open('otters.txt').read().splitlines()
	await ctx.send(random.choice(otters))

@bot.command()
async def quit(ctx):
	if ctx.message.author.id == 330153321262219284: #otter
		await ctx.send("Bye")
		exit()
	else:
		await ctx.send("no u")

#------------------------------------------------------------------------------
# Embeds
#------------------------------------------------------------------------------

def createEmbed(title,team):
	thumbnail = ''
	color = discord.Color(value=int('FFFFFF', 16))
	if(team == 'Arizona Diamondbacks'):
		thumbnail = 'https://i.imgur.com/sQQrkdQ.png'
		color = discord.Color(value=int('A71930', 16))
	elif(team == 'Atlanta Braves'):
		thumbnail = 'https://i.imgur.com/iu3ZrUk.png'
		color = discord.Color(value=int('CE1141', 16))
	elif(team == 'Baltimore Orioles'):
		thumbnail = 'https://i.imgur.com/gOhGpJu.png'
		color = discord.Color(value=int('DF4601', 16))
	elif(team == 'Boston Red Sox'):
		thumbnail = 'https://i.imgur.com/q0e3Ctu.png'
		color = discord.Color(value=int('BD3039', 16))
	elif(team == 'Chicago Cubs'):
		thumbnail = 'https://i.imgur.com/WgIlRAV.png'
		color = discord.Color(value=int('0E3386', 16))
	elif(team == 'Chicago White Sox'):
		thumbnail = 'https://i.imgur.com/NYV2mkz.png'
		color = discord.Color(value=int('27251F', 16))
	elif(team == 'Cincinnati Reds'):
		thumbnail = 'https://i.imgur.com/KyAX7aj.png'
		color = discord.Color(value=int('C6011F', 16))
	elif(team == 'Cleveland Indians'):
		thumbnail = 'https://i.imgur.com/VEj5q3O.png'
		color = discord.Color(value=int('0C2340', 16))
	elif(team == 'Colorado Rockies'):
		thumbnail = 'https://i.imgur.com/HV8jHMA.png'
		color = discord.Color(value=int('33006F', 16))
	elif(team == 'Detroit Tigers'):
		thumbnail = 'https://i.imgur.com/ufZlziV.png'
		color = discord.Color(value=int('0C2340', 16))
	elif(team == 'Houston Astros'):
		thumbnail = 'https://i.imgur.com/b6pMxo6.png'
		color = discord.Color(value=int('002D62', 16))
	elif(team == 'Kansas City Royals'):
		thumbnail = 'https://i.imgur.com/eneNflB.png'
		color = discord.Color(value=int('004687', 16))
	elif(team == 'Los Angeles Angels'):
		thumbnail = 'https://i.imgur.com/5obK9vx.png'
		color = discord.Color(value=int('BA0021', 16))
	elif(team == 'Los Angeles Dodgers'):
		thumbnail = 'https://i.imgur.com/ngNfzws.png'
		color = discord.Color(value=int('005A9C', 16))
	elif(team == 'Miami Marlins'):
		thumbnail = 'https://i.imgur.com/R9dbdsg.png'
		color = discord.Color(value=int('00A3E0', 16))
	elif(team == 'Milwaukee Brewers'):
		thumbnail = 'https://i.imgur.com/vjurP4O.png'
		color = discord.Color(value=int('12284B', 16))
	elif(team == 'Minnesota Twins'):
		thumbnail = 'https://i.imgur.com/Cc4e416.png'
		color = discord.Color(value=int('D31145', 16))
	elif(team == 'New York Mets'):
		thumbnail = 'https://i.imgur.com/m2LQ7OH.png'
		color = discord.Color(value=int('FF5910', 16))
	elif(team == 'New York Yankees'):
		thumbnail = 'https://i.imgur.com/Bh0Mi26.png'
		color = discord.Color(value=int('0C2340', 16))
	elif(team == 'Oakland Athletics'):
		thumbnail = 'https://i.imgur.com/VIDfEdz.png'
		color = discord.Color(value=int('003831', 16))
	elif(team == 'Philadelphia Phillies'):
		thumbnail = 'https://i.imgur.com/GYnxzcB.png'
		color = discord.Color(value=int('E81828', 16))
	elif(team == 'Pittsburgh Pirates'):
		thumbnail = 'https://i.imgur.com/aXTLL3j.png'
		color = discord.Color(value=int('FDB827', 16))
	elif(team == 'San Diego Padres'):
		thumbnail = 'https://i.imgur.com/yyRWQbc.png'
		color = discord.Color(value=int('2F241D', 16))
	elif(team == 'Seattle Mariners'):
		thumbnail = 'https://i.imgur.com/dqIrcTV.png'
		color = discord.Color(value=int('005C5C', 16))
	elif(team == 'San Francisco Giants'):
		thumbnail = 'https://i.imgur.com/3Y5fkBe.png'
		color = discord.Color(value=int('FD5A1E', 16))
	elif(team == 'St. Louis Cardinals'):
		thumbnail = 'https://i.imgur.com/KueM0Nb.png'
		color = discord.Color(value=int('C41E3A', 16))
	elif(team == 'Tampa Bay Rays'):
		thumbnail = 'https://i.imgur.com/CjHp9ae.png'
		color = discord.Color(value=int('8FBCE6', 16))
	elif(team == 'Texas Rangers'):
		thumbnail = 'https://i.imgur.com/ympnCdK.png'
		color = discord.Color(value=int('003278', 16))
	elif(team == 'Toronto Blue Jays'):
		thumbnail = 'https://i.imgur.com/xlqFzBL.png'
		color = discord.Color(value=int('134A8E', 16))
	elif(team == 'Washington Nationals'):
		thumbnail = 'https://i.imgur.com/bdxHcqy.png'
		color = discord.Color(value=int('AB0003', 16))
	else:
		print('fuck')
	embed = discord.Embed(title=title, color=color)
	embed.set_thumbnail(url=thumbnail)
	return embed

bot.run(token)