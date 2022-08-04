#frist attempt
#scrape this website for data in column ordr of 'current_date', 'current_price', 'fwd_month_1', 'fwd_price_1', 'fwd_price_2', fwd_month_2'
#however the actual date of the fwd_month and the fwd price are within the same cell in the table, and the fwd_month is just a month, not a date. So will need to convert month to a date, probably the first day of the month for now
# #https://www.shpgx.com/html/jkxhLNGdajglssj.html

#%%
#nomally you will wanna run the requests html library using async options because of how vs code and juptyer notebooks interact. 
from requests_html import AsyncHTMLSession
from bs4 import BeautifulSoup
import nest_asyncio
#this libarray for some reason will make the below code run in a separate thread? anyway if you want to know more see the two links below. 
#https://stackoverflow.com/questions/46827007/runtimeerror-this-event-loop-is-already-running-in-python
#https://www.blog.pythonlibrary.org/2016/07/26/python-3-an-intro-to-asyncio/


#%%
url = 'https://www.shpgx.com/html/jkxhLNGdajglssj.html'
file_name = '../input_data/html/jkxhLNGdajglssj.txt'

nest_asyncio.apply()#run when doing async things
asession = AsyncHTMLSession()#run when doing async things

async def get_url():
    #use me to scrape data from the website
    r = await asession.get(url)
    await r.html.arender()
    return r

results = asession.run(get_url)#the results are saved in a list. we assume there will be only 1 element in the list, but create a warning in case otehrwise

if len(results) > 1:
    print('WARNING: more than 1 result in results list')

#%%
html = results[0].html.text#get the html from the results

soup = BeautifulSoup(html, 'html.parser')#make easy to interact with the html

with open(file_name, 'w') as f:
    f.write(soup)

    x = f.read()

import re
m = re.search('2022', x)
m
#%%


#we have to interact with the code in chinese. so will be difficult to bug check. tehrefroe insert many checks to double check we have the data correct
soup.select('按时间查询').next_sibling#select the table we want to scrape

#%%
