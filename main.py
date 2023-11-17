from machine import Pin
BTN = Pin(0, Pin.IN, Pin.PULL_UP) # APボタン（アクセスポイント）
LEDR = machine.Pin(13, machine.Pin.OUT) # 赤


if BTN.value() == 0:
    LEDR.value(0)
    import apws_8266
    apws_8266.main()

else:
    LEDR.value(1)

import mqtt
