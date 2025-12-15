import os
import time
import random
import urllib3
import asyncio
import aiohttp
import traceback
import sys
from urllib.parse import urlparse, parse_qsl, urlencode, urlunparse
from aiohttp import ClientConnectorError
import signal
import socket

def handler(signum, frame):
    print("\n[!] Stopped by user. Exiting.")
    sys.exit(0)

signal.signal(signal.SIGINT, handler)



# Disable only the specific warning
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

version="2.0"
try:
    path=os.environ["GETBRUTER_PATH"]+"/"
except:
    path=""


# Clear screen
os.system("clear")
time.sleep(1)
os.system("clear")
print(f"--------------------------Get-Bruter V{version}--------------------------")
print("Author: @Sevada797")
print("[INFO]: Called gbr2 this is useful for 301,302,307 XSS hunting\n")

# Value to use in URL parameters
value = f"NoWayThisCouldBeInHTML64f27e18356fa{random.randint(0, 1000000)}"


# Define headers for requests
headers = {
    "User-Agent": "chrome"
}
# define for global
reflectioncount=0

###########################
## STARTOF simple core funcs
############################

# Check for reflections in the response HTML
def findReflections(n, rcount, value, html):
    global reflectioncount
    reflectioncount=n
    if (int(html.find(value)==-1)): # default reflection 0 return case
        return False
    splited_html = html[int(html.find(value) + len(value)):] if n != 0 else html
    if (splited_html.find(value)==-1 and n<=rcount):
        return False
    elif n > rcount:
        return splited_html.find(value) == -1 or findReflections(n + 1, rcount, value, splited_html)
    else:
        return findReflections(n + 1, rcount, value, splited_html)

## Get the ignore reflection count dynamically
def getIgnoreRcount(value, html):
    rcount = 0
    while html.find(value) != -1:
        html = html[int(html.find(value) + len(value)):]
        rcount += 1
    return rcount
###########################
## ENDOF simple core funcs
############################



# Set a reasonable timeout for aiohttp requests
timeout = aiohttp.ClientTimeout(total=10)  # 5 seconds max for full request



####~~~~~~~~~~~~~~~~~~~~~~#####
####   START OF ASYNCS    #####
####~~~~~~~~~~~~~~~~~~~~~~#####

# Run all tasks asynchronously
async def run_all_tasks(urls, params, querySign, value):
    conn = aiohttp.TCPConnector(limit=100)
    async with aiohttp.ClientSession(connector=conn, timeout=timeout) as session:
        for url in urls:
            try:
                test_url = f"{url}{querySign}someNonExistingParam={value}"
                async with session.get(test_url, headers=headers, allow_redirects=False, ssl=False) as resp:
                    html = await resp.text()
                    rcount = getIgnoreRcount(value, html)
                    print(f"\n[***] Scanning subdomain: {url}")
                    print(f"[~] Found ignore reflection count for {url}: {rcount}")
            except Exception as e:
                print(f"[!] Error while getting ignore reflection count for {url} -> {str(e)}")
                rcount = 0

            # Only gather tasks for this one subdomain
            tasks = []
            for param in params:
                tasks.append(
                    mymain_async(session, url, param, querySign, value, rcount)
                )
            await asyncio.gather(*tasks)

            print(f"[~] Sleeping 0.05 second after {url} to stay stealthy...")
            await asyncio.sleep(0.05)

####################################################################################
# Dynamit mode: each param gets a unique value, then reflection is checked per that value
####################################################################################
async def run_dynamit_mode(filename, base_value):
    try:
        with open(filename, "r") as f:
            urls = [line.strip() for line in f if line.strip()]
    except Exception as e:
        print(f"[!] Failed to read file: {filename} | Error: {e}")
        return

    conn = aiohttp.TCPConnector(limit=100)
    async with aiohttp.ClientSession(connector=conn, timeout=timeout) as session:
        tasks = [handle_url(session, url, base_value) for url in urls]
        await asyncio.gather(*tasks)


