# Workshop: Бои роботов смарт-контрактов

## Введение


## Установка NEO privnet 


```

docker run --name neo-privatenet -p 20333-20336:20333-20336/tcp -p 30333-30336:30333-30336/tcp cityofzion/neo-privatenet


```

## Установка neo-python (CLI)

[https://github.com/CityOfZion/neo-python](https://github.com/CityOfZion/neo-python)

```

sudo apt-get update && sudo apt-get upgrade

sudo apt-get install python3.7 python3.7-dev python3.7-venv python3-pip libleveldb-dev libssl-dev g++

```

```

git clone https://github.com/CityOfZion/neo-python.git

cd neo-python

git checkout development

# create virtual environment using Python 3.7

python3.7 -m venv venv

source venv/bin/activate

 

# install the package in an editable form

(venv) pip install wheel -e .

```
В файле neo/data/protocol.privnet.json нужно изменить строку '"NodePort": 20333,' на '"NodePort": 20331,'

```
rm -rf /home/<username>/.neopython/Chains/privnet*

 

np-prompt -p -v

```


```

neo> config sc-events on

neo> config sc-debug-notify on

neo> sc debugstorage on

```


## Импорт кошелька для Neo Local privnet

Теперь откроем кошелек, чтобы оплачивать транзакции в сети: `wallet open neo-privnet.sample.wallet` (пароль `coz`). `neo-privnet.sample.wallet` – это относительный путь к файлу с кошельком. 

После открытия кошелька можно выполнить команду `wallet` и увидеть его адрес в сети, публичный ключ и синхронизированные балансы токенов NEO и Gas.


 

## Импорт смарт-контракта

Скопируем код контрактов в директорию neo-python из https://github.com/nspcc-dev/workshop/tree/master/contracts.

```
git clone https://github.com/nspcc-dev/workshop.git
```

Скомпилируем и задеплоим каждый контракт.

Между каждой командой deploy необходимо дождаться ее принятия по консенсусу - это может занять около 15 секунд.

```

sc build workshop/contracts/master.py

sc build workshop/contracts/user_contract.py

sc deploy workshop/contracts/master.avm True True True 0710 05 --fee=0.1

sc deploy workshop/contracts/user_contract.avm True True True 0710 05 --fee=0.1

sc deploy workshop/contracts/user2.avm True True True 0710 05 --fee=0.1

```

Посмотреть адрес контракта:
search contract <Name>


Вызовем контракт зарегистрировав два контракта-игрока (адрес в опциях без '0x':
```

sc invoke 0x63c7cb5299c54910b23f10cff35689eff62b813c Register [b'd8a741796e19c83db69bd8806bcc50857dec38ed']

sc invoke 0x63c7cb5299c54910b23f10cff35689eff62b813c Register [b'bbb37941e830ca130e6d47cda5b812e991f010fb']


```

Проведем первый бой:

```

sc invoke 0x63c7cb5299c54910b23f10cff35689eff62b813c Battle [b'd8a741796e19c83db69bd8806bcc50857dec38ed', b'bbb37941e830ca130e6d47cda5b812e991f010fb']

```

 
###  Развернуть конкурсный веб-интерфейс
```
docker pull nspccru/cc-game-ui
docker run -p 3000:80 --rm nspccru/cc-game-ui
```






## Альтернативные способ - создание кошелька, вместо готового

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
 

```


