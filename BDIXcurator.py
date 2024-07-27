from datetime import datetime
import requests
import time
import re
import webbrowser
import os
import sys


FTPurls = [
    "https://sites.google.com/view/bdixftpserverlist/media-ftp-servers", 
    "http://ftp.com.bd/ftp-server/movieserver.html",
]
LiveTVurls = [
    "https://sites.google.com/view/bdixftpserverlist/live-tv-servers", 
    "http://ftp.com.bd/ftp-server/livetv.html",
]


def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)


#Function for the header
def header():
    now = datetime.now()
    dateAndTime = now.strftime("Date: %d-%m-%Y<br>\nTime: %H:%M:%S<br><br>")


    with open("workingsites.html", 'w') as f:
        f.write("""
<style>
    body{
        background-color: #202020;
    }

    #creationInfo{
        text-align: center;
        color: #19c0aa; 
    }

    .title{
        color: #f07b1b;
    }

    a{
        color: #1c86c4;
    }

    .linkslist{
        color: grey;
    }
</style>
<body>

<div id="creationInfo"><PRE>##################
#   Created by   #
#     Shibly     #
##################</PRE><br>"""+
dateAndTime+
"""
</div>
""")






#Function to extract urls from text
def extract_links_from_text(text):
    # url_pattern = r'https?://\d+[^\s<>"]+' #For IPs only
    url_pattern = r'https?://[^\s<>"]+'
    
    sourcelinks = re.findall(url_pattern, text)
    
    return sourcelinks






#Function to get server list from page source
def getServerList(urls, type):
    print(f"Updating {type} server list... ",end="")
    updated = False
    source_code  = ""
    for url in urls:
        try:
            requests.head(url, timeout=2.5)
            response = requests.get(url)
            if response.status_code == 200:
                updated = True
                source_code += response.text
        except:
            pass

    file_path = resource_path(f'{type}source.txt')
    with open(file_path, 'r', encoding='utf-8') as file:
        source_code += file.read()

    sourcelinks = extract_links_from_text(source_code)
    links = [x for x in sourcelinks if "google" not in x and "facebook" and "cloudflare" not in x]
    links = [item.rstrip('/') for item in links]
    links = [link.replace("'", "").replace(",", "") for link in links]
    links = list(set(links))
    if updated:
        print("Updated✅")
    else:
        print("Update failed❌")
    return sorted(links)




#Function for progressbar
def progressbar(progress, total, success):
    percent = 70*(progress/float(total))
    bar = chr(9608)*int(percent) + '-' * (70-int(percent))
    print(f"\r|{bar}| {(percent*100/70):.2f}%   🔴 {progress-success} 🟢 {success}", end="\r")






#Function for main curation process
def curate(urls, type, equalsigns):
    links = getServerList(urls, type)
    size = len(links)
    print(f"Total {size} servers available.")
    print(f"Curating working {type} servers...\n\n")
    current = 0
    count = 0
    
    with open("workingsites.html", 'a') as f:
        f.write("""
<br><br>
<div class="title">
"""+
type+" sites:<br>"+'='*equalsigns+"""<br>
</div>
<div class="linkslist">
""")
        for site in links:
            current += 1
            # start_time = time.time()
            # pos = f"({current}/{size})"
            try:
                
                response = requests.head(site, timeout=0.05)
                if response.status_code == 200:
                    count+=1
                    f.write(f'{count}. <a href="{site}"target="_blank">{site}</a><br>\n')
                    # print(f"{pos.ljust(12)}{site}✅")
                    # f.write(f'{count}. <a href="{site}">{site}</a> (Time taken: {time.time() - start_time:.2f} seconds)<br>\n')
                progressbar(current, size, count)
            except requests.exceptions.RequestException as e:
                # print(f"{pos.ljust(12)}{site}❌")
                progressbar(current, size, count)
                
        f.write("</div>\n\n")







        



#Main interface
def app():
    valid = True
    while(True):
        print(
            chr(9608)*44+"\n"+
            chr(9608)+" "*42+chr(9608)+"\n"+
            chr(9608)+" "*10+"BDIX Curator by Shibly"+" "*10+chr(9608)+"\n"+
            chr(9608)+" "*42+chr(9608)+"\n"+
            chr(9608)*44+"\n"   
        )

        print(" 1. Get working FTP server list")
        print(" 2. Get working LiveTV server list")
        print(" 3. Get both")
        print(" 4. Exit\n\n")
        
        if not valid:
            print("[Enter a valid choice]\n\n")

        try:
            choice = int(input())
            os.system("cls")
            header()
            if choice == 1:
                curate(FTPurls, "FTP", 7)
            elif choice == 2:
                curate(LiveTVurls, "LiveTV", 10)
            elif choice == 3:
                curate(FTPurls, "FTP", 7)
                print("\n"*3)
                curate(LiveTVurls, "LiveTV", 10)
            elif choice == 4:
                return
            print("\n\n\nCompleted. Opening results...")
            webbrowser.open('workingsites.html')
            return
        except ValueError:
                os.system("cls")
                valid = False
                continue
 

app()


