import time
import os
from pypresence import Presence

def update_discord_presence(details="", state=""):
	pass

def connect():
	rpc = None
	try:
		client_id = "945340947951140874"
		rpc = Presence(client_id)
		rpc.connect()
		start_time = time.time()
		
		def update_discord_presence(details=f"{os.path.basename(__file__)}", state="doing stuff"):
			rpc.update(details=details, state=state, large_image="icon_big", start=start_time)
		
	except Exception as e:
		print(e, type(e))
		return e
	