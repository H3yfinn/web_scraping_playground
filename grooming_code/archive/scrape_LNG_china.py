#frist attempt
#scrape this website for data in column ordr of 'current_date', 'current_price', 'fwd_month_1', 'fwd_price_1', 'fwd_price_2', fwd_month_2'
#however the actual date of the fwd_month and the fwd price are within the same cell in the table, and the fwd_month is just a month, not a date. So will need to convert month to a date, probably the first day of the month for now
# #https://www.shpgx.com/html/jkxhLNGdajglssj.html


#%%
#load libraries
import requests
from bs4 import BeautifulSoup

#create funcitons
def save_html(html, path):
    with open(path, 'wb') as f:
        f.write(html)
        
def open_html(path):
    with open(path, 'rb') as f:
        return f.read()

#%%
#create variables

url = 'https://www.shpgx.com/html/jkxhLNGdajglssj.html'
path = '../input_data/html/jkxhLNGdajglssj.html'

r = requests.get(url)

save_html(r.content, path)

#%%

html = open_html(path)


#%%

print(r.content[:100])

soup = BeautifulSoup(r.content, 'html.parser')

#%%

rows = soup.select('tbody tr')
#search for tr content within the tbody tags 
