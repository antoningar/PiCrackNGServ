#!/usr/bin/env python
#-*- coding: utf8 -*-

from flask import Flask
import mysql.connector
import json
import jsonpickle

app = Flask(__name__)

data_add_spot = """ {
    "LatLng":{
        "latitude":46,
        "longitude":-2
    },
    "description":"Jsndndj",
    "id":0,
    "name":"Zjdjd",
    "user":"nepal",
    "type":"Grue"
}
"""

data_update_spot = """ {
    "description":"Bah tiens",
    "id":10,
    "name":"Allal",
    "user":"siloob",
    "type":"Chantier"
}
"""

data_add_vote = """ {
    "username" : "nepal",
    "value" : 1,
    "spot": 10
} """

data_add_comment = """ {
    "username" : "nepal",
    "comment" : "bah super",
    "spot": 10
} """


data_delete_spot = """ {
    "id" : 9
} """

data_delete_vote = """ {
    "id" : 12
} """

data_delete_comment = """ {
    "id" : 8
} """

config = {
  'user': 'root',
  'host': '127.0.0.1',
  'database': 'explodb',
  'raise_on_warnings': True,
  'use_unicode': True,
  'charset' : "utf8"
}

#Get all spots
@app.route('/api/spots/')
def getAllSpots():
    cnx = mysql.connector.connect(**config)
    cursor = cnx.cursor()
    query = ("SELECT * from SPOT")
    cursor.execute(query)

    row_headers=[x[0] for x in cursor.description] #this will extract row headers
    rv = cursor.fetchall()
    json_data=[]
    for result in rv:
        json_data.append(dict(zip(row_headers,result)))
    return json.dumps(json_data, indent=4, sort_keys=True, default=str)

#Add new spot
@app.route('/api/spot/')
def addNewSpot(json_data):
    cnx = mysql.connector.connect(**config)
    cursor = cnx.cursor()

    json_data = json.loads(json_data)
    #Add coordinates
    coordinates_id = addNewCoordinate(cursor,json_data['LatLng'])
    #Search type id
    type_id = getIdType(cursor,json_data['type'])

    spot_id = -1
    if type_id != -1:
        #Add spot
        spot_id = addSpot(cursor, json_data, coordinates_id, type_id)
    
    cnx.commit()
    cursor.close()

    return spot_id

#Add new vote
@app.route('/api/vote')
def addNewVote(json_data):
    cnx = mysql.connector.connect(**config)
    cursor = cnx.cursor()
    json_data = json.loads(json_data)

    datas = (
        json_data['username'],
        json_data['value'],
        json_data['spot']
    )

    rq = (
        "INSERT INTO VOTE (user, value, spot) "
        "VALUES (%s,%s,%s)"
    )

    cursor.execute(rq,datas)
    cnx.commit()
    cursor.close()

    return cursor.lastrowid

#Add new comment
@app.route('/api/comment')
def addNewComment(json_data):
    cnx = mysql.connector.connect(**config)
    cursor = cnx.cursor()
    json_data = json.loads(json_data)

    datas = (
        json_data['username'],
        json_data['comment'],
        json_data['spot']
    )

    rq = (
        "INSERT INTO COMMENT (user, comment, spot) "
        "VALUES (%s,%s,%s)"
    )

    cursor.execute(rq,datas)
    cnx.commit()
    cursor.close()

    return cursor.lastrowid

#Delete a spot
@app.route('/api/delete/spot')
def deleteSpotBydId(json_data):
    cnx = mysql.connector.connect(**config)
    cursor = cnx.cursor()
    json_data = json.loads(json_data)

    #Delete vote linked to this spot
    rq = "DELETE FROM VOTE WHERE spot = %(id)s"
    cursor.execute(rq,{'id':id})

    #Delete comment linked to this spot
    rq = "DELETE FROM COMMENT WHERE spot = %(id)s"
    cursor.execute(rq,{'id':id})
    
    #Delete spot
    rq = "DELETE FROM SPOT WHERE ID = %(id)s"
    cursor.execute(rq,{'id':json_data['id']})
    
    cnx.commit()
    cursor.close()

    return cursor.lastrowid

#Delete a comment
@app.route('/api/delete/comment')
def deleteCommentById(json_data):
    cnx = mysql.connector.connect(**config)
    cursor = cnx.cursor()
    json_data = json.loads(json_data)

    rq = "DELETE FROM COMMENT WHERE id = %(id)s"
    cursor.execute(rq,{'id':json_data['id']})

    cnx.commit()
    cursor.close()

    return cursor.lastrowid

#Delete a vote
@app.route('/api/delete/vote')
def deleteVoteById(json_data):
    cnx = mysql.connector.connect(**config)
    cursor = cnx.cursor()
    json_data = json.loads(json_data)

    rq = "DELETE FROM VOTE WHERE id = %(id)s"
    cursor.execute(rq,{'id':json_data['id']})

    cnx.commit()
    cursor.close()

    return cursor.lastrowid

#Update spot
@app.route('/api/update/spot')
def updateSpot(json_data):
    cnx = mysql.connector.connect(**config)
    cursor = cnx.cursor()
    json_data = json.loads(json_data)

    #Search type id
    type_id = getIdType(cursor,json_data['type'])

    data =(
        json_data['name'],
        type_id,
        json_data['user'],
        json_data['description'],
        json_data['id']
    )

    rq = "UPDATE SPOT SET name = %s, type= %s, user= %s, description= %s WHERE id= %s"
    
    cursor.execute(rq,data)
    cnx.commit()
    cursor.close()
    
    return cursor.lastrowid


def addSpot(cursor, json_data, coordinates_id, type_id):
    data = (
        json_data['name'],
        coordinates_id,
        type_id,
        json_data['description'],
        json_data['user']
    )

    rq = (
        "INSERT INTO SPOT (name,coordinates,type, description, user)"
        "VALUES (%s,%s,%s,%s,%s)"
    )

    cursor.execute(rq, data)
    return cursor.lastrowid

def addNewCoordinate(cursor,coordinate):
    data =(coordinate['latitude'],coordinate['longitude'])
    rq = (
        "INSERT INTO COORDINATE (latitude, longitude)" 
        "VALUES (%s,%s)"
    )
    cursor.execute(rq,data)
    return cursor.lastrowid

def getIdType(cursor,type_name):
    rq = " SELECT id FROM TYPE WHERE name = %(name)s "
    cursor.execute(rq,{'name': type_name})
    result = cursor.fetchall()
    return result[0][0]

if __name__ == "__main__":
    #addNewSpot(data_add_spot)
    #addNewVote(data_add_vote)
    #addNewComment(data_add_comment)

    #deleteSpotById(data_delete_spot)
    
    #deleteVoteById(data_delete_vote)
    #deleteCommentById(data_delete_comment)

    updateSpot(data_update_spot)
