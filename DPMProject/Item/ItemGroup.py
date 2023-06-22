from Core.SpecElements import CoreStat, SpecVector
from Core.Job import JobType, JobTypeInfo
from Core.Enchant.Potential import PotentialOptionSlot, PotentialAbility
from Core.Enchant.SoulWeapon import SoulEnchantOption, SoulWeapon
from Core.Enchant.Scroll import Upgrade, UpgradeScrolls
from Core.Enchant.BonusOption import BonusOptionSlot, BonusOption
from Core.Enchant.StarForce import StarForce
from Core.ABCItem import ItemParts, ABCItem
from Core.Server import GameServer
from Core.ReqLevel import ReqLevel
from Item.ItemSet import ItemSetEnum, BelongedItemSet


class NormalItem(PotentialAbility, BonusOption, StarForce, BelongedItemSet):
    # 아이템 세트
    def __init__(
        self,
        itemName: str,
        requiredLevel: int,
        requiredJobType: list[JobType],
        itemBasicStat: SpecVector,
        itemPart: ItemParts,
        potentialOptionList: list[PotentialOptionSlot],
        optionslot: BonusOptionSlot,
        upgrade_history: list[UpgradeScrolls],
        upgrade_chance: int,
        starforce: int,
        itemset = None,
        additionalPotentialOptionList: list[PotentialOptionSlot] = None,
        server = GameServer.NormalServer
    ):
        PotentialAbility.__init__(
            self=self,
            itemName=itemName,
            requiredLevel=requiredLevel,
            requiredJobType=requiredJobType,
            itemBasicStat=itemBasicStat,
            itemPart=itemPart,
            potentialOptionList=potentialOptionList,
            additionalPotentialOptionList=additionalPotentialOptionList,
            server=server
        )
        BonusOption.__init__(
            self=self,
            itemName=itemName,
            requiredLevel=requiredLevel,
            requiredJobType=requiredJobType,
            itemBasicStat=itemBasicStat,
            itemPart=itemPart,
            optionslot=optionslot,
            server=server
        )
        StarForce.__init__(
            self=self,
            itemName=itemName,
            requiredLevel=requiredLevel,
            requiredJobType=requiredJobType,
            itemBasicStat=itemBasicStat,
            itemPart=itemPart,
            upgrade_chance=upgrade_chance,
            upgrade_history=upgrade_history,
            starforce=starforce,
            server=server
        )
        BelongedItemSet.__init__(self=self, itemset=itemset)

    def TotalSpec(self) -> tuple[SpecVector, int]:
        result = self.ItemBasicStat
        potenSpec, cooldown = PotentialAbility.TotalSpec(self)
        result = result + potenSpec
        bonusstat, _ = BonusOption.TotalSpec(self)
        result = result + bonusstat
        starstat, _ = StarForce.TotalSpec(self)
        result = result + starstat
        return result, cooldown
      
class NoBonusOptionItem(PotentialAbility, StarForce, BelongedItemSet):
    def __init__(
        self,
        itemName: str,
        requiredLevel: int,
        requiredJobType: list[JobType],
        itemBasicStat: SpecVector,
        itemPart: ItemParts,
        potentialOptionList: list[PotentialOptionSlot],
        upgrade_history: list[UpgradeScrolls],
        upgrade_chance: int,
        starforce: int,
        itemset = None,
        additionalPotentialOptionList: list[PotentialOptionSlot] = None,
        server = GameServer.NormalServer
    ):
        PotentialAbility.__init__(
            self=self,
            itemName=itemName,
            requiredLevel=requiredLevel,
            requiredJobType=requiredJobType,
            itemPart=itemPart,
            itemBasicStat=itemBasicStat,
            potentialOptionList=potentialOptionList,
            additionalPotentialOptionList=additionalPotentialOptionList,
            server=server
        )
        StarForce.__init__(
            self=self,
            itemName=itemName,
            requiredLevel=requiredLevel,
            requiredJobType=requiredJobType,
            itemPart=itemPart,
            itemBasicStat=itemBasicStat,
            upgrade_chance=upgrade_chance,
            upgrade_history=upgrade_history,
            starforce=starforce,
            server=server
        )
        BelongedItemSet.__init__(self=self, itemset=itemset)

    def TotalSpec(self) -> tuple[SpecVector, int]:
        result = self.ItemBasicStat
        abilitystat, cooldown = PotentialAbility.TotalSpec(self)
        result = result + abilitystat
        starstat, _ = StarForce.TotalSpec(self)
        result = result + starstat
        return result, cooldown

