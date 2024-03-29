#!/usr/bin/env python3
from ztAPI import ztAPI
from ztConfig import ztConfig

from colorama import init as colorama_init, Fore

def ztconsole():
	config = ztConfig()
	if not config.token:
		print('Please fetch an "API Access Token" from https://my.zerotier.com/account and put it in the "' + config.file + '" file!')
		return
	colorama_init()
	api = ztAPI(config.token)
	myNetworks = api.listNetworks()
	for networkId, networkName in myNetworks.items():
		networkInfo = api.networkInfo(networkId)
		print(f"{networkName}[{networkId}]: {networkInfo['onlineMemberCount']}/{networkInfo['authorizedMemberCount']}")
		networkMembers = api.listNetworkMembers(networkId)
		for memberId, memberInfo in networkMembers.items():
			if not memberInfo['hidden']:
				if memberInfo['lastOnline']:
					print(f"{memberInfo['version']}\t{memberInfo['name']}({memberInfo['description']}) [{memberId}]: {memberInfo['IP']}    {Fore.RED}{memberInfo['lastOnline']}{Fore.RESET}")
				else:
					print(f"{Fore.GREEN}{memberInfo['version']}\t{memberInfo['name']}({memberInfo['description']}) [{memberId}]: {memberInfo['IP']}{'' if memberInfo['zIP'] is None else ' -> ' + memberInfo['zIP']}{Fore.RESET}")

if __name__ == "__main__":
	try:
		ztconsole()
	except KeyboardInterrupt:
		print()