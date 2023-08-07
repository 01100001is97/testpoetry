from Core.Enchant.BonusOption import BonusOptionSlot
from Core.Enchant.Potential import PotentialOptionSlot
from Core.Enchant.Scroll import UpgradeScrolls
from Core.Job import JobType
from Core.Server import GameServer
from Item.ItemGroup import Cap
from Core.SpecElements import CoreStat, SpecVector
from Item.ItemSet import ItemSetEnum
from Core.ReqLevel import ReqLevel
from enum import Enum

CapUpgradeChance = 12

# 파프 모자
class RootAbyssCap(Cap):
    def __init__(
            self, 
            itemName: str, 
            requiredJobType: list[JobType], 
            itemBasicStat: SpecVector, 
            potentialOptionList: list[PotentialOptionSlot], 
            optionslot: BonusOptionSlot, 
            starforce: int, 
            upgrade_history: list[UpgradeScrolls], 
            additionalPotentialOptionList: list[PotentialOptionSlot] = None, 
            server=GameServer.NormalServer
            ):
        
        self.RequiredLevel = ReqLevel.Lv150.value
        self.BelongedItemSet = ItemSetEnum.Rootabyss
        Cap.__init__(
            self=self,
            itemName = itemName, 
            requiredLevel = self.RequiredLevel, 
            requiredJobType = requiredJobType, 
            itemBasicStat= itemBasicStat, 
            potentialOptionList= potentialOptionList, 
            optionslot= optionslot, 
            upgrade_history= upgrade_history, 
            starforce= starforce, 
            itemset= self.BelongedItemSet, 
            additionalPotentialOptionList= additionalPotentialOptionList, 
            server = server
            )

# 전사

# 궁수
class HighnessRangerHat(RootAbyssCap):
    def __init__(
            self,
            potentialOptionList: list[PotentialOptionSlot], 
            optionslot: BonusOptionSlot, 
            starforce: int, 
            upgrade_history: list[UpgradeScrolls], 
            additionalPotentialOptionList: list[PotentialOptionSlot] = None, 
            server=GameServer.NormalServer
            ):
        
        self.ItemName = "하이네스 레인저햇"
        self.RequiredJobType = [JobType.Bowman]
        stat = SpecVector()
        stat[CoreStat.STAT_DEX] = 40  # INT -> DEX
        stat[CoreStat.STAT_STR] = 40
        stat[CoreStat.STAT_HP] = 360
        stat[CoreStat.STAT_MP] = 360
        stat[CoreStat.ATTACK_PHYSICAL] = 2  # ATTACK_SPELL -> ATTACK_PHYSICAL
        stat[CoreStat.IGNORE_GUARD_PERCENTAGE] = 10

        RootAbyssCap.__init__(
            self=self,
            itemName = self.ItemName, 
            requiredJobType = self.RequiredJobType, 
            itemBasicStat= stat, 
            potentialOptionList = potentialOptionList, 
            optionslot=optionslot, 
            starforce=starforce, 
            upgrade_history=upgrade_history, 
            additionalPotentialOptionList=additionalPotentialOptionList, 
            server=server
            )


# 법사
class HighnessDunwitchHat(RootAbyssCap):
    def __init__(
            self,
            potentialOptionList: list[PotentialOptionSlot], 
            optionslot: BonusOptionSlot, 
            starforce: int, 
            upgrade_history: list[UpgradeScrolls], 
            additionalPotentialOptionList: list[PotentialOptionSlot] = None, 
            server=GameServer.NormalServer
            ):
        
        self.ItemName = "하이네스 던위치햇"
        self.RequiredJobType = [JobType.Magician]
        stat = SpecVector()
        stat[CoreStat.STAT_INT] = 40
        stat[CoreStat.STAT_LUK] = 40
        stat[CoreStat.STAT_HP] = 360
        stat[CoreStat.STAT_MP] = 360
        stat[CoreStat.ATTACK_SPELL] = 2
        stat[CoreStat.IGNORE_GUARD_PERCENTAGE] = 10

        RootAbyssCap.__init__(
            self=self,
            itemName = self.ItemName, 
            requiredJobType = self.RequiredJobType, 
            itemBasicStat= stat, 
            potentialOptionList = potentialOptionList, 
            optionslot=optionslot, 
            starforce=starforce, 
            upgrade_history=upgrade_history, 
            additionalPotentialOptionList=additionalPotentialOptionList, 
            server=server
            )
        
