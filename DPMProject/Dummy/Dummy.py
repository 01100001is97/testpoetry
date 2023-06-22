from enum import Enum
from Core.Server import GameServer
from Core.SpecElements import SpecVector, CoreStat
from Core.ABCSkill import Skill

class DummySize:
    small = 0
    medium = 1
    large = 2

class Dummy:
    def __init__(self, Size: DummySize, Level: int, Guard: int, Arcane: int, ElementalResistance: int, Server: GameServer, Health:int):
        self.Size = Size
        self.Level = Level
        self.Guard = Guard
        self.Arcane = Arcane
        self.ElementalResistance = ElementalResistance
        self.Server = Server
        
        
   
    @property
    def Size(self):
        return self._Size

    @Size.setter
    def Size(self, Size: DummySize):
        if not isinstance(Size, DummySize):
            raise TypeError("Size must be an instance of DummySize.")
        self._Size = Size

    @property
    def Level(self):
        return self._Level

    @Level.setter
    def Level(self, Level: int):
        if not isinstance(Level, int):
            raise TypeError("Level must be an integer.")
        if Level < 1:
            raise ValueError("Level must be at least 1.")
        self._Level = Level

    @property
    def Guard(self):
        return self._Guard

    @Guard.setter
    def Guard(self, Guard: int):
        if not isinstance(Guard, int):
            raise TypeError("Guard must be an integer.")
        if Guard < 0:
            raise ValueError("Guard must be non-negative.")
        self._Guard = Guard

    @property
    def Arcane(self):
        return self._Arcane

    @Arcane.setter
    def Arcane(self, Arcane: int):
        if not isinstance(Arcane, int):
            raise TypeError("Arcane must be an integer.")
        if Arcane < 0:
            raise ValueError("Arcane must be non-negative.")
        self._Arcane = Arcane

    @property
    def ElementalResistance(self):
        return self._ElementalResistance

    @ElementalResistance.setter
    def ElementalResistance(self, ElementalResistance: int):
        if not isinstance(ElementalResistance, int):
            raise TypeError("ElementalResistance must be an integer.")
        if ElementalResistance < 0 or ElementalResistance > 100:
            raise ValueError("ElementalResistance must be between 0 and 100.")
        self._ElementalResistance = ElementalResistance

    @property
    def Server(self):
        return self._Server

    @Server.setter
    def Server(self, Server: GameServer):
        if not isinstance(Server, GameServer):
            raise TypeError("Server must be an instance of GameServer.")
        self._Server = Server

    @property
    def Health(self):
        return self._Health

    @Health.setter
    def Health(self, Health: int):
        if not isinstance(Health, int):
            raise TypeError("Health must be an integer.")
        if Health < 0:
            raise ValueError("Health must be non-negative.")
        self._Health = Health

    
    

