from Core.Enchant.BonusOption import BonusOptionSlot
from Core.Enchant.Potential import PotentialOptionSlot
from Core.Enchant.Scroll import UpgradeScrolls
from Core.Job import JobType
from Core.Server import GameServer
from Item.ItemGroup import Cape
from Core.SpecElements import CoreStat, SpecVector
from Item.ItemSet import ItemSetEnum
from Core.ReqLevel import ReqLevel

CapeUpgradeChance = 8

class AbsolabsCape(Cape):
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
        
        self.RequiredLevel = ReqLevel.Lv160.value
        self.BelongedItemSet = ItemSetEnum.Absolabs
        Cape.__init__(
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
        
class AbsolabsMageCape(AbsolabsCape):
    def __init__(
            self,
            potentialOptionList: list[PotentialOptionSlot], 
            optionslot: BonusOptionSlot, 
            starforce: int, 
            upgrade_history: list[UpgradeScrolls], 
            additionalPotentialOptionList: list[PotentialOptionSlot] = None, 
            server=GameServer.NormalServer
            ):
        
        self.ItemName = "앱솔랩스 메이지케이프"
        self.RequiredJobType = [JobType.Magician]
        stat = SpecVector()
        stat[CoreStat.STAT_STR] = 15
        stat[CoreStat.STAT_DEX] = 15
        stat[CoreStat.STAT_INT] = 15
        stat[CoreStat.STAT_LUK] = 15
        stat[CoreStat.ATTACK_PHYSICAL] = 2
        stat[CoreStat.ATTACK_SPELL] = 2

        AbsolabsCape.__init__(
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
        
class ArcaneShadeCape(Cape):
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
        
        self.RequiredLevel = ReqLevel.Lv200.value
        self.BelongedItemSet = ItemSetEnum.ArcaneShade
        Cape.__init__(
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

class ArcaneShadeMageCape(ArcaneShadeCape):
    def __init__(
            self,
            potentialOptionList: list[PotentialOptionSlot], 
            optionslot: BonusOptionSlot, 
            upgrade_history: list[UpgradeScrolls], 
            starforce: int, 
            additionalPotentialOptionList: list[PotentialOptionSlot] = None, 
            server=GameServer.NormalServer
            ):
        self.ItemName = "아케인셰이드 메이지케이프"
        self.RequiredJobType = [JobType.Magician]
        stat = SpecVector()
        stat[CoreStat.STAT_STR] = 35
        stat[CoreStat.STAT_DEX] = 35
        stat[CoreStat.STAT_INT] = 35
        stat[CoreStat.STAT_LUK] = 35
        stat[CoreStat.ATTACK_PHYSICAL] = 6
        stat[CoreStat.ATTACK_SPELL] = 6


        ArcaneShadeCape.__init__(
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
        

class ArcaneShadeArcherCape(ArcaneShadeCape):
    def __init__(
            self,
            potentialOptionList: list[PotentialOptionSlot], 
            optionslot: BonusOptionSlot, 
            upgrade_history: list[UpgradeScrolls], 
            starforce: int, 
            additionalPotentialOptionList: list[PotentialOptionSlot] = None, 
            server=GameServer.NormalServer
            ):
        self.ItemName = "아케인셰이드 아처케이프"
        self.RequiredJobType = [JobType.Bowman]
        stat = SpecVector()
        stat[CoreStat.STAT_STR] = 35
        stat[CoreStat.STAT_DEX] = 35  # INT -> DEX
        stat[CoreStat.STAT_INT] = 35
        stat[CoreStat.STAT_LUK] = 35
        stat[CoreStat.ATTACK_PHYSICAL] = 6  # ATTACK_SPELL -> ATTACK_PHYSICAL
        stat[CoreStat.ATTACK_SPELL] = 6

        ArcaneShadeCape.__init__(
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
