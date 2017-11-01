# The Things Network Python SDK

[![Build Status](https://travis-ci.org/TheThingsNetwork/python-app-sdk.svg?branch=master)](https://travis-ci.org/TheThingsNetwork/python-app-sdk)

![The Things Network](https://thethings.blob.core.windows.net/ttn/logo.svg)

## Table of Contents
* [Description](#description)
* [MQTTClient](#mqttclient)
* [connect](#connect)
* [close](#close)
* [startForever](#startforever)
* [start](#start)
* [stop](#stop)
* [setUplinkCallback](#setuplinkcallback)
  * [uplinkCallback](#uplinkcallback)
* [setConnectCallback](#setconnectcallback)
  * [connectCallback](#connectcallback)
* [setConnectBehavior](#setconnectbehavior)
* [setDownlinkCallback](#setpublishcallback)
  * [downlinkCallback](#publishcallback)
* [setCloseCallback](#setclosecallback)
  * [closeCallback](#closecallback)
* [send](#send)
* [License](#license)

## Description

This package provides you an easy way to connect to The Things Network via MQTT. Take note that, you'll first need to create an application with a device to run the constructor of the MQTT client because you need to provide, an applicationID and a deviceID.
First include the package in your file like this:
```python
from ttnmqtt import MQTTClient as mqtt
```

### MQTTClient

The class constructor can be called following this scheme:
```python
mqtt(appID, appAccessKey)
```
- `appID`: this the name you gave your application when you created it.
- `appAccessKey`: it can be found at the bottom of your application page under **ACCESS KEYS**.
All the above informations can be found in your The Things Network console.
The constructor returns an MQTTClient object set up with your application informations, ready for connection.

### connect
Connects the previously created client to the The Things Network MQTT broker by default.
```python
client.connect([address], [port])
```
- `address`: the address of the MQTT broker you wish to connect to. Default to `eu.thethings.network`
- `port`: the port on which you wish to connect. Default to `1883`

### close
Disconnects the MQTT client from which we call the method. Also able to stop a forever loop in case the client was running on a loop launched by the `startForever()` method.
```python
client.close()
```
### startForever
Start a loop as the main loop of your process. You wont be able to run anything else at the same time on this script.
```python
client.startForever()
```
Take note that a loop need to be started in order to receive uplink messages.

### start
Starts a loop for the client in the background so that it's possible to run another process (such as a web server) in the same script.
```python
client.start()
```
### stop
Stops a loop which was started with the `start()` method. It also disconnect the client.
```python
client.stop()
```
### setUplinkCallback
Set the callback function, to be called when an uplink message is received.
```python
client.setUplinkCallback(uplinkCallback)
```
#### uplinkCallback
The callback function must be declared in your script following this structure:
* `uplinkCallback(msg, client)`
  * `msg`: the message received by the client
  * `client`: the client from which the callback is executed are calling

On each message reception, you should see **MESSAGE RECEIVED** in the console, and the callback will be executed.

### setConnectBehavior
Change the connect callback function, following the paho-mqtt standart.
```python
client.setConnectBehavior(custom_function)
```
- `custom_function(client, userdata, flags, rc)`: the function which will be the new connection behavior for our MQTT client.
  - `client`: the MQTT client from which we call the callback.
  - `userdata`: the data of the user. Default to `''`
  - `flags`: connection flags
  - `rc`: result from the connect method. `0` if the connection succeeded.

click [here](https://pypi.python.org/pypi/paho-mqtt/1.3.0) for more information on the paho-mqtt package.

### setConnectCallback
Set the connection callback function to be executed when the client connect to the broker.
```python
client.setConnectCallback(connectCallback)
```
#### connectCallback
- `connectCallback(res, client)`: the function which will be executed on connection to the broker.
  - `res`: the result of the connection. If it's 0, it went well. If not, it means the connection failed.
  - `client`: the TTN client from which we call the callback.

### setDownlinkCallback
Set the downlink callback function, with actions to execute when a downlink message is sent.
```python
client.setDownlinkCallback(downlinkCallback)
```
#### downlinkCallback
- `downlinkCallback(mid, client)`: the function which will be the new publish behavior for our MQTT client.
  - `mid`: it matches the mid variable returned from the publish call to allow sent messages to be tracked.
  - `client`: the TTN client from which we call the callback.

### setCloseCallback
Set the callback to be executed when the connection to the TTN broker is closed.
```python
client.setCloseCallback(closeCallback)
```
#### closeCallback
- `closeCallback(res, client)`: the function which will be executed when the connection is closed.
  - `res`: the result of the disconnection. If it's 0, it went well. If not, it means the disconnection was unexpected.
  - `client`: the TTN client from which we call the callback.

### send
Publishes a message to the MQTT broker.
```python
client.send(deviceID, message)
```
- `deviceID`: the ID of the device you wish to send the message to.
- `message`: the message to be published to the broker. The message that's sent to the TTN broker needs to be a string and can follow this example (it's not mandatory but they are mostly build on this format):
 ```json
 {"port": 1, "confirmed": false, "payload_raw": "AA=="}
 ```
 This message will send the payload 00 to your device.

## License

Source code for The Things Network is released under the MIT License, which can be found in the [LICENSE](LICENSE) file. A list of authors can be found in the [AUTHORS](AUTHORS) file.
