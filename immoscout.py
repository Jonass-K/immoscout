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
from getpass import getpass

my_mail = ''
to_mail = ''
smtp_host = ''
smtp_port = 0
sleep_time = 60*60*8

msg = MIMEMultipart()
msg['From'] = my_mail
msg['To'] = to_mail
usage = 'usage: "immoscout.py <state> <city> <room> <price>" or "immoscout.py <url>" '

if len(sys.argv) == 5:
    url = 'https://www.immobilienscout24.de/Suche/de/' + sys.argv[1] + '/' + sys.argv[2] + '/' + \
        sys.argv[3] + '-zimmer-wohnung-mieten?price=-' + \
        sys.argv[4] + '.0&enteredFrom=result_list#/'
elif len(sys.argv) == 2:
    url = sys.argv[1].replace('"', '')   
else:
    print(usage)
    sys.exit()

my_password = getpass()

k = 0

while True:
    old_apartements = []
    new_apartements = []
    i = 0
    apartement_found = False

    # sleep for 8 hours
    if k != 0:
        time.sleep(sleep_time)

    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    results = soup.find('ul', id='resultListItems')
    results = results.find_all('a', 'result-list-entry__brand-title-container')
    new_apartements.append(['Title', 'Id', 'Link', 'Old/New'])

    for result in results:
        if (str(result.h5.span) == 'None'):
            new_apartement = [result.h5.string, result['href'].replace(
                '/expose/', ''), 'https://www.immobilienscout24.de' + result['href'], 'Old']
        else:
            new_apartement = [str(result.h5).rsplit('</span>')[1].replace('</h5>', ''), result['href'].replace(
                '/expose/', ''), 'https://www.immobilienscout24.de' + result['href'], 'Old']
        new_apartements.append(new_apartement)

    with open('./apartements.csv', 'w+', newline='') as my_file:
        if k == 0:
            for apartement in new_apartements:
                i += 1
                apartement[3] = 'New'
                apartement_found = True
        else:
            reader = csv.reader(my_file)
            for apartement in new_apartements:
                for old_apartement in old_apartements:
                    if apartement[1] == old_apartement[1]:
                        i += 1
                        apartement[3] = 'New'
                        apartement_found = True

        writer = csv.writer(my_file, quoting=csv.QUOTE_ALL)
        writer.writerows(new_apartements)

    with open('./apartements.csv', 'r', newline='') as my_file:
        part = MIMEApplication(my_file.read(), Name='apartements.csv')

    part['Content-Disposition'] = 'attachment; filename="%s"' % 'apartements.csv'
    msg.attach(part)

    if apartement_found is True:
        if i == 2:
            msg['Subject'] = str(i - 1) + ' neues Apartement wurde gefunden.'
        else:
            msg['Subject'] = str(i - 1) + ' neue Apartements wurden gefunden.'
        emailText = 'Im Anhang befindet sich eine CSV Datei mit allen Apartements.'
        msg.attach(MIMEText(emailText, 'html'))

        server = smtplib.SMTP(smtp_host, smtp_port)
        server.starttls()
        server.login(my_mail, my_password)
        text = msg.as_string()
        server.sendmail(my_mail, to_mail, text)
        server.quit()
    k += 1
