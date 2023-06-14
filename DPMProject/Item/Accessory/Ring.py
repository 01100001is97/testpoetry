from Core.Server import GameServer
from Core.SpecElements import CoreStat, SpecVector
from Core.Enchant.Potential import PotentialOptionSlot
from Core.Enchant.Scroll import UpgradeScrolls
from Core.Server import GameServer
from Item.ItemGroup import Ring
from Item.ItemSet import ItemSet
from Core.ReqLevel import ReqLevel
from enum import Enum

class RingUpgradeChance(Enum):
    Meister = 2
    Guardian = 3
    Endless = 3
    Event = 0
    Seed = 0

class MeisterRing(Ring):
    def __init__(
            self, 
            potentialOptionList: list[PotentialOptionSlot],
            upgrade_history: list[UpgradeScrolls], 
            starforce: int, 
            additionalPotentialOptionList: list[PotentialOptionSlot] = None, 
            server=GameServer.NormalServer
            ):
        
        self.ItemName = "마이스터 링"
        self.RequiredLevel = ReqLevel.Lv140.value

        stat = SpecVector()
        stat[CoreStat.STAT_STR] = 5
        stat[CoreStat.STAT_DEX] = 5
        stat[CoreStat.STAT_INT] = 5
        stat[CoreStat.STAT_LUK] = 5
        stat[CoreStat.STAT_HP] = 200
        stat[CoreStat.STAT_MP] = 200
        stat[CoreStat.ATTACK_PHYSICAL] = 1
        stat[CoreStat.ATTACK_SPELL] = 1

        self.ItemBasicStat = stat

        self.UpgradeChance = RingUpgradeChance.Meister.value
        self.BelongedItemSet = ItemSet.Meister

        Ring.__init__(
            self=self,
            itemName = self.ItemName, 
            itemBasicStat= stat, 
            requiredLevel=self.RequiredLevel,
            potentialOptionList = potentialOptionList, 
            starforce=starforce, 
            upgrade_history=upgrade_history, 
            upgrade_chance=self.UpgradeChance,
            additionalPotentialOptionList=additionalPotentialOptionList, 
            itemset=self.BelongedItemSet,
            server=server,
            )

class GuardianAngelRing(Ring):
    def __init__(
            self, 
            potentialOptionList: list[PotentialOptionSlot], 
            upgrade_history: list[UpgradeScrolls], 
            starforce: int, 
            additionalPotentialOptionList: list[PotentialOptionSlot] = None, 
            server=GameServer.NormalServer
            ):
        
        self.ItemName = "가디언 엔젤 링"
        self.RequiredLevel = ReqLevel.Lv160.value
        self.UpgradeChance = RingUpgradeChance.Guardian.value
        self.BelongedItemSet = ItemSet.DawnBoss

        stat = SpecVector()
        stat[CoreStat.STAT_STR] = 5
        stat[CoreStat.STAT_DEX] = 5
        stat[CoreStat.STAT_INT] = 5
        stat[CoreStat.STAT_LUK] = 5
        stat[CoreStat.STAT_HP] = 200
        stat[CoreStat.STAT_MP] = 200
        stat[CoreStat.ATTACK_PHYSICAL] = 2
        stat[CoreStat.ATTACK_SPELL] = 2

        self.ItemBasicStat = stat

        Ring.__init__(
            self=self,
            itemName = self.ItemName, 
            itemBasicStat= stat, 
            requiredLevel=self.RequiredLevel,
            potentialOptionList = potentialOptionList, 
            starforce=starforce, 
            upgrade_history=upgrade_history, 
            upgrade_chance=self.UpgradeChance,
            additionalPotentialOptionList=additionalPotentialOptionList, 
            itemset=self.BelongedItemSet,
            server=server,
            )

