#frist attempt
#scrape this website for data in column ordr of 'current_date', 'current_price', 'fwd_month_1', 'fwd_price_1', 'fwd_price_2', fwd_month_2'
#however the actual date of the fwd_month and the fwd price are within the same cell in the table, and the fwd_month is just a month, not a date. So will need to convert month to a date, probably the first day of the month for now
# #https://www.shpgx.com/html/jkxhLNGdajglssj.html

#%%
# LOAD LIBRARIES
#nomally you will wanna run the requests html library using async options because of how vs code and juptyer notebooks interact. 
from requests_html import AsyncHTMLSession
from bs4 import BeautifulSoup
import re
import pandas as pd
import datetime
import nest_asyncio
#this libarray for some reason will make the below code run in a separate thread? anyway if you want to know more see the two links below. 
#https://stackoverflow.com/questions/46827007/runtimeerror-this-event-loop-is-already-running-in-python
#https://www.blog.pythonlibrary.org/2016/07/26/python-3-an-intro-to-asyncio/


#%%
#PLease note that you will need to b using the office guest wifi cause of security tag issues
url = 'https://www.shpgx.com/html/jkxhLNGdajglssj.html'
file_name = '../input_data/html/jkxhLNGdajglssj.txt'
file_name_csv = '../output_data/csv/LNG_China_{}.csv'.format(datetime.datetime.now().strftime('%Y%m%d'))

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

with open(file_name, 'w', encoding='utf-8') as f:
    f.write(str(soup))#write the html to a file 

#%%
 
with open(file_name, 'r', encoding='utf-8') as f:    
    html_string = f.read()#read the file back in

string1 = '按时间查询\n'
string2 = '\n第一页'
text_after_string1 = html_string.split(string1)[1]#split the html string at the string1 and get the text after the string1
text_after_string2 = text_after_string1.split(string2)[0]#split the text after string1 at the string2 and get the text before the string2

#now we have our data separate it into our 7 columns per row. 
#first col is a date, second col is a month, third col is a price, fourth col is a month, fifth col is a price, sixth col is a month, seventh col is a price
#name the cols as 'current_date','fwd_month_1', 'fwd_price_1',  fwd_month_2', 'fwd_price_2',  'fwd_month_3', 'fwd_price_3'

#each row ends at the 4th \n string. also the 2nd/3rd, 4th/5th and 6th/7th cols are between \n's themselves So we will separate our rows using that pattern first

rows = text_after_string2.split('\n')

#do a quick test to make sure we ahve X rows. The expectation is that this wbesite will only show data for X rows, so if there are not X rows then the weebstie probably changed and the results form this program wont be correct. hopefully the change is easy!
no_expected_rows = 100
if len(rows) != no_expected_rows:
    #throw error
    print('ERROR: unexpected number of rows')
    print('expected: ', no_expected_rows)
    print('actual: ', len(rows))
    raise ValueError('unexpected number of rows')


#%%

df = pd.DataFrame(columns=['current_date','fwd_month_1', 'fwd_price_1',  'fwd_month_2', 'fwd_price_2',  'fwd_month_3', 'fwd_price_3'])#create a dataframe to hold our data

months_dict = {'Jan':1, 'Feb':2, 'Mar':3, 'Apr':4, 'May':5, 'Jun':6, 'Jul':7, 'Aug':8, 'Sep':9, 'Oct':10, 'Nov':11, 'Dec':12}

# go through the rows and add them to the columns
for i in range(int(len(rows)/4)):
    row_data = rows[(4*i) : 4*(i+1)]#get datga for entire row

    current_date = pd.to_datetime(row_data[0])
    #if current date is Oct or later,then our fwd_month's may be in the next year.
    current_month = current_date.month
    current_year = current_date.year
    extra_year_1 = 0
    extra_year_2= 0 
    extra_year_3 =0#use these to add 1 or 0 to the year of the date.

    if current_month == 10:
        extra_year_1 = 1
        extra_year_2 = 1
        extra_year_3 = 1
    elif current_month == 11:
        extra_year_2 = 1
        extra_year_3 = 1
    elif current_month == 12:
        extra_year_3 = 1

    #now loop through our months dict to see what month is the fwd_month
    for month_name, month_number in months_dict.items():
        if month_name in row_data[1]:
            month = month_number
            year = current_year + extra_year_1
            fwd_month_1 = pd.to_datetime(datetime.datetime(year, month, 1))
            break
    fwd_price_1 = row_data[1].split(':')[1]

    #do same again for 2nd fwd_month, and 3rd fwd_month
    for month_name, month_number in months_dict.items():
        if month_name in row_data[2]:
            month = month_number
            year = current_year + extra_year_2
            fwd_month_2 = pd.to_datetime(datetime.datetime(year, month, 1))
            break
    fwd_price_2 = row_data[2].split(':')[1]

    for month_name, month_number in months_dict.items():
        if month_name in row_data[3]:
            month = month_number
            year = current_year + extra_year_3
            fwd_month_3 = pd.to_datetime(datetime.datetime(year, month, 1))
            break
    fwd_price_3 = row_data[3].split(':')[1]
    
    new_row = pd.DataFrame([current_date, fwd_month_1, fwd_price_1, fwd_month_2, fwd_price_2, fwd_month_3, fwd_price_3])
    #add all to a row
    df = pd.concat([new_row, df], axis=0)#add the row to the dataframe

#%%
#we now have the data we wanted. save to csv cause we done


df.to_csv(file_name_csv, index=False)#save the dataframe to a csv file

#%%