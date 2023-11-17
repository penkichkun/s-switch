# s-switch

カズヤさんにもらったスマートスイッチ
https://eiwa-up.jp/product/cloud-computing/smart-switch/
ESP8266 を使っているので、これに MicroPython を載せて、MQTTで使えるように改造してみる（テスト）。
とりあえず、BROKER = 'broker.emqx.io' に決め打ち
2023-09-23 Nishijima
スマートスイッチのハードは
BTN = machine.Pin(0, Pin.IN, Pin.PULL_UP) # タクトスイッチ（モード設定用）
LEDR = machine.Pin(13, machine.Pin.OUT) # 赤
LEDG = machine.Pin(12, machine.Pin.OUT) # 緑
LEDB = machine.Pin(14, machine.Pin.OUT) # 青
RELAY = machine.Pin(15, machine.Pin.OUT) # リレー
 
リセットボタンを押し、素早くBTN を押すと（LED赤が点灯）⇒サーバーモードになります。
ESSID = 
