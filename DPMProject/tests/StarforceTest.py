from Core.Enchant.StarForce import StarForce
from Core.Job import JobType
from Core.SpecElements import SpecVector, CoreStat
from Core.ABCItem import ItemParts
from Core.Enchant.Scroll import UpgradeScrolls
from Core.Server import GameServer

stat = SpecVector()
stat[CoreStat.STAT_INT] = 150
stat[CoreStat.STAT_LUK] = 150
stat[CoreStat.ATTACK_PHYSICAL] = 251
stat[CoreStat.ATTACK_SPELL] = 406
stat[CoreStat.DAMAGE_PERCENTAGE_BOSS] = 30
stat[CoreStat.IGNORE_GUARD_PERCENTAGE] = 20
stat[CoreStat.FINAL_DAMAGE_PERCENT] = 10

upgradelist = []
for i in range(0,8):
    upgradelist.append(UpgradeScrolls().Weapon.PieceINT15)


item = StarForce(
    itemName="제네시스 스태프",
    requiredLevel=200,
    requiredJobType=[JobType.Magician],
    itemBasicStat= stat,
    itemPart=ItemParts.Weapon,
    upgrade_chance=8,
    upgrade_history= upgradelist,
    starforce=22    
    )

print(item.TotalSpec()+item.UpgradeSpec()+item.ItemBasicStat)