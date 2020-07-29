import requests
import urllib.request
import time
import sys
import csv
import smtplib
from os.path import basename
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication
from bs4 import BeautifulSoup


def checkInput():
    states = ['baden-wuerttemberg', 'bayern', 'berlin', 'brandenburg', 'bremen', 'hamburg', 'hessen', 'mecklenburg-vorpommern',
        'niedersachsen', 'nordrhein-westfalen', 'rheinland-pfalz', 'saarland', 'sachsen', 'sachsen-anhalt', 'schleswig-holstein', 'thueringen']
    if sys.argv[1] not in states:
        print(usage)
        sys.exit()

my_mail = ''
to_mail = ''
msg = MIMEMultipart()
msg['From'] = my_mail
msg['To'] = to_mail
usage = 'usage: immoscout.py <state> <city> <room> <price>'
url = "https://www.immobilienscout24.de/Suche/de/" + 
    state + "/" + 
    city + "/" + 
    room + "-zimmer-wohnung-mieten?price=-" +
    price + ".0&enteredFrom=result_list#/"

checkInput()
state = sys.argv[1]
city = sys.argv[2]
room = sys.argv[3]
price = sys.argv[4]

my_password = ''


response = requests.get(url)
soup = BeautifulSoup(response.text, 'html.parser')
results = soup.find_all('a', 'result-list-entry__brand-title-container')
new_apartements = []
old_apartements = []
new_apartements.append(['Title', 'Id', 'Link', 'Old/New'])
i = 0
apartement_found = False

for result in results:
    if (str(result.h5.span) == 'None'):
        new_apartement = [result.h5.string, result['href'].replace(
            '/expose/', ''), 'https://www.immobilienscout24.de' + result['href'], 'Old']
    else:
        new_apartement = [str(result.h5).rsplit('</span>')[1].replace('</h5>', ''), result['href'].replace(
            '/expose/', ''), 'https://www.immobilienscout24.de' + result['href'], 'Old']
    new_apartements.append(new_apartement)
    print(result.h5.span)


with open('./apartements.csv', 'w+', newline='') as my_file:
    reader = csv.DictReader(my_file)
    for row in reader:
        old_apartement = [row['Title'], row['Id'], row['Link']]
    old_apartements.append(old_apartement)

    for apartement in new_apartements:
        if apartement not in old_apartements:
            i += 1
            apartement[3] = 'New'
            apartement_found = True
                
    writer = csv.writer(my_file, quoting=csv.QUOTE_ALL)
    writer.writerows(new_apartements)
    part = MIMEApplication(my_file.read(), Name='apartements.csv')
    
part['Content-Disposition'] = 'attachment; filename="%s"' % 'apartements.csv'        
msg.attach(part)

if apartement_found is True:
    if i is 1:
        msg['Subject'] = i + ' neues Apartement wurde gefunden.'
    else:
        msg['Subject'] = i + ' neue Apartements wurden gefunden.'     
    emailText = 'Im Anhang befindet sich eine CSV Datei mit allen Apartements.'
    msg.attach(MIMEText(emailText, 'html'))
    
    server = smtplib.SMTP('', 587)
    server.starttls()
    server.login(my_mail, my_password)
    text = msg.as_string()
    server.sendmail(my_mail, to_mail, text)
    server.quit()
        
