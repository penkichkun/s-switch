# s-switch

カズヤさんにもらったスマートスイッチ
https://eiwa-up.jp/product/cloud-computing/smart-switch/<br>
ESP8266 を使っているので、これに MicroPython を載せて、MQTTで使えるように改造してみる（テスト）。<bR>
とりあえず、BROKER = 'broker.emqx.io' に決め打ち<br>
2023-09-23 Nishijima<br>
# ハード
BTN = machine.Pin(0, Pin.IN, Pin.PULL_UP) # タクトスイッチ（モード設定用）<br>
LEDR = machine.Pin(13, machine.Pin.OUT) # 赤<br>
LEDG = machine.Pin(12, machine.Pin.OUT) # 緑<br>
LEDB = machine.Pin(14, machine.Pin.OUT) # 青<br>
RELAY = machine.Pin(15, machine.Pin.OUT) # リレー<br>

# 使い方の概要
リセットボタンを押し、素早くBTN を押すと（LED赤が点灯）⇒サーバーモードになります。<br>
「SmartSwitch」ではじまるWifi ESSIDが出てるので、これに接続し、Webブラウザーで 192.168.4.1 にアクセス、パスワードは micropythoN （最後は大文字）。<br>
使用する環境に合わせて、wifiとパスワードを設定します。<br>
MQTTは、スマートスイッチのMACアドレスで購読して1を送信するとリレーON、0でOFFします。<br>

# 製品の概要はこちら
https://eiwa-up.jp/product/cloud-computing/smart-switch/<br>

