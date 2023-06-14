from Core.Enchant.Potential import PotentialAbility, PotentialEnum, PotentialOptionSlot, PotentialGrade
from Core.Job import JobType
from Core.SpecElements import SpecVector
from Core.ABCItem import ItemParts
from Core.Server import GameServer

opt1 = PotentialOptionSlot(option=PotentialEnum.AllPercentage, grade=PotentialGrade.Legendary, isadditional=False)
opt2 = PotentialOptionSlot(option=PotentialEnum.StrPercentage, grade=PotentialGrade.Unique, isadditional=False)
opt3 = PotentialOptionSlot(option=PotentialEnum.Cooldown, grade=PotentialGrade.Legendary, isadditional=False)

optionlist = [opt1,opt2,opt3]

aopt1 = PotentialOptionSlot(option=PotentialEnum.LukOverLevel9, grade=PotentialGrade.Unique, isadditional= True)
aopt2 = PotentialOptionSlot(option=PotentialEnum.LukOverLevel9, grade=PotentialGrade.Unique, isadditional= True)
aopt3 = PotentialOptionSlot(option=PotentialEnum.LukPercentage, grade=PotentialGrade.Unique, isadditional= True)

addoptionlist = [aopt1, aopt2, aopt3]

item = PotentialAbility(
    itemName="거공",
    requiredLevel=200,
    requiredJobType=[JobType.Bowman],
    itemBasicStat=SpecVector(),
    itemPart=ItemParts.Belt,
    potentialOptionList=optionlist,
    additionalPotentialOptionList=addoptionlist,
    server=GameServer.NormalServer
)

print(item.TotalSpec())