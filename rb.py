#!/usr/bin/python
#Reconbear is a web application reconaissance tool. The purpose is to automate the opening tasks of a Web Application Penetration Test.
#The tools integrated into this application should provide a unique perspective on what is being scanned. The goal is to minimize duplicate
#efforts. #The focus should be: Port Enumeration, backend server and front end applications identified if possible. Review of authentication, ntlm, potential
#debugging opportunities, reviewing methods, reviewing potential leads on XSS, fuzzing common extensions both infront of the URL and behind (FUzz.URL/URL.FUZZ)
#all this gets outputed into an easy to read/review report. which helps with pulling out artifacts.
#The ultimate goal is to make this app modular (which it sort of is) to ultimately improve on the initial design.
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

def format_text(title,item): #this is an autoformating feature for HTTP response data
    cr = '\r\n'
    section_break = cr + "*"*40 + cr
    item = str(item)
    text = Style.BRIGHT + Fore.GREEN + title + Fore.RESET + section_break + item + section_break
    return text;allPorts =[f"nmap -vv -sU -p-  {site}", f"nmap -vv -sT -p- {site}"]


def text_header(respd): #this autoformats the headers
    cr = '\r\n'
    section_break = cr + "*"*40
    respd = str(respd)
    text = Style.BRIGHT + Fore.GREEN + cr+ respd + Fore.RESET
    return text;

def targetPorts(): #target ports is for deeper scans if you know which ports are of interest to you.
    raw_port_input = input(colored('which ports would you like to focus your scans on today?[separate each port by a ","]\n >>', "cyan"))
    return str(raw_port_input).strip()


def main():
  
    if not os.path.exists("logs"):
        os.makedirs("logs")
 #if the logs path does not exist, the app will make one.


    #-----------------Opening-------------    
    bear()

    raw_site_input = input(colored('Hello!, which site would you like to scan today?[Include http:// or https://]\n >>', "cyan"))
    site = str(raw_site_input).strip()
    site = site.replace("http://", "").replace("https://", "")
    
    raw_allPortsQ = input(colored('Would you like to scan all ports first and then designate target ports?\n(Y/N)', "cyan"))
#As it currently works, RB will scann all ports with this feature and then once it is complete, prompt the user which ports would they like to focus on
#Potential Upgrade Idea: build out variables which then flow into the main application without user intervention.

    allPortsQ = str(raw_allPortsQ).strip()
    
    allPorts =[f"nmap -vv -sT -Pn -p- -T4{site}",f"nmap -vv -sU -p- -Pn -T4 {site}"]
    
    if allPortsQ == 'Y':
        print("")
        for cmd in allPorts:
            print(f"\n\n Running: {cmd}")
            map = subprocess.Popen(cmd.split(), stdout=subprocess.PIPE)
            output, err = map.communicate()
            allPort_Results = output.decode('ascii')
    #       f.write(output)
            print(output)   
        print(f"\n\n(Complete:,{cmd}\n,{output}\n")
        print(f"--------------------------------------")
    #        f.write(f"\n\n(Complete:,{cmd}\n,{output}\n")
    #        f.write(f"--------------------------------------")
        port = targetPorts()

    else: 
        allPortsQ != 'Y'
        if allPortsQ == 'N':
            print("*****Moving on to the next step*****")
            port = targetPorts()
        else:
            print('invalid input,print a Y or N for yes or no')
            port = fullscan()              
    
    # configuration = Configuration(site, port, {"http":"http://127.0.0.1:8080","https": "http://127.0.0.1:8080"})
    configuration = Configuration(site, port)
    proxies = configuration.proxies
    cmds = configuration.cmds
    port = configuration.ports
    site = configuration.site 
    r = requests.get(f"{configuration.http + configuration.site}", proxies=proxies, verify=False)
    headers = r.headers
    

    #---------------Opening for the log path---------------
    logpath = f"logs/{date.isoformat(date.today()).replace('-',' ')}_{site}.log"

    with open(logpath, 'w') as f:

        f.write(colored("\nInitiating Recon Scan\n\n\n", "green"))
        print(colored("\nInitiating Recon Scan\n\n\n", "green"))

            #The intent with this section of the script is to pull as much information as possible from the header data before ever
            #manipulating the application. 
            
            #-----------------Response Status Code------------------------         
        f.write(format_text('Response status_code is: ',r.status_code))
        print(format_text('Response status_code is: ',r.status_code))
            
            #-----------------Header/CSP Begin------------------------        
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
            #-----------Header/CSP End/ Cookie Pull start--------------- 

        f.write(format_text('\n\nCookies: \n',r.cookies)),
        print(format_text('\n\nCookies: \n',r.cookies)),
        f.write(format_text('HTML ',r.text)),
        print(format_text('HTML: ',r.text)),
            
            #----------------- Cookie Pull End/CMD Start---------------
            #this section runs through all the commands in config.py. this is apart of the modular features of Reconbear.
            #Maybe in the future we have different "configurations" for different types of actions.

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
        exit()
#-------------------------------- Cookie Pull End/CMD Start---------------      

if __name__ == "__main__":
    main()
