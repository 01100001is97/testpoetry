from Item.ItemGroup import PetAccessory
from Core.Enchant.Scroll import UpgradeScrolls
from enum import Enum
from Core.SpecElements import SpecVector, CoreStat
from Item.ItemSet import ItemSetEnum
class PetAccessoryUpgradeChance(Enum):
    Dream = 9
    Petit = 8


class LunarDream(PetAccessory):
    _upgradeChance = 9
    _itemName = "루나 드림 펫장비"
    _basicStat = SpecVector()
    def __init__(
            self,
            upgrade_history: list[UpgradeScrolls]
    ):
        self._basicStat[CoreStat.ATTACK_PHYSICAL] = 5
        self._basicStat[CoreStat.ATTACK_SPELL] = 5

        PetAccessory.__init__(
            self=self,
            itemName=self._itemName,
            upgrade_chance=self._upgradeChance,
            itembasicstat=self._basicStat,
            upgrade_history=upgrade_history,
            setitem=ItemSetEnum.LunarDream
        )

class LunarPetit(PetAccessory):
    _upgradeChance = 8
    _itemName = "루나 쁘띠 펫장비"
    _basicStat = SpecVector()
    def __init__(
            self,
            upgrade_history: list[UpgradeScrolls]
    ):
        self._basicStat[CoreStat.ATTACK_PHYSICAL] = 10
        self._basicStat[CoreStat.ATTACK_SPELL] = 10

        PetAccessory.__init__(
            self=self,
            itemName=self._itemName,
            upgrade_chance=self._upgradeChance,
            itembasicstat=self._basicStat,
            upgrade_history=upgrade_history,
            setitem=ItemSetEnum.LunarPetit
        )