async def handle_url(session, raw_url, base_value):
    try:
        parsed = urlparse(raw_url)
        qs = dict(parse_qsl(parsed.query))
        param_names = list(qs.keys())

        dummy_param = "someNonExistingParam"
        qs[dummy_param] = base_value

        # Rebuild the URL with dummy param
        new_query = urlencode(qs)
        parsed = parsed._replace(query=new_query)
        full_url = urlunparse(parsed)

        print(f"\n[~] Testing: {raw_url}")
        
        try:
            async with session.get(full_url, headers=headers, allow_redirects=False, ssl=False) as resp:
                html = await resp.text()
                rcount = getIgnoreRcount(base_value, html)
                print(f"[+] Reflection count for {raw_url}: {rcount}")
        except (ClientConnectorError, socket.gaierror) as dns_error:
            print(f"[!] DNS error or cannot resolve host: {raw_url}")
            return
        except asyncio.TimeoutError:
            print(f"[!] Timeout while accessing: {raw_url}")
            return
        except Exception as e:
            print(f"[!] General error for {raw_url}: {e}")
            return

        tasks = []
        for param in param_names:
            unique_val = f"NoWayThisCouldBeInHTML{random.randint(0,9999999)}"
            tasks.append(mymain_async(session, raw_url, param, "?" if "?" not in raw_url else "&", unique_val, rcount))
        await asyncio.gather(*tasks)

    except Exception as e:
        print(f"[!] Unexpected error on URL {raw_url}: {e}")
############################
## endof dynamit mode
###########################

##################################
## STARTOF dynamit-inject module
##################################

# New Dynamit Inject mode module
async def run_dynamit_inject_mode(filename):
    payload = "mySafeStr'NoWayThisCouldBeInHTML_1<NoWayThisCouldBeInHTML_2\"mySafeStr"
    try:
        with open(filename, "r") as f:
            urls = [line.strip() for line in f if line.strip() and "?" in line]
    except Exception as e:
        print(f"[!] Failed to read file: {filename} | Error: {e}")
        return

    conn = aiohttp.TCPConnector(limit=100)
    async with aiohttp.ClientSession(connector=conn, timeout=timeout) as session:
        tasks = [handle_dynamit_inject(session, url, payload) for url in urls]
        await asyncio.gather(*tasks)


async def handle_dynamit_inject(session, raw_url, payload):
    try:
        parsed = urlparse(raw_url)
        qs = dict(parse_qsl(parsed.query))
        if not qs:
            return

        # Replace all parameter values with payload
        injected_qs = {k: payload for k in qs.keys()}
        new_query = urlencode(injected_qs)
        parsed = parsed._replace(query=new_query)
        full_url = urlunparse(parsed)

        print(f"[⚡] Injecting: {full_url}")

        async with session.get(full_url, headers=headers, allow_redirects=False, ssl=False) as resp:
            html = await resp.text()

            risk_level = 0

            if "mySafeStr'NoWayThisCouldBeInHTML_1" in html:
                risk_level += 1
            if "NoWayThisCouldBeInHTML_1<NoWayThisCouldBeInHTML_2" in html:
                risk_level += 1
            if "NoWayThisCouldBeInHTML_2\"mySafeStr" in html:
                risk_level += 1
            if "`mySafeStr" in html or "mySafeStr`" in html or "mySafeStr>" in html :
                risk_level=900

            print(f"[!] Risk Level: {risk_level} | {raw_url}")

            if risk_level >= 1:
                with open(resfile, "a") as log:
                    log.write(f"Risk {risk_level}: {full_url}\n")

    except Exception as e:
        print(f"[!] Error in inject handler: {e}")

##################################
## ENDOF dynamit-inject module
#################################



##################################
## STARTOF dynamit-cookie module
##################################
async def run_dynamit_cookie_mode(filename):
    try:
        with open(filename, "r") as f:
            urls = [line.strip() for line in f if line.strip()]
    except Exception as e:
        print(f"[!] Failed to read file: {filename} | Error: {e}")
        return

    conn = aiohttp.TCPConnector(limit=100)
    async with aiohttp.ClientSession(connector=conn, timeout=timeout) as session:
        tasks = [handle_cookie_reflection(session, url) for url in urls]
        await asyncio.gather(*tasks)