# 도적
class HighnessAssassinHood(RootAbyssCap):
    def __init__(
            self,
            potentialOptionList: list[PotentialOptionSlot], 
            optionslot: BonusOptionSlot, 
            starforce: int, 
            upgrade_history: list[UpgradeScrolls], 
            additionalPotentialOptionList: list[PotentialOptionSlot] = None, 
            server=GameServer.NormalServer
            ):
        
        self.ItemName = "하이네스 어쌔신후드"
        self.RequiredJobType = [JobType.Thief]
        stat = SpecVector()
        stat[CoreStat.STAT_LUK] = 40
        stat[CoreStat.STAT_DEX] = 40
        stat[CoreStat.STAT_HP] = 360
        stat[CoreStat.STAT_MP] = 360
        stat[CoreStat.ATTACK_PHYSICAL] = 2
        stat[CoreStat.IGNORE_GUARD_PERCENTAGE] = 10

        RootAbyssCap.__init__(
            self=self,
            itemName = self.ItemName, 
            requiredJobType = self.RequiredJobType, 
            itemBasicStat= stat, 
            potentialOptionList = potentialOptionList, 
            optionslot=optionslot, 
            starforce=starforce, 
            upgrade_history=upgrade_history, 
            additionalPotentialOptionList=additionalPotentialOptionList, 
            server=server
            )

# 해적

# 에테르넬 모자
class EternelCap(Cap):
    def __init__(
            self, 
            itemName: str, 
            requiredJobType: list[JobType], 
            itemBasicStat: SpecVector, 
            potentialOptionList: list[PotentialOptionSlot], 
            optionslot: BonusOptionSlot, 
            upgrade_history: list[UpgradeScrolls], 
            starforce: int, 
            additionalPotentialOptionList: list[PotentialOptionSlot] = None, 
            server=GameServer.NormalServer
            ):
        
        self.RequiredLevel = ReqLevel.Lv250.value
        self.BelongedItemSet = ItemSetEnum.Eternel
        Cap.__init__(
            self=self,
            itemName = itemName, 
            requiredLevel = self.RequiredLevel, 
            requiredJobType = requiredJobType, 
            itemBasicStat= itemBasicStat, 
            potentialOptionList= potentialOptionList, 
            optionslot= optionslot, 
            upgrade_history= upgrade_history, 
            starforce= starforce, 
            itemset= self.BelongedItemSet, 
            additionalPotentialOptionList= additionalPotentialOptionList, 
            server = server
            )
    
# 전사

# 궁수

# 법사
class EternelMageHat(EternelCap):
    def __init__(
            self,
            potentialOptionList: list[PotentialOptionSlot], 
            optionslot: BonusOptionSlot, 
            upgrade_history: list[UpgradeScrolls], 
            starforce: int, 
            additionalPotentialOptionList: list[PotentialOptionSlot] = None, 
            server=GameServer.NormalServer
            ):
        self.ItemName = "에테르넬 메이지햇"
        self.RequiredJobType = [JobType.Magician]
        stat = SpecVector()
        stat[CoreStat.STAT_INT] = 80
        stat[CoreStat.STAT_LUK] = 80
        stat[CoreStat.ATTACK_SPELL] = 10
        stat[CoreStat.IGNORE_GUARD_PERCENTAGE] = 15

        EternelCap.__init__(
            self=self,
            itemName = self.ItemName, 
            requiredJobType = self.RequiredJobType, 
            itemBasicStat= stat, 
            potentialOptionList = potentialOptionList, 
            optionslot=optionslot, 
            starforce=starforce, 
            upgrade_history=upgrade_history, 
            additionalPotentialOptionList=additionalPotentialOptionList, 
            server=server
            )

# 도적

# 해적