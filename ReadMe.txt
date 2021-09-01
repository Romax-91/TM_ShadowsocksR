#=================================================================#
#   System Required:  Ubuntu 20					  #
#   Description: Инструкция  установки и настройки 	          #
#		      ShadowsocksR Server 			  #
#   Author: Romax911 <Romax911@gmail.com>                         #
#   Thanks: Teddysun <i@teddysun.com>  				  #
#=================================================================#

# Введение
Данная инструкция поможет быстро установить и настроить ShadowsocksR Server на VPS сервере. Тестировал на AWS Ubuntu Server 20.04 LTS.
Дополнительно:
	Установка и настройка WebMin - быстрой доступ к серверу
	Установка и настройка Telegram-send - система оповещения (для мониторинга объема сетевого трафика, на основе скриптов выполняемых в cron)
	Настройка Cron

Какой сервер выбрать:
	AWS EC2 (https://aws.amazon.com/) - Один год бесплатного использования (Ограничения: Только Один VPS, 15ГБ/мес, 750 часов/мес)
	Amazon Lightsail (https://aws.amazon.com/ru/lightsail/pricing/?opdp1=pricing) - 3,50 USD в месяц, Передача данных: 1 ТБ*
	Google Cloud Platform(https://console.cloud.google.com/) - один год бесплатного использования + подарок в 400$/год, нет ограничений по трафику
	Linode (https://cloud.linode.com/) - платный, минум 5$ за 300ГБ/мес

#1 Установка и настройка ShadowsocksR

	#1.1 Установка и настройка ShadowsocksR by teddysun (https://www.tipsforchina.com/how-to-setup-a-fast-shadowsocks-server-on-vultr-vps-the-easy-way.html#install)
		# !Если не хочется тыкать и выбирать то переходи к пункту 1.3
		sudo apt-get update && sudo apt-get upgrade -y
		wget --no-check-certificate https://raw.githubusercontent.com/teddysun/shadowsocks_install/master/shadowsocksR.sh
		chmod +x shadowsocksR.sh
		sudo ./shadowsocksR.sh 2>&1 | tee shadowsocksR.log

	#1.2 настройка при установке (Рекомендуемые параметры)
		1.2.1 - введите пароль
		1.2.2 Введите "12" - 12) chacha20
		1.2.3 Введите "1" - 1) origin
		1.2.4 Введите "3" - 3) http_simple_compatible

	#1.3 Установка ShadowsocksR by Me (Рекомендуемые параметры выставлены по умолчанию)
		# !Не выполнять если выполнено 1.1
		sudo apt-get update && sudo apt-get upgrade -y
		wget --no-check-certificate https://raw.githubusercontent.com/Romax-91/TM_ShadowsocksR/master/shadowsocksR.sh
		chmod +x shadowsocksR.sh
		sudo ./shadowsocksR.sh 2>&1 | tee shadowsocksR.log

	#1.4 Изменение настроек подключения
		nano /etc/shadowsocks.json

	#1.5 Рестарт SSR server
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
	sudo -s
	sudo apt install python3-pip
	sudo pip3 install telegram-send
	sudo telegram-send --configure

#4 Скрипты для оповещения через телеграмм
	4.1 Загрузка и начальный запуск
	wget https://codeload.github.com/Romax-91/TM_ShadowsocksR/zip/refs/heads/main
	unzip main
	cd TM_ShadowsocksR-main
	chmod +x data_limit_clear.sh data_limit_info.sh data_limit_init.sh 
	
	4.2 Запуск скрипта для Добавления правила в брандмауэр, ограничивает объем 14 Гб(14000000000 байт) по 443 порту
		sudo ./data_limit_init.sh 
	
	4.2 Добавление скрипта оповещения и обнуления в cron (Информация каждый день в MSC19.00(UTC 16.00), сброс статистики каждый месяц в MSC03.00(UTC 00.00))
		sudo -s
		crontab -e	
		#Скопируйте и добавьте все как в "crontab_example.txt"  (https://devacademy.ru/article/15-otlichnykh-primierov-dlia-sozdaniia-cron-zadach-v-linux)

#5 api - Vnstat
    sudo apt-get update
    sudo apt install unzip

    wget https://codeload.github.com/Romax-91/TM_ShadowsocksR/zip/refs/heads/main
    unzip main
    cd TM_ShadowsocksR-main/api
    chmod +x init.sh restart_api.sh


#Команды для ограничения Трафика по сети.
	!При перезагрузке сбрасываются данные по статистике и по добаленным правилам.

1. Добавлениt правила в брандмауэр, ограничивает объем 50 Гб(50000000000 байт) по 443 порту
	sudo iptables -I OUTPUT -p tcp --sport 443 -j DROP
	sudo iptables -I OUTPUT -p tcp --sport 443 -m quota --quota 50000000000 -j ACCEPT
	
2. Просмотр текущих данных по использованному трафику
	sudo iptables -nvL -t filter --line-numbers

3.Сброс данных по собранной статистике (обнуление)
	sudo iptables -nvL -t filter --line-numbers


#SSR Клиенты
	ShadowsocksR for Windows (Download version 4.9.0, the newer ones have DNS leaks) (https://github.com/shadowsocksrr/shadowsocksr-csharp/releases)
	ShadowsocksR for Android (https://github.com/shadowsocksrr/shadowsocksr-android/releases)
	ShadowsocksR for Mac (https://github.com/qinyuhang/ShadowsocksX-NG-R/releases)
	iOS Potatso Lite (FREE) (https://itunes.apple.com/app/potatso-lite/id1239860606?mt=8)
	iOS Shadowrocket ($2.99) (https://itunes.apple.com/us/app/shadowrocket/id932747118)


