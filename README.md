# immoscout
 
Immoscout can be used for parsing [immobilienscout24.de](https://immobilienscout24.de) and sending a mail from yourself to yourself (and others) with new listings.

*[immowelt.de](https://immowelt.de) and [ebay-kleinanzeigen.de](https://ebay-kleinanzeigen.de) will be added soon.*

Customize the file [immoscout.py](https://github.com/Jonass-K/immoscout/blob/master/immoscout.py) by adding your e-mail-address, your smtp host & port and how often the site gets checked (line 14-18): 

14. `my_mail = ''`

15. `to_mail = ''`

16. `smtp_host = ''`

17. `smtp_port = 0`

18. `sleep_time = 60*60*8`

**Usage:**
* `immoscout.py <state> <city> <rooms> <max_price>`
* `immoscout.py <url>`

**Usual e-mail-providers:**
* Outlook: 
    * SMTP-Server: smtp.office365.com
    * SMTP-Port: 587
* Gmail:
    * SMTP-Server: smtp.gmail.com
    * SMTP-Port: 587
* GMX:
    * SMTP-Server: mail.gmx.net
    * SMTP-Port: 587
* Web:
    * SMTP-Server: smtp.web.de
    * SMTP-Port: 587
