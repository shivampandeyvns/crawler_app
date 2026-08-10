from datetime import datetime

history=[]

def add(query):

    history.append({

        "time":datetime.now(),

        "query":query

    })

def get():

    return history[::-1]