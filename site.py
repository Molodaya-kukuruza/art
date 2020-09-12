import requests 
from bs4 import BeautifulSoup 
  
def news(): 
    # the target we want to open     
    url='https://horo.mail.ru/prediction/virgo/today/'
      
    #open with GET method 
    resp=requests.get(url) 
      
    #http_respone 200 means OK status 
    if resp.status_code==200: 
      
        # we need a parser,Python built-in HTML parser is enough . 
        soup=BeautifulSoup(resp.text,'html.parser')     
  
        # l is the list which contains all the text i.e news  S
        l=soup.find("div",{"class":"article__item article__item_alignment_left article__item_html"}) 
      
        #now we want to print only the text part of the anchor. 
        #find all the elements of a, i.e anchor 
        for note in l:
            print (str(note)[3:-4])
    else: 
        print("Error") 
          
news()