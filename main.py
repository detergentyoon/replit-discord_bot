import discord
import os
import requests
import json
import random
from replit import db

client = discord.Client()

sad_words = ["ㅠ", "ㅜㅜ"]

starter_encouragements = [
	"즙 짜지 마세요",
	"징징대지마세요",
	"애같이 굴지 마세요"
]

if "responding" not in db.keys():
	db["responding"] = True

def get_quote():
	response = requests.get("https://zenquotes.io/api/random")
	json_data = json.loads(response.text)
	quote = json_data[0]['q'] + " -" + json_data[0]['a']
	return(quote)

def update_encouragements(encouraging_message):
	if "encouragements" in db.keys():
		encouragements = db["encouragements"]
		encouragements.append(encouraging_message)
		db["encouragements"] = encouragements
	else:
		db["encouragements"] = [encouraging_message]
		
def delete_encouragement(index):
	encouragements = db["encouragements"]
	if len(encouragements) > index:
		del encouragements[index]
		db["encouragements"] = encouragements

@client.event
async def on_ready():
	print('We have logged in as {0.user}'.format(client))

@client.event
async def on_message(message): 
	if message.author == client.user:
		return
	
	msg = message.content

	if message.content.startswith('$inspire'):
		quote = get_quote()
		await message.channel.send(quote)

	if db["responding"]:
		options = starter_encouragements
		if "encouragements" in db.keys():
			options += db["encouragements"]

		if any(word in msg for word in sad_words):
			await message.channel.send(random.choice(options))

	if msg.startswith("$new"):
		encouraging_message = msg.split("$new ", 1)[1]
		update_encouragements(encouraging_message)
		await message.channel.send("New encouraging message added.")

	if msg.startswith("$del"):
		encouragements = []
		if "encouragements" in db.keys():
			index = int(msg.split("$del", 1)[1])
			delete_encouragement(index)
			encouragements = db["encouragements"] # 업데이트된 메세지 목록 유저에게 보여주기
		await message.channel.send(encouragements) # 빈 목록 []을 만든 이유 : 만약 목록이 비어있을 때는 비어있는 목록을 반환, or DB에 메세지가 있는 경우에는 메세지를 받은 후 반환

	if msg.startswith("$list"):
		encouragements = []
		if "encouragements" in db.keys():
			encouragements = db["encouragements"]
		await message.channel.send(encouragements)

	if msg.startswith("$responding"):
		value = msg.split("$responding ", 1)[1]

		if value.lower() == "true":
			db["responding"] = True
			await message.channel.send("Responding is on.")
		else:
			db["responding"] = False
			await message.channel.send("Responding is off.")

client.run(os.environ['TOKEN'])