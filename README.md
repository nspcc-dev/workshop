## Развертывание смарт-контракта NEO
### Запуск окружения
1. `git clone https://github.com/CityOfZion/neo-local && cd neo-local/`
2. `sudo make start`
3. в открывшемся промпте: `wallet open neo-privnet.wallet`; пароль от кошелька `coz`

### Деплоймент и вызов смарт-контракта
1. `sc build sc.py`
2. `sc deploy sc.avm False False False 07 05`
3. `sc invoke 0xef87ab3f689fb591eaad0f72d88723eb79cf92ee`
