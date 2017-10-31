import os
import time
import json
from ttnmqtt.ttnmqtt import MQTTClient as mqtt


def test_connection():
    ttn_client = mqtt('appid', 'psw')
    ttn_client.start()
    try:
        ttn_client.connect(
            os.getenv("MQTT_HOST", "localhost"),
            os.getenv("MQTT_PORT", 1883))
    except:
        print("Error connecting")
    assert ttn_client.connectFlag == 1


def test_connect_callback():
    ttn_client = mqtt('appid', 'psw')

    def connectcallback(rc, client):
        if(rc == 0):
            print("connected")
        else:
            print("not connected")
        assert client.connectFlag == 1
    ttn_client.setConnectCallback(connectcallback)
    ttn_client.start()
    try:
        ttn_client.connect(
            os.getenv("MQTT_HOST", "localhost"),
            os.getenv("MQTT_PORT", 1883))
    except:
        print("Error connecting")


def test_disconnection():
    ttn_client = mqtt('appid', 'psw')
    ttn_client.connect(
        os.getenv("MQTT_HOST", "localhost"),
        os.getenv("MQTT_PORT", 1883))
    ttn_client.close()
    assert ttn_client.disconnectFlag == 1


def test_close_callback():
    ttn_client = mqtt('appid', 'psw')
    ttn_client.connect(
        os.getenv("MQTT_HOST", "localhost"),
        os.getenv("MQTT_PORT", 1883))

    def closecallback(rc, client):
        print("closing connection")
        assert client.disconnectFlag == 1
    ttn_client.setCloseCallback(closecallback)
    ttn_client.close()


def test_connect_behavior():
    ttn_client1 = mqtt('appid', 'psw')
    ttn_client2 = mqtt('appid', 'psw')

    def on_connect(client, userdata, flags, rc):
        client.subscribe("appid/devices/devid/down")

    def msgcallback(msg, client):
        print(msg)
        msgReceived = msg['payload_raw']
        assert msgReceived == "AQ=="
        client.stop()

    ttn_client1.setConnectBehavior(on_connect)
    ttn_client2.setConnectBehavior(on_connect)
    ttn_client2.setUplinkCallback(msgcallback)
    ttn_client1.connect(
        os.getenv("MQTT_HOST", "localhost"),
        os.getenv("MQTT_PORT", 1883))
    ttn_client2.connect(
        os.getenv("MQTT_HOST", "localhost"),
        os.getenv("MQTT_PORT", 1883))
    ttn_client2.start()
    ttn_client1.publish(
        'devid',
        '{"port": 1, "confirmed": "false", "payload_raw": "AQ=="}')
    ttn_client2.publish(
        'devid',
        '{"port": 1, "confirmed": "false", "payload_raw": "AQ=="}')


def test_downlink_field_msg():
    ttn_client1 = mqtt('appid', 'psw')
    ttn_client2 = mqtt('appid', 'psw')

    def on_connect(client, userdata, flags, rc):
        client.subscribe("appid/devices/devid/down")

    def msgcallback(msg, client):
        print(msg)
        msgReceived = msg.payload_raw
        assert msgReceived == "AQ=="
        client.stop()

    ttn_client1.setConnectBehavior(on_connect)
    ttn_client2.setConnectBehavior(on_connect)
    ttn_client2.setUplinkCallback(msgcallback)
    ttn_client1.connect(
        os.getenv("MQTT_HOST", "localhost"),
        os.getenv("MQTT_PORT", 1883))
    ttn_client2.connect(
        os.getenv("MQTT_HOST", "localhost"),
        os.getenv("MQTT_PORT", 1883))
    ttn_client2.start()
    ttn_client1.publish(
        'devid',
        {"port": 1, "payload_raw": "AQ=="})
    ttn_client2.publish(
        'devid',
        {"port": 1, "payload_raw": "AQ=="})


def test_message_callback():
    ttn_client1 = mqtt('appid', 'psw')
    ttn_client2 = mqtt('appid', 'psw')

    ttn_client1.connect(
        os.getenv("MQTT_HOST", "localhost"),
        os.getenv("MQTT_PORT", 1883))

    def on_connect(client, userdata, flags, rc):
        client.subscribe("appid/devices/devid/down")

    ttn_client1.setConnectBehavior(on_connect)
    ttn_client2.setConnectBehavior(on_connect)
    ttn_client2.connect(
        os.getenv("MQTT_HOST", "localhost"),
        os.getenv("MQTT_PORT", 1883))

    def msgcallback(msg, client):
        print(msg)
        assert msg == '{"port": 1, "confirmed": false, "payload_raw": "AQ=="}'
        client.stop()

    ttn_client2.setUplinkCallback(msgcallback)
    ttn_client2.start()
    ttn_client1.publish(
        'devid',
        '{"port": 1, "confirmed": false, "payload_raw": "AQ=="}')
    ttn_client2.publish(
        'devid',
        '{"port": 1, "confirmed": false, "payload_raw": "AQ=="}')


def test_publish_callback():
    ttn_client1 = mqtt('appid', 'psw')

    ttn_client1.connect(
        os.getenv("MQTT_HOST", "localhost"),
        os.getenv("MQTT_PORT", 1883))

    def on_connect(client, userdata, flags, rc):
        client.subscribe("appid/devices/devid/down")

    ttn_client1.setConnectBehavior(on_connect)

    def publishcallback(mid, client):
        print(mid)
        assert mid == 1
        client.stop()

    ttn_client1.setDownlinkCallback(publishcallback)
    ttn_client1.start()
    ttn_client1.publish(
        'devid',
        '{"port": 1, "confirmed": false, "payload_raw": "AQ=="}')


def test_connect_error():
    ttn_client = mqtt('appid', 'psw')
    ttn_client.start()
    try:
        ttn_client.connect(
            os.getenv("MQTT_HOST", "localhost"),
            os.getenv("MQTT_PORT", 8883))
    except:
        ttn_client.stop()
    assert ttn_client.connectFlag == 0
