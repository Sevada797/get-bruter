import os
import time
import random
import urllib3
import asyncio
import aiohttp
import traceback
import sys
from urllib.parse import urlparse, parse_qsl, urlencode, urlunparse



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
print("Author: @Sevada797\n")

# Value to use in URL parameters
value = f"NoWayThisCouldBeInHTML64f27e18356fa{random.randint(0, 1000000)}"


# Define headers for requests
headers = {
    "User-Agent": "chrome",
    "Accept-Encoding": "gzip, deflate, br"
}
# define for global
reflectioncount=0

# Check for reflections in the response HTML
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

# Get the ignore reflection count dynamically
def getIgnoreRcount(value, html):
    rcount = 0
    while html.find(value) != -1:
        html = html[int(html.find(value) + len(value)):]
        rcount += 1
    return rcount

# Set a reasonable timeout for aiohttp requests
timeout = aiohttp.ClientTimeout(total=10)  # 5 seconds max for full request

# Run all tasks asynchronously
async def run_all_tasks(urls, params, querySign, value):
    conn = aiohttp.TCPConnector(limit=100)
    async with aiohttp.ClientSession(connector=conn, timeout=timeout) as session:
        for url in urls:
            try:
                test_url = f"{url}{querySign}someNonExistingParam={value}"
                async with session.get(test_url, headers=headers, allow_redirects=True, ssl=False) as resp:
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

# Dynamit mode: each param gets a unique value, then reflection is checked per that value
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

        # Step 1: Add dummy param to calculate ignore reflection count
        dummy_param = "someNonExistingParam"
        while dummy_param in qs:
            dummy_param += "_x"
        qs[dummy_param] = base_value

        # Step 2: Create a unique value for each real param
        unique_values = {}
        for param in param_names:
            unique_values[param] = f"NoWayThisCouldBeInHTML64f27e18356fa{random.randint(0, 1000000)}"
            qs[param] = unique_values[param]  # Replace value

        full_qs = urlencode(qs)
        full_url = urlunparse((parsed.scheme, parsed.netloc, parsed.path, parsed.params, full_qs, parsed.fragment))

        # Step 3: Make the request with all modified param values
        async with session.get(full_url, headers=headers, allow_redirects=True, ssl=False) as resp:
            html = await resp.text()
            rcount = getIgnoreRcount(base_value, html)
            print(f"\n[***] {raw_url}")
            print(f"[~] Status: {resp.status} | Ignore reflection count (base): {rcount}")

        # Step 4: Check each param's unique value in the response
        for param, unique_val in unique_values.items():
            print(f"    [~] Scanning param: {param} = {unique_val}")
            if findReflections(0, rcount, unique_val, html):
                print(f"    [+] Reflected param: {param}")
                with open("getfound.txt", "a") as f:
                    f.write(f"{full_url} -> {param}={unique_val} (ignoreRCount={rcount})\n")

    except Exception as e:
        print(f"[!] Error on {raw_url}: {e}")






# Async version of mymain with timeout handled by session
async def mymain_async(session, url, param, querySign, value, rcount):
    global reflectioncount
    full_url = f"{url}{querySign}{param.strip()}={value}"
    print(f"Testing URL: {full_url}")

    try:
        async with session.get(full_url, headers=headers, allow_redirects=True, ssl=False) as response:
            html = await response.text()
            if findReflections(0, rcount, value, html):
                print(f"\n[+] Found reflections for parameter - {param.strip()}")
                with open("getfound.txt", "a") as f:
                    f.write(f"{full_url} -> {str(reflectioncount)} (ignoreRCount={rcount})\n")  # +" -> "+ str(reflectioncount)   later add this but not rn, since I used recursion, it stops on found item and doesn't get for you all reflection differences -_-
                    # ahh yeahh recursion + or logic haha 
    except Exception as e:
        #print(f"[-] Error on {param.strip()} -> {type(e).__name__}: {e}")
        #traceback.print_exc()
        pass  # stay silent like a shadow 😎


# CLI check
# Main logic to check if URL or file is provided
if "--dynamit" in sys.argv:
    filename = input("Enter file with URLs: ")
    asyncio.run(run_dynamit_mode(filename, value))
else:
    # User input
    urlOrFile = input("Enter url or filename: ")
    querySign = input("Choose either ? or & (if there is ? in url, choose &, default is ?): ") or "?"
    wlist_choice = input("""~Worldlists available~
1) alpha1+2
2) commonparams
3) (enter wordlist if not in current path use absolute path)
Your choice: """)
    wlists = [path+'wlists/alpha1+2.txt', path+'wlists/commonparams.txt']
    try: 
        wlist = wlists[int(wlist_choice) - 1]
    except:
        wlist=wlist_choice

    if urlOrFile.startswith("http://") or urlOrFile.startswith("https://"):
        # Direct URL input
        with open(wlist, "r") as file:
            params = [line.strip() for line in file]
        urls = [urlOrFile]
        # Run tasks with direct URL, no need for prefix/suffix
        asyncio.run(run_all_tasks(urls, params, querySign, value))
    else:
        # Handling subdomains
        with open(wlist, "r") as file1, open(urlOrFile, "r") as file2:
            # Adding the proper prefix for subdomains
            params = [line.strip() for line in file1 if line.strip()]
            urls = [f"https://{line.strip()}/" for line in file2 if line.strip()]
        # Run tasks for subdomains
        asyncio.run(run_all_tasks(urls, params, querySign, value))

print("STATUS: Scan finished, check getfound.txt for results 😉")
