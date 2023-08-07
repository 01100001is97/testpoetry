from Core.Enchant.BonusOption import BonusOptionSlot
from Core.Enchant.Potential import PotentialOptionSlot
from Core.Enchant.Scroll import UpgradeScrolls
from Core.Enchant.SoulWeapon import SoulEnchantOption
from Core.Enchant.StarForce import StarForce
from Core.Job import JobType
from Core.Server import GameServer
from Item.ItemGroup import Weapon
from Core.SpecElements import CoreStat, SpecVector
from Item.ItemSet import ItemSetEnum
from Core.ReqLevel import ReqLevel
from enum import Enum


class WeaponTypeEnum(Enum):
    한손검 = 0
    한손도끼 = 1
    한손둔기 = 2
    두손검 = 3
    두손도끼 = 4
    두손둔기 = 5
    창 = 6
    폴암 = 7
    완드 = 8
    스태프 = 9
    활 = 10
    석궁 = 11
    단검 = 12
    아대 =13
    건 = 14
    너클 =15
    핸드캐논 = 16
    듀얼보우건 = 17
    케인 = 18
    샤이닝로드 = 19
    소울슈터 = 20
    데스페라도 = 21
    에너지소드 = 22
    ESP리미터 =23
    건틀렛리볼버 = 24
    체인 = 25
    매직건틀렛 = 26
    에인션트보우 = 27
    부채 = 28
    튜너 = 29
    브레스슈터 = 30
    태도 = 31
    대검 = 32


class WeaponUpgradeChance(Enum):
    Arcane = 9
    Genesis = 8

class GenesisWeapon(Weapon):
    pass

class ArcaneShadeWeapon(Weapon):
    _itemset: ItemSetEnum
    _RequiredLevel: int
    _upgrade_chance:int
    def __init__(
            self,
            itemName: str,
            requiredJobType: list[JobType],
            itemBasicStat: SpecVector,
            potentialOptionList: list[PotentialOptionSlot],
            optionSlot: BonusOptionSlot,
            upgrade_history: list[UpgradeScrolls],
            starforce: int,
            enchant: SoulEnchantOption,
            additionalPotentialOptionList: list[PotentialOptionSlot] = None,
            server = GameServer.NormalServer
    ):
        self._RequiredLevel = 200
        self._itemset = ItemSetEnum.ArcaneShade
        self._upgrade_chance = WeaponUpgradeChance.Arcane.value

        # 무기류 주스텟, 부스텟 100 고정. 무기 보공30 방무 20 적용
        statSet = self.GetStatSetOfReqiredJob(jobList=requiredJobType)
        for stat in statSet:
            itemBasicStat[stat] = 100

        itemBasicStat[CoreStat.DAMAGE_PERCENTAGE_BOSS] = 30
        itemBasicStat[CoreStat.IGNORE_GUARD_PERCENTAGE] = 20

        Weapon.__init__(
            self=self,
            itemName=itemName,
            requiredLevel=self._RequiredLevel,
            requiredJobType=requiredJobType,
            itemBasicStat=itemBasicStat,
            potentialOptionList=potentialOptionList,
            optionslot=optionSlot,
            upgrade_history=upgrade_history,
            upgrade_chance=self._upgrade_chance,
            starforce=starforce,
            enchant=enchant,
            itemset=self._itemset,
            additionalPotentialOptionList=additionalPotentialOptionList,
            server=server
        )


class ArcaneShadeStaff(ArcaneShadeWeapon):
    _itemName:str
    _requiredJobType: list[JobType]
    

    def __init__(
            self,
            potentialOptionList: list[PotentialOptionSlot],
            optionSlot: BonusOptionSlot,
            upgrade_history: list[UpgradeScrolls],
            starforce: int,
            enchant: SoulEnchantOption,
            additionalPotentialOptionList: list[PotentialOptionSlot] = None,
            server = GameServer.NormalServer
    ):
        self._itemName = "아케인셰이드 스태프"
        self._requiredJobType = [JobType.Magician]
        
        
        weaponBasicATKList = self.BonusOptionDict[ReqLevel.Lv200ArcaneWeapon.value]
        stat = SpecVector()
        stat[CoreStat.ATTACK_SPELL] = weaponBasicATKList[self._weaponbasicATK][WeaponTypeEnum.스태프.value]

        ArcaneShadeWeapon.__init__(
            self=self,
            itemName=self._itemName,
            requiredJobType=self._requiredJobType,
            itemBasicStat=stat,
            potentialOptionList=potentialOptionList,
            optionSlot=optionSlot,
            upgrade_history=upgrade_history,
            starforce=starforce,
            enchant=enchant,
            additionalPotentialOptionList=additionalPotentialOptionList,
            server=server
        )


class ArcaneShadeAncientBow(ArcaneShadeWeapon):
    _itemName:str
    _requiredJobType: list[JobType]

    def __init__(
            self,
            potentialOptionList: list[PotentialOptionSlot],
            optionSlot: BonusOptionSlot,
            upgrade_history: list[UpgradeScrolls],
            starforce: int,
            enchant: SoulEnchantOption,
            additionalPotentialOptionList: list[PotentialOptionSlot] = None,
            server = GameServer.NormalServer
    ):
        self._itemName = "아케인셰이드 에인션트 보우"
        self._requiredJobType = [JobType.Bowman]
        
        
        weaponBasicATKList = self.BonusOptionDict[ReqLevel.Lv200ArcaneWeapon.value]
        stat = SpecVector()
        stat[CoreStat.ATTACK_PHYSICAL] = weaponBasicATKList[self._weaponbasicATK][WeaponTypeEnum.에인션트보우.value]

        ArcaneShadeWeapon.__init__(
            self=self,
            itemName=self._itemName,
            requiredJobType=self._requiredJobType,
            itemBasicStat=stat,
            potentialOptionList=potentialOptionList,
            optionSlot=optionSlot,
            upgrade_history=upgrade_history,
            starforce=starforce,
            enchant=enchant,
            additionalPotentialOptionList=additionalPotentialOptionList,
            server=server
        )

class ArcaneShadeBuchae(ArcaneShadeWeapon):
    _itemName:str
    _requiredJobType: list[JobType]

    def __init__(
            self,
            potentialOptionList: list[PotentialOptionSlot],
            optionSlot: BonusOptionSlot,
            upgrade_history: list[UpgradeScrolls],
            starforce: int,
            enchant: SoulEnchantOption,
            additionalPotentialOptionList: list[PotentialOptionSlot] = None,
            server = GameServer.NormalServer    
        ):
        self._itemName = "아케인셰이드 부채"
        self._requiredJobType = [JobType.Thief]

        weaponBasicATKList = self.BonusOptionDict[ReqLevel.Lv200ArcaneWeapon.value]
        stat = SpecVector()
        stat[CoreStat.ATTACK_PHYSICAL] = weaponBasicATKList[self._weaponbasicATK][WeaponTypeEnum.부채.value]

        ArcaneShadeWeapon.__init__(
            self=self,
            itemName=self._itemName,
            requiredJobType=self._requiredJobType,
            itemBasicStat=stat,
            potentialOptionList=potentialOptionList,
            optionSlot=optionSlot,
            upgrade_history=upgrade_history,
            starforce=starforce,
            enchant=enchant,
            additionalPotentialOptionList=additionalPotentialOptionList,
            server=server
        )
    
        
