from Item.Accessory.Heart import BlackHeart, FairyHeart
from Core.Enchant.Potential import PotentialOptionSlot, PotentialEnum, PotentialGrade
from Core.Enchant.Scroll import Upgrade, UpgradeScrolls
from Item.Accessory.Shoulder import ArcaneShadeMageShoulder
from Core.Server import GameServer
bh = BlackHeart()
#print(bh.TotalSpec())

fhpotentialo1 = PotentialOptionSlot(option=PotentialEnum.CriticalDamage, grade=PotentialGrade.Legendary, isadditional= False)
fhol = [fhpotentialo1]

fhaddio1 = [PotentialOptionSlot(option=PotentialEnum.DexOverLevel9, grade=PotentialGrade.Legendary, isadditional=True)]

fhupgradelist = []
for i in range(0,10):
    fhupgradelist.append(UpgradeScrolls().Heart.MagicalATK)


fh = FairyHeart(potentialOptionList=fhol, upgrade_history=fhupgradelist,starforce=8, additionalPotentialOptionList=fhaddio1)
#print(fh.TotalSpec().Show())

shoulderOption1 =  PotentialOptionSlot(option=PotentialEnum.IntPercentage, grade=PotentialGrade.Legendary, isadditional= False)
shoulderOption2 =  PotentialOptionSlot(option=PotentialEnum.IntPercentage, grade=PotentialGrade.Unique, isadditional= False)
shoulderOption3 =  PotentialOptionSlot(option=PotentialEnum.IntPercentage, grade=PotentialGrade.Unique, isadditional= False)

soptionslot = [shoulderOption1, shoulderOption2, shoulderOption3]

supgrade = []
for i in range(0, 2):
    supgrade.append(UpgradeScrolls().Accessory.PremiumSPELL)

ASShoulder = ArcaneShadeMageShoulder(
    potentialOptionList= soptionslot,
    starforce= 17,
    upgrade_history= supgrade,
    additionalPotentialOptionList=None,
    server= GameServer.RebootServer
)

#ASShoulder.TotalSpec().Show()

