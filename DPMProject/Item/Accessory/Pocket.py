from Core.Enchant.BonusOption import BonusOptionSlot
from Core.Enchant.Potential import PotentialOptionSlot
from Core.Enchant.Scroll import UpgradeScrolls
from Core.Job import JobType
from Core.Server import GameServer
from Item.ItemGroup import Pocket
from Core.SpecElements import CoreStat, SpecVector
from Item.ItemSet import ItemSet
from Core.ReqLevel import ReqLevel


class PinkHolyCup(Pocket):
    def __init__(
            self, 
            optionslot: BonusOptionSlot, 
            server=GameServer.NormalServer
            ):
        self.ItemName = "핑크빛 성배"
        self.RequiredLevel = ReqLevel.Lv140.value

        stat = SpecVector()
        stat[CoreStat.STAT_STR] = 5
        stat[CoreStat.STAT_DEX] = 5
        stat[CoreStat.STAT_INT] = 5
        stat[CoreStat.STAT_LUK] = 5
        stat[CoreStat.STAT_HP] = 50
        stat[CoreStat.STAT_MP] = 50
        stat[CoreStat.ATTACK_PHYSICAL] = 5
        stat[CoreStat.ATTACK_SPELL] = 5

        self.ItemBasicStat = stat
        self.BelongedItemSet = ItemSet.BossAccessory

        Pocket.__init__(
            self=self,
            itemName = self.ItemName, 
            requiredLevel=self.RequiredLevel,
            itemBasicStat= stat, 
            optionslot=optionslot, 
            itemset=self.BelongedItemSet,
            server=server,
            )

class CursedRedSpellbook(Pocket):
    def __init__(
            self, 
            potentialOptionList: list[PotentialOptionSlot], 
            optionslot: BonusOptionSlot, 
            server=GameServer.NormalServer
            ):
        
        self.ItemName = "저주받은 적의 마도서"
        self.RequiredLevel = ReqLevel.Lv160.value

        stat = SpecVector()
        stat[CoreStat.STAT_STR] = 20
        stat[CoreStat.STAT_DEX] = 10
        stat[CoreStat.STAT_INT] = 10
        stat[CoreStat.STAT_LUK] = 10
        stat[CoreStat.STAT_HP] = 100
        stat[CoreStat.STAT_MP] = 100
        stat[CoreStat.ATTACK_PHYSICAL] = 10
        stat[CoreStat.ATTACK_SPELL] = 10

        self.ItemBasicStat = stat
        self.BelongedItemSet = ItemSet.PitchedBoss

        Pocket.__init__(
            self=self,
            itemName = self.ItemName, 
            itemBasicStat= stat,
            requiredLevel=self.RequiredLevel, 
            optionslot=optionslot, 
            itemset=self.BelongedItemSet,
            server=server,
            )

class CursedGreenSpellbook(Pocket):
    def __init__(
            self, 
            potentialOptionList: list[PotentialOptionSlot], 
            optionslot: BonusOptionSlot, 
            server=GameServer.NormalServer
            ):
        
        self.ItemName = "저주받은 녹의 마도서"
        self.RequiredLevel = ReqLevel.Lv160.value

        stat = SpecVector()
        stat[CoreStat.STAT_STR] = 10
        stat[CoreStat.STAT_DEX] = 20
        stat[CoreStat.STAT_INT] = 10
        stat[CoreStat.STAT_LUK] = 10
        stat[CoreStat.STAT_HP] = 100
        stat[CoreStat.STAT_MP] = 100
        stat[CoreStat.ATTACK_PHYSICAL] = 10
        stat[CoreStat.ATTACK_SPELL] = 10

        self.ItemBasicStat = stat
        self.BelongedItemSet = ItemSet.PitchedBoss

        Pocket.__init__(
            self=self,
            itemName = self.ItemName, 
            itemBasicStat= stat,
            requiredLevel=self.RequiredLevel, 
            optionslot=optionslot, 
            itemset=self.BelongedItemSet,
            server=server,
            )

class CursedBlueSpellbook(Pocket):
    def __init__(
            self, 
            potentialOptionList: list[PotentialOptionSlot], 
            optionslot: BonusOptionSlot, 
            server=GameServer.NormalServer
            ):
        
        self.ItemName = "저주받은 청의 마도서"
        self.RequiredLevel = ReqLevel.Lv160.value

        stat = SpecVector()
        stat[CoreStat.STAT_STR] = 10
        stat[CoreStat.STAT_DEX] = 10
        stat[CoreStat.STAT_INT] = 20
        stat[CoreStat.STAT_LUK] = 10
        stat[CoreStat.STAT_HP] = 100
        stat[CoreStat.STAT_MP] = 100
        stat[CoreStat.ATTACK_PHYSICAL] = 10
        stat[CoreStat.ATTACK_SPELL] = 10

        self.ItemBasicStat = stat
        self.BelongedItemSet = ItemSet.PitchedBoss

        Pocket.__init__(
            self=self,
            itemName = self.ItemName, 
            itemBasicStat= stat,
            requiredLevel=self.RequiredLevel, 
            optionslot=optionslot, 
            itemset=self.BelongedItemSet,
            server=server,
            )

class CursedYellowSpellbook(Pocket):
    def __init__(
            self, 
            potentialOptionList: list[PotentialOptionSlot], 
            optionslot: BonusOptionSlot, 
            server=GameServer.NormalServer
            ):
        
        self.ItemName = "저주받은 황의 마도서"
        self.RequiredLevel = ReqLevel.Lv160.value

        stat = SpecVector()
        stat[CoreStat.STAT_STR] = 10
        stat[CoreStat.STAT_DEX] = 10
        stat[CoreStat.STAT_INT] = 10
        stat[CoreStat.STAT_LUK] = 20
        stat[CoreStat.STAT_HP] = 100
        stat[CoreStat.STAT_MP] = 100
        stat[CoreStat.ATTACK_PHYSICAL] = 10
        stat[CoreStat.ATTACK_SPELL] = 10

        self.ItemBasicStat = stat
        self.BelongedItemSet = ItemSet.PitchedBoss

        Pocket.__init__(
            self=self,
            itemName = self.ItemName, 
            itemBasicStat= stat,
            requiredLevel=self.RequiredLevel, 
            optionslot=optionslot, 
            itemset=self.BelongedItemSet,
            server=server,
            )
