#!/usr/bin/env python3
from time import sleep
from datetime import datetime
from ztAPI import ztAPI
from ztConfig import ztConfig

from rich.live import Live
from rich.console import Console, Group
from rich.layout import Layout
from rich.panel import Panel
from rich.table import Table
from rich.text import Text
from rich.box import SQUARE

class ztHeader:
	"""Display header with general ZeroTier stats"""
	def __init__(self, api:'ztAPI', networkId:'str'):
		self._api = api
		self._networkId = networkId

	def __rich__(self) -> Panel:
		grid = Table.grid(expand=True)
		grid.add_column(justify="left", ratio=1)
		grid.add_column(justify="right")
		grid.add_column(justify="right")
		networkInfo = self._api.networkInfo(self._networkId)
		clock = datetime.fromtimestamp(networkInfo['clock']/1000)
		countLen = len(str(networkInfo['authorizedMemberCount']))
		grid.add_row(
			f"{networkInfo['config']['name']}[{networkInfo['config']['id']}]:",
			Text.assemble(f"[{clock.strftime('%H')}", (":", "blink"), f"{clock.strftime('%M')}", (":", "blink"), f"{clock.strftime('%S')}]", style="magenta"),
			f" {networkInfo['onlineMemberCount']:{countLen}d}/{networkInfo['authorizedMemberCount']}",
		)
		return Panel(grid, box=SQUARE, title="ZeroTier status", style="white on black")

class ztStatus:
	"""Display info about all network members"""
	def __init__(self, console:'Console', api:'ztAPI', networkId:'str'):
		self._console = console
		self._api = api
		self._networkId = networkId
		self._lastState = {}

	def __rich__(self) -> Group:
		networkMembers = self._api.listNetworkMembers(self._networkId)
		if self._lastState:
			pass
		output = []
		changes = False
		for memberId, memberInfo in networkMembers.items():
			text = Text()
			if memberInfo['lastOnline']:
				text.append(f"{memberInfo['version']}\t{memberInfo['name']}({memberInfo['description']}) [{memberId}]: {memberInfo['IP']}    ", style=(None if memberId not in self._lastState or self._lastState[memberId]['lastOnline'] else "white on red"))
				text.append(f"{memberInfo['lastOnline']}", style=("red" if memberId not in self._lastState or self._lastState[memberId]['lastOnline'] else "white on red"))
				if memberId in self._lastState and \
					not self._lastState[memberId]['lastOnline']:
					changes = True
			else:
				text.append(f"{memberInfo['version']}\t{memberInfo['name']}({memberInfo['description']}) [{memberId}]: {memberInfo['IP']}{'' if memberInfo['zIP'] is None else ' -> ' + memberInfo['zIP']}", style=("green" if memberId not in self._lastState or not self._lastState[memberId]['lastOnline'] else "white on green"))
				if memberId in self._lastState and \
					self._lastState[memberId]['lastOnline']:
					changes = True
			output.append(text)
		self._lastState = networkMembers
		if changes:
			self._console.bell()
		return Group(*output)

def ztGUI():
	config = ztConfig()
	if not config.token:
		print('Please fetch an "API Access Token" from https://my.zerotier.com/account and put it in the "' + config.file + '" file!')
		return

	api = ztAPI(config.token)
	if not config.networkId:
		print('Please pick a networkId you would like to monitor from the first column and put it in the "' + config.file + '" file:')
		myNetworks = api.listNetworks()
		for networkId, networkName in myNetworks.items():
			networkInfo = api.networkInfo(networkId)
			print(f"{networkId} ({networkName}): {networkInfo['onlineMemberCount']}/{networkInfo['authorizedMemberCount']}")
		return

	console = Console()

	layout = Layout(name="main")
	layout.split(
		Layout(name="header", size=3),
		Layout(name="content", ratio=1),
	)

	layout['header'].update(ztHeader(api, config.networkId))
	layout['content'].update(ztStatus(console, api, config.networkId))

	#Refresh once a minute
	live = Live(layout, refresh_per_second=(1/60), screen=True)
	live.start(refresh=live._renderable is not None)
	try:
		while True:
			sleep(60)
	except KeyboardInterrupt:
		live.stop()
		raise

if __name__ == "__main__":
	try:
		ztGUI()
	except KeyboardInterrupt:
		pass