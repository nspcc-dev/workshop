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


## Импорт кошелька для Neo privnet

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

sc build workshop/contracts/user_contract_test.py


sc deploy workshop/contracts/master.avm True True True 0710 05 --fee=0.1

sc deploy workshop/contracts/user_contract.avm True True True 0710 05 --fee=0.1

sc deploy workshop/contracts/user_contract_test.avm True True True 0710 05 --fee=0.1

```

Посмотреть адрес контракта:
search contract <Name>


Вызовем контракт зарегистрировав два контракта-игрока (адрес в опциях без '0x':
```

sc invoke 0x63c7cb5299c54910b23f10cff35689eff62b813c Register [b'93b8354f27c0757e865a3940787622fe6e32355d']

sc invoke 0x63c7cb5299c54910b23f10cff35689eff62b813c Register [b'bdd69f3dfd1492b3434303d4bc0da1328fb68492']


```

Проведем первый бой:

```

sc invoke 0x63c7cb5299c54910b23f10cff35689eff62b813c Battle [b'93b8354f27c0757e865a3940787622fe6e32355d', b'bdd69f3dfd1492b3434303d4bc0da1328fb68492', 0, 0] 


```

 
###  Развернуть конкурсный веб-интерфейс
```
docker pull nspccru/cc-game-ui
docker run -p 3000:80 --rm nspccru/cc-game-ui
```

Ввести в поле идентификатор выполненной транзакции:
[I 190824 22:32:40 EventHub:62] [SmartContract.Execution.Success][4170] [63c7cb5299c54910b23f10cff35689eff62b813c] [tx d5d62bcf102bd6adfba033c63b45630e794cff536f1dd18bbdf8f3d19a493f8d] {'type': 'Array', 'value': [{'type': 'Integer', 'value': '1'}]}

Перейти на localhost:3000 и введя транзакцию - увидеть результаты боя, полученные из блокчейна.


