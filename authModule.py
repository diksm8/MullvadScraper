#!/usr/bin/python
# -*- coding: utf-8 -*-
import requests
timeout = 30 #Set timeout
homepage = 'https://mullvad.net/'

def oldAuth(account):
	session = requests.Session()
	session.headers.update({
		'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.106 Safari/537.36 OPR/38.0.2220.41',
		'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
		'Accept-Language': 'en-US,en;q=0.8',
		'Accept-Encoding': 'gzip, deflate, br',
		'Cache-Control': 'max-age=0',
	})
	req = session.get(homepage, timeout=timeout)
	csrfCookie = requests.utils.dict_from_cookiejar(session.cookies)['csrftoken']
	loginData = {
		'csrfmiddlewaretoken': csrfCookie,
		'next': '%252F',
		'account_number': account,
	}
	req = session.post('https://mullvad.net/account/auth/', data=loginData, headers = {'Referer': homepage}, timeout=timeout)
	if req:
		return True
	else:
		return False

def auth(account):
	from bs4 import BeautifulSoup
	session = requests.Session()
	session.headers.update({
		'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.106 Safari/537.36 OPR/38.0.2220.41',
		'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
		'Accept-Language': 'en-US,en;q=0.8',
		'Accept-Encoding': 'gzip, deflate, br',
		'Cache-Control': 'max-age=0',
	})
	req = session.get(homepage, timeout=timeout)

	csrfCookie = requests.utils.dict_from_cookiejar(session.cookies)['csrftoken']
	loginData = {
		'csrfmiddlewaretoken': csrfCookie,
		'next': '%252F',
		'account_number': account,
	}
	req = session.post('https://mullvad.net/account/auth/', data=loginData, headers = {'Referer': homepage}, timeout=timeout)
	if req:
		soup = BeautifulSoup(req.text, 'lxml')
		left = soup.h4.text
		if '-' in left:
			return False
		else:
			return left
	return False
if __name__ == '__main__':
	exit('Run Mullvad.py instead.')