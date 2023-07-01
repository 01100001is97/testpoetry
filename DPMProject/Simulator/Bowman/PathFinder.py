
from Dummy.Dummy import Dummy, DummySize
from datetime import timedelta
from Character.Adventurer.Archer.PathFinder import PathFinder
from Skill.CommonSkill import *
from Item.Preset.Arcane1715Archer import ItemPreset_1715_dex
from Core.Server import GameServer
from Simulator.Bowman.PathFinderDealingCycle import *
from Simulator.Simulate import Simulator, SimulatorEnum

PathFinder_1715 = PathFinder(level=275)

PathFinder_1715.CharItemSlot = ItemPreset_1715_dex

PathFinder_1715.Optimization(weapon=False, hyper=False, printing = True)


PathFinder_1715_Simulator = Simulator(
    character=PathFinder_1715,
    dummy=Dummy(
        Size=DummySize.large,
        Level=270,
        Guard=300,
        Arcane=0,
        ElementalResistance=True,
        Server=GameServer.NormalServer
    ),
    petbuff=[쓸만한_컴뱃오더스],
    mode=SimulatorEnum.Preset
)

PathFinder_1715_Simulator.Simulate(
    duration=timedelta(seconds=180),
    schedule=연계테스트,
    OnOffList=[]
    
)

PathFinder_1715_Simulator.ShowStackedBar()