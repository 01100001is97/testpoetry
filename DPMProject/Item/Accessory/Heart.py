from Core.Enchant.BonusOption import BonusOptionSlot
from Core.Enchant.Potential import PotentialOptionSlot, PotentialEnum, PotentialGrade
from Core.Enchant.Scroll import UpgradeScrolls
from Core.Job import JobType
from Core.Server import GameServer
from Item.ItemGroup import Heart
from Item.ItemSet import ItemSet
from Core.ReqLevel import ReqLevel
from Core.SpecElements import CoreStat, SpecVector
from enum import Enum

class HeartUpgradeChance(Enum):
    Fairy = 10

class FairyHeart(Heart):
    def __init__(
            self, 
            potentialOptionList: list[PotentialOptionSlot], 
            upgrade_history: list[UpgradeScrolls], 
            starforce: int, 
            additionalPotentialOptionList: list[PotentialOptionSlot] = None, 
            server=GameServer.NormalServer
    ):
        starforce = min(starforce, 8)
        
        self.ItemName = "페어리 하트"
        self.RequiredLevel = ReqLevel.Lv100.value

        stat = SpecVector()
        stat[CoreStat.STAT_HP] = 100

        self.UpgradeChance = HeartUpgradeChance.Fairy.value

        Heart.__init__(
            self=self,
            itemName=self.ItemName,
            requiredLevel=self.RequiredLevel,
            itemBasicStat=stat,
            potentialOptionList=potentialOptionList,
            upgrade_history=upgrade_history,
            upgrade_chance=self.UpgradeChance,
            starforce=starforce,
            additionalPotentialOptionList=additionalPotentialOptionList,
            server=server
        )

class BlackHeart(Heart):
    def __init__(
            self, 
            server=GameServer.NormalServer
            ):
        self.ItemName="블랙 하트"
        # 블랙하트 레벨 제한은 100이지만, 편의를 위해 130으로 설정
        self.RequiredLevel = ReqLevel.Lv120.value
        stat = SpecVector()
        stat[CoreStat.STAT_STR] = 10
        stat[CoreStat.STAT_DEX] = 10
        stat[CoreStat.STAT_INT] = 10
        stat[CoreStat.STAT_LUK] = 10
        stat[CoreStat.STAT_HP] = 100
        
        opt1 = PotentialOptionSlot(option=PotentialEnum.BossDamage, grade=PotentialGrade.Unique, isadditional=False)
        opt2 = PotentialOptionSlot(option=PotentialEnum.IgnoreGuard, grade=PotentialGrade.Unique, isadditional=False)
        
        optionlist = [opt1,opt2]

        upgradelist = []
        self.UpgradeChance = 11
        for i in range(0,self.UpgradeChance):
            upgradelist.append(UpgradeScrolls().Heart.BlackHeart)

        
        self.StarforceLevel = 15
        self.BelongedItemSet = ItemSet.PitchedBoss

        Heart.__init__(
            self=self,
            itemName=self.ItemName,
            requiredLevel=self.RequiredLevel,
            itemBasicStat=stat,
            potentialOptionList=optionlist,
            upgrade_history=upgradelist,
            upgrade_chance=self.UpgradeChance,
            starforce=self.StarforceLevel,
            itemset=self.BelongedItemSet,
            additionalPotentialOptionList=None,
            server=server
        )