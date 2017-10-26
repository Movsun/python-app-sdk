import os
from ttnmqtt.ttnmqtt import MQTTClient as mqtt

def test_connection():
    ttn_client = mqtt('appid','appeui','psw')
    ttn_client.startBackground()
    try:
        ttn_client.connect(os.getenv("MQTT_HOST", "localhost"), os.getenv("MQTT_PORT", 1883))
    except:
        print("Error connecting")
    assert ttn_client.connectFlag == 1

def test_disconnection():
    ttn_client = mqtt('appid','appeui','psw')
    ttn_client.connect(os.getenv("MQTT_HOST", "localhost"), os.getenv("MQTT_PORT", 1883))
    ttn_client.disconnect()
    assert ttn_client.disconnectFlag == 1

def test_set_message():
    ttn_client1 = mqtt('appid','appeui','psw')
    ttn_client2 = mqtt('appid','appeui','psw')

    def on_connect(client, userdata, flags, rc):
        client.subscribe("appid/devices/devid/down")
    def on_message(client, userdata, msg):
        client.disconnect()
        assert msg.payload.decode() == "Hello world!"
    ttn_client1.setConnectBehavior(on_connect)
    ttn_client1.setMessageBehavior(on_message)
    ttn_client2.setConnectBehavior(on_connect)
    ttn_client2.setMessageBehavior(on_message)
    ttn_client1.connect(os.getenv("MQTT_HOST", "localhost"), os.getenv("MQTT_PORT", 1883))
    ttn_client2.connect(os.getenv("MQTT_HOST", "localhost"), os.getenv("MQTT_PORT", 1883))
    ttn_client1.publish('devid', "Hello world!")
    ttn_client2.publish('devid', "Hello world!")

#def test_background_loop():
#    ttn_client = mqtt('appid','appeui','psw')
#    ttn_client.connect(os.getenv("MQTT_HOST", "localhost"), os.getenv("MQTT_PORT", 1883))
#    ttn_client.startBackground()
#    ttn_client.stopBackground()
#    assert ttn_client.disconnectFlag == 1

#def test_set_publish():
#    ttn_client = mqtt('appid','appeui','psw')
#    def on_publish(client, userdata, mid):
#        print('MSG PUBLISHED', mid)
#        ttn_client.midCounter = mid
#    ttn_client.setPublishBehavior(on_publish)
#    ttn_client.connect(os.getenv("MQTT_HOST", "localhost"), os.getenv("MQTT_PORT", 1883))
#    ttn_client.publish('devid', "Hello world!")
#    assert ttn_client.midCounter == 1

def test_set_globalbehaviors():
    ttn_client = mqtt('appid','appeui','psw')
    def on_connect(client, userdata, flags, rc):
        client.subscribe("appid/devices/devid/down")
    def on_message(client, userdata, msg):
        print(msg.payload.decode())
        assert msg.payload.decode() == "Hello world!"
    def on_publish(client, userdata, mid):
        print('MSG PUBLISHED', mid)

    ttn_client.setGlobalBehavior(on_connect, on_message, on_publish)
    ttn_client.connect(os.getenv("MQTT_HOST", "localhost"), os.getenv("MQTT_PORT", 1883))
    ttn_client.publish('devid', "Hello world!")

def test_set_behaviors():
    ttn_client = mqtt('appid','appeui','psw')
    def on_connect(client, userdata, flags, rc):
        client.subscribe("appid/devices/devid/down")
    def on_message(client, userdata, msg):
        print(msg.payload.decode())
        assert msg.payload.decode() == "Hello world!"
    def on_publish(client, userdata, mid):
        print('MSG PUBLISHED', mid)

    ttn_client.setConnectBehavior(on_connect)
    ttn_client.setMessageBehavior(on_message)
    ttn_client.setPublishBehavior(on_publish)
    ttn_client.connect(os.getenv("MQTT_HOST", "localhost"), os.getenv("MQTT_PORT", 1883))
    ttn_client.publish('devid', "Hello world!")

def test_first_set_message_handler():
    ttn_client1 = mqtt('appid','appeui','psw')
    ttn_client2 = mqtt('appid','appeui','psw')

    ttn_client1.connect(os.getenv("MQTT_HOST", "localhost"), os.getenv("MQTT_PORT", 1883))

    def on_connect(client, userdata, flags, rc):
        client.subscribe("appid/devices/devid/down")
    ttn_client1.setConnectBehavior(on_connect)
    ttn_client2.setConnectBehavior(on_connect)
    ttn_client2.connect(os.getenv("MQTT_HOST", "localhost"), os.getenv("MQTT_PORT", 1883))

    def handler():
        print("using message handler for client 1")

    ttn_client1.setMessageHandler(handler)
    ttn_client2.startBackground()
    ttn_client1.publish('devid', '{"port": 1, "confirmed": false, "payload_raw": "AQ=="}')
    ttn_client2.publish('devid', '{"port": 1, "confirmed": false, "payload_raw": "AQ=="}')
    assert ttn_client1.getLastMessage() != '{}'

def test_second_set_message_handler():
    ttn_client1 = mqtt('appid','appeui','psw')
    ttn_client2 = mqtt('appid','appeui','psw')

    def on_connect(client, userdata, flags, rc):
        client.subscribe("appid/devices/devid/down")

    ttn_client1.setConnectBehavior(on_connect)
    ttn_client2.setConnectBehavior(on_connect)
    ttn_client1.connect(os.getenv("MQTT_HOST", "localhost"), os.getenv("MQTT_PORT", 1883))
    ttn_client2.connect(os.getenv("MQTT_HOST", "localhost"), os.getenv("MQTT_PORT", 1883))

    def handler1():
        print("using message handler1")
    def handler2():
        print("using message handler2")

    ttn_client1.setMessageHandler(handler1)
    ttn_client2.startBackground()
    ttn_client1.setMessageHandler(handler2)
    ttn_client1.publish('devid', '{"port": 1, "confirmed": false, "payload_raw": "AQ=="}')
    ttn_client2.publish('devid', '{"port": 1, "confirmed": false, "payload_raw": "AQ=="}')
    ttn_client2.stopBackground()
    assert ttn_client1._MQTTClient__messageHandler == handler2

def test_connect_error():
    ttn_client = mqtt('appid', 'appeui', 'psw')
    ttn_client.startBackground()
    try:
        ttn_client.connect(os.getenv("MQTT_HOST", "localhost"), os.getenv("MQTT_PORT", 8883))
    except:
        ttn_client.stopBackground()
        assert ttn_client.connectFlag == 0
