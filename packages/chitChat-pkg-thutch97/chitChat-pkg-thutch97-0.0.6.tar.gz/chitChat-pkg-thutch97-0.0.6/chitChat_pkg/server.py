from flask import Flask
from flask_restful import Api, Resource, reqparse
import sqlite3
import bcrypt
# import createDB

''' SQL Functions '''
def newUser(username, password, display_name, friend1, friend2, friend3, friend4, friend5):
	
	conn = sqlite3.connect('users.db') # Setting up the database (and where)
	c = conn.cursor() # This allows us to run commands to database

	password = password.encode('utf-8')
	password = bcrypt.hashpw(password, bcrypt.gensalt())

	with conn:
		c.execute("INSERT INTO users VALUES(?,?,?,?,?,?,?,?)", (username, password, 
																display_name, friend1, 
																friend2, friend3, 
																friend4, friend5))
	
	conn.close()

def findUser(username):
	
	conn = sqlite3.connect('users.db') # Setting up the database (and where)
	c = conn.cursor() # This allows us to run commands to database

	c.execute("SELECT * FROM users WHERE username=?", (username,))
	results = c.fetchall()
	return results

	conn.close()

def findAll():

	conn = sqlite3.connect('users.db') # Setting up the database (and where)
	c = conn.cursor() # This allows us to run commands to database

	c.execute("SELECT * FROM users")
	results = c.fetchall()
	return results

	conn.close()

def delUser(username):

	conn = sqlite3.connect('users.db') # Setting up the database (and where)
	c = conn.cursor() # This allows us to run commands to database

	with conn:
		c.execute("DELETE FROM users WHERE username=?", (username,))

	conn.close()


''' Initialising the server with API '''
app = Flask(__name__) # 0.0.0.0 to hear from any computer
api = Api(app)


''' Conversations holder '''
convos = [['testuser1', 'testuser2', [['testuser1', 'message1'], ['testuser2', 'message2'],['testuser1',"here's another message"]]],
		['testuser1', 'testuser3', [['testuser3', 'message1'], ['testuser1', 'message2'], ['testuser1',"how are you today?"]]],
		['testuser1', 'thutch97', [['testuser1', 'What is my purpose?'], ['thutch97', 'You pass butter'], ['testuser1',"Oh my God"]]],
		['testuser2', 'testuser3', [['testuser2', 'message1'], ['testuser3', 'message2'],['testuser2',"here's another message"]]]]


''' API Resources '''
class Login(Resource):
	''' Login resource '''

	def get(self):
		
		''' Define arguments for get request '''
		login_get_args = reqparse.RequestParser()
		login_get_args.add_argument('username', type=str, help='Username required', required=True)
		login_get_args.add_argument('password', type=str, help='Password required', required=True)
		args = login_get_args.parse_args()

		''' Get user information '''
		givenUsername = args['username']
		givenPassword = args['password'].encode('utf-8')
		userInfo = findUser(givenUsername)
		
		if userInfo != []:
			password = userInfo[0][1]
		
		else: return {'error': 'This user does not exist.'}

		''' Check password '''
		if bcrypt.checkpw(givenPassword, password):
			return {'success': 'Passwords match.'}
		else:
			return {'error': 'Passwords do not match.'}
api.add_resource(Login, "/login")


class Register(Resource):
	''' Register resource '''

	def post(self):
		
		''' Define arguments for post request '''
		register_post_args = reqparse.RequestParser()
		register_post_args.add_argument('username', type=str, help='Username required', required=True)
		register_post_args.add_argument('password', type=str, help='Password required', required=True)
		register_post_args.add_argument('display_name', type=str, help='Display name required', required=True)
		register_post_args.add_argument('friend1', type=str, help='friend1 required')
		register_post_args.add_argument('friend2', type=str, help='friend2 required')
		register_post_args.add_argument('friend3', type=str, help='friend3 required')
		register_post_args.add_argument('friend4', type=str, help='friend4 required')
		register_post_args.add_argument('friend5', type=str, help='friend5 required')

		args = register_post_args.parse_args()

		''' Check if username already taken '''
		username = args['username']
		if findUser(username) != []: return {'message': 'Username already taken'}

		else:

			''' Create new user in the database '''
			password = args['password']
			display_name, friend1 = args['display_name'], args['friend1']
			friend2, friend3 = args['friend2'], args['friend3']
			friend4, friend5 = args['friend4'], args['friend5']
			
			newUser(username, password, display_name, 
					friend1, friend2, friend3, friend4, friend5)

			''' To check new user has been added '''
			if findUser(username) != []: added = True
			else: added = False 

			return {'user_added': added}
api.add_resource(Register, "/register")