class EndlessTerror(Ring):
    def __init__(
            self, 
            potentialOptionList: list[PotentialOptionSlot], 
            upgrade_history: list[UpgradeScrolls], 
            starforce: int, 
            additionalPotentialOptionList: list[PotentialOptionSlot] = None, 
            server=GameServer.NormalServer
            ):
        
        self.ItemName = "거대한 공포"
        self.RequiredLevel = ReqLevel.Lv200.value

        stat = SpecVector()
        stat[CoreStat.STAT_STR] = 5
        stat[CoreStat.STAT_DEX] = 5
        stat[CoreStat.STAT_INT] = 5
        stat[CoreStat.STAT_LUK] = 5
        stat[CoreStat.STAT_HP] = 250
        stat[CoreStat.STAT_MP] = 250
        stat[CoreStat.ATTACK_PHYSICAL] = 4
        stat[CoreStat.ATTACK_SPELL] = 4

        self.ItemBasicStat = stat

        self.UpgradeChance = RingUpgradeChance.Endless.value
        self.BelongedItemSet = ItemSet.PitchedBoss

        Ring.__init__(
            self=self,
            itemName = self.ItemName, 
            itemBasicStat= stat, 
            requiredLevel=self.RequiredLevel,
            potentialOptionList = potentialOptionList, 
            starforce=starforce, 
            upgrade_history=upgrade_history, 
            upgrade_chance=self.UpgradeChance,
            additionalPotentialOptionList=additionalPotentialOptionList, 
            itemset=self.BelongedItemSet,
            server=server,
            )

class EventRing(Ring):
    def __init__(
            self, 
            potentialOptionList: list[PotentialOptionSlot], 
            additionalPotentialOptionList: list[PotentialOptionSlot] = None, 
            server=GameServer.NormalServer
    ):
        self.ItemName = "이벤트 링"
        self.RequiredLevel = ReqLevel.Lv120.value

        stat = SpecVector()
        stat[CoreStat.STAT_STR] = 40
        stat[CoreStat.STAT_DEX] = 40
        stat[CoreStat.STAT_INT] = 40
        stat[CoreStat.STAT_LUK] = 40
        stat[CoreStat.STAT_HP] = 4000
        stat[CoreStat.STAT_MP] = 4000
        stat[CoreStat.ATTACK_PHYSICAL] = 25
        stat[CoreStat.ATTACK_SPELL] = 25

        self.ItemBasicStat = stat

        self.UpgradeChance = RingUpgradeChance.Event.value
        self.BelongedItemSet = None

        Ring.__init__(
            self=self,
            itemName = self.ItemName, 
            itemBasicStat= stat, 
            requiredLevel=self.RequiredLevel,
            potentialOptionList = potentialOptionList, 
            starforce=0, 
            upgrade_history=[], 
            upgrade_chance=self.UpgradeChance,
            additionalPotentialOptionList=additionalPotentialOptionList, 
            itemset=self.BelongedItemSet,
            server=server,
            )


class SeedRing(Ring):
    def __init__(
            self, 
            server=GameServer.NormalServer
    ):
        self.ItemName = "시드링"
        self.RequiredLevel = ReqLevel.Lv110.value

        stat = SpecVector()
        stat[CoreStat.STAT_STR] = 4
        stat[CoreStat.STAT_DEX] = 4
        stat[CoreStat.STAT_INT] = 4
        stat[CoreStat.STAT_LUK] = 4
        stat[CoreStat.ATTACK_PHYSICAL] = 4
        stat[CoreStat.ATTACK_SPELL] = 4

        self.ItemBasicStat = stat

        self.UpgradeChance = RingUpgradeChance.Seed.value
        self.BelongedItemSet = None

        Ring.__init__(
            self=self,
            itemName = self.ItemName, 
            itemBasicStat= stat, 
            requiredLevel=self.RequiredLevel,
            potentialOptionList = [], 
            starforce=0, 
            upgrade_history=[], 
            upgrade_chance=self.UpgradeChance,
            additionalPotentialOptionList=[], 
            itemset=self.BelongedItemSet,
            server=server,
            )
