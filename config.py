class Configuration:

    def __init__(self, site, ports, proxies):
        self.proxies = proxies
        self.cmds =[
            f"nmap -Pn -sC -T4 --reason {site}",
            f"nmap -Pn -T4 --script ssl-enum-ciphers --reason {site}",
            f"nmap -p {ports} --script http-auth, {site}",
            f"nmap -p {ports} --script http-auth-finder, {site}",
            f"nmap -p {ports} --script http-ntlm-info {site}",
            f"nmap -p {ports} --script http-aspnet-debug {site}",
            f"nmap -p {ports} --script http-stored-xss {site}",
            f"nmap -p {ports} --script http-methods {site}",
            f"nmap -sS -A -sV --reason --script=http-enum {site}",
            f"nmap -p 139,145 --script=smb-enum* {site}",
            f"nmap -p 139,145 --script=smb-os-discovery.nse {site}",
            f"nmap -p {ports} --script=http-sitemap-generator.nse {site}",
            f"nikto -p {ports} -h {site}",
            f"hping3 -S {site} -c 15 -p {ports}", #note to research this function further
            f"curl -k https://{site}/images",
            f"curl -k https://{site}/Images",
            f"curl -svk https://{site}/asdf",
            f"ffuf -w /usr/share/wordlists/SecLists/Discovery/DNS/deepmagic.com_top50kprefixes.txt -u https://{site}/FUZZ -c -v -fc 404,302,301",
            #f"ffuf -w /usr/share/seclists/Discovery/DNS/dns-Jhaddix.txt -u http://target.com/ -H "Host:FUZZ.{site}" -of md -o subdomain/fuzzing_dnsjhaddix.md",
            f"feroxbuster -u https://{site} --filter-status 400,404,302,301 --extract-links --auto-bail",
            f"nmap -vv -sU -p-  {site}",
            f"nmap -vv -sT -p-  {site}"]
