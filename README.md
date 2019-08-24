# Развертывание смарт-контракта NEO

 
## Шаги:
1) Что такое смарт-контракты в NEO
2) Развернуть privnet
3) Развернуть NEO python CLI
4) Развернуть конкурсный веб-интерфейс
5) Открыть кошелек
6) Скомпилировать контракт и развернуть в сети
7) Внести исправления и разобрать конкурсный контракт
8) Провести пробный бой
9) Записать в память контракта и прочитать из памяти


## Файлы:

 

- master.py - код смарт-контракта для игры
- user_contract.py - бот для боёв

## Введение


## Установка NEO privnet (Neo local)  
Развернем privnet из этого [https://github.com/CityOfZion/neo-local](https://github.com/CityOfZion/neo-local) репозитория. Для поднятия окружения необходим установленный docker-compose.

Склонируем репозиторий и перейдем в нужную директорию.

```
git clone https://github.com/CityOfZion/neo-local && cd neo-local/
```
дадим команду на поднятие окружения. Она запустит нужные контейнеры и подготовит консоль.   
```
sudo make start
```
После поднятия должны увидеть вот такие docker-контейнеры:
1. четыре бегущих консенсус-узла: neo-cli-privatenet-[1:4]  
2. монитор блокчейна и его инфраструктура: neo-scan-api, neo-scan-sync, postgres. По адресу [http://127.0.0.1:4000](http://127.0.0.1:4000) можно увидеть состояние локального блокчейна: созданные блоки, транзакции в них, адреса кошельков и т.п.   
3. форма для запроса тестовых токенов neo-local-faucet по адресу [http://127.0.0.1:4002](http://127.0.0.1:4002/)
4. notifications_server: API-сервер, расположенный по адресу [http://127.0.0.1:8080](http://127.0.0.1:8080) и отдающий данные о состоянии блокчейна (по ссылке список доступных эндпоинтов)
5. neo-python: консоль для взаимодействия с блокчейном, в которой будет происходить дальнейшая работа

Видим версию NEO и лог о том, что создалась новая база для хранения блоков. Кроме этого, видим задеплоенный тестовый смарт-контракт.

Внизу экрана будет строка, показывающая, сколько блоков из ныне доступных вычитано. Что это означает? Существует понятие “высоты блокчейна”: это номер самого позднего блока в цепочке. Privnet создает блокчейн не с нуля, а запускается на заранее подготовленном блокчейне некоторой высоты (примерно шесть тысяч блоков). Эти блоки состоят из транзакций, которые приводят сеть в некоторое состояние, до которого privnet и должен дойти, последовательно вычитывая блоки.

Подождем синхронизации блокчейна, то есть, пока числа слева и справа от слэша в строке станут одинаковыми. После этого можно начинать работать с консолью.

Откроем кошелек, чтобы оплачивать транзакции в сети (пароль ```coz```).
```
wallet open neo-privnet.wallet
```
neo-privnet.wallet – это относительный путь к файлу с кошельком. После открытия кошелька можно выполнить команду wallet и увидеть его адрес в сети, публичный ключ и синхронизированные балансы токенов NEO и NEOGas (подробнее по ссылке [http://www.intoken.ru/neo/](http://www.intoken.ru/neo/)).

Окружение поднято, теперь можно написать смарт-контракт и задеплоить его в сеть.

#### Альтернативный способ подготовить окружение

Промпт, в который мы попали после выполнения команды make start, представляет собой CLI на python, запущенный внутри docker-контейнера. Как попасть в промпт вручную, если вы, например, случайно вышли из контейнера:

1.  sudo docker exec -it neo-python /bin/bash : зайдем в контейнер для работы с консолью
   
2.  в контейнере выполним команду np-prompt -p, которая инициализирует блокчейн и запустит промпт для взаимодействия с ним. Ключ -р означает, что мы стартуем privnet
   
3.  прежде, чем деплоить смарт-контракт, рекомендую выполнить команды config sc-events on и config sc-debug-notify on -- в результате логи блокчейна будут выводиться в консоль, что поможет понять, в каком состоянии находятся транзакции по деплойменту или вызову смарт-контракта.

## Еще один способ развернуть окружение (COZ)

[https://github.com/slipo/neo-scan-docker](https://github.com/slipo/neo-scan-docker)

```

docker run --name neo-privatenet -p 20333-20336:20333-20336/tcp -p 30333-30336:30333-30336/tcp cityofzion/neo-privatenet


```

## Установка neo-python (docker)
[https://hub.docker.com/r/cityofzion/neo-python/](https://hub.docker.com/r/cityofzion/neo-python/)



## Альтернативная установка neo-python

[https://github.com/CityOfZion/neo-python](https://github.com/CityOfZion/neo-python)

```

sudo apt-get update && sudo apt-get upgrade

sudo apt-get install python3.7 python3.7-dev python3.7-venv python3-pip libleveldb-dev libssl-dev g++

```

```

git clone https://github.com/CityOfZion/neo-python.git

cd neo-python

# create virtual environment using Python 3.7

python3.7 -m venv venv

source venv/bin/activate

 

# install the package in an editable form

(venv) pip install wheel -e .

 

rm -rf /home/<username>/.neopython/Chains/privnet*

 

np-prompt -p

```


```

neo> config sc-events on

neo> config sc-debug-notify on

neo> sc debugstorage on

```

 
###  Развернуть конкурсный веб-интерфейс
```
docker pull nspccru/cc-game-ui:1.2
docker run -p 3000:80 --rm nspccru/cc-game-ui:1.2
```

## Импорт кошелька для Neo Local privnet

Теперь откроем кошелек, чтобы оплачивать транзакции в сети: `wallet open neo-privnet.wallet` (пароль `coz`). `neo-privnet.wallet` – это относительный путь к файлу с кошельком. После открытия кошелька можно выполнить команду `wallet` и увидеть его адрес в сети, публичный ключ и синхронизированные балансы токенов NEO и NEOGas (подробнее по ссылке [http://www.intoken.ru/neo/](http://www.intoken.ru/neo/)).

## Создание кошелька для CoZ privnet


```

neo> wallet help

```

```

neo> wallet create wallet_test.wallet

[password]> **********

[password again]> **********

[I 190801 18:41:30 UserWallet:480] Script hash b"\x99\x07Cg\xfd\x8e)\xee\x94\x88'5+#gt\x0b\xc6s\x1c" <class 'bytes'>

Wallet {

"path": "wallet_test.wallet",

"addresses": [

{

"address": "AVj1jWdbmwvKR4VHAVouMEjCLYK258DXJM",

"script_hash": "99074367fd8e29ee948827352b2367740bc6731c",

"tokens": null

}

],

"height": 0,

"percent_synced": 0,

"synced_balances": [],

"public_keys": [

{

"Address": "AVj1jWdbmwvKR4VHAVouMEjCLYK258DXJM",

"Public Key": "02e46e1972268e45edf95906adbae0355bf323d7606d9dbea43e2f5da72ad36bc4"

}

],

"tokens": [],

"claims": {

"available": "0.0",

"unavailable": "0.0"

}

}

Pubkey b'02e46e1972268e45edf95906adbae0355bf323d7606d9dbea43e2f5da72ad36bc4'

neo>

```

To remove the pre-created address:

```

neo> wallet address delete AVj1jWdbmwvKR4VHAVouMEjCLYK258DXJM

Deleted address AVj1jWdbmwvKR4VHAVouMEjCLYK258DXJM

```

 

Import default address with all GAS in the privnet:

 

```

neo> wallet import wif KxDgvEKzgSBPPfuVfw67oPQBSjidEiqTHURKSDL1R7yGaGYAeYnr

Imported key: KxDgvEKzgSBPPfuVfw67oPQBSjidEiqTHURKSDL1R7yGaGYAeYnr

Pubkey: 031a6c6fbbdf02ca351745fa86b9ba5a9452d785ac4f7fc2b7548ca2a46c4fcf4a

Address: AK2nJJpJr6o664CWJKi1QRXjqeic2zRp8y
```
 
 

## Импорт смарт-контракта

Скопируем код контракта внутрь контейнера. 

```
sudo docker cp sc.py neo-python:/neo-python
```

Скомпилируем и задеплоим контракт.

```
sc build help

sc build sc.py

sc deploy sc.avm True True True 0710 05 --fee=0.1

```

Вызовем контракт:
```

sc invoke 0x43f0ce40eba822dee478b3650a75b52b6edd0c81 Operation ['arguments']

```


