from flask import Flask
from Server.main import Main as server


if __name__ == "__main__":
	"""
	TODO: May have to add code for initializing the db
	"""
	
	app = Flask(__name__)
	myServer=server(app)
    myServer.run()