async def handle_cookie_reflection(session, raw_url):
    try:
        parsed = urlparse(raw_url)
        qs = dict(parse_qsl(parsed.query))
        param_names = list(qs.keys())

        # Assign unique values
        values = {param: f"CheckMeInCookie_{random.randint(0, 99999)}_{i}" for i, param in enumerate(param_names)}
        for param, val in values.items():
            qs[param] = val

        # Rebuild the URL
        new_query = urlencode(qs)
        parsed = parsed._replace(query=new_query)
        full_url = urlunparse(parsed)

        print(f"\n[🍪] Testing (cookies): {full_url}")
        async with session.get(full_url, headers=headers, allow_redirects=False, ssl=False) as resp:
            cookies = resp.cookies
            set_cookie_headers = resp.headers.getall("Set-Cookie", [])

            if not set_cookie_headers:
                print("[~] No Set-Cookie headers.")
                return

            matched = False
            for param, val in values.items():
                for cookie in set_cookie_headers:
                    if val in cookie:
                        print(f"[+] Param '{param}' reflected in cookie!")
                        with open(resfile, "a") as f:
                            f.write(f"{full_url} -> {param} reflected in cookie\n")
                        matched = True
                        break
            if not matched:
                print("[~] No values reflected in cookies.")
    except Exception as e:
        print(f"[!] Error in cookie reflection check: {e}")
###############################
## ENDOF dynamit-cookie module
###############################

# Async version of mymain with timeout handled by session
async def mymain_async(session, url, param, querySign, value, rcount):
    global reflectioncount
    full_url = f"{url}{querySign}{param.strip()}={value}"
    print(f"Testing URL: {full_url}")

    try:
        async with session.get(full_url, headers=headers, allow_redirects=False, ssl=False) as response:
            html = await response.text()
            if findReflections(0, rcount, value, html):
                print(f"\n[+] Found reflections for parameter - {param.strip()}")
                with open(resfile, "a") as f:
                    f.write(f"{full_url} -> {str(reflectioncount)} (ignoreRCount={rcount})\n")  # +" -> "+ str(reflectioncount)   later add this but not rn, since I used recursion, it stops on found item and doesn't get for you all reflection differences -_-
                    # ahh yeahh recursion + or logic haha 
    except Exception as e:
        #print(f"[-] Error on {param.strip()} -> {type(e).__name__}: {e}")
        #traceback.print_exc()
        pass  # stay silent like a shadow 😎

####~~~~~~~~~~~~~~~~~~~~#####
####    END OF ASYNCS   #####
####~~~~~~~~~~~~~~~~~~~~#####




# CLI check
# Main logic to check if URL or file is provided

if "--dynamit" in sys.argv:
    resfile = 'getfound.txt'
    filename = input("Enter file with URLs: ").strip()
    asyncio.run(run_dynamit_mode(filename, value))

elif "--dynamit-cookies" in sys.argv:
    resfile = 'cookie_reflections.txt'
    filename = input("Enter file with URLs: ").strip()
    asyncio.run(run_dynamit_cookie_mode(filename))

elif "--dynamit-inject" in sys.argv:
    resfile = 'inject_reflections.txt'
    filename = input("Enter file with URLs: ").strip()
    asyncio.run(run_dynamit_inject_mode(filename))

else:
    url_or_file = input("Enter URL or filename: ").strip()
    query_sign = input("Choose either ? or & (if there is ? in URL, choose &, default is ?): ").strip() or "?"

    print("""\n~Wordlists available~
1) alpha1+2
2) commonparams
3) (Enter custom path to a wordlist)\n""")
    wlist_choice = input("Your choice: ").strip()
    default_wlists = [path + 'wlists/alpha1+2.txt', path + 'wlists/commonparams.txt']

    if wlist_choice in ['1', '2']:
        wlist = default_wlists[int(wlist_choice) - 1]
    else:
        wlist = wlist_choice

    with open(wlist, "r") as f:
        params = [line.strip() for line in f if line.strip()]

    if url_or_file.startswith(("http://", "https://")):
        urls = [url_or_file]
    else:
        with open(url_or_file, "r") as f:
            urls = [f"https://{line.strip()}/" for line in f if line.strip()]

    resfile = 'getfound.txt'
    asyncio.run(run_all_tasks(urls, params, query_sign, value))

print(f"STATUS: Scan finished, check {resfile} for results 😉")
