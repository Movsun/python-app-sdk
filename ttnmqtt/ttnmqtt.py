import paho.mqtt.client as mqtt
from events import Events
import base64
from collections import namedtuple
import json


def _json_object_hook(d): return namedtuple('MSG', d.keys())(*d.values())


def json2obj(data): return json.loads(data, object_hook=_json_object_hook)


class DownlinkMessage:
    def __init__(self, port, conf=False, sched=None, praw=None, pfields=None):

        self.port = port
        if praw:
            self.praw = praw
        if pfields:
            self.pfields = pfields
        if conf:
            self.confirmed = conf
        if sched:
            self.schedule = sched

    def obj2json(self):
        json_msg = json.dumps(self.__dict__)
        return str(json_msg)


class MyEvents(Events):
    __events__ = ("uplink_msg", "downlink_msg", "connect", "close")


class MQTTClient:

    def __init__(self, appID, appAccessKey):
        self.__client = mqtt.Client()
        self.__APPID = appID
        self.__APPACCESSKEY = appAccessKey
        self.__events = MyEvents()
        self.connectFlag = 1
        self.disconnectFlag = 0
        self.midCounter = 0

    def connect(self, address='eu.thethings.network', port=1883):
        if self.__client.on_connect is None:
            self.__client.on_connect = self._onConnect()
        self.__client.on_publish = self._onDownlink()
        self.__client.on_message = self._onMessage()
        self.__client.on_disconnect = self._onClose()

        self.__client.username_pw_set(self.__APPID, self.__APPACCESSKEY)
        self.__client.connect(address, port, 5000)

    def _onConnect(self):
        def on_connect(client, userdata, flags, rc):
            if(rc == 0):
                print('CONNECTED AND SUBSCRIBED')
                client.subscribe(self.__APPID+'/devices/+/up')
                self.connectFlag = 1
            else:
                print('ERROR CONNECTING')
                self.connectFlag = 0
            if self.__events.connect:
                self.__events.connect(rc, client=self)
        return on_connect

    def _onClose(self):
        def on_close(client, userdata, rc):
            if rc != 0:
                print('UNEXPECTED DISCONNECTION')
                self.disconnectFlag = 0
            else:
                self.disconnectFlag = 1
                print('DISCONNECTED')
            if self.__events.close:
                self.__events.close(rc, client=self)
        return on_close

    def _onMessage(self):
        def on_message(client, userdata, msg):
            print('MESSAGE RECEIVED')
            j_msg = str(json.dumps(json.loads(msg.payload.decode('utf-8'))))
            obj = json2obj(j_msg)
            print("received message from "+str(obj.dev_id))
            if self.__events.uplink_msg:
                self.__events.uplink_msg(obj, client=self)
        return on_message

    def _onDownlink(self):
        def on_downlink(client, userdata, mid):
            print('MSG PUBLISHED')
            self.midCounter = mid
            if self.__events.downlink_msg:
                self.__events.downlink_msg(mid, client=self)
        return on_downlink

    def setUplinkCallback(self, callback):
        self.__events.uplink_msg += callback

    def setDownlinkCallback(self, callback):
        self.__events.downlink_msg += callback

    def setConnectCallback(self, callback):
        self.__events.connect += callback

    def setCloseCallback(self, callback):
        self.__events.close += callback

    def setConnectBehavior(self, connect):
        self.__client.on_connect = connect

    def startForever(self):
        print('LOOP STARTED')
        self.__client.loop_forever()

    def start(self):
        print('LOOP STARTED BACKGROUND')
        self.__client.loop_start()

    def stop(self):
        print('LOOP STOPPED BACKGROUND')
        self.__client.loop_stop()
        self.close()

    def close(self):
        self.__client.disconnect()
        self.connectFlag = 0

    def publish(self, devID, payload, port=1, conf=False, sched="replace"):
        message = DownlinkMessage(port, conf, sched)
        if isinstance(payload, str):
            message.payload_raw = payload
        else:
            message.payload_fields = payload

        msg = message.obj2json()

        print("publishing message to "+devID+": "+msg)
        self.__client.publish(
            self.__APPID+'/devices/'+devID+'/down',
            msg)
