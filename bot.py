import discord
import sqlite3
import requests

interest_categories = ["video games", "programming", "reading", "movies", "sports", "social media", "shopping", "art", "relaxing", "talking"]


#client_id = 592761539061350436
#token = token

token = "Enter your token

client = discord.Client()

#connect to the database
conn = sqlite3.connect('discord_users.db')
c = conn.cursor()

#create sqlite3 table for users
def create_table():
	c.execute("CREATE TABLE IF NOT EXISTS userTable(username TEXT, bio TEXT, interests TEXT, favorites TEXT, user_id INTEGER PRIMARY KEY AUTOINCREMENT)")

#add a user
def new_user(username, bio, interests, favorites):
	c.execute("INSERT INTO userTable (username, bio, interests, favorites) VALUES (?, ?, ?, ?)",(str(username), str(bio), str(interests), str(favorites)))
	conn.commit()

#check for a user
def check_for_user(username):
	c.execute('SELECT * FROM userTable')
	data = c.fetchall()
	for row in data:
		if str(row[0]) == str(username):
			exists = True
		else:
			exists = False
	return exists

#create a bio
def new_bio(bio, username):
	c.execute('''UPDATE userTable SET bio = ? WHERE username = ?''', (str(bio), str(username)))
	conn.commit()

#lookup a user
def get_user_profile(username):
	c.execute("SELECT * FROM userTable")
	data = c.fetchall()
	for row in data:
		if str(row[0]) == str(username):
			user_bio = str(row[1])
			status = True
		else:
			user_bio = None
			status = False
	return status, user_bio

#set the interest of a user
def user_interest(interest, username):
	c.execute("UPDATE userTable SET interests = ? WHERE username = ?", ((str(interest)), str(username)))
	conn.commit()

#find users with the same interests
def find_friends(interest, username):
	c.execute("SELECT * FROM userTable")
	data = c.fetchall()
	possible_friends = []
	for row in data:
		if row[2] == str(interest):
			possible_friends.append(row[0])
		else:
			pass
	return possible_friends

#lookup the interests of a user
def get_user_interest(username):
	c.execute("SELECT * FROM userTable")
	data = c.fetchall()
	for row in data:
		if str(row[0]) == str(username):
			interest = str(row[2])
			print(interest)
		else:
			interest = None
	return interest


#run the create_table function
create_table()

#establish connection
@client.event
async def on_ready():
    print(f"logged in as {client.user}")

#commands!
@client.event
async def on_message(message):

	print(f"{message.channel}: {message.author}: {message.author.name}: {message.content}")
	if message.content.lower() == "!help":
		await message.channel.send(f"Welcome {message.author}")
		await message.channel.send("This is your user profile. Other users will be able to see this profile. This profile will be the same across multiple servers")
		await message.channel.send("```profile commands: \n !interests - to write about things you like \n !bio set [your bio] - set a bio! Tell people about yourself \n !bio lookup [user] - find a users bio \n !find friends - find people with the same interest as you.```")

	elif message.content.lower() == ("!profile_help"):
		await message.channel.send("```profile commands: \n !interest - to write about things you like \n !bio set [your bio] - set a bio! Tell people about yourself \n !bio lookup [user] - find a users bio \n !find friends - find people with the same interest as you.```")				

	elif message.content.lower() == "!register":
		msg = message.content.lower()
		msg_author = message.author
		status = check_for_user(msg_author)
		if status == False:
			new_user(username=msg_author, bio='None', interests='None', favorites='None')
			await message.channel.send(f"Created new user for {msg_author}")
		else:
			await message.channel.send("User already exists. Use !bio to change your bio.")

	elif "!bio set " in message.content.lower():
		msg = message.content
		msg = msg.replace("!bio set ", "")
		status = check_for_user(message.author)
		if status == True:
			new_bio(msg, message.author)
			await message.channel.send(f"Bio set to: {msg}")
		else:
			await message.channel.send("You havent registered yet. Type !register to do so.")

	elif "!bio lookup" in message.content.lower():
		msg = message.content
		msg = msg.replace("!bio lookup ", "")
		if "@" in msg:
			msg = msg.replace("@", "")
		else:
			pass
		status, bio = get_user_profile(msg)
		if status == True:
			await message.channel.send(bio)
		else:
			await message.channel.send("User not found.")

	elif message.content.lower() == "!interests":
		for interest in interest_categories:
			await message.channel.send(interest)
		await message.channel.send("Type ! followed by an interest of yours to be added to the list!")

	elif "!interest" in message.content.lower():

		user = message.author
		interest = message.content.lower()
		interest = interest.replace("!interest ", "")
		user_exists = check_for_user(user)
		if user_exists == True:
			user_interest(interest, user)
			await message.channel.send(f"Set interest to {interest}")
		else:
			pass

	elif message.content.lower() == "!find friends":
		user = message.author
		interest = get_user_interest(user)
		print(interest)
		possible_friends = find_friends(interest, user)
		await message.channel.send(possible_friends)


	# elif message.content.lower() == "!find friends":
	# 	user = message.author
	# 	status = check_for_user(user)
	# 	if status == True:
	# 		interest = get_user_interest(user)
	# 		if interest != False:
	# 			possible_friends = find_friends(interest, user)
	# 			if len(possible_friends) > 0:
	# 				await message.channe.send(possible_friends)
	# 			else:
	# 				await message.channel.send("There are no other people with the same interest as you.")
	# 		else:
	# 			await message.channel.send("You have not set your interest yet")
	# 	else:
	# 		await message.channel.send("You haven't created a profile yet. Type !register to do so.")
	elif message.content.lower() == "!joke":
		r = requests.get('https://icanhazdadjoke.com', headers={"Accept":"application/json"})
		joke = r.json()['joke']
		await message.channel.send(joke)







client.run(token)
