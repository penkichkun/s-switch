import ujson
import network
#import webrepl

class Wificonf:
    def __init__(self):
        self.fname = "wifi_cfg.py"
    def get_essid_wifipass(self):
        try:
            f = open(self.fname)
            dic = ujson.loads(f.read())
            f.close()
        except:
            self.set_wificonf("essid", "wifipassword")
            essid = '"essid"'
            wifipass = '"wifipass"'
            dic = '{"essid":' + essid + ',' + '"wifipass:"' + wifipass + '}'
        return dic["essid"], dic["wifipass"]
    def set_wificonf(self, essid, wifipass):
        essid = '"' + essid + '"'
        wifipass = '"' + wifipass + '"'
        f = open(self.fname, mode = 'w+')
        dic = '{"essid":' + essid + ',' + '"wifipass":' + wifipass + '}'
        f.write(dic)
        f.close()
    def set_ap(self, essid):
        wlan = network.WLAN(network.STA_IF)
        wlan.active(False)
        #webrepl_pass = self.get_webrepl_pass()
        ap = network.WLAN(network.AP_IF)
        ap.active(True)
        #ap.config(essid = essid, password = webrepl_pass)
        ap.config(essid = essid)
        #ap.config(max_clients=2)
        #ap.ifconfig(('192.168.4.1', '255.255.255.0', '192.168.4.1', '8.8.8.8'))
        #webrepl.start()
#    def get_webrepl_pass(self):
#        f = open('webrepl_cfg.py')
#        webrepl_pass = f.read()[8:12]
#        f.close()
#        return webrepl_pass
#    def set_webrepl_pass(self, webrepl_pass):
#        f = open('webrepl_cfg.py', mode='w+')
#        f.write("PASS = " + "'" + webrepl_pass + "'\n")
#        f.close()
#    def set_random_webrepl_pass(self):
#        random_pass = "%04d" % random.randint(0,9999)
#        self.set_webrepl_pass(random_pass)




