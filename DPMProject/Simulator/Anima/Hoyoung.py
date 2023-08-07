
from Dummy.Dummy import Dummy, DummySize
from datetime import timedelta
from Character.Anima.Hoyoung import Hoyoung
from Skill.CommonSkill import *
from Skill.Anima.Hoyoung import *
from Item.Preset.Arcane1715Theif import ItemPreset_1715_luk
from Core.Server import GameServer
from Character.Anima.Hoyoung import Hoyoung
from Simulator.Anima.HoyoungDealingCycle import HoyoungDealingMode
from Simulator.Simulate import Simulator, SimulatorEnum

Hoyoung_1715 = Hoyoung(level=275)

Hoyoung_1715.CharItemSlot = ItemPreset_1715_luk

Hoyoung_1715.Optimization(weapon=False, hyper=False, printing = True)


Hoyoung_1715_Simulator = Simulator(
    character=Hoyoung_1715,
    dummy=Dummy(
        Size=DummySize.large,
        Level=270,
        Guard=300,
        Arcane=0,
        ElementalResistance=True,
        Server=GameServer.NormalServer
    ),
    petbuff=[쓸만한_컴뱃오더스,쓸만한_샤프아이즈, 메이플_용사],
    mode=SimulatorEnum.Preset
)

Hoyoung_1715_Simulator.Simulate(
    duration=timedelta(seconds=50),
    schedule=Hoyoung_1715.GetFlexibleScheduler(HoyoungDealingMode.토금파금),
    OnOffList=[부채가속]
    
)

Hoyoung_1715_Simulator.ShowStackedBar()