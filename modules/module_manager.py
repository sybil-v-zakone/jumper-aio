from logger import logger
from modules.collector import collector_batch
from modules.database import Database
from modules.manual_bridge import manual_bridge
from modules.volume import volume
from modules.warmup import warmup


async def menu() -> None:
    await greeting()
    module_num = input("Enter a module number: ")
    if module_num == "1":
        Database.create_database()
    if module_num == "2":
        await warmup()
    if module_num == "3":
        await volume()
    if module_num == "4":
        await collector_batch()
    if module_num == "5":
        await manual_bridge()


async def greeting() -> None:
    logger.debug(
        r"""

                  __  '              _ ,.,              ,.,  ' ‘                       _ ‘     
            ,·:'´/::::/'`;·.,        '/:::::/`,           /:::/';       /:¯:'`:*:^:*:´':¯::/'`;‘  
        .:´::::/::::/:::::::`;     /;: :;/:::\         /;:;/:'i‘      /:: :: : : : : : :::/::'/   
       /:;:· '´ ¯¯'`^·-;::::/' ‘  ,´     `;::';       ,´   'i:'i     ,´¯ '` * ^ * ´' ¯   '`;/    ‘
      /·´           _   '`;/‘     i        \::',      ,:    'i:';    '`,                  ,·'   '   
     'i            ;::::'`;*       ;         ';::\ .,_';     ';:'i'      '`*^*'´;       .´         ‘
      `;           '`;:::::'`:,    ';         ';::/::::';     ;':;            .´     .'      _   ' ‘
        `·,           '`·;:::::';   \          \/::::;'      i:/'°        .´      ,'´~:~/:::/`:, 
      ,~:-'`·,           `:;::/'    '\          '`~'´     ,'/          .´      ,'´::::::/:::/:::'i‘
     /:::::::::';           ';/        \                  /          ,'        '*^~·~*'´¯'`·;:/ 
   ,:~·- . -·'´          ,'´           '`,             ;'           /                        ,'/  
   '`·,               , ·'´                `·.,    ,.·´            ';                      ,.´    
        '`*^·–·^*'´'           ‘               ¯         °         '`*^~–––––-·~^'´       

        ___  _  _ ____   / ____ _   _ ___  _ _        _  _     ___  ____ _  _ ____ _  _ ____ 
         |   |\/| |___  /  [__   \_/  |__] | |        |  |       /  |__| |_/  |  | |\ | |___ 
         |  .|  | |___ /   ___]   |   |__] | |___ ___  \/  ___  /__ |  | | \_ |__| | \| |___ 
                                                                                     
1. [DATABASE] Создать базу данных      | Create database
2. [WARMUP] Прогрев кошельков          | Wallets warmup
3. [VOLUME] Набив объемов              | Volume Mode
4. [COLLECTOR] Сборщик токенов         | Collector
5. [MANUAL BRIDGE] Ручной режим        | Manual bridge
"""
    )
