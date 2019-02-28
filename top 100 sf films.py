import requests

ua = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36'
headers = {'User-Agent': ua }

filename = "C:/Users/LeeMarc-Paul/Downloads/top 100 sf results.txt"
open(filename, 'w') 

stop = 100

for i in range(1,stop+1):
    topsf = 'https://www.ign.com/lists/best-science-fiction-movies/' + str(i)
    r = requests.get(topsf, headers = headers)
    x = str(r.content)

    title = x[x.find('<title>')+7:x.find(' 100 Best Sci-Fi Movies')]


    with open(filename, 'a') as fd:
            print (title, file=fd)
	
