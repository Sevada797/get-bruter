import os
import time
import random
import urllib3
import asyncio
import aiohttp

# Disable only the specific warning
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# Clear screen
os.system("clear")
time.sleep(1)
os.system("clear")
print("--------------------------MyGetBruter1.0.1--------------------------")
print("Author: @Sevada797\n")

# User input
urlOrFile = input("Enter url or filename: ")
querySign = input("Choose either ? or & (if there is ? in url, choose &, default is ?): ") or "?"
wlist_choice = int(input("""~Worldlists available~
1) alpha1+2
2) commonparams
Your choice: """))
wlists = ['./wlists/alpha1+2.txt', './wlists/commonparams.txt']
wlist = wlists[wlist_choice - 1]

# Value to use in URL parameters
value = f"NoWayThisCouldBeInHTML64f27e18356fa{random.randint(0, 1000000)}"

# Define headers for requests
headers = {
    "User-Agent": "chrome",
    "Accept-Encoding": "gzip, deflate, br"
}

# Async version of mymain
async def mymain_async(session, url, param, querySign, value, rcount):
    full_url = f"{url}{querySign}{param.strip()}={value}"
    print(f"Testing URL: {full_url}")

    try:
        async with session.get(full_url, headers=headers, allow_redirects=True, ssl=False) as response:
            html = await response.text()
            if findReflections(0, rcount, value, html):
                print(f"\n[+] Found reflections for parameter - {param.strip()}")
                with open("getfound.txt", "a") as f:
                    f.write(full_url + "\n")
    except Exception as e:
        print(f"[-] Error on {param.strip()} -> {str(e)}")

# Check for reflections in the response HTML
def findReflections(n, rcount, value, html):
    splited_html = html[int(html.find(value) + len(value)):] if n != 0 else html
    if n == rcount:
        return splited_html.find(value) != -1
    else:
        return findReflections(n + 1, rcount, value, splited_html)

# Get the ignore reflection count dynamically
def getIgnoreRcount(value, html):
    rcount = 0
    while html.find(value) != -1:
        html = html[int(html.find(value) + len(value)):]
        rcount += 1
    return rcount

# Run all tasks asynchronously
async def run_all_tasks(urls, params, querySign, value):
    conn = aiohttp.TCPConnector(limit=100)  # Set limit based on aggressiveness
    async with aiohttp.ClientSession(connector=conn) as session:
        tasks = []
        for url in urls:
            try:
                # Get the reflection count once for the URL before looping through params
                test_url = f"{url}{querySign}someNonExistingParam={value}"
                async with session.get(test_url, headers=headers, allow_redirects=True, ssl=False) as resp:
                    html = await resp.text()
                    rcount = getIgnoreRcount(value, html)
                    print(f"Found ignore reflection count for {url}: {rcount}")
            except:
                rcount = 0

            # Now loop through params and run mymain_async for each one
            for param in params:
                tasks.append(
                    mymain_async(session, url, param, querySign, value, rcount)
                )

        await asyncio.gather(*tasks)

# Main logic to check if URL or file is provided
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
        params = [line.strip() for line in file1]
        # Adding the proper prefix for subdomains
        urls = [f"http://{line.strip()}/" for line in file2]  # Use "https://" for production if needed
    # Run tasks for subdomains
    asyncio.run(run_all_tasks(urls, params, querySign, value))

print("STATUS: Scan finished, check getfound.txt for results 😉")
