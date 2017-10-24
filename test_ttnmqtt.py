from ttnmqtt.ttnmqtt import MQTTClient as mqtt

def test_connection():
    ttn_client = mqtt('appid','appeui','psw')
    ttn_client.connect("localhost", 1883)
    assert ttn_client.connectFlag == 1

def test_disconnection():
    ttn_client = mqtt('appid','appeui','psw')
    ttn_client.connect("localhost", 1883)
    ttn_client.disconnect()
    assert ttn_client.disconectFlag == 1

def test_message():
    ttn_client = mqtt('appid','appeui','psw')
    def on_connect(client, userdata, flags, rc):
        client.subscribe("appid/devices/devid/down")
    def on_message(client, userdata, msg):
        client.disconnect()
        assert msg.payload.decode() == "Hello world!"
    ttn_client.setConnectBehavior(on_connect)
    ttn_client.setMessageBehavior(on_message)
    ttn_client.connect('localhost')
    ttn_client.publish('devid', "Hello world!")
