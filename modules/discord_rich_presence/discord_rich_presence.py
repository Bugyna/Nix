import time
import os
import pypresence

class DISCORD_RICH_PRESENCE:
	def __init__(self, parent):
		# try:
			# self.importable = True
		# except Exception as e:
			# print(e)
			# self.notify(e)
			# self.importable = False
			
		self.importable = True
			
		self.parent = parent
		self.rpc = None

		self.commands = {
			"discord_presence" : [self.presence_set, "(dis)connects discord presence | usage discord_presnce [on|off]"],
		}

		self.add_self()

	def add_self(self):
		if (self.importable): self.parent.parser.commands.update(self.commands)

	def presence_set(self, arg=None):
		if (not arg[1:]): self.parent.error(f"{self.commands[arg[0]][1]}"); return
		if (arg[1] == "on"): self.connect()
		elif (arg[1] == "off"): self.disconnect()
		return "break"
	
	# def update_discord_presence(self, details="", state=""):
		# pass

	def disconnect(self, arg=None):
		pass
	
	def connect(self, arg=None):
		try:
			client_id = "945340947951140874"
			self.rpc = pypresence.Presence(client_id)
			self.rpc.connect()
			start_time = time.time()

			def update_discord_presence(details=f"{os.path.basename(__file__)}", state="doing stuff"):
				self.rpc.update(details=details, state=state, large_image="icon_big", start=start_time)

			self.update_discord_presence = update_discord_presence
			self.update_discord_presence()
			
		except Exception as e:
			print(e, type(e))
			self.parent.error(f"{self}: {e}")
			return e
	
