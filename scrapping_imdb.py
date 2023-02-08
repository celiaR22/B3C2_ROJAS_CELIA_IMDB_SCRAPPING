from bs4 import BeautifulSoup
import requests
import re
import csv

url = 'http://www.imdb.com/chart/top'
res = requests.get(url)
soup = BeautifulSoup(res.text, 'lxml')

movies = soup.select('td.titleColumn')
links = [a.attrs.get('href') for a in soup.select('td.titleColumn a')]
casting = [a.attrs.get('title') for a in soup.select('td.titleColumn a')]
sortie = [b.attrs.get('data-value') for b in soup.select('td.posterColumn span[name=ir]')]
votes = [b.attrs.get('data-value') for b in soup.select('td.ratingColumn strong')]

imdb = []
# On ouvre le fichier en mode écriture
fichier = open('250films.csv','w',encoding='utf-8')
# Créer l'writeret fichier
# writer = csv.writer(fichier, delimiter=',')
writer = csv.writer(fichier, lineterminator='\n')
for index in range(0, len(movies)):
    movies_string = movies[index].get_text()
    movie = (' '.join(movies_string.split()).replace('.', ''))
    movie_title = movie[len(str(index))+1:-7]
    year = re.search('\((.*?)\)', movies_string).group(1)
    place = movie[:len(str(index))-(len(movie))]
    data = {"movie_title": movie_title,
            "year": year,
            "place": place,
            "star_cast": casting[index],
            "rating": sortie[index],
            "vote": votes[index],
            "link": links[index]}
    imdb.append(data)
    writer.writerow(place)
    writer.writerow(movie_title)
    writer.writerow(year)
    writer.writerow(casting[index])
    writer.writerow(' ')
fichier.close()