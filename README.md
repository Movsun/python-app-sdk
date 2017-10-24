# The Things Network Python SDK

[![Build Status](https://travis-ci.org/TheThingsNetwork/python-app-sdk.svg?branch=master)](https://travis-ci.org/TheThingsNetwork/python-app-sdk)

![The Things Network](https://thethings.blob.core.windows.net/ttn/logo.svg)

## Usage

This package provides you an easy way to connect to The Things Network via MQTT. Take note that, you'll first need to create an application with a device to run the constructor of the MQTT client because you need to provide, an applicationID and a deviceID.
First include the package in your file like this:
```python
from ttnmqtt import MQTTClient as mqtt
```

### Constructor

The class constructor can be called following this scheme:
```python
mqtt(APPID, APPEUI, PSW)
```
All the following informations can be found in your The Things Network console.
*APPID*: this the name you gave your application when you created it.
*APPEUI*: this the unique identifier of your application on the TTN platform.
*PSW*: it can be found at the bottom of your application page under **ACCESS KEYS**.

The constructor returns an MQTTClient object set up with your application informations, ready for connection.

### Connection

Once you created your client, you need to connect it to the The Things Network MQTT broker.
```python
client.connect(address, port)
```
*client* is the client object you previously created. We simply call the connect() method on it which by default connect you to **eu.thethings.network** via **1883** port.
If you wish to connect with another configuration, you need to provide the address of the broker and the port to be used for connection.

### Start and Stop loops

Our client is now connected to the broker but we need to set a loop for it to keep listenning for potential incomming messages (take note that **we don't need to start a loop** if we simply want to send downlink messages).

Two different options are possible:
* The loop is your main process:
In that case you need to start the loop like this:
```python
client.start()
```
Please take note that you wont be able to run any other process at the same time and other functions will be executed once the loop is stopped with:
```python
client.disconnect()
```
* The loop needs to be run as a background process:
In that case start looping with the following method:
```python
client.startBackground()
```
This way you will be able to run another process (such as the web server for example) at the same time.
Stop the loop with this method:
```python
client.stopBackground()
```
This method will also disconnect your client.

### Access messages

Now that our client is connected and looping, we will be able to receive uplink messages. On each message reception, you should see **MESSAGE RECEIVED** in the console.
Our object/client has one method that you can call to access the message:
```python
# returns the last message received
client.getLastMessage()
```

### Publish
If you wish to publish a message to the device you passed in argument while creating the client you can do so, using the following method:
```python
client.publish(deviceID, message)
```
You need to provide the ID of the device which will receive the message (it can be found on the device page of your application in the TTN console). 
The message that you send to the TTN broker needs to be a string and can follow this example (it's not mandatory but they are mostly build on this format):
 ```json
 {"port": 1, "confirmed": false, "payload_raw": "AA=="}
 ```
 This message will send the payload 00 to your device.

### Set custom behaviors

While calling the connect method, default behaviors are set for the following events triggering our client: connection, receiving messages, publishing messages and disconnection. However if you wish to redefine them, you can do so, by calling the following methods:
```python
client.setConnectBehavior(custom_function)
client.setMessageBehavior(custom_function)
client.setPublishBehavior(custom_function)
client.setGlobalBehavior(custom_connect, custom_message, custom_publish)
```
The custom functions need to be defined in your project and accessible from where you are setting the behaviors. They also need to follow the paho-mqtt standart which is the following:
```python
custom_message(client, userdata, message)
custom_connect(client, userdata, falgs, rc)
custom_publish(client, userdata, mid)
```
for more information over paho-mqtt package go to: https://pypi.python.org/pypi/paho-mqtt/1.3.0

### Set a message handler

If you simply wish to execute a few instructions when receiving a message, such as a data treament or store the message that you received in a file or in a database, it's much advised to set a message handler instead of redefining the message behavior of the client.
Where you create the client, define a procedure without arguments (this is very important that your procedure doesn't take any arguments) in which you will put the instructions to be executed when you receive a new message. Then call the following method:
```python
def customHandler():
  print('My personnal handler!')

client.setMessageHandler(customHandler)
```
Everytime you receive a new message, the customHandler() function will be executed and no need to worry about the paho-mqtt syntax.


## License

Source code for The Things Network is released under the MIT License, which can be found in the [LICENSE](LICENSE) file. A list of authors can be found in the [AUTHORS](AUTHORS) file.
