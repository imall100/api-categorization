
import numpy as np
from bs4 import BeautifulSoup
import requests
import pandas as pd


#programmableweb.com is the best search tool I've found. The problem is the searches are format dependent

def api_category(api_name):
    
    try:
    
        keyword = api_name.replace(" ", "%20")
        
        url = 'https://www.programmableweb.com/category/all/apis?keyword={}'.format(keyword)
        
        response = requests.get(url)
        content = BeautifulSoup(response.content, "html.parser")
        
        table = content.find('table', attrs={'class':'views-table cols-5 table'})
        dirty_categories = table.find_all('td', attrs={'class':'views-field views-field-field-article-primary-category'})
        
        clean_categories = []
        
        for i in np.arange(len(dirty_categories)):
            clean_category = dirty_categories[i].text
            clean_categories = np.append(clean_category, clean_categories)
            
        clean_categories_list = list(clean_categories)   
        #index is inverted for some reason
        clean_categories_list.reverse()
    
        return clean_categories_list[0]
        
    except AttributeError or IndexError:
        return 'error'
    

#import dictionary of APIs
dictionary = open('<file path>')

with dictionary as f:
    mylist = list(f)
    
    
def clean_name(index):
    string = mylist[index].split(':')[0].replace("'", '').replace('{', '')
    if len(string) <=4:
        string = string
    elif (string[len(string)-1] =='I' and string[len(string)-2] == 'P' and string[len(string)-3] == 'A'):
        string = string[:-3]
    elif(string[len(string)-1] == 's' and string[len(string)-2] == 'I' and string[len(string)-3] == 'P' and string[len(string)-4] == 'A'):
        string = string[:-4]
        
    return string
        

categories = []

for i in np.arange(len(mylist)):
    api_name = clean_name(i)
    category = api_category(api_name)
    categories = np.append(categories, category)
    
names = []
for i in np.arange(len(mylist)):
    api_name = clean_name(i)
    names = np.append(names, api_name)
    
names = list(names)
categories = list(categories)
    

df = pd.DataFrame({'name':names, 'category': categories})
df = df[df.category != 'error']
