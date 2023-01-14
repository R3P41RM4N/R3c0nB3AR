#!/usr/bin/python

import os
import re
import string
import subprocess
import sys
import requests
from datetime import date
from termcolor import colored, cprint
from art import *
from colorama import Fore, Back, Style
art1=text2art("R3c0nB3AR v1.1", font="standard")
art2=(colored('''MMMMMMMMMMMWMMWNKXWMMMMMMMMMMMMMMMMMMMMM
MMMMMMMMWXOxxxl:co0MMMMMMMMMMMMMMMMMMMMM
MMMMMMWKxlccc:..'.,xKNMMMMMMMMMMMMMMMMMM
MMN0OOxl;:cllc,.  .';lONMMMMMMMMMMMMMMMM
MMO;'ccclllllllc;;ccc:cxXMMMMMMMMMMMMMMM
MMWOc;:;:lllllllllllllllxXMMMMMMMMMMMMMM
MMMWOlc;;;clllllllllllllldOXWMMMMMMMMMMM
MMMMMWNX0c.':clllllllllllccokKWMMMMMMMMM
MMMMMMMMK:..';cc;:llllllllllclxXMMMMMMMM
MMMMMMMM0c.'::c;,:lllllllllllcckWMMMMMMM
MMMMMMMWk'.'cll:';lllllllllllc:xWMMMMMMM
MMMMMMMWx..;lllc:;;:cclllllllcckWMMMMMMM
MMMMMMWO, .clllllc:;;;;cllllllckWMMMMMMM
MMMMMMNd. ,lllcc::c::;,;clllll:dNMMMMMMM
MMMMMMXl. 'ccc::cllllllcc:;;;:;:0MMMMMMM
MMMMW0c.  .:c::lllc;,''...    ..dNMMMMMM
MMW0l.     ,c::c;'"",,,,,,,,;;,.;0MMMMMM
MWOc:,.    ,lc;,""":ccclllllllc;'lXMMMMM
MNklll:.  .;llcccclllccclllllllc;,xWMMMM
MMNkocc;ldccllllllllllccclllllll;.cXMMMM
MMMWX0xkKKocllllllllcc:ccllllllc'.;0MMMM
MMMMMMMMMXdclllllll:;;::ccllllc;..;0MMMM
MMMMMMMMMWOlclllllc::cllclllllc,..lXMMMM
MMMMMMMMMNd,:lllllc::clllllllll:',OWMMMM
MMMMMMMMMNo.,clllll:,:cllllllllc:oXMMMMM
MMMMMMMMMMO,.,:lllc;;:clllllllllcdXMMMMM
MMMMMMMMMWx'...,::::::cllllllllllcxNMMMM
MMMMMMMMMNx;......;llc:llllllllllcoKMMMM
MMMMMMMMMW0o:,....'cdlcclllllllllcl0MMMM
MMMMMMMMMMWKdc:,...';cl:cllllllllcl0MMMM
MMMMMMMMMMMW0olc;....:dc:clllllllcxNMMMM
MMMMMMMMMMMW0ollc;.,ckXx::clllllcc0MMMMM
MMMMMMWXOkxxollllc;cxKMNd',clllc:xNMMMMM
MMMMMMNd;,;::cccc::dO00kx:':lll:;xMMMMMM
MMMMMMMN0kxkO0KXK0Kxc;,,,,'',;,.'kMMMMMM
MMMMMMMMMMMMMMMMMMWOoc,......'',dNMMMMMM''',"green", attrs=["bold"]))
art3=(colored("created by r3p41rm4n and bwalvarado", "green", attrs=["bold"]))

print(art1)
print(art2)
print(art3+"\n\n\n")

raw_site_input = input(colored('Hello!, which site would you like to scan today?[Do not include http:// or https://]\n >>', "white"))
site = str(raw_site_input).strip()

raw_port_input = input(colored('and which ports would you like to scan today?[separate each port by a ","]\n >>', "white"))
port = str(raw_port_input).strip()

#establish burp connection
proxies = {"http":"http://127.0.0.1:8080","https": "http://127.0.0.1:8080"}
#define r = get requests
r = requests.get(f"https://{site}", proxies=proxies, verify=False)

def format_text(title,item): #this is an autoformating feature for HTTP resposne data
    cr = '\r\n'
    section_break = cr + "*"*40 + cr
    item = str(item)
    text = Style.BRIGHT + Fore.GREEN + title + Fore.RESET + section_break + item + section_break
    return text;

def text_header(respd):
    cr = '\r\n'
    section_break = cr + "*"*40
    respd = str(respd)
    text = Style.BRIGHT + Fore.GREEN + cr+ respd + Fore.RESET
    return text;
#Opening for the log path
logpath = f"logs/{date.isoformat(date.today()).replace('-',' ')}_{site}.log"