class NoEnchantItem(ABCItem, BelongedItemSet):
    
    def __init__(self, itemName: str, requiredLevel: int, requiredJobType: list[JobType], itemBasicStat: SpecVector, itemPart: ItemParts, itemset = None, server=GameServer.NormalServer):
        ABCItem.__init__(self, itemName, requiredLevel, requiredJobType, itemBasicStat, itemPart, server)
        BelongedItemSet.__init__(self=self, itemset=itemset)

    def TotalSpec(self) -> tuple[SpecVector, int]:
        return self.ItemBasicStat, 0
    
class OnlyPotentialItem(PotentialAbility, BelongedItemSet):
    def __init__(
        self,
        itemName: str,
        requiredLevel: int,
        requiredJobType: list[JobType],
        itemBasicStat: SpecVector,
        itempart: ItemParts,
        potentialOptionList: list[PotentialOptionSlot],
        itemset = None,
        additionalPotentialOptionList: list[PotentialOptionSlot] = None,
        server = GameServer.NormalServer
    ):
        PotentialAbility.__init__(
            self=self,
            itemName=itemName,
            requiredJobType=requiredJobType,
            requiredLevel=requiredLevel,
            itemBasicStat=itemBasicStat,
            itemPart=itempart,
            potentialOptionList=potentialOptionList,
            additionalPotentialOptionList=additionalPotentialOptionList,
            server=server
        )
        BelongedItemSet.__init__(self=self, itemset=itemset)

    def TotalSpec(self) -> SpecVector:
        result = SpecVector()
        result += self.ItemBasicStat
        potenSpec, cooldown = PotentialAbility.TotalSpec(self)
        result = result + potenSpec
        return result, cooldown
    
class OnlyBonusOptionItem(BonusOption, BelongedItemSet):
    def __init__(
        self,
        itemName: str,
        requiredLevel: int,
        requiredJobType: list[JobType],
        itemBasicStat: SpecVector,
        itemPart: ItemParts,
        optionslot: BonusOptionSlot,
        itemset = None,
        server = GameServer.NormalServer
    ):
        BonusOption.__init__(
            self=self,
            itemName=itemName,
            requiredLevel=requiredLevel,
            requiredJobType=requiredJobType,
            itemBasicStat=itemBasicStat,
            itemPart=itemPart,
            optionslot=optionslot,
            server=server
        )
        BelongedItemSet.__init__(self=self, itemset=itemset)

    def TotalSpec(self) -> tuple[SpecVector, int]:
        result = self.ItemBasicStat
        bonusstat, _ = BonusOption.TotalSpec(self)
        result = result + bonusstat
        return result, 0

# 방어구류
class Cap(NormalItem):
    _UpgradeChance = 12
    _ItemPart = ItemParts.Cap
    def __init__(
        self,
        itemName: str,
        requiredLevel: int,
        requiredJobType: list[JobType],
        itemBasicStat: SpecVector,
        potentialOptionList: list[PotentialOptionSlot],
        optionslot: BonusOptionSlot,
        upgrade_history: list[UpgradeScrolls],
        starforce: int,
        itemset = None,
        additionalPotentialOptionList: list[PotentialOptionSlot] = None,
        server = GameServer.NormalServer
    ):
        NormalItem.__init__(
            self=self,
            itemName=itemName,
            requiredLevel=requiredLevel,
            requiredJobType=requiredJobType,
            itemBasicStat=itemBasicStat,
            itemPart=self._ItemPart,
            potentialOptionList=potentialOptionList,
            optionslot=optionslot,
            upgrade_history=upgrade_history,
            upgrade_chance=self._UpgradeChance,
            starforce=starforce,
            itemset=itemset,
            additionalPotentialOptionList=additionalPotentialOptionList,
            server=server

        )
        
