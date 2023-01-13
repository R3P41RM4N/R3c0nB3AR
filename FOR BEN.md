Notes for Ben: It took me a bit, but I got the application to parse our the headers as well as the CSP. 
Changed the colors to something more readable (Green), 
Labelled the headers, and basically was prettying it up. 

Would love your thoughts on how we can improve it and also what other apps we should add. 
I did fix the output to log issue vs. what's displayed on the terminal. It's not pretty, but it works. 
Basically I use f.write and then go back and print() for the terminal's sake. That's where I left off with it. 

It's connecting to burp now and I think we're close to just tweaking it for basic webapp reconaissance. 

One of my friends suggested using a wordpress app, nuclei, and maybe something else for a common web application as well. I'm just spitballing here.


From my perspective initial release criteria would look something like this:
  1. Port Enumeration
  2. ID Crypto
  3. Fuzzing
  4. directory enumeration
  5. Identifying common vulnerabilities
  6. useful apps. 

What do you think? What is your success criteria look like? Are there any other apps we might want to be able to proxy through?
