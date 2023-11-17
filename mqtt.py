#
# カズヤさんにもらったスマートスイッチを改造してみる
# 2023-09-23 Nishijima
#
from machine import Pin, I2C, SoftI2C, Timer, reset
import time

BTN = Pin(0, Pin.IN, Pin.PULL_UP) # タクトスイッチ（モード設定用）
BROKER = 'broker.emqx.io'

import network
sta_if = network.WLAN(network.STA_IF)
sta_if.active(True)

import wificonf # wifi の設定は別途行っておく
w = wificonf.Wificonf()
essid, wifipass = w.get_essid_wifipass()

def do_connect():
    import network
    sta_if = network.WLAN(network.STA_IF)
    if not sta_if.isconnected():
        print('connecting to network...')
        sta_if.active(True)
        sta_if.connect(essid, wifipass)
        while not sta_if.isconnected():
            pass
    print('network config:', sta_if.ifconfig())

do_connect()
MAC = sta_if.config('mac').hex()
import ntptime
JST_OFFSET = 9 * 60 * 60 # JST = UTC + 9H(32400秒）
ntptime.settime()
import machine
import ubinascii

LEDR = machine.Pin(13, machine.Pin.OUT) # 赤
LEDR.value(1)
LEDG = machine.Pin(12, machine.Pin.OUT) # 緑
LEDG.value(1)
LEDB = machine.Pin(14, machine.Pin.OUT) # 青
LEDB.value(1)
RELAY = machine.Pin(15, machine.Pin.OUT) # リレー
from umqtt.simple import MQTTClient

def sub_cb(topic, msg):
    global MSG
    MSG = (topic, msg)

MSG=('',b'')

client_id =  ubinascii.hexlify(machine.unique_id())
cl = MQTTClient(client_id, BROKER, keepalive = 60) # オブジェクト生成
cl.set_callback(sub_cb)
cl.connect() # オブジェクトは同時に１つしかつながらない
cl.subscribe(MAC) # MACアドレスで購読
i = 0
j = 0
while True:
    j += 1
    try:
        (year, month, day, hour, min, sec, wd, yd) = time.localtime(time.time() + JST_OFFSET)
        cl.check_msg()
        if MSG[1] == b'1':
            RELAY.value(1)
            LEDG.value(0)
            cl.publish(MAC, f'{month}/{day} {hour}:{min}:{sec} --- ON')
            print(f'Hit ! {i} {j-1}')
            i +=1
            MSG=('',b'')
        if MSG[1] == b'0':
            RELAY.value(0)
            LEDG.value(1)
            cl.publish(MAC, f'{month}/{day} {hour}:{min}:{sec} --- OFF')
            print(f'Hit ! {i} {j-1}')
            i +=1
            MSG=('',b'')
    except:
        print('exception')
    time.sleep(1)
    if j % 50 == 0:
        cl.ping() # タイムアウトする前にピンを打っとく
        j = 0
cl.disconnect()
