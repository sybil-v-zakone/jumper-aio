"""
НАСТРОЙКА СЕТЕЙ
"""

BASE_RPC_ENDPOINT = "https://base-mainnet.public.blastapi.io"
ETHEREUM_RPC_ENDPOINT = "https://rpc.ankr.com/eth"
ARBITRUM_RPC_ENDPOINT = "https://rpc.ankr.com/arbitrum"
OPTIMISM_RPC_ENDPOINT = "https://rpc.ankr.com/optimism"
ZKSYNC_RPC_ENDPOINT = "https://mainnet.era.zksync.io"
BSC_RPC_ENDPOINT = "wss://bsc-rpc.publicnode.com"
POLYGON_RPC_ENDPOINT = "https://1rpc.io/matic"
LINEA_RPC_ENDPOINT = "https://linea.drpc.org"
ZKERA_RPC_ENDPOINT = "https://mainnet.era.zksync.io"

"""
ОБЩИЕ НАСТРОЙКИ
"""
# Минимальный Gwei в сети ETH, при котором не будут отправляться транзакции
GAS_THRESHOLD = 15

# Промежуток времени ожидания между проверками текущего Gwei
GAS_DELAY_RANGE = [30, 30]

# Промежуток времени ожидания между проверками поступления средств
WAIT_FOR_DEPOSIT_DELAY_RANGE = [60, 60]

# Диапазон для задержки между транзакциями
TX_DELAY_RANGE = [10, 15]

# Стартовая сеть для вольюм и manual bridge (варианты: arbitrum, base, bsc, ethereum, linea, optimism, polygon, zkera).
# Если этот параметр пуст для вольюм мода, то стартовая сеть будет выбрана случайно из CHAINS_TO_VOLUME
START_CHAIN = "base"

# Укажите сеть в которой модуль должен завершить свою работу, так как для вармапа в любом случае на последней транзакции
# не будет возможным подобрать сеть назначения или если вам важно в какой сети окончится прогрев, необходимо заполнить
# этот параметр. Если для вас это не имеет значения в вармапе, то оставьте поле пустым.
# Учитывается в ВАРМАПЕ, MANUAL BRIDGE и COLLECTOR
# Варианты сетей: arbitrum, base, bsc, ethereum, linea, optimism, polygon, zkera
FINISH_CHAIN = "arbitrum"

# Бридж всего баланса (True/False). Учитывается в ВАРМАПЕ, ВОЛЬЮМЕ и MANUAL BRIDGE. В коллекторе он всегда True
BRIDGE_FULL_BALANCE = True

# Настройка диапазона процента баланса от нативного токена для бриджа. Учитывается в ВАРМАПЕ и MANUAL BRIDGE
BRIDGE_PERCENTAGE_RANGE = [45, 50]

# Ручной режим на вывод и отправку окх, если False, то в начале и по окончанию модуля на кошельке
# потребуется ввести число, обозначающее сколько нативного токена будет выведено или отправлено на okx
# (если 0, тогда вывода с кошелька не будет). Учитывается в ВАРМАПЕ и ВОЛЬЮМЕ
MANUAL_TRANSFERS_MODE = False

"""
НАСТРОЙКИ ПРОГРЕВА
"""
# Настройка кол-ва бриджей для прогрева аккаунтов
ARBITRUM_BRIDGE_COUNT = [0, 1]
BASE_BRIDGE_COUNT = [0, 1]
BSC_BRIDGE_COUNT = [0, 1]
OPTIMISM_BRIDGE_COUNT = [0, 1]
POLYGON_BRIDGE_COUNT = [0, 1]
ETHEREUM_BRIDGE_COUNT = [0, 1]
LINEA_BRIDGE_COUNT = [0, 1]
ZKERA_BRIDGE_COUNT = [0, 1]

"""
НАСТРОЙКА VOLUME MODE
"""
# Сети, которые будут участвовать в вольюме, начиная от START_CHAIN будет выбрана следующая сеть из этого списка
# Варианты сетей: arbitrum, base, bsc, ethereum, linea, optimism, polygon, zkera
CHAINS_TO_VOLUME = ["arbitrum", "base", "linea", "optimism"]

# Промежуток необходимого объема для кошелька (в $)
VOLUME_GOAL_RANGE = [100, 110]

# Настройка диапазона процента баланса от токена для бриджа
VOLUME_BRIDGE_PERCENTAGE_RANGE = [60, 65]

# Промежуток количества нативного токена, которое будет оставлено в сети при выводе на OKX
AMOUNT_TO_LEAVE_RANGE = [0.0001, 0.0002]

# Промежуток задержки между кошельками
WALLET_DELAY_RANGE = [20, 30]

"""
НАСТРОЙКА OKX
"""
# Нужно ли выводить с окх (будет учитываться в вармапе и вольюме)
USE_OKX_WITHDRAW = True

# Промежуток количества нативного токена для вывода с OKX
OKX_WITHDRAW_AMOUNT_RANGE = [0.005, 0.01]

# API ключ от OKX.
OKX_API_KEY = ""

# Секрет от API ключа от OKX
OKX_API_SECRET = ""

# Пароль от API ключа от OKX
OKX_API_PASSWORD = ""

"""
НАСТРОЙКА ПРОКСИ
----------------
Если вы используете мобильные прокси, то в файле data/proxies.txt нужно указать прокси только ОДИН раз на первой строке.
"""
USE_MOBILE_PROXY = False

# Ссылка на смену IP
PROXY_CHANGE_IP_URL = ""

"""
НАСТРОЙКА ЛОГОВ В ТЕЛЕГРАММ
"""

TG_TOKEN = ""

TG_IDS = []

USE_TG_BOT = False
