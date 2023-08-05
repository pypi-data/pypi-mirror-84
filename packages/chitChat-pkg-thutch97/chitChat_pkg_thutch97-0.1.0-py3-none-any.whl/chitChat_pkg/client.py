import requests

BASE = 'http://127.0.0.1:5000/' # The endpoint of the API

''' Functions '''
def register():
	''' Give a username and password '''
	username = input('Please provide a username. ')
	if username == 'back': return False # To go back to previous layer

	display_name = input('Please provide a display name. ')
	if display_name == 'back': return False # To go back to previous layer

	while True:

		password1 = input('Please provide a password. ')
		if password1 == 'back': return False # To go back to previous layer

		password2 = input('Please repeat the password. ')
		if password2 == 'back': return False # To go back to previous layer

		if password1 == password2:
			password = password1
			break
		else:
			print('Sorry, the passwords do not match, please try again.')

	''' Adding friends '''
	print('If applicable, please provide usernames of up to five friends who already use chitChat.')
	print("Leave empty if you don't have any friends. ;(")
	response = input('Please leave a space between each username. ')
	if response == 'back': return False # To go back to previous layer

	names = response.split()

	''' Creating arguments for register API call '''
	argKeys = ['username', 'password', 'display_name', 'friend1', 'friend2', 'friend3', 'friend4', 'friend5']
	argValues = [username, password, display_name]
	for name in names: argValues.append(name)
	args = dict(zip(argKeys, argValues))

	''' Making the API call '''
	response = requests.post(BASE + "register", args)
	result = response.json()

	''' If username taken, try again. If not, login '''
	if 'user_added' in result:
		print('')
		return True

	else: print('Sorry, this username is taken, please try a different username.')

def login():
	username = input('Please provide a username. ')
	if username == 'back': return ['back', None] # This will allow the login/register screen to reset

	password = input('Please provide a password. ')
	if password == 'back': return ['back', None] # This will allow the login/register screen to reset

	''' Creating arguments for register API call '''
	argKeys = ['username', 'password']
	argValues = [username, password]
	args = dict(zip(argKeys, argValues))

	''' Making the API call '''
	response = requests.get(BASE + "login", args)
	result = response.json()

	''' Respond appropriately '''
	if result == {'success': 'Passwords match.'}:
		return [True, username]

	elif result == {'error': 'Passwords do not match.'}:
		print('Sorry, your password is incorrect, please try again.')

	elif result == {'error': 'This user does not exist.'}:
		print('Sorry, this user does not exist, please try another username.')

def border(message, where='topAndBottom', border='-'):
	
	length = len(message)

	if where == 'top':
		print(length * border)
		print(message)

	elif where == 'bottom':
		print(message)
		print(length * border)

	else:
		print(length * border)
		print(message)
		print(length * border)
	
def home(username):

	''' Find conversations via API call '''
	response = requests.get(BASE + "home", {'username': username})
	result = response.json()

	''' Check if there are any conversations '''
	if 'None' in result:

		toPrint = ["You don't have any conversations, why don't you start a new one?", '']
		return [None, toPrint]

	else: 

		toPrint = ["Here are your ongoing conversations.", '']

		''' Present conversations nicely '''
		chatPoss = [] # This will be useful for chat_name API call

		for convo in result:
			friend = result[convo][0]
			friendUserName = convo
			chatPoss.append([friend, friendUserName])
			message = result[convo][1][:35]
			space_size = 15-len(friend)
			spaces = " " * space_size

			toPrint.append("{}{}{}".format(friend, spaces, message))

		return [chatPoss, toPrint]

def chat_name(username, friendUserName, friendDisplayName):
	''' API call to get chat messages '''
	response = requests.get(BASE + "chat_name", {'username':username, 'friend':friendUserName})
	result = response.json()

	convo = result['conversation']

	''' Present nicely '''
	border('Here is your conversation with {}'.format(friendDisplayName))
	[print("{}>> {}".format(message[0],message[1])) for message in convo]

def chat_new(friend_name):

	''' Create new conversation using API call '''
	response = requests.post(BASE + "chat_new", {'username':username, 'friend_name': friend_name})

	''' API call to find display name for friend '''
	response = requests.get(BASE + "display_name", {'username': friend_name})
	result = response.json()

	try:
		friend_display_name = result['display_name']
		return friend_display_name

	except:
		return False


''' Pathway '''
border('Welcome to chitChat!')

