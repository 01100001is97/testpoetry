from Item.ItemGroup import CashItem
from Core.SpecElements import CoreStat, SpecVector
from Item.ItemSet import ItemSetEnum
from Core.ABCItem import ItemParts

class MasterLabel(CashItem):
    def __init__(
            self,
            itemName: str,
            itembasicstat: SpecVector,
            itempart: ItemParts
    ):
        CashItem.__init__(
            self=self,
            itemName=itemName,
            itemBasicStat=itembasicstat,
            itemset=ItemSetEnum.Master,
            itempart=itempart
        )

class BlackLabel(CashItem):
     def __init__(
            self,
            itemName: str,
            itembasicstat: SpecVector,
            itempart: ItemParts
    ):
        CashItem.__init__(
            self=self,
            itemName=itemName,
            itemBasicStat=itembasicstat,
            itemset=ItemSetEnum.Black,
            itempart=itempart
        )

class BlackLabelWeapon(BlackLabel):
    def __init__(self):
        stat = SpecVector()
        stat[CoreStat.ATTACK_PHYSICAL] = 25
        stat[CoreStat.ATTACK_SPELL] = 25
        BlackLabel.__init__(
            self=self,
            itemName="블랙 라벨 무기",
            itembasicstat=stat,
            itempart=ItemParts.CashWeapon
        )

class BlackLabelCap(BlackLabel):
    def __init__(self):
        stat = SpecVector()
        stat[CoreStat.STAT_ALL] = 20
        
        BlackLabel.__init__(
            self=self,
            itemName="블랙 라벨 모자",
            itembasicstat=stat,
            itempart=ItemParts.CashArmor
        )

class BlackLabelCape(BlackLabel):
    def __init__(self):
        stat = SpecVector()
        stat[CoreStat.STAT_ALL] = 20
        
        BlackLabel.__init__(
            self=self,
            itemName="블랙 라벨 망토",
            itembasicstat=stat,
            itempart=ItemParts.CashArmor
        )
        

class BlackLabelClothes(BlackLabel):
    def __init__(self):
        BlackLabel.__init__(
            self=self,
            itemName="블랙 라벨 한벌옷",
            itembasicstat=SpecVector(),
            itempart=ItemParts.CashArmor
        )

class BlacklabelShoes(BlackLabelClothes):
    def __init__(self):
        BlackLabel.__init__(
            self=self,
            itemName="블랙 라벨 슈즈",
            itembasicstat=SpecVector(),
            itempart=ItemParts.CashArmor
        )
