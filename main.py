from machine import Pin
AP_btn = Pin(0, Pin.IN, Pin.PULL_UP) # APボタン（アクセスポイント）

if AP_btn.value() == 0:
    import apws_8266
    apws.main()

import mqtt