while True: # Layer 1 - login/register/leave

	loggedIn = False

	print('Would you like to login, register or leave? ')
	print("(Type 'back' to return to previous stage at any time)")
	print('')
	response = input('')
	print('') # Line space

	''' Handling response '''
	if response == 'leave': break

	elif response != 'leave' and response != 'login' and response != 'register':

		print('Please choose from the following options.')
		print('')
		continue

	if response == 'register':

		''' Registering '''
		stillRegistering, registered = True, False
		while stillRegistering == True: # Keep users in loop while trying to register

			register_value = register()
			if register_value != None:
				if register_value == False: 
					stillRegistering = False # If user pressed 'back', they restart process
					print('')

				else: # User successfully registers
					stillRegistering, registered = False, True

			else: print('') # If user entered incorrect values

		if registered == False: continue # Sends users back to login/register


	''' Logging in '''
	stillLoggingIn, loggedIn = True, False
	while stillLoggingIn == True: # Keep users in loop while trying to register

		try:
			success, username = login()

			if [success, username] == ['back', None]: 
				stillLoggingIn = False
				print('')
				 
			else: # User successfully logs in
				stillLoggingIn, loggedIn = False, True

		except: pass # If user entered incorrect values

	if loggedIn == False: continue # Sends users back to login/register


	border('Welcome {}, you are now logged in!'.format(username))

	while True: # Layer 2 - Home screen (view conversations)

		chatPoss, toPrint = home(username)
		
		for line in toPrint:
			print(line)

		if chatPoss != None: # User has ongoing conversations
			
			display_names = [poss[0] for poss in chatPoss] # Display names for friends user has conversations with

		else: # There are no ongoing conversations

			display_names = []

		print('')
		print("Chat with a friend in your conversations list by typing their display name,")
		print("start a new chat by typing 'new'")
		print("check for new messages with 'refresh'")
		print("or log-out of chat server by typing 'log-out'")
		print('')

		response = input('')

		if response == 'log-out': 

			print('')
			break # Takes users back to login/registration

		elif response == 'refresh': 

			print('')
			continue

		elif response not in display_names and response != 'new':

			print('Please choose from the following options.')
			print('')
			continue

		elif response == 'new': # User wants to start a new chat

			stillFindingFriend, foundFriend = True, False
			while stillFindingFriend == True: # Keep users in loop till they have found a friend to chat with

				''' Ask for friend's name '''
				maybeFriend = input('Please give the username for a friend you would like to chat to. ')
				print('')
				if maybeFriend == 'back': stillFindingFriend = False

				else: # Actual response

					''' Check if maybeFriend is actually a friend of their's '''
					result = requests.get(BASE + "friends_info", {'username': username}).json()
					friends = result['friends_info']

					if maybeFriend in friends:
						
						''' Create new conversation and jump into it '''
						friend_name = maybeFriend
						friend_display_name = chat_new(friend_name) # Create variable response so that it can be used in chat_name
						stillFindingFriend, foundFriend = False, True

					else: # User gave an invalid username

						print('You do not have a friend by that username, please try a different username.')
						print('')

			if foundFriend == False: continue # Sends user back to home screen
			if foundFriend == True: response = friend_display_name # Create variable response so that it can be used in chat_name


		''' Jump into an ongoing conversation '''
		chatPoss, toPrint = home(username) # Check if there are any new conversations added
		display_names = [poss[0] for poss in chatPoss] # Display names for friends user has conversations with
		user_names = [poss[1] for poss in chatPoss] # Display names for friends user has conversations with

		index = 0
		for name in display_names:
			if name == response:
				break
			index += 1
		friend_user_name = user_names[index] # Inelegant way of finding friend_user_name

		chat_name(username, friend_user_name, response)
		print('')


		while True: # Layer 3 - Sending messages

			''' Check for commands '''
			message = input('>> ')
			if message == 'back': 

				print('')
				break # Send user back to home screen

			if message == 'refresh': 

				chat_name(username, friend_user_name, response)
				print('')
				continue

			''' Send message '''
			requests.post(BASE + "send", {'username':username, 'friend_name':friend_user_name, 'message':message})
			chat_name(username, friend_user_name, response)
			print('')
			
		





				


				
				


		# ''' Be able to send messages '''
		# while True: # User should be able to send as many messages as they please

		# 	''' Send message '''
		# 	message = input('>> ')
		# 	requests.post(BASE + "send", {'username':username, 'friend_name':friend_name, 'message':message})
		# 	chat_name(username, friend_name, friend_display_name)
