class Clothes(NormalItem):
    _UpgradeChance = 8
    _ItemPart = ItemParts.Clothes

    def __init__(
        self,
        itemName: str,
        requiredLevel: int,
        requiredJobType: list[JobType],
        itemBasicStat: SpecVector,
        potentialOptionList: list[PotentialOptionSlot],
        optionslot: BonusOptionSlot,
        upgrade_history: list[UpgradeScrolls],
        starforce: int,
        itemset = None,
        additionalPotentialOptionList: list[PotentialOptionSlot] = None,
        server = GameServer.NormalServer
    ):
        NormalItem.__init__(
            self=self,
            itemName=itemName,
            requiredLevel=requiredLevel,
            requiredJobType=requiredJobType,
            itemBasicStat=itemBasicStat,
            itemPart=self._ItemPart,
            potentialOptionList=potentialOptionList,
            optionslot=optionslot,
            upgrade_history=upgrade_history,
            upgrade_chance=self._UpgradeChance,
            starforce=starforce,
            itemset=itemset,
            additionalPotentialOptionList=additionalPotentialOptionList,
            server=server
        )

class Pants(NormalItem):
    _UpgradeChance = 8
    _ItemPart = ItemParts.Pants

    def __init__(
        self,
        itemName: str,
        requiredLevel: int,
        requiredJobType: list[JobType],
        itemBasicStat: SpecVector,
        potentialOptionList: list[PotentialOptionSlot],
        optionslot: BonusOptionSlot,
        upgrade_history: list[UpgradeScrolls],
        starforce: int,
        itemset = None,
        additionalPotentialOptionList: list[PotentialOptionSlot] = None,
        server = GameServer.NormalServer
    ):
        NormalItem.__init__(
            self=self,
            itemName=itemName,
            requiredLevel=requiredLevel,
            requiredJobType=requiredJobType,
            itemBasicStat=itemBasicStat,
            itemPart=self._ItemPart,
            potentialOptionList=potentialOptionList,
            optionslot=optionslot,
            upgrade_history=upgrade_history,
            upgrade_chance=self._UpgradeChance,
            starforce=starforce,
            itemset=itemset,
            additionalPotentialOptionList=additionalPotentialOptionList,
            server=server
        )

class Cape(NormalItem):
    _UpgradeChance = 8
    _ItemPart = ItemParts.Cape

    def __init__(
        self,
        itemName: str,
        requiredLevel: int,
        requiredJobType: list[JobType],
        itemBasicStat: SpecVector,
        potentialOptionList: list[PotentialOptionSlot],
        optionslot: BonusOptionSlot,
        upgrade_history: list[UpgradeScrolls],
        starforce: int,
        itemset = None,
        additionalPotentialOptionList: list[PotentialOptionSlot] = None,
        server = GameServer.NormalServer
    ):
        NormalItem.__init__(
            self=self,
            itemName=itemName,
            requiredLevel=requiredLevel,
            requiredJobType=requiredJobType,
            itemBasicStat=itemBasicStat,
            itemPart=self._ItemPart,
            potentialOptionList=potentialOptionList,
            optionslot=optionslot,
            upgrade_history=upgrade_history,
            upgrade_chance=self._UpgradeChance,
            starforce=starforce,
            itemset=itemset,
            additionalPotentialOptionList=additionalPotentialOptionList,
            server=server
        )

class Gloves(NormalItem):
    _UpgradeChance = 8
    _ItemPart = ItemParts.Gloves

    def __init__(
        self,
        itemName: str,
        requiredLevel: int,
        requiredJobType: list[JobType],
        itemBasicStat: SpecVector,
        potentialOptionList: list[PotentialOptionSlot],
        optionslot: BonusOptionSlot,
        upgrade_history: list[UpgradeScrolls],
        starforce: int,
        itemset = None,
        additionalPotentialOptionList: list[PotentialOptionSlot] = None,
        server = GameServer.NormalServer
    ):
        NormalItem.__init__(
            self=self,
            itemName=itemName,
            requiredLevel=requiredLevel,
            requiredJobType=requiredJobType,
            itemBasicStat=itemBasicStat,
            itemPart=self._ItemPart,
            potentialOptionList=potentialOptionList,
            optionslot=optionslot,
            upgrade_history=upgrade_history,
            upgrade_chance=self._UpgradeChance,
            starforce=starforce,
            itemset=itemset,
            additionalPotentialOptionList=additionalPotentialOptionList,
            server=server
        )

