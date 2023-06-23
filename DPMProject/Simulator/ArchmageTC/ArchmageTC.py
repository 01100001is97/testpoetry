from Character.Adventurer.Magician.ArchmageTC import ArchmageTC
from Item.Preset.Arcane1715Mage import ItemPreset_1715_int
from Core.Damage import BattlePower
from Simulator.Simulate import Simulator, SimulatorEnum
from Dummy.Dummy import Dummy, DummySize
from Core.Server import GameServer
from datetime import timedelta    
from Skill.Adventurer.Magician.Archmage import *
from Skill.Adventurer.Magician.ThunderCold import *
from Skill.CommonSkill import 쓸만한_샤프아이즈, 쓸만한_컴뱃오더스
from Simulator.ArchmageTC.ArchmageTCDealingCycle import testCycle


#1. 아이템 슬롯
#2. 하이퍼스텟
# 컴뱃오더스를 포함한 펫버프, 온오프 스킬, 시드링, 특수코어 설정은 Simulation.py 에서 수행
ArchmageTC_1715 = ArchmageTC(level=275)
# 1. 아이템 슬롯 설정
ArchmageTC_1715.CharItemSlot = ItemPreset_1715_int
ArchmageTC_1715.Optimization(weapon=False, hyper=False)

sim = Simulator(
    character=ArchmageTC_1715,
    dummy=Dummy(
        Size=DummySize.large,
        Level=270,
        Guard=300,
        Arcane=0,
        ElementalResistance=True,
        Server=GameServer.NormalServer
    ),
    petbuff=[쓸만한_컴뱃오더스, 쓸만한_샤프아이즈, 메디테이션],
    mode=SimulatorEnum.Preset
)

sim.Simulate(
    duration=timedelta(milliseconds=3000), 
    skillQueue=testCycle
    )