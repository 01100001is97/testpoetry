from Core.Enchant.BonusOption import BonusOptionSlot
from Core.Enchant.Potential import PotentialOptionSlot
from Core.Enchant.Scroll import UpgradeScrolls
from Core.Job import JobType
from Core.Server import GameServer
from Item.ItemGroup import Shoulder
from Core.SpecElements import CoreStat, SpecVector
from Item.ItemSet import ItemSet
from Core.ReqLevel import ReqLevel
from enum import Enum

class ShoulderUpgradeChance(Enum):
    Meister = 2
    Absolabs = 2
    Arcane = 2

class MeisterShoulder(Shoulder):
    def __init__(
            self, 
            itemName: str, 
            potentialOptionList: list[PotentialOptionSlot], 
            starforce: int, 
            upgrade_history: list[UpgradeScrolls], 
            additionalPotentialOptionList: list[PotentialOptionSlot] = None, 
            server=GameServer.NormalServer
    ):
        self.ItemName = "마이스터 숄더"
        self.RequiredLevel = ReqLevel.Lv140.value
        self.BelongedItemSet = ItemSet.Meister
        self.RequiredJobType = [e for e in JobType]

        stat = SpecVector()
        stat[CoreStat.STAT_STR] = 13
        stat[CoreStat.STAT_DEX] = 13
        stat[CoreStat.STAT_INT] = 13
        stat[CoreStat.STAT_LUK] = 13
        stat[CoreStat.ATTACK_PHYSICAL] = 9
        stat[CoreStat.ATTACK_SPELL] = 9

        self.UpgradeChance = ShoulderUpgradeChance.Meister.value

        Shoulder.__init__(
            self=self,
            itemName=itemName,
            requiredLevel=self.RequiredLevel,
            requiredJobType=self.RequiredJobType,
            itemBasicStat=stat,
            potentialOptionList=potentialOptionList,
            upgrade_history=upgrade_history,
            upgrade_chance=self.UpgradeChance,
            starforce=starforce,
            itemset=self.BelongedItemSet,
            additionalPotentialOptionList=additionalPotentialOptionList,
            server=server
        )

class AbsolabsShoulder(Shoulder):
    def __init__(
            self,
            itemName: str,
            requiredJobType: list[JobType],
            potentialOptionList: list[PotentialOptionSlot], 
            starforce: int, 
            upgrade_history: list[UpgradeScrolls], 
            additionalPotentialOptionList: list[PotentialOptionSlot] = None, 
            server=GameServer.NormalServer
    ):
        self.RequiredLevel = ReqLevel.Lv160.value
        self.BelongedItemSet = ItemSet.Absolabs

        stat = SpecVector()
        stat[CoreStat.STAT_STR] = 14
        stat[CoreStat.STAT_DEX] = 14
        stat[CoreStat.STAT_INT] = 14
        stat[CoreStat.STAT_LUK] = 14
        stat[CoreStat.ATTACK_PHYSICAL] = 10
        stat[CoreStat.ATTACK_SPELL] = 10

        self.UpgradeChance = ShoulderUpgradeChance.Absolabs.value

        Shoulder.__init__(
            self=self,
            itemName=itemName,
            requiredLevel=self.RequiredLevel,
            requiredJobType=requiredJobType,
            itemBasicStat=stat,
            potentialOptionList=potentialOptionList,
            upgrade_history=upgrade_history,
            upgrade_chance=self.UpgradeChance,
            starforce=starforce,
            itemset=self.BelongedItemSet,
            additionalPotentialOptionList=additionalPotentialOptionList,
            server=server
        )

class ArcaneShadeShoulder(Shoulder):
    def __init__(
            self,
            itemName: str,
            requiredJobType: list[JobType],
            potentialOptionList: list[PotentialOptionSlot], 
            starforce: int, 
            upgrade_history: list[UpgradeScrolls], 
            additionalPotentialOptionList: list[PotentialOptionSlot] = None, 
            server=GameServer.NormalServer
    ):
        
        self.RequiredLevel = ReqLevel.Lv200.value
        self.BelongedItemSet = ItemSet.ArcaneShade

        stat = SpecVector()
        stat[CoreStat.STAT_STR] = 35
        stat[CoreStat.STAT_DEX] = 35
        stat[CoreStat.STAT_INT] = 35
        stat[CoreStat.STAT_LUK] = 35
        stat[CoreStat.ATTACK_PHYSICAL] = 20
        stat[CoreStat.ATTACK_SPELL] = 20

        self.UpgradeChance = ShoulderUpgradeChance.Arcane.value

        Shoulder.__init__(
            self=self,
            itemName=itemName,
            requiredLevel=self.RequiredLevel,
            requiredJobType=requiredJobType,
            itemBasicStat=stat,
            potentialOptionList=potentialOptionList,
            upgrade_history=upgrade_history,
            upgrade_chance=self.UpgradeChance,
            starforce=starforce,
            itemset=self.BelongedItemSet,
            additionalPotentialOptionList=additionalPotentialOptionList,
            server=server
        )

class ArcaneShadeMageShoulder(ArcaneShadeShoulder):
    def __init__(
            self,
            potentialOptionList: list[PotentialOptionSlot], 
            starforce: int, 
            upgrade_history: list[UpgradeScrolls], 
            additionalPotentialOptionList: list[PotentialOptionSlot] = None, 
            server=GameServer.NormalServer
    ):
        self.ItemName = "아케인셰이드 메이지숄더"
        self.RequiredJobType = [JobType.Magician]
        

        ArcaneShadeShoulder.__init__(
            self=self,
            itemName=self.ItemName,
            requiredJobType=self.RequiredJobType,
            potentialOptionList=potentialOptionList,
            starforce=starforce,
            upgrade_history=upgrade_history,
            additionalPotentialOptionList=additionalPotentialOptionList,
            server=server
        )