from Core.Enchant.BonusOption import BonusOptionSlot
from Core.Enchant.Potential import PotentialOptionSlot
from Core.Enchant.Scroll import UpgradeScrolls
from Core.Job import JobType
from Core.Server import GameServer
from Item.ItemGroup import Shoes
from Core.SpecElements import CoreStat, SpecVector
from Item.ItemSet import ItemSetEnum
from Core.ReqLevel import ReqLevel

ShoesUpgradeChance = 8

class AbsolabsShoes(Shoes):
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
        Shoes.__init__(
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
        
class AbsolabsMageShoes(AbsolabsShoes):
    def __init__(
            self,
            potentialOptionList: list[PotentialOptionSlot], 
            optionslot: BonusOptionSlot, 
            starforce: int, 
            upgrade_history: list[UpgradeScrolls], 
            additionalPotentialOptionList: list[PotentialOptionSlot] = None, 
            server=GameServer.NormalServer
            ):
        
        self.ItemName = "앱솔랩스 메이지슈즈"
        self.RequiredJobType = [JobType.Magician]
        stat = SpecVector()
        stat[CoreStat.STAT_INT] = 20
        stat[CoreStat.STAT_LUK] = 20
        stat[CoreStat.ATTACK_SPELL] = 5

        AbsolabsShoes.__init__(
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
        
class ArcaneShadeShoes(Shoes):
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
        Shoes.__init__(
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

class ArcaneShadeMageShoes(ArcaneShadeShoes):
    """ 아케인셰이드 법사 장비류 중 마법사가 착용하는 신발
        
    """
    def __init__(
            self,
            potentialOptionList: list[PotentialOptionSlot], 
            optionslot: BonusOptionSlot, 
            upgrade_history: list[UpgradeScrolls], 
            starforce: int, 
            additionalPotentialOptionList: list[PotentialOptionSlot] = None, 
            server=GameServer.NormalServer
            ):
        self.ItemName = "아케인셰이드 메이지슈즈"
        self.RequiredJobType = [JobType.Magician]
        stat = SpecVector()
        stat[CoreStat.STAT_INT] = 40
        stat[CoreStat.STAT_LUK] = 40
        stat[CoreStat.ATTACK_SPELL] = 9

        ArcaneShadeShoes.__init__(
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

class ArcaneShadeArcherShoes(ArcaneShadeShoes):
    def __init__(
            self,
            potentialOptionList: list[PotentialOptionSlot], 
            optionslot: BonusOptionSlot, 
            upgrade_history: list[UpgradeScrolls], 
            starforce: int, 
            additionalPotentialOptionList: list[PotentialOptionSlot] = None, 
            server=GameServer.NormalServer
            ):
        self.ItemName = "아케인셰이드 아처슈즈"
        self.RequiredJobType = [JobType.Bowman]
        stat = SpecVector()
        stat[CoreStat.STAT_DEX] = 40  # INT -> DEX
        stat[CoreStat.STAT_STR] = 40
        stat[CoreStat.ATTACK_PHYSICAL] = 9  # ATTACK_SPELL -> ATTACK_PHYSICAL

        ArcaneShadeShoes.__init__(
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


class ArcaneShadeThiefShoes(ArcaneShadeShoes):
    def __init__(
            self,
            potentialOptionList: list[PotentialOptionSlot], 
            optionslot: BonusOptionSlot, 
            upgrade_history: list[UpgradeScrolls], 
            starforce: int, 
            additionalPotentialOptionList: list[PotentialOptionSlot] = None, 
            server=GameServer.NormalServer
            ):
        self.ItemName = "아케인셰이드 시프슈즈"
        self.RequiredJobType = [JobType.Thief]
        stat = SpecVector()
        stat[CoreStat.STAT_LUK] = 40  # INT -> LUK
        stat[CoreStat.STAT_DEX] = 40  # STR -> DEX
        stat[CoreStat.ATTACK_PHYSICAL] = 9  # ATTACK_SPELL -> ATTACK_PHYSICAL

        ArcaneShadeShoes.__init__(
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

