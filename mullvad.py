import requests, time, os, sys
from Queue import Queue
from authModule import auth
import threading
import click

queue = Queue()
working = []
print_lock = threading.Lock()

@click.command()
@click.option('--threads', default=1, help='Number of threads.')
@click.option('--accounts', default=5, help='Number of accounts.')
@click.option('--start', default=0)
def main(accounts, threads, start):
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
			working.append(account)

def Worker(q):
	while True:
		account = q.get()
		DoWork(account)
		q.task_done()

if __name__ == '__main__':
	main()