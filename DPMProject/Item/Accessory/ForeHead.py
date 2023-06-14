from Core.Enchant.BonusOption import BonusOptionSlot
from Core.Enchant.Potential import PotentialOptionSlot
from Core.Enchant.Scroll import UpgradeScrolls
from Core.Job import JobType
from Core.Server import GameServer
from Item.ItemGroup import ForeHead
from Core.SpecElements import CoreStat, SpecVector
from Item.ItemSet import ItemSet
from Core.ReqLevel import ReqLevel
from enum import Enum

class ForeHeadUpgradeChance(Enum):
    TwilightMark = 4
    LooseControl = 6

class TwilightMark(ForeHead):
    def __init__(
            self,
            potentialOptionList: list[PotentialOptionSlot], 
            optionslot: BonusOptionSlot, 
            upgrade_history: list[UpgradeScrolls], 
            starforce: int, 
            additionalPotentialOptionList: list[PotentialOptionSlot] = None, 
            server=GameServer.NormalServer
            ):
        
        self.ItemName = "트와일라이트 마크"
        self.RequiredLevel = ReqLevel.Lv140.value

        stat = SpecVector()
        stat[CoreStat.STAT_STR] = 5
        stat[CoreStat.STAT_DEX] = 5
        stat[CoreStat.STAT_INT] = 5
        stat[CoreStat.STAT_LUK] = 5
        stat[CoreStat.ATTACK_PHYSICAL] = 5
        stat[CoreStat.ATTACK_SPELL] = 5
        

        self.UpgradeChance = ForeHeadUpgradeChance.TwilightMark.value
        self.BelongedItemSet = ItemSet.DawnBoss

        ForeHead.__init__(
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



class LooseControlMachineMark(ForeHead):
    def __init__(
            self,
            potentialOptionList: list[PotentialOptionSlot], 
            optionslot: BonusOptionSlot, 
            upgrade_history: list[UpgradeScrolls], 
            starforce: int, 
            additionalPotentialOptionList: list[PotentialOptionSlot] = None, 
            server=GameServer.NormalServer
            ):
        
        self.ItemName = "루즈 컨트롤 머신 마크"
        self.RequiredLevel = ReqLevel.Lv160.value

        stat = SpecVector()
        stat[CoreStat.STAT_STR] = 10
        stat[CoreStat.STAT_DEX] = 10
        stat[CoreStat.STAT_INT] = 10
        stat[CoreStat.STAT_LUK] = 10
        stat[CoreStat.ATTACK_PHYSICAL] = 10
        stat[CoreStat.ATTACK_SPELL] = 10
        

        self.UpgradeChance = ForeHeadUpgradeChance.LooseControl.value
        self.BelongedItemSet = ItemSet.PitchedBoss

        ForeHead.__init__(
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
