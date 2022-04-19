# Youtube Search App

A Flask backend to Query Youtube using its API v3 to fetch videos related to a query.

The server search for new videos every 60s and stores VideoID, (we can append https://www.youtube.com/watch?v= to make it video url), Title, Description, Publish Date (RFC 3339), channel name & thumburl.

## Requirements

- Python 3.10+
- To Install all required Libs run:
  pip install google-api-python-client flask pymysql pyrfc3339

## Testing API

- Git Clone/Download the folder
- Launch a terminal/cmd inside the folder (Windows: type cmd in Address Bar and hit enter inside the folder)
- Enter python app.py
- Send a GET Request to http://127.0.0.1:5000/ (Postman, Thunder Client, browser will do)
- Paginated Result: Send GET Request to http://127.0.0.1:5000/latestVids?page=n where n in any page number
- Search: Send GET Request to http://127.0.0.1:5000/searchDB?q=QUERY where QUERY is any string on which we want to search
