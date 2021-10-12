import os
import discord
import requests
import json
import random
from replit import db
from keep_online import keep_online

client = discord.Client()

sad_words = [
    "sad", "depressed", "unhappy", "not happy", "angry", "miserable",
    "depressing"
]

starter_encouragements = [
    "Cheer up!", "Hang in there.", "You are a great person!"
]

if "responding" not in db.keys():
    db["responding"] = True


def get_quote():
    response = requests.get("https://zenquotes.io/api/random")
    json_data = json.loads(response.text)
    quote = "*" + json_data[0]['q'] + "*" + "\n-" + json_data[0]['a']
    return (quote)


def update_encouragements(encouraging_message):
    if "encouragements" in db.keys():
        encouragements = db["encouragements"]
        encouragements.append(encouraging_message)
        db["encouragements"] = encouragements
    else:
        db["encouragements"] = [encouraging_message]


def delete_encouragements(index):
    encouragements = db["encouragements"]
    if len(encouragements) > index:
        del encouragements[index]
    db["encouragements"] = encouragements


@client.event
async def on_ready():
    await client.change_presence(activity=discord.Activity(
        type=discord.ActivityType.watching, name='over servers.'))
    print('We have logged in as {0.user}'.format(client))


@client.event
async def on_message(message):
    if message.author == client.user:
        return

    msg = message.content

    if message.content.startswith('.hello'):
        await message.channel.send('Hello!')

    if message.content.startswith('.inspire'):
        quote = get_quote()
        await message.channel.send(quote)
    if db["responding"]:
        options = starter_encouragements
        if "encouragements" in db.keys():
            options = options + db["encouragements"].value

        if any(word in msg for word in sad_words):
            await message.channel.send(random.choice(starter_encouragements))

    if msg.startswith(".new"):
        encouraging_message = msg.split(".new ", 1)[1]
        update_encouragements(encouraging_message)
        await message.channel.send("New encouraging message added.")

    if msg.startswith(".del"):
        encouragements = []
        if "encouragements" in db.keys():
            index = int(msg.split(".del", 1)[1])
            delete_encouragements(index)
            encouragements = db["encouragements"]
        await message.channel.send(encouragements)

    if msg.startswith(".list"):
        encouragements = []
        if "encouragements" in db.keys():
            encouragements = db["encouragements"].value
        await message.channel.send(encouragements)

    if msg.startswith(".responding on"):
        db["responding"] = True
        await message.channel.send("Responding is on.")
    if msg.startswith(".responding off"):
        db["responding"] = False
        await message.channel.send("Responding is off.")


keep_online()

my_secret = os.environ['TOKEN']
client.run(my_secret)
