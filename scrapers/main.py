import requests
import sys
from bs4 import BeautifulSoup

osszes = []

base_url = 'https://www.citatum.hu/toplista.php?ido=kezdetek&lap='

for i in range(1, 11):

    sys.stdout.write("\r"+ str(i) + " [" + (i * "=") + ((10-i) * " ")  + "]")
    sys.stdout.flush()

    r = requests.get(base_url+str(i))

    soup = BeautifulSoup(r.text, 'html.parser')

    idezetek = soup.find('div', {'id':'idz'}).find_all('p', {'class':None})

    for idezet in idezetek:
        osszes.append(idezet.text)
        
with open('idezetek', 'w') as f:
	for idezet in osszes:
		f.write(idezet+'\n')
