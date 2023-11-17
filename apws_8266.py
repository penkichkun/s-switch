# apws_8266.py
# httpdサーバーとして設定する（アクセスポイント前提）
# by Nishijima Taisaku 2021-06-11
#

import network
import gc
import time
import random
rand = f"{random.getrandbits(8):03d}"

#gc.collect()

header = """<head>
<meta http-equiv="Content-Type" content="text/html; charset=utf-8"/>
<title>スマートスイッチ</title>
<meta name="viewport" content="width=device-width, initial-scale=1">
<link rel="icon" href="data:,">
<style>html{font-family: Helvetica; display:inline-block; margin: 0px auto; text-align: center;}
h1{color: #0F3376; padding: 2vh;}p{font-size: 1.5rem;}.button{display: inline-block; background-color: #e7bd3b; border: none;
border-radius: 4px; color: white; padding: 16px 40px; text-decoration: none; font-size: 30px; margin: 2px; cursor: pointer;}
.button2{background-color: #4286f4;}
.profile{color: white; background-color: #4286f4;}
</style>
</head>
"""

def web_page_main(): # メインメニュー
    html = "<html>"
    html += header
    html += """
<body>
<h1>スマートスイッチ</h1>
<p><a href="/?menu=setwificonf">
<button class="button">WIFIを設定する</button></a></p>
<p><a href="/?menu=showconf">
<button class="button button2">WIFIの設定を見る</button></a></p>
<p><a href="/?menu=showSA">
<button class="button button2">WIFIの接続チェック</button></a></p>
<p><a href="/?menu=reset">
<button class="button">設定終了（再起動）</button></a></p>
</body></html>
"""
    return html


def web_page_showconf(): # 設定情報の表示ページ
    #gc.collect()
    import wificonf
    wificonf = wificonf.Wificonf()
    essid, wifipass = wificonf.get_essid_wifipass()
    html = "<html>"
    html += header
    html += "<body><h1>DIY農業</h1>"
    html += """<table class="profile">"""
    html += "<tr><td>ESSID</td><td>" + essid + "</td></tr>"
    html += "<tr><td>WIFI パスワード</td><td>" + wifipass + "</td></tr>"
    html += "</table>"
    html += """
<p><a href="/?menu=main">
<button class="button button2">戻る</button></a></p>
</body></html>
"""
    return html

def web_page_wificonf(): # WIFI設定入力ページ
    #gc.collect()
    html = "<html>"
    html += header
    html += "<body><h1>DIY農業</h1>"
    html += """
<form action="/?DATA=1" method="GET">
<p>ESSID：<input type="text" name="essid" size="40"></p>
<p>パスワード：<input type="text" name="wifipass" size="40"></p>
<p><input type="submit" value="送信"><input type="reset" value="リセット"></p>
</form>
<p><a href="/?menu=main">
<button class="button button2">戻る</button></a></p>
</body></html>
"""
    return html

def web_page_showSta(Sta_ip): # sta_if IPアドレス表示
    #gc.collect()
    html = "<html>"
    html += header
    html += "<body><h1>スマートスイッチ</h1>"
    html += "ＷｉＦｉに接続できました。ＩＰアドレスは、<p>"
    html += Sta_ip
    html += "</p>です。アンビエントの設定などは、このアドレスをアクセスしてください。"
    html += """
<p><a href="/?menu=main">
<button class="button button2">戻る</button></a></p>
</body></html>
"""
    return html

def web_page_notconnected(): # sta_if つながらない
    #gc.collect()
    html = "<html>"
    html += header
    html += "<body><h1>スマートスイッチ</h1>"
    html += "<p>ＷｉＦｉに接続できませんでした。</p>"
    html += """
<p><a href="/?menu=main">
<button class="button button2">戻る</button></a></p>
</body></html>
"""
    return html

def web_page_reset(): # reset表示ページ
    #gc.collect()
    html = "<html>"
    html += header
    html += "<body><h1>スマートスイッチ</h1>"
    html += """
<p>ボードの再起動ボタンを押して、再起動してください。</p>
</body></html>
"""
    return html


def main():
    import wificonf
    wificonf = wificonf.Wificonf()
    wificonf.set_ap(f"SmartSwitch{rand}")
    time.sleep(1)

    import usocket as socket
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind(('', 80))
    s.listen(1)

    while True:
        conn, addr = s.accept()
        print('Got a connection from %s' % str(addr))
        request = conn.recv(1024)
        request = str(request)
        print('Content = %s' % request)
        if len(request) < 10:
            continue
        menu_wificonf = request.find('/?menu=setwificonf')
        menu_showconf = request.find('/?menu=showconf')
        menu_showSA = request.find('/?menu=showSA')
        menu_reset = request.find('/?menu=reset')
        if menu_wificonf == 6:
            response = web_page_wificonf()
        elif menu_showconf == 6:
            response = web_page_showconf()
        elif menu_showSA == 6:
            essid, wifipass = wificonf.get_essid_wifipass()
            sta_if = network.WLAN(network.STA_IF)
            sta_if.active(True)
            """
            if sta_if.isconnected(): # 一旦切断
                sta_if.disconnect()
            time.sleep(0.1)
            """
            print("Debug1")
            if not sta_if.isconnected():
                try:
                    sta_if.connect(essid, wifipass)
                except:
                    response = web_page_main()
            i = 0
            for i in range(30):
                if not sta_if.isconnected():
                    time.sleep(0.5)
            if not sta_if.isconnected():
                response = web_page_notconnected()
            else:
                #global Sta_ip
                print("Debug2")
                Sta_ip = sta_if.ifconfig()[0]
                response = web_page_showSta(Sta_ip)
        elif menu_reset == 6:
            response = web_page_reset()
        else:
            response = web_page_main()

        pos0 = request.find('GET /?essid=')
        pos1 = request.find('&wifipass=')
        pos2 = request.find(' HTTP')
        if pos0 > 0:
            essid = request[pos0 +12 :pos1]
            essid = essid.strip()
            wifipass = request[pos1 +10 :pos2]
            wifipass = wifipass.strip()
            wificonf.set_wificonf(essid, wifipass)
        conn.send('HTTP/1.1 200 OK\n')
        conn.send('Content-Type: text/html\n')
        conn.send('Connection: close\n\n')
        conn.sendall(response)
        conn.close()

