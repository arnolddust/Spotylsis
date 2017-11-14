from pymongo import MongoClient
from bokeh.charts import Bar, show, output_file
from bokeh.plotting import figure, output_file,show
import pandas as pd
import pprint

def extractData():
    dates = []
    artist = []

    client = MongoClient()
    db = client.SpotifyDB
    genreCollection = db['TopGenres']
    trackCollection = db['TopTracks']

    for document in genreCollection.find():
        if not dates: #Check if dates list is empty
            dates.append(document['date'])
        elif dates[len(dates)-1] != document['date']: #Append date if not matching previous entry
            dates.append(document['date'])

    genreList = [ #Create a list based on the amount of days of data collected
        [] for i in range(len(dates))
    ]
    pprint.pprint(dates)
    for day in dates: #Appends all genres to a list separated by day
        index = dates.index(day)

        for document in genreCollection.find({"date":day}):
            genreList[index].append(document['genre'])

    print("genre list" + str(len(genreList[2])))
    genreCount = [ #Create a list based on the amount of days of data collected
        [] for i in range(len(dates))
    ]
    for days in genreList:
        index = genreList.index(days)
        print("DAYS" + str(len(days)))
        for genre in days:

            genreCount[index].append(days.count(genre))

        print(genreCount[index])
    data = {
        #'Date' : dates,
        'interpreter' : genreList[7],
        'Count' : genreCount[7]
    }


    """
    df = pd.DataFrame(data)
    #df['Date'] = pd.to_datetime(df['Date'])

    #bar = Bar(data,values = 'Count', lavel = 'Date', group = 'interpreter',
           #   title = 'Trend in Genres by Day',
           #   legend = 'top-left', plot_width = 500, xlabel = 'Date', ylabel= 'Count')


    #bar = Bar(df,'interpreter', values = 'Count', title = "TEST", plot_width = 1500, legend = False)

    output_file('Grouped_Bar.html')
    #show(bar)
    """


    for length in range(len(genreList)-1):
        print("INDEX = " + str(length))

        data = {
            # 'Date' : dates,
            'interpreter': genreList[length],
            'Count': genreCount[length]
        }
        print(" LIST" + str(len(genreList[length])))
        print(" COUNT" + str(len(genreCount[length])))

        if (len(genreList[length]) != len(genreCount[length])):
            print("####MISMATCHED INDEXES CHECK DATABASE####")
            continue

        df = pd.DataFrame(data)
        # df['Date'] = pd.to_datetime(df['Date'])

        #bar = Bar(data,values = 'Count', lavel = 'Date', group = 'interpreter',
         #  title = 'Trend in Genres by Day',
          # legend = 'top-left', plot_width = 500, xlabel = 'Date', ylabel= 'Count')


        bar = Bar(df, 'interpreter', values='Count', title="TEST", plot_width=1500, legend=False)

        output_file('Grouped_Bar.html')
        show(bar)






extractData()