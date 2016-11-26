#!/usr/bin/python
# -*- coding: utf-8 -*-
from authModule import auth
import threading
import click

@click.command()
@click.argument('input', type=click.File('r'))
def main(input):
	"""Really quick script for checking accounts in a file."""
	for line in input:
		newLine = line.replace("\n", "")
		authresponse = auth(newLine)
		if authresponse:
			click.secho('Account %s has %s days left.' % (newLine, authresponse.split()[5]), fg='green')
		else:
			click.secho('Account %s is dead.' % newLine, fg='red')

if __name__ == '__main__':
	main()