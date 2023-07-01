from Core.Job import JobType
from Item.Accessory.Badge import CristalVentusBadge
from Item.Accessory.Medal import ChaosVellumCrusher, SevenDayMonsterParker
from Item.Symbol.AuthenticSymbol import AuthenticSymbol
from Item.Symbol.ArcaneSymbol import ArcaneSymbol
from Item.Cash.BlackLabel import *
from Item.Cash.MasterLabel import *
from Item.CharacterTitle.Title import KingOfRootAbyss, YetiPinkBean

# 크리스탈 웬투스 뱃지
VentusBadge = CristalVentusBadge()

# 훈장(메달)
SevendaysMedal = SevenDayMonsterParker()
ChaosVellum = ChaosVellumCrusher()

# 아케인 심볼
# 인트
VanishingJourneySymbol_int_20 = ArcaneSymbol([JobType.Magician],symbollevel=20)
ChuChuSymbol_int_20 = ArcaneSymbol([JobType.Magician],symbollevel=20)
LacheleinSymbol_int_20 = ArcaneSymbol([JobType.Magician],symbollevel=20)
ArcanaSymbol_int_20 = ArcaneSymbol([JobType.Magician],symbollevel=20)
MorassSymbol_int_20 = ArcaneSymbol([JobType.Magician],symbollevel=20)
EsferaSymbol_int_20 = ArcaneSymbol([JobType.Magician],symbollevel=20)

ArcaneSymbols_int = [
    VanishingJourneySymbol_int_20,
    ChuChuSymbol_int_20,
    LacheleinSymbol_int_20,
    ArcanaSymbol_int_20,
    MorassSymbol_int_20,
    EsferaSymbol_int_20
]

# 어센틱 심볼
CerniumSymbol_int_11 = AuthenticSymbol([JobType.Magician], symbolLevel=11)
HotelArcsSymbol_int_7 = AuthenticSymbol([JobType.Magician], symbolLevel=7)
DowonSymbol_int_3 = AuthenticSymbol([JobType.Magician], symbolLevel=3)

AuthSymbols_int = [
    CerniumSymbol_int_11,
    HotelArcsSymbol_int_7,
    DowonSymbol_int_3    
]

# 덱스
# 아케인 심볼
VanishingJourneySymbol_dex_20 = ArcaneSymbol([JobType.Bowman],symbollevel=20)
ChuChuSymbol_dex_20 = ArcaneSymbol([JobType.Bowman],symbollevel=20)
LacheleinSymbol_dex_20 = ArcaneSymbol([JobType.Bowman],symbollevel=20)
ArcanaSymbol_dex_20 = ArcaneSymbol([JobType.Bowman],symbollevel=20)
MorassSymbol_dex_20 = ArcaneSymbol([JobType.Bowman],symbollevel=20)
EsferaSymbol_dex_20 = ArcaneSymbol([JobType.Bowman],symbollevel=20)

ArcaneSymbols_dex = [
    VanishingJourneySymbol_dex_20,
    ChuChuSymbol_dex_20,
    LacheleinSymbol_dex_20,
    ArcanaSymbol_dex_20,
    MorassSymbol_dex_20,
    EsferaSymbol_dex_20
]

# 어센틱 심볼
CerniumSymbol_dex_11 = AuthenticSymbol([JobType.Bowman], symbolLevel=11)
HotelArcsSymbol_dex_7 = AuthenticSymbol([JobType.Bowman], symbolLevel=7)
DowonSymbol_dex_3 = AuthenticSymbol([JobType.Bowman], symbolLevel=3)

AuthSymbols_dex = [
    CerniumSymbol_dex_11,
    HotelArcsSymbol_dex_7,
    DowonSymbol_dex_3    
]


## 캐시 코디장비 인스턴스 ##
blacklabel_weapon = BlackLabelWeapon()
blacklabel_cap = BlackLabelCap()
blacklabel_cape = BlackLabelCape()
blacklabel_shoes = BlacklabelShoes()
blacklabel_clothes = BlackLabelClothes()

Blacklabels = [
    blacklabel_cap,
    blacklabel_cape,
    blacklabel_shoes,
    blacklabel_clothes
]

# 칭호
KOR = KingOfRootAbyss()
Yeping = YetiPinkBean()