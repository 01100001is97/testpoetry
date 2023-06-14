from Core.Job import JobType
from Core.SpecElements import SpecVector, CoreStat
from Core.ABCItem import ItemParts
from Core.Server import GameServer
from Core.Enchant.BonusOption import BonusOption, BonusOptionSlot, BonusOptionEnum, BonusOptionGrade


slot = BonusOptionSlot({})
#slot.update({(BonusOptionEnum.AllStatPercentage, BonusOptionGrade.second)})
#slot.update({(BonusOptionEnum.StrSingleStat, BonusOptionGrade.second)})
slot.update({(BonusOptionEnum.StrDexDoubleStat, BonusOptionGrade.second)})
slot.update({(BonusOptionEnum.AttackSpell, BonusOptionGrade.second)})
slot.update({(BonusOptionEnum.Damage, BonusOptionGrade.second)})
slot.update({(BonusOptionEnum.HPStat, BonusOptionGrade.first)})

itemstat = SpecVector()
itemstat[CoreStat.ATTACK_PHYSICAL] = 180
itemstat[CoreStat.ATTACK_SPELL] = 302
itemstat[CoreStat.STAT_STR] = 5
itemstat[CoreStat.STAT_DEX] = 5
itemstat[CoreStat.STAT_INT] = 5
itemstat[CoreStat.STAT_LUK] = 5

item = BonusOption(
    itemName="아케인셰이드 스태프",
    requiredLevel=200,
    requiredJobType=[JobType.Magician],
    itemBasicStat=itemstat,
    itemPart=ItemParts.Weapon,
    optionslot=slot,
    server=GameServer.NormalServer
)

print(item.TotalSpec())