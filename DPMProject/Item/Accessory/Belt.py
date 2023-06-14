from Core.Enchant.BonusOption import BonusOptionSlot
from Core.Enchant.Potential import PotentialOptionSlot
from Core.Enchant.Scroll import UpgradeScrolls
from Core.Job import JobType
from Core.Server import GameServer
from Item.ItemGroup import Belt
from Core.SpecElements import CoreStat, SpecVector
from Item.ItemSet import ItemSet
from Core.ReqLevel import ReqLevel
from enum import Enum

class BeltUpgradeChance(Enum):
    Zaqqum = 4
    Dreamy = 4

class EnragedZaqqumBelt(Belt):
    def __init__(
            self, 
            potentialOptionList: list[PotentialOptionSlot], 
            optionslot: BonusOptionSlot, 
            upgrade_history: list[UpgradeScrolls], 
            starforce: int, 
            additionalPotentialOptionList: list[PotentialOptionSlot] = None, 
            server=GameServer.NormalServer
            ):
        
        self.ItemName = "분노한 자쿰의 벨트"
        self.RequiredLevel = ReqLevel.Lv150.value

        stat = SpecVector()
        stat[CoreStat.STAT_STR] = 18
        stat[CoreStat.STAT_DEX] = 18
        stat[CoreStat.STAT_INT] = 18
        stat[CoreStat.STAT_LUK] = 18
        stat[CoreStat.STAT_HP] = 150
        stat[CoreStat.STAT_MP] = 150
        stat[CoreStat.ATTACK_PHYSICAL] = 1
        stat[CoreStat.ATTACK_SPELL] = 1

        self.ItemBasicStat = stat

        self.UpgradeChance = BeltUpgradeChance.Zaqqum.value
        self.BelongedItemSet = ItemSet.BossAccessory

        Belt.__init__(
            self=self,
            itemName = self.ItemName,  
            itemBasicStat= stat, 
            requiredLevel=self.RequiredLevel,
            potentialOptionList = potentialOptionList, 
            optionslot=optionslot, 
            starforce=starforce, 
            upgrade_history=upgrade_history, 
            upgrade_chance=self.UpgradeChance,
            additionalPotentialOptionList=additionalPotentialOptionList, 
            itemset=self.BelongedItemSet,
            server=server,
            )


class DreamyBelt(Belt):
    def __init__(
            self, 
            potentialOptionList: list[PotentialOptionSlot], 
            optionslot: BonusOptionSlot, 
            upgrade_history: list[UpgradeScrolls], 
            starforce: int, 
            additionalPotentialOptionList: list[PotentialOptionSlot] = None, 
            server=GameServer.NormalServer
            ):
        
        self.ItemName = "몽환의 벨트"
        self.RequiredLevel = ReqLevel.Lv200.value

        stat = SpecVector()
        stat[CoreStat.STAT_STR] = 50
        stat[CoreStat.STAT_DEX] = 50
        stat[CoreStat.STAT_INT] = 50
        stat[CoreStat.STAT_LUK] = 50
        stat[CoreStat.STAT_HP] = 150
        stat[CoreStat.STAT_MP] = 150
        stat[CoreStat.ATTACK_PHYSICAL] = 6
        stat[CoreStat.ATTACK_SPELL] = 6

        self.ItemBasicStat = stat

        self.UpgradeChance = BeltUpgradeChance.Dreamy.value
        self.BelongedItemSet = ItemSet.PitchedBoss

        Belt.__init__(
            self=self,
            itemName = self.ItemName, 
            requiredJobType = self.RequiredJobType, 
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