class Shoes(NormalItem):
    _UpgradeChance = 8
    _ItemPart = ItemParts.Shoes

    def __init__(
        self,
        itemName: str,
        requiredLevel: int,
        requiredJobType: list[JobType],
        itemBasicStat: SpecVector,
        potentialOptionList: list[PotentialOptionSlot],
        optionslot: BonusOptionSlot,
        upgrade_history: list[UpgradeScrolls],
        starforce: int,
        itemset = None,
        additionalPotentialOptionList: list[PotentialOptionSlot] = None,
        server = GameServer.NormalServer
    ):
        NormalItem.__init__(
            self=self,
            itemName=itemName,
            requiredLevel=requiredLevel,
            requiredJobType=requiredJobType,
            itemBasicStat=itemBasicStat,
            itemPart=self._ItemPart,
            potentialOptionList=potentialOptionList,
            optionslot=optionslot,
            upgrade_history=upgrade_history,
            upgrade_chance=self._UpgradeChance,
            starforce=starforce,
            itemset=itemset,
            additionalPotentialOptionList=additionalPotentialOptionList,
            server=server
        )


# 무기류
class Weapon(PotentialAbility, BonusOption, StarForce, SoulWeapon, BelongedItemSet):
    _ItemPart = ItemParts.Weapon
    def __init__(
        self,
        itemName: str,
        requiredLevel: int,
        requiredJobType: list[JobType],
        itemBasicStat: SpecVector,
        potentialOptionList: list[PotentialOptionSlot],
        optionslot: BonusOptionSlot,
        upgrade_history: list[UpgradeScrolls],
        upgrade_chance: int,
        starforce: int,
        enchant: SoulEnchantOption,
        itemset = None,
        additionalPotentialOptionList: list[PotentialOptionSlot] = None,
        server = GameServer.NormalServer
    ):
        PotentialAbility.__init__(
            self=self,
            itemName=itemName,
            requiredLevel=requiredLevel,
            requiredJobType=requiredJobType,
            itemBasicStat=itemBasicStat,
            itemPart=self._ItemPart,
            potentialOptionList=potentialOptionList,
            additionalPotentialOptionList=additionalPotentialOptionList,
            server=server
        )
        BonusOption.__init__(
            self=self,
            itemName=itemName,
            requiredLevel=requiredLevel,
            requiredJobType=requiredJobType,
            itemBasicStat=itemBasicStat,
            itemPart=self._ItemPart,
            optionslot=optionslot,
            server=server
        )
        StarForce.__init__(
            self=self,
            itemName=itemName,
            requiredLevel=requiredLevel,
            requiredJobType=requiredJobType,
            itemBasicStat=itemBasicStat,
            itemPart=self._ItemPart,
            upgrade_chance=upgrade_chance,
            upgrade_history=upgrade_history,
            starforce=starforce,
            server=server
        )
        SoulWeapon.__init__(
            self=self,
            itemName=itemName,
            requiredJobType=requiredJobType,
            requiredLevel=requiredLevel,
            itemBasicStat=itemBasicStat,
            itemPart=self._ItemPart,
            enchant=enchant
            
        )
        BelongedItemSet.__init__(self=self, itemset=itemset)

    def TotalSpec(self) -> tuple[SpecVector, int]:
        result = self.ItemBasicStat
        potenSpec, cooldown = PotentialAbility.TotalSpec(self)
        result = result + potenSpec
        bonusstat, _ = BonusOption.TotalSpec(self)
        result = result + bonusstat
        starstat, _ = StarForce.TotalSpec(self)
        result = result + starstat
        # 소울웨폰의 스펙에 소울 게이지로 인한 공마 20 옵션 추가됨
        soulstat, _ = SoulWeapon.TotalSpec(self)
        result = result + soulstat
        return result, cooldown
      
class SubWeapon(OnlyPotentialItem):
    _ItemPart = ItemParts.SubWeapon

    def __init__(
        self,
        itemName: str,
        requiredLevel: int,
        requiredJobType: list[JobType],
        itemBasicStat: SpecVector,
        potentialOptionList: list[PotentialOptionSlot],
        itemset = None,
        additionalPotentialOptionList: list[PotentialOptionSlot] = None,
        server = GameServer.NormalServer
    ):
        OnlyPotentialItem.__init__(
            self=self,
            itemName=itemName,
            requiredLevel=requiredLevel,
            requiredJobType=requiredJobType,
            itemBasicStat=itemBasicStat,
            itempart=self._ItemPart,
            potentialOptionList=potentialOptionList,
            itemset=itemset,
            additionalPotentialOptionList=additionalPotentialOptionList,
            server=server
        )

