class Configuration:

    def __init__(self, site, ports, proxies=None):

        self.http = "https://" if site.find("https://") == 0 else "http://"
        self.site = site.replace("http://", "").replace("https://", "")
        self.ports = ports
        self.proxies = proxies
        site = self.site.split(":")[0]

        self.cmds =[
            f"whatweb -a 3 --verbose {site}",
            f"nmap -Pn -sC -T4 --reason {site}",
            f"nmap -Pn -T4 --script ssl-enum-ciphers --reason {site}",
            f"nmap -p {self.ports} --script http-auth, {site}",
            f"nmap -p {self.ports} --script http-auth-finder, {site}",
            f"nmap -p {self.ports} --script http-ntlm-info {site}",
            f"nmap -p {self.ports} --script http-aspnet-debug {site}",
            f"nmap -p {self.ports} --script http-stored-xss {site}",#I am planning on adding XSStrike to this application and replace this one.
            f"nmap -p {self.ports} --script http-methods {site}",
            f"nmap -sS -A -sV --reason --script=http-enum {site}",
            f"nmap -p 139,145 --script=smb-enum* {site}",
            f"nmap -p 139,145 --script=smb-os-discovery.nse {site}",
            f"nmap -p {self.ports} --script=http-sitemap-generator.nse {site}",
            f"nikto -p {self.ports} -h {site}",
            f"hping3 -S {self.site} -c 15 -p {ports}", #note to research this function further
            f"curl -kLv {self.http}{site} --proxy 127.0.0.1 --proxy-anyauth", #| grep hidden -A 
            #15 -B 5 ",
            f"curl -k {self.http}{site}/images",
            f"curl -k {self.http}{site}/Images",
            f"curl -svk {self.http}{site}/asdf",
            f"gobuster dir -r -e --url https://{site} -w /usr/share/wordlists/SecLists/Discovery/Web_Content/common.txt --proxy 127.0.0.1:8080 -k",
            #f"gobuster fuzz -r -w /usr/share/wordlists/SecLists/Discovery/Web_Content/common.txt -u https://FUZZ.{site}",
            
            #f"ffuf -w /usr/share/wordlists/SecLists/Discovery/DNS/deepmagic.com_top50kprefixes.txt -u https://{site}/FUZZ -c -v -fc 404,302,301",
            #f"ffuf -w /usr/share/seclists/Discovery/DNS/dns-Jhaddix.txt -u http://target.com/ -H "Host:FUZZ.{site}" -of md -o subdomain/fuzzing_dnsjhaddix.md",
        ] 
