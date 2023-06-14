from enum import Enum


class ReqLevel(Enum):
    # 130이하 레벨 제한은 130레벨 표를 따르도록 임시조치함
    Lv100 = 130
    Lv110 = 130
    Lv120 = 130
    Lv130 = 130
    Lv140 = 140
    Lv150 = 150
    Lv160 = 160
    Lv200 = 200
    Lv250 = 250
    Lv200ArcaneWeapon = 211
    Lv200GenesisWeapon = 221
    Lv200Weapon = 201