class Home(Resource):
	''' Home resource '''

	def get(self):

		''' Define arguments for get request '''
		login_get_args = reqparse.RequestParser()
		login_get_args.add_argument('username', type=str, help='Username required', required=True)
		args = login_get_args.parse_args()

		username = args['username']

		''' Display conversations '''
		myConversations = []

		for conversation in convos:

			if username in conversation:
				myConversations.append(conversation)

		if myConversations == []: 
			return {'None': 'No conversations'}

		else:

			toReturn = {}

			for conversation in myConversations:

				for item in conversation:
					if item != username: 
						friend = item
						break

				friendDisplayName = findUser(friend)[0][2]
				messages = conversation[-1]

				''' Different result if conversation is empty '''
				try:
					lastMessage = messages[-1]
					lastMessageContent = lastMessage[-1]
					toReturn[friend] = [friendDisplayName,lastMessageContent]

				except:
					toReturn[friend] = [friendDisplayName,' ']

			return toReturn
api.add_resource(Home, "/home")


class Chat_name(Resource):
	''' Chat_name resource '''

	def get(self):
		''' Give conversation when given username '''

		''' Define arguments for get request '''
		login_get_args = reqparse.RequestParser()
		login_get_args.add_argument('username', type=str, help='Username required', required=True)
		login_get_args.add_argument('friend', type=str, help='Friend required', required=True)
		args = login_get_args.parse_args()

		username = args['username']
		friend = args['friend']

		''' Get conversation from convos list '''
		myConversations = []

		for conversation in convos:

			if username in conversation:
				myConversations.append(conversation)

		for item in myConversations:
			if friend in item: 
				yesConvo = item # Indicating this is the correct conversation
				break

		''' Return conversation '''
		try:
			messages = yesConvo[-1]
			return {'conversation': messages}

		except:
			return {'None': 'This conversation does not exist.'}
api.add_resource(Chat_name, "/chat_name")


class Friends_info(Resource):

	def get(self):
		''' Give conversation when given username '''

		''' Define arguments for get request '''
		login_get_args = reqparse.RequestParser()
		login_get_args.add_argument('username', type=str, help='Username required', required=True)
		args = login_get_args.parse_args()

		username = args['username']

		''' Get friends info for this username '''
		try:
			friends_info = findUser(username)[0][3:]
			return {'friends_info':friends_info}

		except:
			return {'None': 'There is no user by this username.'}
api.add_resource(Friends_info, "/friends_info")


class Chat_new(Resource):
	''' Chat_new resource '''

	def post(self):

		''' Define arguments for get request '''
		login_get_args = reqparse.RequestParser()
		login_get_args.add_argument('username', type=str, help='Username required', required=True)
		login_get_args.add_argument('friend_name', type=str, help='Friend name required', required=True)
		args = login_get_args.parse_args()

		username = args['username']
		friend_name = args['friend_name']

		''' Find username's conversations '''
		myConversations = []

		for conversation in convos:

			if username in conversation:
				myConversations.append(conversation)

		''' Check if conversation with friend already exists '''
		for convo in myConversations:
			if friend_name in convo:
				return {'Already exists': 'This conversation already exists.'}

		''' Create new conversation if this conversation doesn't already exist '''
		convos.append([username, friend_name,[]])
		return {'New': 'New conversation set up.'}
api.add_resource(Chat_new, "/chat_new")


class Display_name(Resource):

	def get(self):
		''' Get display name if given username '''

		''' Define arguments for get request '''
		login_get_args = reqparse.RequestParser()
		login_get_args.add_argument('username', type=str, help='Username required', required=True)
		args = login_get_args.parse_args()

		username = args['username']

		''' Get display name '''
		try:
			display_name = findUser(username)[0][2]
			return {'display_name':display_name}

		except:
			return {'None': 'There is no user by this username.'}
api.add_resource(Display_name, "/display_name")


class Send(Resource):
	''' Send resource '''
	
	def post(self):

		''' Define arguments for get request '''
		login_get_args = reqparse.RequestParser()
		login_get_args.add_argument('username', type=str, help='Username required', required=True)
		login_get_args.add_argument('friend_name', type=str, help='Friend name required', required=True)
		login_get_args.add_argument('message', type=str, help='Message required', required=True)
		args = login_get_args.parse_args()

		username = args['username']
		friend_name = args['friend_name']
		message = args['message']

		''' Find relevant conversation '''
		index, found = 0, False
		for convo in convos:

			if username in convo and friend_name in convo:
				
				yesConvoIndex, found = index, True
				break
			index += 1

		if found == True: # Ensuring the correct message has been found

			''' Add message to conversation '''
			yesConvo = convos[yesConvoIndex] # Find correct conversation
			messages = yesConvo[-1]
			messages.append([username,message])

			return {'Sent': yesConvo}

		else:
			return {'None': 'Message not sent'}
api.add_resource(Send, "/send")


if __name__ == '__main__':
	app.run(debug=True)