class Blade(NoBonusOptionItem):
    ItemPart = ItemParts.Blade
    RequiredJobType = [JobType.Theif]

class Shield(NoBonusOptionItem):
    ItemPart = ItemParts.Shield
    
class Emblem(OnlyPotentialItem):
    _ItemPart = ItemParts.Emblem
    def __init__(
        self,
        itemName: str,
        requiredLevel: int,
        requiredJobType: list[JobType],
        itemBasicStat: SpecVector,
        potentialOptionList: list[PotentialOptionSlot],
        itemset = None,
        additionalPotentialOptionList: list[PotentialOptionSlot] = None,
        server = GameServer.NormalServer
    ):
        OnlyPotentialItem.__init__(
            self=self,
            itemName=itemName,
            requiredLevel=requiredLevel,
            requiredJobType=requiredJobType,
            itemBasicStat=itemBasicStat,
            itempart=self._ItemPart,
            potentialOptionList=potentialOptionList,
            itemset=itemset,
            additionalPotentialOptionList=additionalPotentialOptionList,
            server=server
        )

# 장신구
class Pendant(NormalItem):
    _ItemPart = ItemParts.Pendant
    _RequiredJobType = [JobType.Worrior, JobType.Bowman, JobType.Magician, JobType.Theif, JobType.Pirate]

    def __init__(
        self,
        itemName: str,
        requiredLevel: int,
        itemBasicStat: SpecVector,
        potentialOptionList: list[PotentialOptionSlot],
        optionslot: BonusOptionSlot,
        upgrade_history: list[UpgradeScrolls],
        upgrade_chance: int,
        starforce: int,
        itemset = None,
        additionalPotentialOptionList: list[PotentialOptionSlot] = None,
        server = GameServer.NormalServer
    ):
        NormalItem.__init__(
            self=self,
            itemName=itemName,
            requiredLevel=requiredLevel,
            requiredJobType=self._RequiredJobType,
            itemBasicStat=itemBasicStat,
            itemPart=self._ItemPart,
            potentialOptionList=potentialOptionList,
            optionslot=optionslot,
            upgrade_history=upgrade_history,
            upgrade_chance=upgrade_chance,
            starforce=starforce,
            itemset=itemset,
            additionalPotentialOptionList=additionalPotentialOptionList,
            server=server
        )

class Belt(NormalItem):
    _ItemPart = ItemParts.Belt
    _RequiredJobType = [JobType.Worrior, JobType.Bowman, JobType.Magician, JobType.Theif, JobType.Pirate]

    def __init__(
        self,
        itemName: str,
        requiredLevel: int,
        itemBasicStat: SpecVector,
        potentialOptionList: list[PotentialOptionSlot],
        optionslot: BonusOptionSlot,
        upgrade_history: list[UpgradeScrolls],
        upgrade_chance: int,
        starforce: int,
        itemset = None,
        additionalPotentialOptionList: list[PotentialOptionSlot] = None,
        server = GameServer.NormalServer
    ):
        NormalItem.__init__(
            self=self,
            itemName=itemName,
            requiredLevel=requiredLevel,
            requiredJobType=self._RequiredJobType,
            itemBasicStat=itemBasicStat,
            itemPart=self._ItemPart,
            potentialOptionList=potentialOptionList,
            optionslot=optionslot,
            upgrade_history=upgrade_history,
            upgrade_chance=upgrade_chance,
            starforce=starforce,
            itemset=itemset,
            additionalPotentialOptionList=additionalPotentialOptionList,
            server=server
        )

class ForeHead(NormalItem):
    _ItemPart = ItemParts.ForeHead
    _RequiredJobType = [JobType.Worrior, JobType.Bowman, JobType.Magician, JobType.Theif, JobType.Pirate]

    def __init__(
        self,
        itemName: str,
        requiredLevel: int,
        itemBasicStat: SpecVector,
        potentialOptionList: list[PotentialOptionSlot],
        optionslot: BonusOptionSlot,
        upgrade_history: list[UpgradeScrolls],
        upgrade_chance: int,
        starforce: int,
        itemset = None,
        additionalPotentialOptionList: list[PotentialOptionSlot] = None,
        server = GameServer.NormalServer
    ):
        NormalItem.__init__(
            self=self,
            itemName=itemName,
            requiredLevel=requiredLevel,
            requiredJobType=self._RequiredJobType,
            itemBasicStat=itemBasicStat,
            itemPart=self._ItemPart,
            potentialOptionList=potentialOptionList,
            optionslot=optionslot,
            upgrade_history=upgrade_history,
            upgrade_chance=upgrade_chance,
            starforce=starforce,
            itemset=itemset,
            additionalPotentialOptionList=additionalPotentialOptionList,
            server=server
        )