# # while loggedIn == False:
# # 	if response == 'login':

# # 		try:
# # 			success, username = login()
# # 			if [success, username] == ['back', None]: # For if you want to return to login/register
# # 				response = 'else'
# # 				print('')
			
# # 			else: loggedIn = True

# # 		except: pass
		
# # 	elif response == 'register':
# # 		if register() == True: 
# # 			print('Please enter your log-in details.')
			
# # 			while True:

# # 				try:
# # 					success, username = login()
# # 					loggedIn = True
# # 					break

# # 				except: pass
					
# # 	elif response == 'leave':
# # 		print('Press Ctrl+C to leave chitChat.')
# # 		break

# # 	else: response = input('Please choose one of the following: "login", "register", "leave" ')


# ''' Home screen '''
# border('Welcome {}, you are now logged in!'.format(username))
# chatPoss = home(username) # To check input against
# print('')

# ''' User input on home screen '''
# while True:

# 	print("Chat with a friend in your conversations list by typing their display name,")
# 	print("start a new chat by typing 'new'") 
# 	print("or leave chat server by typing 'leave'")
# 	print('')
# 	response = input('')

# 	if response == 'leave': break # This will change when it is in a while loop

# 	elif response == 'new': 

# 		maybeFriend = input('Please give the username for which friend you would like to chat to. ') 
# 		print('')
		
# 		''' Call API to find which friends the user has '''
# 		result = requests.get(BASE + "friends_info", {'username': username}).json()

# 		''' Check if maybeFriend is actually a friend of their's '''
# 		friends = result['friends_info']
# 		if maybeFriend in friends:
			
# 			''' Create new conversation and jump into it '''
# 			friend_name = maybeFriend
# 			friend_display_name = chat_new(friend_name)
# 			chat_name(username, friend_name, friend_display_name)

# 			''' Be able to send messages '''
# 			while True: # User should be able to send as many messages as they please

# 				''' Send message '''
# 				message = input('>>')
# 				requests.post(BASE + "send", {'username':username, 'friend_name':friend_name, 'message':message})
# 				chat_name(username, friend_name, friend_display_name)

# 		else: 
# 			print('You do not have a friend with that username, please choose someone else.')
# 			print('')

# 	else: # User may have wanted to view a chat

# 		''' Work out whether user inputted a friend's name '''
# 		friendHere = False

# 		try:
# 			for poss in chatPoss:
# 				friendDisplayName = poss[0]
# 				friendUserName = poss[1]

# 				if response == friendDisplayName:
# 					friendHere = True
# 					break

# 		except:
# 			pass

# 		if friendHere == True:
# 			''' API call to get chat messages '''
# 			chat_name(username, friendUserName, friendDisplayName)
			
# 			''' Be able to send messages '''
# 			while True: # User should be able to send as many messages as they please

# 				''' Send message '''
# 				message = input('>> ')
# 				requests.post(BASE + "send", {'username':username, 'friend_name':friend_name, 'message':message})
# 				chat_name(username, friend_name, friend_display_name)

# 		else:
# 			print('Please try one of the following options')
# 			print('') # Line break




# # Scenarios where you need to be able to go back:
# # Everywhere where there is user input






















# userPathway

# get login_register - brings up log-in / register page 

# while True: # You log-out when you press leave

# 	user input - login, register or press Ctrl+C to exit the server
# 	if login:
# 		user input - please give username and password
# 		get login - lets you in, passing in username and password

# 	elif register:
# 		user input - provide username, password and repeated password
# 		post register - creates new user in database
# 		user input - please give username and password
# 		get login - lets you in, passing in username and password

# 	while True:

# 		get home - brings up conversations
# 		user input - your options are: chat [name], chat [new], leave
# 		if chat [name]:
			
# 			(chat_name function)
# 			while True:

# 				get chat_name - brings up conversation, pass in name
# 				user input - enter send to send a message, refresh to refresh page

# 				if send:
# 					user input - >> 
# 					post send - adds message to conversation, passing in message

# 				elif refresh:
# 					pass

# 				elif home:
# 					break

# 		elif chat [new]:
# 			get friends_names - brings up list of friends names
# 			user input - please give name
# 			post chat_new - adds conversation to conversations list
# 			run chat_name function again

# 		elif leave:
# 			break
