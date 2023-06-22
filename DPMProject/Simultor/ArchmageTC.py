from Simulate import Simulator, SimulatorEnum
from Character.Adventurer.Magician.ArchmageTC import ArchmageTC
from Item.Preset.Arcane1715Mage import ItemPreset_1715_int
from Core.Damage import BattlePower

#1. 아이템 슬롯
#2. 하이퍼스텟
# 컴뱃오더스를 포함한 펫버프, 온오프 스킬, 시드링, 특수코어 설정은 Simulation.py 에서 수행
ArchmageTC_1715 = ArchmageTC(level=275)
# 1. 아이템 슬롯 설정
ArchmageTC_1715.CharItemSlot = ItemPreset_1715_int
ArchmageTC_1715.Optimization()

#print(ArchmageTC_1715.SetupCheckList)
ArchmageTC_1715.TotalSpec.Show()

print(BattlePower(
    ArchmageTC_1715.TotalSpec,
    jobtype=ArchmageTC_1715._Job,
    considerGuard=300,
    isBoss=True
))