class EyeAccessory(NormalItem):
    _ItemPart = ItemParts.EyeAccessory
    _RequiredJobType = [JobType.Worrior, JobType.Bowman, JobType.Magician, JobType.Theif, JobType.Pirate]

    def __init__(
        self,
        itemName: str,
        requiredLevel: int,
        itemBasicStat: SpecVector,
        potentialOptionList: list[PotentialOptionSlot],
        optionslot: BonusOptionSlot,
        upgrade_history: list[UpgradeScrolls],
        upgrade_chance: int,
        starforce: int,
        itemset = None,
        additionalPotentialOptionList: list[PotentialOptionSlot] = None,
        server = GameServer.NormalServer
    ):
        NormalItem.__init__(
            self=self,
            itemName=itemName,
            requiredLevel=requiredLevel,
            requiredJobType=self._RequiredJobType,
            itemBasicStat=itemBasicStat,
            itemPart=self._ItemPart,
            potentialOptionList=potentialOptionList,
            optionslot=optionslot,
            upgrade_history=upgrade_history,
            upgrade_chance=upgrade_chance,
            starforce=starforce,
            itemset=itemset,
            additionalPotentialOptionList=additionalPotentialOptionList,
            server=server
        )

class EarAccessory(NormalItem):
    _ItemPart = ItemParts.EarAccessory
    _RequiredJobType = [JobType.Worrior, JobType.Bowman, JobType.Magician, JobType.Theif, JobType.Pirate]

    def __init__(
        self,
        itemName: str,
        requiredLevel: int,
        itemBasicStat: SpecVector,
        potentialOptionList: list[PotentialOptionSlot],
        optionslot: BonusOptionSlot,
        upgrade_history: list[UpgradeScrolls],
        upgrade_chance: int,
        starforce: int,
        itemset = None,
        additionalPotentialOptionList: list[PotentialOptionSlot] = None,
        server = GameServer.NormalServer
    ):
        NormalItem.__init__(
            self=self,
            itemName=itemName,
            requiredLevel=requiredLevel,
            requiredJobType=self._RequiredJobType,
            itemBasicStat=itemBasicStat,
            itemPart=self._ItemPart,
            potentialOptionList=potentialOptionList,
            optionslot=optionslot,
            upgrade_history=upgrade_history,
            upgrade_chance=upgrade_chance,
            starforce=starforce,
            itemset=itemset,
            additionalPotentialOptionList=additionalPotentialOptionList,
            server=server
        )

class Pocket(OnlyBonusOptionItem):
    _ItemPart = ItemParts.Pocket
    _RequiredJobType = [JobType.Worrior, JobType.Bowman, JobType.Magician, JobType.Theif, JobType.Pirate]

    def __init__(
        self,
        itemName: str,
        requiredLevel: int,
        itemBasicStat: SpecVector,
        optionslot: BonusOptionSlot,
        itemset = None,
        server = GameServer.NormalServer
    ):
        OnlyBonusOptionItem.__init__(
            self=self,
            itemName=itemName,
            requiredLevel=requiredLevel,
            requiredJobType=self._RequiredJobType,
            itemBasicStat=itemBasicStat,
            itemPart=self._ItemPart,
            optionslot=optionslot,
            itemset=itemset,
            server=server
        )

class Ring(NoBonusOptionItem):
    _ItemPart = ItemParts.Ring
    _RequiredJobType = [JobType.Worrior, JobType.Bowman, JobType.Magician, JobType.Theif, JobType.Pirate]

    def __init__(
        self,
        itemName: str,
        requiredLevel: int,
        itemBasicStat: SpecVector,
        potentialOptionList: list[PotentialOptionSlot],
        upgrade_history: list[UpgradeScrolls],
        upgrade_chance: int,
        starforce: int,
        itemset = None,
        additionalPotentialOptionList: list[PotentialOptionSlot] = None,
        server = GameServer.NormalServer
    ):
        NoBonusOptionItem.__init__(
            self=self,
            itemName=itemName,
            requiredLevel=requiredLevel,
            requiredJobType=self._RequiredJobType,
            itemBasicStat=itemBasicStat,
            itemPart=self._ItemPart,
            potentialOptionList=potentialOptionList,
            upgrade_history=upgrade_history,
            upgrade_chance=upgrade_chance,
            starforce=starforce,
            itemset=itemset,
            additionalPotentialOptionList=additionalPotentialOptionList,
            server=server
        )

