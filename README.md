# get-bruter
This is a passive get parameter brute-forcing tool,
my tool is good for "ignore reflections count" future.

The main minuse is that it works slow for now, but I am tending to make it faster without usnig pythons requests library.


Why you need that future?
Well consider your ?ANYTHING=test get's reflected in HTML like this --> "x.com/?ANYTHING=test", 

this means any parameter's value will get reflected, and that's where you need "Ignore reflections count".

Also tell me if you want me to add up 
"add session cookies" future, if there is at least one person who will want that future I will add it up.

About wordlist
I got wordlist by merging AI generated wordlist + some github wordlist.
