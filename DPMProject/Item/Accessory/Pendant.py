from Core.Enchant.BonusOption import BonusOptionSlot
from Core.Enchant.Potential import PotentialOptionSlot
from Core.Enchant.Scroll import UpgradeScrolls
from Core.Server import GameServer
from Item.ItemGroup import Pendant
from Core.SpecElements import CoreStat, SpecVector
from Item.ItemSet import ItemSetEnum
from Core.ReqLevel import ReqLevel
from enum import Enum

class PendantUpgradeChance(Enum):
    Dominator = 6
    Daybreak = 6
    Suffering = 6

class DominatorPendant(Pendant):
    def __init__(
            self, 
            potentialOptionList: list[PotentialOptionSlot], 
            optionslot: BonusOptionSlot, 
            upgrade_history: list[UpgradeScrolls], 
            starforce: int, 
            additionalPotentialOptionList: list[PotentialOptionSlot] = None, 
            server=GameServer.NormalServer
            ):
        
        self.ItemName = "도미네이터 펜던트"
        self.RequiredLevel = ReqLevel.Lv140.value

        stat = SpecVector()
        stat[CoreStat.STAT_STR] = 20
        stat[CoreStat.STAT_DEX] = 20
        stat[CoreStat.STAT_INT] = 20
        stat[CoreStat.STAT_LUK] = 20
        stat[CoreStat.STAT_HP_PERCENTAGE] = 10
        stat[CoreStat.STAT_MP_PERCENTAGE] = 10
        stat[CoreStat.ATTACK_PHYSICAL] = 3
        stat[CoreStat.ATTACK_SPELL] = 3

        self.ItemBasicStat = stat

        self.UpgradeChance = PendantUpgradeChance.Dominator.value
        self.BelongedItemSet = ItemSetEnum.BossAccessory

        Pendant.__init__(
            self=self,
            itemName = self.ItemName, 
            itemBasicStat= stat, 
            requiredLevel= self.RequiredLevel,
            potentialOptionList = potentialOptionList, 
            optionslot=optionslot, 
            starforce=starforce, 
            upgrade_history=upgrade_history, 
            upgrade_chance=self.UpgradeChance,
            additionalPotentialOptionList=additionalPotentialOptionList, 
            itemset=self.BelongedItemSet,
            server=server,
            )
        
class DayBreakPendant(Pendant):
    def __init__(
            self, 
            potentialOptionList: list[PotentialOptionSlot], 
            optionslot: BonusOptionSlot, 
            upgrade_history: list[UpgradeScrolls], 
            starforce: int, 
            additionalPotentialOptionList: list[PotentialOptionSlot] = None, 
            server=GameServer.NormalServer
            ):
        
        self.ItemName = "데이브레이크 펜던트"
        self.RequiredLevel = ReqLevel.Lv140.value

        stat = SpecVector()
        stat[CoreStat.STAT_STR] = 8
        stat[CoreStat.STAT_DEX] = 8
        stat[CoreStat.STAT_INT] = 8
        stat[CoreStat.STAT_LUK] = 8
        stat[CoreStat.STAT_HP_PERCENTAGE] = 5
        stat[CoreStat.ATTACK_PHYSICAL] = 2
        stat[CoreStat.ATTACK_SPELL] = 2

        self.ItemBasicStat = stat

        self.UpgradeChance = PendantUpgradeChance.Daybreak.value
        self.BelongedItemSet = ItemSetEnum.DawnBoss

        Pendant.__init__(
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
        
class SourceOfSuffering(Pendant):
    def __init__(
            self, 
            potentialOptionList: list[PotentialOptionSlot], 
            optionslot: BonusOptionSlot, 
            upgrade_history: list[UpgradeScrolls], 
            starforce: int, 
            additionalPotentialOptionList: list[PotentialOptionSlot] = None, 
            server=GameServer.NormalServer
            ):
        
        self.ItemName = "고통의 근원"
        self.RequiredLevel = ReqLevel.Lv160.value

        stat = SpecVector()
        stat[CoreStat.STAT_STR] = 10
        stat[CoreStat.STAT_DEX] = 10
        stat[CoreStat.STAT_INT] = 10
        stat[CoreStat.STAT_LUK] = 10
        stat[CoreStat.STAT_HP_PERCENTAGE] = 5
        stat[CoreStat.ATTACK_PHYSICAL] = 3
        stat[CoreStat.ATTACK_SPELL] = 3

        self.ItemBasicStat = stat

        self.UpgradeChance = PendantUpgradeChance.Suffering.value
        self.BelongedItemSet = ItemSetEnum.PitchedBoss

        Pendant.__init__(
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