class Shoulder(NoBonusOptionItem):
    _ItemPart = ItemParts.Shoulder

    def __init__(
        self,
        itemName: str,
        requiredLevel: int,
        requiredJobType: list[JobType],
        itemBasicStat: SpecVector,
        potentialOptionList: list[PotentialOptionSlot],
        upgrade_history: list[UpgradeScrolls],
        upgrade_chance: int,
        starforce: int,
        itemset = None,
        additionalPotentialOptionList: list[PotentialOptionSlot] = None,
        server = GameServer.NormalServer
    ):
        NoBonusOptionItem.__init__(
            self=self,
            itemName=itemName,
            requiredLevel=requiredLevel,
            requiredJobType=requiredJobType,
            itemBasicStat=itemBasicStat,
            itemPart=self._ItemPart,
            potentialOptionList=potentialOptionList,
            upgrade_history=upgrade_history,
            upgrade_chance=upgrade_chance,
            starforce=starforce,
            itemset=itemset,
            additionalPotentialOptionList=additionalPotentialOptionList,
            server=server
        )

class Heart(NoBonusOptionItem):
    _ItemPart = ItemParts.Heart
    _RequiredJobType = [JobType.Worrior, JobType.Bowman, JobType.Magician, JobType.Theif, JobType.Pirate]
    def __init__(
        self,
        itemName: str,
        requiredLevel: int,
        itemBasicStat: SpecVector,
        potentialOptionList: list[PotentialOptionSlot],
        upgrade_history: list[UpgradeScrolls],
        upgrade_chance: int,
        starforce: int,
        itemset = None,
        additionalPotentialOptionList: list[PotentialOptionSlot] = None,
        server = GameServer.NormalServer
    ):
        self.ItemPart = self._ItemPart
        self.RequiredJobType = self._RequiredJobType

        NoBonusOptionItem.__init__(
            self=self,
            itemName=itemName,
            requiredLevel=requiredLevel,
            requiredJobType=self.RequiredJobType,
            itemBasicStat=itemBasicStat,
            itemPart=self.ItemPart,
            potentialOptionList=potentialOptionList,
            upgrade_history=upgrade_history,
            upgrade_chance=upgrade_chance,
            starforce=starforce,
            itemset=itemset,
            additionalPotentialOptionList=additionalPotentialOptionList,
            server=server
        )
  
class Badge(NoEnchantItem):
    _ItemPart = ItemParts.Badge
    _RequiredJobType = [JobType.Worrior, JobType.Bowman, JobType.Magician, JobType.Theif, JobType.Pirate]

    def __init__(
        self,
        itemName: str,
        requiredLevel: int,
        itemBasicStat: SpecVector,
        itemset = None,
        server = GameServer.NormalServer
    ):
        NoEnchantItem.__init__(
            self=self,
            itemName=itemName,
            requiredLevel=requiredLevel,
            requiredJobType=self._RequiredJobType,
            itemBasicStat=itemBasicStat,
            itemPart=self._ItemPart,
            itemset=itemset,
            server=server
        )

class Medal(NoEnchantItem):
    _ItemPart = ItemParts.Medal
    _RequiredJobType = [JobType.Worrior, JobType.Bowman, JobType.Magician, JobType.Theif, JobType.Pirate]

    def __init__(
        self,
        itemName: str,
        requiredLevel: int,
        itemBasicStat: SpecVector,
        itemset = None,
        server = GameServer.NormalServer
    ):
        NoEnchantItem.__init__(
            self=self,
            itemName=itemName,
            requiredLevel=requiredLevel,
            requiredJobType=self._RequiredJobType,
            itemBasicStat=itemBasicStat,
            itemPart=self._ItemPart,
            itemset=itemset,
            server=server
        )

