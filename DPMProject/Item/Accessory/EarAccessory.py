from Core.Enchant.BonusOption import BonusOptionSlot
from Core.Enchant.Potential import PotentialOptionSlot
from Core.Enchant.Scroll import UpgradeScrolls
from Core.Job import JobType
from Core.Server import GameServer
from Item.ItemGroup import EarAccessory
from Core.SpecElements import CoreStat, SpecVector
from Item.ItemSet import ItemSet
from Core.ReqLevel import ReqLevel
from enum import Enum

class EarRingUpgradeChance(Enum):
    Meister = 7
    Estella = 7
    Commanding = 7

class MeisterEarRings(EarAccessory):
    def __init__(
            self, 
            potentialOptionList: list[PotentialOptionSlot], 
            optionslot: BonusOptionSlot, 
            upgrade_history: list[UpgradeScrolls], 
            starforce: int, 
            additionalPotentialOptionList: list[PotentialOptionSlot] = None, 
            server=GameServer.NormalServer
            ):
        
        self.ItemName = "마이스터 이어링"
        self.RequiredLevel = ReqLevel.Lv140.value

        stat = SpecVector()
        stat[CoreStat.STAT_STR] = 5
        stat[CoreStat.STAT_DEX] = 5
        stat[CoreStat.STAT_INT] = 5
        stat[CoreStat.STAT_LUK] = 5
        stat[CoreStat.STAT_HP] = 500
        stat[CoreStat.STAT_MP] = 500
        stat[CoreStat.ATTACK_PHYSICAL] = 4
        stat[CoreStat.ATTACK_SPELL] = 4

        self.ItemBasicStat = stat

        self.UpgradeChance = EarRingUpgradeChance.Meister.value
        self.BelongedItemSet = ItemSet.Meister

        EarAccessory.__init__(
            self=self,
            itemName = self.ItemName, 
            requiredLevel=self.RequiredLevel,
            itemBasicStat= stat, 
            potentialOptionList = potentialOptionList, 
            optionslot=optionslot, 
            starforce=starforce, 
            upgrade_history=upgrade_history, 
            upgrade_chance=self.UpgradeChance,
            additionalPotentialOptionList=additionalPotentialOptionList, 
            itemset=self.BelongedItemSet,
            server=server,
            )

class EstellaEarRings(EarAccessory):
    def __init__(
            self, 
            potentialOptionList: list[PotentialOptionSlot], 
            optionslot: BonusOptionSlot, 
            upgrade_history: list[UpgradeScrolls], 
            starforce: int, 
            additionalPotentialOptionList: list[PotentialOptionSlot] = None, 
            server=GameServer.NormalServer
            ):
        
        self.ItemName = "에스텔라 이어링"
        self.RequiredLevel = ReqLevel.Lv160.value

        stat = SpecVector()
        stat[CoreStat.STAT_STR] = 7
        stat[CoreStat.STAT_DEX] = 7
        stat[CoreStat.STAT_INT] = 7
        stat[CoreStat.STAT_LUK] = 7
        stat[CoreStat.STAT_HP] = 300
        stat[CoreStat.STAT_MP] = 300
        stat[CoreStat.ATTACK_PHYSICAL] = 2
        stat[CoreStat.ATTACK_SPELL] = 2

        self.ItemBasicStat = stat

        self.UpgradeChance = EarRingUpgradeChance.Estella.value
        self.BelongedItemSet = ItemSet.DawnBoss

        EarAccessory.__init__(
            self=self,
            itemName = self.ItemName, 
            requiredLevel=self.RequiredLevel,
            itemBasicStat= stat, 
            potentialOptionList = potentialOptionList, 
            optionslot=optionslot, 
            starforce=starforce, 
            upgrade_history=upgrade_history, 
            upgrade_chance=self.UpgradeChance,
            additionalPotentialOptionList=additionalPotentialOptionList, 
            itemset=self.BelongedItemSet,
            server=server,
            )
        
class CommandingForceEarRing(EarAccessory):
    def __init__(
            self,
            potentialOptionList: list[PotentialOptionSlot], 
            optionslot: BonusOptionSlot, 
            upgrade_history: list[UpgradeScrolls], 
            starforce: int, 
            additionalPotentialOptionList: list[PotentialOptionSlot] = None, 
            server=GameServer.NormalServer
            ):
        
        self.ItemName = "커맨더 포스 링"
        self.RequiredLevel = ReqLevel.Lv200.value
        self.RequiredJobType = [e for e in JobType]

        stat = SpecVector()
        stat[CoreStat.STAT_STR] = 7
        stat[CoreStat.STAT_DEX] = 7
        stat[CoreStat.STAT_INT] = 7
        stat[CoreStat.STAT_LUK] = 7
        stat[CoreStat.STAT_HP] = 500
        stat[CoreStat.STAT_MP] = 500
        stat[CoreStat.ATTACK_PHYSICAL] = 5
        stat[CoreStat.ATTACK_SPELL] = 5

        self.ItemBasicStat = stat
        self.UpgradeChance = EarRingUpgradeChance.Commanding.value
        self.BelongedItemSet = ItemSet.PitchedBoss

        EarAccessory.__init__(
            self=self,
            itemName = self.ItemName, 
            requiredLevel = self.RequiredLevel, 
            itemBasicStat= stat, 
            potentialOptionList = potentialOptionList, 
            optionslot=optionslot, 
            starforce=starforce, 
            upgrade_history=upgrade_history, 
            upgrade_chance=self.UpgradeChance,
            additionalPotentialOptionList=additionalPotentialOptionList, 
            itemset=self.BelongedItemSet,
            server=server,
            )
