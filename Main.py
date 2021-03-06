# In The Name Of God
# Creation Date : 7/25/17
# Created By : maryam ebrahimzadeh(maryam.ebrahimzadeh1997@yahoo.com)
#              monireh safari(monirehsafari18@gmail.com)
import time
import json
import paho.mqtt.client as mqtt
from flask import Flask,request
from pymongo import MongoClient


publishTime = 0
requestId = -1

client = mqtt.Client("C1")#create a client
broker_address="" #use external broker
client.connect(broker_address) #connect to broker

mongoclient = MongoClient()
db = mongoclient.database

def on_message(client, userdata, message):
    print ("message received " + str(message.payload))
    print("topic " + str(message.topic))

    receivedMessage = json.dumps(message.payload)
    finalReceivedMessage = json.loads(receivedMessage)


    responseTime = time.time()
    timeout = publishTime - responseTime

    if timeout > 0.010 or finalReceivedMessage['id'] != requestId:
        print('no response')
        # no response
        #json format of next layer   :  json request + is done : true / false

    else :
        print('is Done')
        # response is Done


    #we dont know what we get in this message :D

def on_log(client, userdata, level, buf):
    print("log: ",buf)



client.on_message=on_message        #attach function to callback
client.on_log = on_log


client.loop_start()    #start the loop when we should finish it ?

client.subscribe("set")


app = Flask(name)
@app.route('/', methods=['PUT'])
def getMessage():
    if request.headers['Content-Type'] == 'application/json':
        jsonfile =  request.json()
        newjson = json.dumps(jsonfile)
        finaljson = json.loads(newjson)

        global requestId
        requestId = requestId + 1
        finaljson['id'] = requestId
        client.publish("set",finaljson)
        global publishTime
        publishTime = time.time()


if name == "main":
    app.run(host='0.0.0.0')