# 심볼
class Symbol(NoEnchantItem):
    _level:int
    _basicForce: int
    _levelForce = 10
    _symbolBasicStat: SpecVector
    _symbolLevelStat: SpecVector
    ItemPart = ItemParts.Symbol
    RequiredLevel = 200
    def __init__(
            self, 
            itemName: str, 
            requiredJobType: list[JobType], 
            Symbollevel:int,
            basicForce: int,
            symbolBasicStat:SpecVector,
            symbolLevelStat:SpecVector,
            ):
        if len(requiredJobType) != 1:
            raise ValueError("아케인 심볼 직업은 1개로 설정")
        
        if not isinstance(Symbollevel, int):
            raise TypeError("level is int type")
        self._level = Symbollevel

        if not isinstance(basicForce, int):
            raise TypeError("basicforce is int type")
        self._basicForce = basicForce

        if not isinstance(symbolBasicStat, SpecVector):
            raise TypeError("symbolBasicStat is SpecVector type")
        self._symbolBasicStat = symbolBasicStat

        if not isinstance(symbolLevelStat, SpecVector):
            raise TypeError("symbolLevelStat is SpecVector type")
        self._symbolLevelStat = symbolLevelStat

        

        NoEnchantItem.__init__(
            self=self,
            requiredLevel= ReqLevel.Lv200.value, 
            itemName= itemName,
            requiredJobType= requiredJobType, 
            itemBasicStat= self.SetSymbolStat(),
            itemPart= self.ItemPart
            )
        

    def SetSymbolStat(self) -> SpecVector:
        result = SpecVector()
        result = result + self._symbolBasicStat

        for i in range(0, self._level):
            result = result + self._symbolLevelStat

        return result
    
    def GetForce(self) -> int:
        return self._basicForce + self._levelForce*self._level

# 펫장비
class PetAccessory(Upgrade, BelongedItemSet):
    _RequiredLevel: int
    _RequiredJobType: list
    _ItemPart: ItemParts
    
    def __init__(
        self,
        itemName: str,
        upgrade_chance: int,
        itembasicstat: SpecVector,
        upgrade_history: list[UpgradeScrolls],
        setitem = ItemSetEnum
    ):
        if upgrade_chance > 10:
            raise ValueError("펫 장비 업그레이드 최대 횟수는 10회")
        
        if not isinstance(itembasicstat, SpecVector):
            raise TypeError("아이템 기본 스펙은 SpecVector 타입")
        
        self._RequiredLevel = 0
        self._ItemPart = ItemParts.PetAccessory
        self._RequiredJobType = [JobType.Worrior, JobType.Bowman, JobType.Magician, JobType.Theif, JobType.Pirate]


        Upgrade.__init__(
            self=self,
            itemName=itemName,
            requiredLevel=self._RequiredLevel,
            requiredJobType=self._RequiredJobType,
            itemBasicStat=itembasicstat,
            itemPart=self._ItemPart,
            upgrade_chance=upgrade_chance,
            upgrade_history=upgrade_history,
            server=None
        )
        BelongedItemSet.__init__(self=self, itemset=setitem)

    def TotalSpec(self) -> tuple[SpecVector, int]:
        stat, _ = Upgrade.TotalSpec(self)
        return self.ItemBasicStat + stat, 0

# 칭호
class CharacterTitle(NoEnchantItem):
    _ItemPart = ItemParts.CharacterTitle
    _RequiredJobType = [JobType.Worrior, JobType.Bowman, JobType.Magician, JobType.Theif, JobType.Pirate]

    def __init__(
            self,
            itemName: str,
            requiredLevel: int,
            itemBasicStat: SpecVector
    ):
        NoEnchantItem.__init__(
            self=self,
            itemName=itemName,
            itemBasicStat=itemBasicStat,
            requiredLevel=requiredLevel,
            requiredJobType=self._RequiredJobType,
            itemPart=self._ItemPart
        )

# 캐시 장비
class CashItem(NoEnchantItem):
    _reqJob: list[JobType]
    def __init__(
            self,
            itemName: str,
            itemBasicStat: SpecVector,
            itemset: ItemSetEnum,
            itempart: ItemParts
    ):
        self._reqJob = [JobType.Worrior, JobType.Bowman, JobType.Magician, JobType.Theif, JobType.Pirate]
        
        NoEnchantItem.__init__(
            self=self,
            itemName=itemName,
            requiredJobType=self._reqJob,
            requiredLevel=0,
            itemBasicStat=itemBasicStat,
            itemPart=itempart,
            itemset=itemset,
            server=GameServer.NormalServer
        )
