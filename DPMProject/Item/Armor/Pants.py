from Core.Enchant.BonusOption import BonusOptionSlot
from Core.Enchant.Potential import PotentialOptionSlot
from Core.Enchant.Scroll import UpgradeScrolls
from Core.Job import JobType
from Core.Server import GameServer
from Item.ItemGroup import Pants
from Core.SpecElements import CoreStat, SpecVector
from Item.ItemSet import ItemSetEnum
from Core.ReqLevel import ReqLevel

PantsUpgradeChance = 8

# 파프 모자
class RootAbyssPants(Pants):
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
        Pants.__init__(
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
class TricksterRangerPants(RootAbyssPants):
    def __init__(
            self,
            potentialOptionList: list[PotentialOptionSlot], 
            optionslot: BonusOptionSlot, 
            starforce: int, 
            upgrade_history: list[UpgradeScrolls], 
            additionalPotentialOptionList: list[PotentialOptionSlot] = None, 
            server=GameServer.NormalServer
            ):
        
        self.ItemName = "트릭스터 레인저팬츠"
        self.RequiredJobType = [JobType.Bowman]
        stat = SpecVector()
        stat[CoreStat.STAT_DEX] = 30  # INT -> DEX
        stat[CoreStat.STAT_STR] = 30
        stat[CoreStat.ATTACK_PHYSICAL] = 2  # ATTACK_SPELL -> ATTACK_PHYSICAL
        stat[CoreStat.IGNORE_GUARD_PERCENTAGE] = 5

        RootAbyssPants.__init__(
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
class TricksterDunwitchPants(RootAbyssPants):
    def __init__(
            self,
            potentialOptionList: list[PotentialOptionSlot], 
            optionslot: BonusOptionSlot, 
            starforce: int, 
            upgrade_history: list[UpgradeScrolls], 
            additionalPotentialOptionList: list[PotentialOptionSlot] = None, 
            server=GameServer.NormalServer
            ):
        
        self.ItemName = "하이네스 던위치팬츠"
        self.RequiredJobType = [JobType.Magician]
        stat = SpecVector()
        stat[CoreStat.STAT_INT] = 30
        stat[CoreStat.STAT_LUK] = 30
        stat[CoreStat.ATTACK_SPELL] = 2
        stat[CoreStat.IGNORE_GUARD_PERCENTAGE] = 5

        RootAbyssPants.__init__(
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
class TricksterAssassinPants(RootAbyssPants):
    def __init__(
            self,
            potentialOptionList: list[PotentialOptionSlot], 
            optionslot: BonusOptionSlot, 
            starforce: int, 
            upgrade_history: list[UpgradeScrolls], 
            additionalPotentialOptionList: list[PotentialOptionSlot] = None, 
            server=GameServer.NormalServer
            ):
        
        self.ItemName = "하이네스 어쌔신팬츠"
        self.RequiredJobType = [JobType.Thief]
        stat = SpecVector()
        stat[CoreStat.STAT_LUK] = 30  # INT -> LUK
        stat[CoreStat.STAT_DEX] = 30  # STR -> DEX
        stat[CoreStat.ATTACK_PHYSICAL] = 2  # ATTACK_SPELL -> ATTACK_PHYSICAL
        stat[CoreStat.IGNORE_GUARD_PERCENTAGE] = 5

        RootAbyssPants.__init__(
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
class EternelPants(Pants):
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
        Pants.__init__(
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
class EternelMagePants(EternelPants):
    def __init__(
            self,
            potentialOptionList: list[PotentialOptionSlot], 
            optionslot: BonusOptionSlot, 
            upgrade_history: list[UpgradeScrolls], 
            starforce: int, 
            additionalPotentialOptionList: list[PotentialOptionSlot] = None, 
            server=GameServer.NormalServer
            ):
        self.ItemName = "에테르넬 메이지팬츠"
        self.RequiredJobType = [JobType.Magician]
        stat = SpecVector()
        stat[CoreStat.STAT_INT] = 50
        stat[CoreStat.STAT_LUK] = 50
        stat[CoreStat.ATTACK_SPELL] = 6
        stat[CoreStat.IGNORE_GUARD_PERCENTAGE] = 5

        EternelPants.__init__(
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