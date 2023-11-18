# s-switch

大阪デジモク会で、カズヤさんにスマートスイッチもらったんで、ちょっと改造してみました。<br>
これ、ESP8266 を使っているので、MicroPython を載せて、MQTTで使えるように改造テスト。<br>
とりあえず、BROKER = 'broker.emqx.io' に決め打ち<br>
（今久しぶりにやってみると繋がらなかったので、'broker.hivemq.com'に変えたらOKでした）<br>
コードはあくまでテストです（いい加減です）。<br>
2023-09-23 Nishijima<br>

# ハード
BTN = machine.Pin(0, Pin.IN, Pin.PULL_UP) # タクトスイッチ（モード設定用）<br>
LEDR = machine.Pin(13, machine.Pin.OUT) # 赤<br>
LEDG = machine.Pin(12, machine.Pin.OUT) # 緑<br>
LEDB = machine.Pin(14, machine.Pin.OUT) # 青<br>
RELAY = machine.Pin(15, machine.Pin.OUT) # リレー<br>

# 使い方の概要
リセットボタンを押して指を離した瞬間、素早くBTN を押すと（LED赤が点灯するまで何回かトライください）⇒サーバーモードになります。<br>
「SmartSwitch」ではじまるWifi ESSIDが出てるので、これに接続し、Webブラウザーで 192.168.4.1 にアクセス、パスワードは micropythoN （最後は大文字）。<br>
使用する環境に合わせて、wifiとパスワードを設定します。<br>
![image](https://github.com/penkichkun/s-switch/assets/151262367/4c385db8-2ada-4bf3-8bf2-6432ef250fcd) <br>
MQTTは、スマートスイッチのMACアドレスで購読して1を送信するとリレーON、0でOFFします。<br>
僕は、「MQTT Dashboard」というスマホアプリから使っていますが結構便利です。<br>

# スマートスイッチ製品の概要はこちら
https://eiwa-up.jp/product/cloud-computing/smart-switch/<br>

