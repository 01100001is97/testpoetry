from Core.Enchant.BonusOption import BonusOptionSlot
from Core.Enchant.Potential import PotentialOptionSlot
from Core.Enchant.Scroll import UpgradeScrolls
from Core.Server import GameServer
from Item.ItemGroup import EyeAccessory
from Core.SpecElements import CoreStat, SpecVector
from Item.ItemSet import ItemSetEnum
from Core.ReqLevel import ReqLevel
from enum import Enum

class EyeAccessoryUpgradeChance(Enum):
    PapulatusMark = 6
    Berserked = 4

class PapulatusMark(EyeAccessory):
    def __init__(
            self, 
            potentialOptionList: list[PotentialOptionSlot], 
            optionslot: BonusOptionSlot, 
            upgrade_history: list[UpgradeScrolls], 
            starforce: int, 
            additionalPotentialOptionList: list[PotentialOptionSlot] = None, 
            server=GameServer.NormalServer
            ):
        
        self.ItemName = "파풀라투스 마크"
        self.RequiredLevel = ReqLevel.Lv140.value

        stat = SpecVector()
        stat[CoreStat.STAT_STR] = 8
        stat[CoreStat.STAT_DEX] = 8
        stat[CoreStat.STAT_INT] = 8
        stat[CoreStat.STAT_LUK] = 8
        stat[CoreStat.ATTACK_PHYSICAL] = 1
        stat[CoreStat.ATTACK_SPELL] = 1

        self.ItemBasicStat = stat

        self.UpgradeChance = EyeAccessoryUpgradeChance.PapulatusMark.value
        self.BelongedItemSet = ItemSetEnum.BossAccessory

        EyeAccessory.__init__(
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
        
class Berserked(EyeAccessory):
    def __init__(
            self, 
            potentialOptionList: list[PotentialOptionSlot], 
            optionslot: BonusOptionSlot, 
            upgrade_history: list[UpgradeScrolls], 
            starforce: int, 
            additionalPotentialOptionList: list[PotentialOptionSlot] = None, 
            server=GameServer.NormalServer
            ):
        
        self.ItemName = "마력이 깃든 안대"
        self.RequiredLevel = ReqLevel.Lv160.value

        stat = SpecVector()
        stat[CoreStat.STAT_STR] = 15
        stat[CoreStat.STAT_DEX] = 15
        stat[CoreStat.STAT_INT] = 15
        stat[CoreStat.STAT_LUK] = 15
        stat[CoreStat.ATTACK_PHYSICAL] = 3
        stat[CoreStat.ATTACK_SPELL] = 3

        self.ItemBasicStat = stat

        self.UpgradeChance = EyeAccessoryUpgradeChance.Berserked.value
        self.BelongedItemSet = ItemSetEnum.PitchedBoss

        EyeAccessory.__init__(
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