import json
import subprocess
import configparser

if __name__ == '__main__':

    # load default config
    config = configparser.ConfigParser()
    config.read('init.ini')

    interface = config['SETTINGS']['interface']
    print("interface ", interface)

    port = config['SETTINGS']['port']
    print("PORT ", port)

    limit = config['SETTINGS']['limit']
    print("LIMIT ", port)

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
            if total >= limit:
                print("iptables block port")
                # Чтобы заблокировать 443 порт iptables для входящего соединения
                subprocess.getoutput("iptables -t filter -A INPUT -p tcp --dport {} -j DROP".format(port))
            else:
                print("iptables unblock")
                subprocess.getoutput("Iptable -Z INPUT".format(port))
