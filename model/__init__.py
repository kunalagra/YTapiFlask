from flask import request,jsonify
import googleapiclient.discovery
from pyrfc3339 import generate
from datetime import datetime
import pymysql,random,pytz,time
from threading import Thread

# Server Connection
conn = pymysql.connect(host = "sql11.freesqldatabase.com",user = "sql11486628", password = "3J4eryW635", db = "sql11486628")
cur = conn.cursor()

# API information
api_service_name = "youtube"
api_version = "v3"

#API KEYs LIST (Constant)
#DKEY holds API Keys in List format
DKEY = ["AIzaSyAYYkNgRxEd_dX8aO7Qiy19jyXv6W22pEU","AIzaSyCuJWUnozckP2JXAqDKfaPyZeOhpg5YWDA","AIzaSyAmA6TFH2zbCo2RZgmRLQ9g1muWqBja1po","AIzaSyBHyCa_gtQos5TZYuuGjHK4Bu2Z_zd8Ddc","AIzaSyAv2jISMaQw4OTsDzefwF9BVG3MavGy73I"]

# Run the task in backgroung Thread every 60 seconds
class worker(Thread):
    def run(self):
        while True:
            #Generate Random Int to select a key
            youtube = googleapiclient.discovery.build(api_service_name, api_version, developerKey = DKEY[random.randint(0,len(DKEY)-1)])

            #YT API Requires Time to be RFC 3339 format
            # Thus using the module to get the time in correct format
            curTime=generate(datetime.utcnow().replace(tzinfo=pytz.utc))

            # Set Requests args for youtube
            request = youtube.search().list(
                part="id,snippet",
                type='video',
                q="india",
                publishedAfter=curTime,
                maxResults=50,
                order="date",
                fields="items(id(videoId),snippet(publishedAt,channelTitle,title,description,thumbnails))",
                
            )
            # sleep for next 60s
            time.sleep(60)
            try:
                response = request.execute()
            #Incase API Key reaches limit, try randomly another
            # Future: Create A copy of list at run time
            # and pop keys not working
            
            except:
                youtube = googleapiclient.discovery.build(api_service_name, api_version, developerKey = DKEY[random.randint(0,len(DKEY)-1)])
                request = youtube.search().list(
                part="id,snippet",
                type='video',
                q="india",
                publishedAfter=curTime,
                maxResults=50,
                order="date",
                fields="items(id(videoId),snippet(publishedAt,channelTitle,title,description,thumbnails))",
                )
                # recreated the request with new API Key
                response = request.execute()
            print(response)
            c=[]
            # iterate over the response and store it in list
            for x in response['items']:
                vId=(x['id']['videoId'])
                pub=(x['snippet']['publishedAt'])
                title=(x['snippet']['title'])
                description=(x['snippet']['description'])
                thumburl=(x['snippet']['thumbnails']['high']['url'])
                channelTitle=(x['snippet']['channelTitle'])
                b = (vId, pub,title, description,thumburl,channelTitle)
                c.append(b)

            #id is auto increment in MySQl
            #inserting the list c in reverse format se we the table is always have values in time ascending format
            cur.executemany("INSERT INTO `ytVid` (`videoId`,`publishedAt`,`title`,`description`,`thumburl`,`channelTitle`) VALUES (%s,%s,%s,%s,%s,%s)",c[::-1])
            conn.commit()
            
# RUn the thread		
def run():
    worker().start()


# API Def for paginating response in Desc Order by Time
# Each Page has 5 Response in List format (
# Future: can be made key-value pair using Dict Zip
def fetchPage():
    page= int(request.args.get('page', default=1))
    # offset defines how many rows to be skipped 
    offset = 5*(page-1)
    #SQL Query
    query = "SELECT `videoId`,`publishedAt`,`title`,`description`,`thumburl`,`channelTitle` FROM `ytVid` ORDER BY id DESC LIMIT 5 OFFSET %s"
    cur.execute(query, offset)
    data = list(cur.fetchall())
    if data==[]:
        return("No Data Found")
    return(jsonify(data))


#Search in title & description fields
def search():
    s= request.args.get('q', default="India")

    #To search for occurence anyhwere in the fields
    s = "%" + s + "%"

    # Base Query
    query = "SELECT `videoId`,`publishedAt`,`title`,`description`,`thumburl`,`channelTitle` FROM `ytVid` WHERE title Like %s or description Like %s"
    cur.execute(query, (s,s))
    data = list(cur.fetchall())
    if data==[]:
        return("No Data Found")
    return(jsonify(data))