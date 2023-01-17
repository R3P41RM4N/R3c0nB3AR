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
from bear import bear
from config import Configuration

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


def main():
  
    if not os.path.exists("logs"):
        os.makedirs("logs")

#-----------------Opening-------------    
    bear()
    
    #target web address
    raw_site_input = input(colored('Hello!, which site would you like to scan today?[Include http:// or https://]\n >>', "white"))
    site = str(raw_site_input).strip()
    
    #allPorts Scan First?
    raw_allPortsQ = input(colored('Would you like to scan all ports first and then designate target ports?\n(Y/N)', "cyan"))
    allPortsQ = str(raw_allPortsQ).strip()
    
    #if/elif/else for all ports
         
    if allPortsQ.upper() == 'Y':
        cmd_allPorts()
    
    elif allPortsQ.upper() == 'N':
        pass()
    
    else:
        print('that is not an option, please try again')
        exit()   

    #---------------------------------------------------------------------
    raw_port_input = input(colored('and which ports would you like to scan today?[separate each port by a ","]\n >>', "white"))
    port = str(raw_port_input).strip()
    


    # configuration = Configuration(site, port, {"http":"http://127.0.0.1:8080","https": "http://127.0.0.1:8080"})
    configuration = Configuration(site, port)
    proxies = configuration.proxies
    cmds = configuration.cmds
    site = configuration.site
    allPortsQ = configuration.allPorts
    r = requests.get(f"{configuration.http + configuration.site}", proxies=proxies, verify=False)
    headers = r.headers
    
    #Opening for the log path
    logpath = f"logs/{date.isoformat(date.today()).replace('-',' ')}_{site}.log"

    with open(logpath, 'w') as f:
        
        f.write(colored("\nInitiating Recon Scan\n\n\n", "green"))
        print(colored("\nInitiating Recon Scan\n\n\n", "green"))
        #headers Scan functions
        


        #Future looks like complete scan first and designate variables based on open ports
        #Then they wouldn't have to specify ports. Research how to designate results as new variables in Python.
        
#-----------------Response Status Code------------------------         
        f.write(format_text('Response status_code is: ',r.status_code))
        print(format_text('Response status_code is: ',r.status_code))
        
        #f.write(format_text('headers are: ',r.headers))/print(format_text('headers are: ',r.headers)), Only way to get them to print to document
        
#-----------------Header/CSP Begin------------------------        
        f.write(text_header('The Headers returned are: '))
        print(text_header('The Headers returned are: '))
http://host1.metaproblems.com:4500/
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
#--------------------------------Header/CSP End/ Cookie Pull start--------------- 

        f.write(format_text('\n\nCookies: \n',r.cookies)),
        print(format_text('\n\nCookies: \n',r.cookies)),
        f.write(format_text('HTML ',r.text)),
        print(format_text('HTML: ',r.text)),
#-------------------------------- Cookie Pull End/CMD Start---------------       
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
#-------------------------------- Cookie Pull End/CMD Start---------------      

if __name__ == "__main__":
    main()
