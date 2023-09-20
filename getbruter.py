import os
import time
import requests
os.system("clear")
print("NOTE: redirecting is enabled, to disable edit source code.")
print("NOTE: word list is wlist.txt, for changing it pls edit the source code, or rename your file to wlist.txt")
time.sleep(3)
os.system("clear")
print("--------------------------MyGetBruter1.0.0--------------------------\n")
url=input("Enter url: ")
#params=input("Enter file containing parameter names: ")
rcount=int(input("Enter how many reflections should be ignored: "))
value=input("Enter value for parameter(leave blank for default, default is-NoWayThisCouldBeInHTML64f27e18356fa): ")
querySign=input("Choose eighter ? or & (if there is ? in url choose &, default is ?): ")
if (value==""):
    value="NoWayThisCouldBeInHTML64f27e18356fa"
if (querySign==""):
    querySign="?"

with open("wlist.txt", "r") as file:
    for line in file:
        print("testing url: "+url+querySign+"{}={}".format(line.strip(), value))
        html=requests.get(url+querySign+"{}={}".format(line.strip(), value), allow_redirects=True)
        #print(url+"?{}={}".format(line.strip(), value))
        def findReflections(n, rcount, value, html):
            if (n==0):
                splited_html=html.text
            else:
                splited_html=html[int(html.find(value)+len(value)):]
            if(n==rcount):
                return splited_html.find(value)!=-1
            else:
                n=n+1
                return findReflections(n, rcount, value, splited_html)
        if findReflections(0, rcount, value, html):
            print("\nFound reflections for parameter - {}".format(line.strip()))
            f=open("getfound.txt", "a")
            f.write("{}".format(line.strip())+"\n")
            f.close()