with open(logpath, 'w') as f:
    f.write(colored("\nInitiating Recon Scan\n\n\n", "green"))
    print(colored("\nInitiating Recon Scan\n\n\n", "green"))
    #headers Scan functions
    headers = r.headers
    #cookies scan functions
    #response = requests.get(f"https://{site}")
    #cookies = response.cookies
    #s = requests.Session()
    #r = s.get(f"https://{site}")
    #sCookies = r.cookies
#scans to be performed:
cmds =[
    #f"nmap -p 80,443,3389 --script http-bigip-cookie {site}",
    #f"nmap -p 80,443,3389 --script http-headers {site}",
    #f"nmap -p 80,443,3389 --script http-security-headers {site}",
    #f"nmap -p 139,145 --script=smb-vuln* {site}",
    # f"nmap -vv -p 139,145 --script=smb-server-stats.nse {site}",
    # f"nmap -vv -p 139,145 --script=smb-brute.nse {site}",
    #f"nmap -vv -p 139,145 --script=smb-double-pulsar-backdoor.nse {site}",
    f"nmap -Pn -T4 --script ssl-enum-ciphers --reason {site}",
    f"nmap -Pn -sC -T4 --reason {site}",
    f"nmap -p {port} --script http-auth, {site}",
    f"nmap -p {port} --script http-auth-finder, {site}",
    f"nmap -p {port} --script http-ntlm-info {site}",
    f"nmap -p {port} --script http-aspnet-debug {site}",
    f"nmap -p {port} --script http-stored-xss {site}",
    f"nmap -p {port} --script http-methods {site}",
    f"nmap -vv -sT -A -sV --reason --script=http-enum {site}",
    f"nmap -vv -p 139,145 --script=smb-enum* {site}",
    f"nmap -vv -p 139,145 --script=smb-os-discovery.nse {site}",
    f"nmap -vv -p {port} --script=http-sitemap-generator.nse {site}",
    f"nikto -p {port} -h {site}",
    f"hping3 -S {site} -c 15 -p {port}", #note to research this function further
    f"curl -k https://{site}/images",
    f"curl -k https://{site}/Images",
    f"curl -svk https://{site}/asdf",
    f"dirb https://{site}/ /usr/share/wordlists/SecLists/Discovery/Web_Content/Top500-RobotsDisallowed.txt -S -l",
    f"ffuf -w /usr/share/wordlists/SecLists/Discovery/DNS/deepmagic.com_top50kprefixes.txt -u https://{site}/FUZZ -c -v -fc 404,302,301",
    f"feroxbuster -u https://{site} --filter-status 400,404,302,301 --extract-links --auto-bail",
    f"nmap -vv -sU -p-  {site}",
    f"nmap -vv -sT -p-  {site}"
]
#Future looks like complete scan first and designate variables based on open ports
#Then they wouldn't have to specify ports. Research how to designate results as new variables in Python.
f.write(format_text('Response status_code is: ',r.status_code))
print(format_text('Response status_code is: ',r.status_code))
#f.write(format_text('headers are: ',r.headers)), #expiriment with a for loop for formatting
#print(format_text('headers are: ',r.headers)), #expiriment with a for loop for formatting
f.write(text_header('The Headers returned are: '))
print(text_header('The Headers returned are: '))

for header in headers:
    if (header.upper() == 'CONTENT-SECURITY-POLICY'):
        csp = headers[header].split(";")
        f.write(format_text('', header))
        print(format_text('', header))
        for c in csp:
            f.write(f"\t{c}")
            print(f"\t{c}")
        else:
            (header.upper() != 'CONTENT-SECURITY-POLICY')
            head = headers[header].split(":")
            f.write(format_text('', header))
            print(format_text('', header))
            for h in head:
                f.write(f"\t{h}")
                print(f"\t{h}")
    f.write(format_text('\n\nCookies: \n',r.cookies)), #build in a session cookie request
    print(format_text('\n\nCookies: \n',r.cookies)),
    f.write(format_text('HTML ',r.text)),
    print(format_text('HTML: ',r.text)),
    #else:
    #   f.write(f"{headers} : {headers[header]}")
    #  print(f"{headers} : {headers[header]}")
    #  for sCookie in sCookies:
    #   print('sCookie name : '+sCookie.name)
    #   print('sCookie value : '+sCookie.value)
    #  for cookie in resp.cookies:
    #  print('cookie name : ',[cookie.name](http://cookie.name/))
    # print('cookie value : ',cookie.value)
    for cmd in cmds:
        f.write(f"\n\n Running: {cmd}")
        map = subprocess.Popen(cmd.split(), stdout=subprocess.PIPE)
        output, err = map.communicate()
        output = output.decode('ascii')
        f.write(output)
        print(output)
        print(f"\n\n(Complete:,{cmd}\n,{output}\n")
        print(f"--------------------------------------")
        f.write(f"\n\n(Complete:,{cmd}\n,{output}\n")
        f.write(f"--------------------------------------")
    f.write(colored('**Scan Complete**','green'))
