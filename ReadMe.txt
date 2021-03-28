#=================================================================#
#   System Required:  Ubuntu 20					  #
#   Description: ИНструкция для удобства установки и настройки 	  #
#		ShadowsocksR Server 				  #
#   Author: Romax911 <Romax911@gmail.com>                         #
#   Thanks: Teddysun <i@teddysun.com>  				  #
#=================================================================#


#1.1 Установка и настройка ShadowsocksR by teddysun (https://www.tipsforchina.com/how-to-setup-a-fast-shadowsocks-server-on-vultr-vps-the-easy-way.html#install)
	sudo apt-get update && sudo apt-get upgrade -y
	wget --no-check-certificate https://raw.githubusercontent.com/teddysun/shadowsocks_install/master/shadowsocksR.sh
	chmod +x shadowsocksR.sh
	./shadowsocksR.sh 2>&1 | tee shadowsocksR.log

#1.2 настройка при установке (Рекомендуемые параметры)
	1.2.1 - введите пароль
	1.2.2 Введите "12" - 12) chacha20
	1.2.3 Введите "1" - 1) origin
	1.2.4 Введите "3" - 3) http_simple_compatible

#1.2 Установка ShadowsocksR by Me (Рекомендуемые параметры выставлены по умолчанию)

	sudo apt-get update && sudo apt-get upgrade -y
	wget --no-check-certificate https://raw.githubusercontent.com/Romax-91/TM_ShadowsocksR/master/shadowsocksR.sh
	chmod +x shadowsocksR.sh
	./shadowsocksR.sh 2>&1 | tee shadowsocksR.log

#1.3 Изменение настроек подключения 
	nano /etc/shadowsocks.json

#1.4 Рестарт SSR server
	/etc/init.d/shadowsocks restart

#2 Установка и настройка WebMin (https://wilddiary.com/install-webmin-on-aws-ec2-server/)
	2.1 Установка
		wget http://www.webmin.com/download/deb/webmin-current.deb
		sudo apt-get update
		sudo apt-get install perl libnet-ssleay-perl openssl libauthen-pam-perl libpam-runtime libio-pty-perl apt-show-versions python
		sudo dpkg --install webmin-current.deb
		sudo apt-get --fix-broken install
	
	2.2 Добавление пользователя и пароля
		sudo useradd -g sudo webmin
		sudo passwd webmin


#3 Установка Telegram-send для оповещения (https://github.com/rahiel/telegram-send)
	sudo apt install python3-pip
	sudo pip3 install telegram-send
	sudo telegram-send --configure

#4 Скрипты для оповещения через телеграмм
	4.1 Загрузка и начальный запуск
	wget https://codeload.github.com/Romax-91/TM_ShadowsocksR/zip/refs/heads/main
	unzip main
	cd TM_ShadowsocksR-main
	chmod +x data_limit_clear.sh data_limit_info.sh data_limit_init.sh 
	
	4.2 Запуск скрипта для установки правил по ограничению
		sudo ./data_limit_init.sh 
	
	4.2 Добавление скрипта оповещения и обнуления в cron (Информация каждый день в MSC19.00(UTC 16.00), сброс статистики каждый месяц в MSC03.00(UTC 00.00))
		sudo -s
		crontab -e	
		#Скопируйте и добавьте все как в "crontab_example.txt"  (https://devacademy.ru/article/15-otlichnykh-primierov-dlia-sozdaniia-cron-zadach-v-linux)
	

