import praw, csv
from datetime import datetime
from datetime import date
import pandas as pd

path= 'C:/____' #Where the csv file is saved
now=datetime.now()
today=now.strftime("%b %d %Y")   #Date in Jul 25 2020 format
time=now.strftime("%H:%M:%S")   # to get the time when code is run

reddit = praw.Reddit(client_id='________', # see to get
                     client_secret='____________',
                     username='__________',
                     password='___________',user_agent='bot')

subreddits=['all','popular'] # we are scrapping r/all and r/popular
sr_lst=[]      # this list will collect the subreddits appearing on r/all or r/popular
for sr in subreddits:
    subreddit = reddit.subreddit(sr).hot(limit=40)
    for submission in subreddit:
        k=(submission.permalink.split('/')[2])  #string manipulation will give the exact subreddits from links
        sr_lst.append(k)
#print(sr_lst)
    dct={}   #this dictionary is used to count the number of times a subreddit is appeared in the list sr_lst
    for item in sr_lst:
        if item in dct:
            dct[item]=dct[item]+1
        else:
            dct[item]=1

    lst2=(sorted(dct.items(), key=lambda x: x[1], reverse=True)) #This arranges list in descending order of their appearance
    
    pb_cmnt='The most often repeated subreddits on r/'+sr+ ' at '+time+','+today+ ' are: \n'
    
    for i in lst2: #lst2 contains the subreddits in sorted order, but they also have lot of spl characters like (), etc. This loop will get rid of it
        #print(i) #i2,i3,i4,i5 are just string manipulations and temp variables
        i2=str(i).replace('(','').replace(')','').replace('\'','').replace(',',(' ->'))
        pb_cmnt=pb_cmnt+'\n'+'r/'+i2+'\n'
        #print(pb_cmnt)
        i3=str(i).replace('(','').replace(')','').replace('\'','').replace(',','').split(' ')
        i4,i5=i3[0],i3[1]
        print(i4,i5)   #i4, i5 are the subreddits and their occurence respectively
        
        with open('c:/movers/PRAW Files/TopSubReddits.csv','a', newline='') as file:
           write=csv.writer(file)
           write.writerow([sr,i4,i5,today,time]) #All this data is saved to a csv file
           
#sr=[all,popular'],i4=subreddit mentioned in all or popular(i.e news,politics etc,i5=count
    post='On '+today+', at '+time+', r/'+sr+' was scrapped and the following subreddits appeared on '+sr+' these many times'
    #this is the headline of the post. Chek out r/subredditanalysis2
    text =('The script was run at '+ time +' '+today+
                    '. '+'r/'+sr+' Hot = 100 was used to scrap the data'+
                    '. This is only to check my pythonic skills and not intended for any other purposes')
    m=reddit.subreddit('SubredditAnalysis2').submit(post,selftext=text)
    m.reply(pb_cmnt)  #this is the reply that will be replied to the above post
    
df=pd.read_csv('c:/movers/PRAW Files/TopSubReddits.csv')
##print(df)
df1=df[df['Default']=='popular']
df1=df1.groupby(['SubReddit','Date']).mean()['Counts'].unstack()

df=pd.read_csv('c:/movers/PRAW Files/TopSubReddits.csv')
df2=df[df['Default']=='all']

df2=df2.groupby(['SubReddit','Date']).mean()['Counts'].unstack()
#df1.to_excel(path+'TopSubReddits2EveryDay.xlsx', sheet_name = 'All')

from pandas import ExcelWriter
with ExcelWriter(path+'TopSubRedditsEveryDay.xlsx') as writer:
    df1.to_excel(writer, sheet_name='Popular')
    df2.to_excel(writer, sheet_name='All')
