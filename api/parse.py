import json
import subprocess
import configparser
from hurry.filesize import size

if __name__ == '__main__':

    # load default config
    config = configparser.ConfigParser()
    config.read('init.ini')

    interface = config['SETTINGS']['interface']
    print("interface ", interface)

    port = config['SETTINGS']['port']
    print("PORT ", port)

    limit = config['SETTINGS']['limit']
    print("LIMIT ", limit)

    # Port for SSR
    # limit 450 Gb 450 000 000 000
    # limit = 450000000000
    # limit = 797395

    output = subprocess.getoutput("vnstat --json")
    data = json.loads(output)

    for i in data['interfaces']:
        if i['name'] == interface:
            last_h = i['traffic']['hour'][0]
            for h in i['traffic']['hour']:
                if h['id'] > last_h['id']:
                    last_h = h

            total = last_h['rx'] + last_h['tx']
            if total > int(limit):
                print("iptables block port")
                print("Total ", size(total))
                print("Total ", total)
                # Чтобы заблокировать 443 порт iptables для входящего соединения
                subprocess.getoutput("Iptable -Z INPUT".format(port))
                subprocess.getoutput("iptables -t filter -A INPUT -p tcp --dport {} -j DROP".format(port))
            else:
                print("iptables unblock")
                print("Total ", size(total))
                print("Total ", total)
                subprocess.getoutput("Iptable -Z INPUT".format(port))
                # subprocess.getoutput("iptables -I INPUT -m state --state NEW -m tcp -p tcp --dport {} -j ACCEPT".format(port))
                # subprocess.getoutput("iptables -I INPUT -m state --state NEW -m udp -p udp --dport {} -j ACCEPT".format(port))
                # subprocess.getoutput("/etc/init.d/iptables save")
                # subprocess.getoutput("/etc/init.d/iptables restart")
