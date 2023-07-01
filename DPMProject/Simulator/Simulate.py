from datetime import timedelta
from enum import Enum
from Dummy.Dummy import Dummy
from Character.ABCCharacter import ABCCharacter, CharacterStatus
from Core.Job import JobNameInfo
from Core.Cooldown import Cooldown, TIME_UNIT, TIME_ZERO
from Core.ABCSkill import *
from Skill.Attributes import *
from Skill.CommonSkill import 쓸만한_샤프아이즈, 쓸만한_컴뱃오더스, 대기
from Simulator.DamageLog import DamageLog
from Simulator.SkillSchedule import SkillSchedule
from collections import defaultdict
import bisect
import matplotlib.pyplot as plt
from matplotlib import rc
import pandas as pd
import numpy as np
from collections import defaultdict
import matplotlib.dates as mdates
from copy import deepcopy
import math

class SimulatorEnum(Enum):
    Preset = 0
    Realtime = 1
    

class Simulator:
    """
    시뮬레이션을 수행하는 Simulator 클래스.

    Args:
        character (ABCCharacter): 시뮬레이션에 사용할 캐릭터 인스턴스.
        dummy (Dummy): 공격 대상인 더미 인스턴스.
        mode (SimulatorEnum): 시뮬레이션 모드, SimulatorEnum의 값이어야 함.

    Raises:
        TypeError: character가 ABCCharacter의 인스턴스가 아닐 경우,
                   dummy가 Dummy의 인스턴스가 아닐 경우,
                   mode가 SimulatorEnum의 인스턴스가 아닐 경우,
                   skill이 ActiveSkill의 인스턴스가 아닐 경우,
                   damage가 int가 아닐 경우.
                   
        ValueError: damage 값이 음수일 경우.
    """
    def __init__(self, character:ABCCharacter, dummy: Dummy, mode: SimulatorEnum, petbuff:list[Skill]):
        self.Character = character
        self.DummyTarget = dummy
        self.SimulationTime = timedelta(seconds=0)
        self.Mode = mode
        self.petBuffList = petbuff
        self.SimulationLog = []
        self._CurrentTime = timedelta(seconds=0)
        self.nothing = ""
        self.waiting = 대기()
        self.savepath = "Simulator/Logs/"
    @property
    def Character(self):
        """시뮬레이션 하는 캐릭터 인스턴스

        Returns:
            _type_: _description_
        """
        return self._Character

    @Character.setter
    def Character(self, character: ABCCharacter):
        if not isinstance(character, ABCCharacter):
            raise TypeError("Character must be an instance of ABC")
        self._Character = character

    @property
    def DummyTarget(self):
        """공격의 대상이 되는 허수아비

        Returns:
            _type_: _description_
        """
        return self._Dummy

    @DummyTarget.setter
    def DummyTarget(self, dummy: Dummy):
        if not isinstance(dummy, Dummy):
            raise TypeError("Dummy must be an instance of Dummy")
        self._Dummy = dummy

    @property
    def SimulationTime(self):
        """시뮬레이션을 진행할 총 시간

        Returns:
            _type_: _description_
        """
        return self._SimulationTime

    @SimulationTime.setter
    def SimulationTime(self, time: timedelta):
        if not isinstance(time, timedelta):
            raise TypeError("SimulationTime must be an instance of timedelta")
        self._SimulationTime = time

    @property
    def Mode(self):
        """시뮬레이션 모드. 모드는 총 2가지로, SimulatorEnum 을 따름

        Returns:
            _type_: _description_
        """
        return self._Mode

    @Mode.setter
    def Mode(self, mode: 'SimulatorEnum'):
        if not isinstance(mode, SimulatorEnum):
            raise TypeError("Mode must be an instance of SimulatorEnum")
        self._Mode = mode
    
    
    @property
    def Cumulative15(self):
        """DPM 시뮬레이션 시 데미지 누적값

        Returns:
            _type_: _description_
        """
        damage_logs = self.SimulationLog
        max_damage = 0
        max_interval = None
        start = 0
        end = 0
        total_damage = 0

        while start < len(damage_logs):
            # Find the maximum index within 15 seconds
            while end < len(damage_logs) and damage_logs[end].Timestamp - damage_logs[start].Timestamp <= timedelta(seconds=15):
                total_damage += damage_logs[end]._Damage
                end += 1

            # Update maximum damage and interval
            if total_damage > max_damage:
                max_damage = total_damage
                max_interval = (start, end - 1)

            # Subtract the damage of the start log and move the start pointer
            total_damage -= damage_logs[start]._Damage
            start += 1

        return max_damage, max_interval

    

    @property
    def NextSkill(self):
        return self._NextSkill
    
    @NextSkill.setter
    def NextSkill(self, skill):
        if not isinstance(skill, ActiveSkill):
            raise TypeError("사용할 스킬은 ActiveSkill 형태여야 함")
        self._NextSkill = skill

    @property
    def CurrentTime(self):
        return self._CurrentTime
    
    @CurrentTime.setter
    def CurrentTime(self, time:timedelta):
        if not isinstance(time, timedelta):
            raise TypeError("CurrentTime must be a timedelta type")
        if time < TIME_ZERO:
            raise AttributeError("시뮬레이션 시간이 0초이상")
        
        self._CurrentTime = time

    def Simulate(self, duration:timedelta, schedule: SkillSchedule, OnOffList: list):
        """캐릭터와 더미를 대상으로 DPM 시뮬레이션을 수행함

        Args:
            duration (timedelta): _description_
        """

        for buff in OnOffList:
            if issubclass(buff, SummonAttribute):
                buff = buff()
                buff.Owner = self.Character
                buff.Target = self.DummyTarget

                self.Character.SummonManager.Add(buff)
            elif issubclass(buff, BuffAttribute):
                
                self.Character.BuffManager.Add(buff)
        NextSkill = False
        while self.CurrentTime < duration:
            # 0. 캐릭터가 행동할 수 있는 상태인지 확인: 만약 연계할 수 있다면 연계 가능한 스킬 사용 가능 = 캐릭터의 정보 로딩
                # 1. 사용할 스킬을 받아옴 (Realtime 모드에서는 어떤 스킬을 사용할 수 있는지 보여주고 입력을 대기)
                # 1.5 컴뱃 오더스 있다면 적용
                # 2. 스킬을 시전 = 스킬에 타겟, 캐릭터 설정, 스킬 딜레이 적용, 쿨타임이 있다면 적용,
                # 3. 데미지 저장, 디버그용 기록 저장
            # 1. 예약된 스킬들 사용
            # 2. 시간 0.01초 증가
            # 3. 버프의 지속시간이 종료되면 버프를 해제함
            
            
                        

            # 다음 사용할 스킬을 불러옴
            if not callable(NextSkill):
                NextSkill = schedule.Next()

                # 스킬 딜사이클의 마지막
                if NextSkill == None:
                    self.EndSimulation(schedule)
                    break
                
                if issubclass(NextSkill, 대기):
                    NextSkill = self.waiting
                    self.Tick()
                    #self.Timestamping(self.waiting.UseSkill())
                    continue

            
            
            # 스킬 후딜 중인지 체크함
            isSkipable = False
            if self.Character.Status in [CharacterStatus.Using_Skill]:
                if issubclass(NextSkill, SkipableAttribute):
                    
                    skipableList = NextSkill().ComboSkillList
                    for i in range(0, len(skipableList)):
                        lastSkill = schedule.Before()
                        if lastSkill == skipableList[i]:
                            if NextSkill().Skip[i] <= lastSkill().AttackDelay - self.Character._Delay:
                                isSkipable = True
                                break

            
            # 스킬 사용 가능 조건: 캐릭터의 휴식 혹은 다음 스킬 차례가 연계 가능한 스킬
            if self.Character.Status in [CharacterStatus.Idle] or isSkipable:
                for skill in self.Character._OnPressSkillList + self.Character._KeydownSkillList:
                    if skill == NextSkill:
                        # 만약 예약된 스킬이 쿨타임중이라면 다음 기회로 넘김
                        if issubclass(NextSkill, (CooldownAttribute, ChargedCooldownAttribute)):
                            if not self.Character.ReadyFor(skill):
                                break
                        
                        # 스킬 인스턴스 설정
                        NextSkill = NextSkill()

                        # 스킬의 사용자, 타겟 설정
                        NextSkill._Owner = self.Character
                        NextSkill._Target = self.DummyTarget

                        # 컴뱃오더스가 사용중이라면 스킬에 적용
                        if issubclass(type(NextSkill), CombatOrdersAttribute):  
                            if not self.Character._JobName == JobName.Paladin:  
                                NextSkill.ApplyCombat(isOriginal = 쓸만한_컴뱃오더스 not in self.petBuffList)
                            pass

                        # 메르, 쿨감모 옵션에 따라 스킬 쿨타임 설정
                        if isinstance(NextSkill, CooldownAttribute):
                            self.Character.CooldownManager.Count(type(NextSkill))

                        
                        # 소환수 스킬을 사용한 경우 SummonManager 에 등록함
                        # 공격 스킬을(소환수가 아닌) 사용한 경우 DamageLog 를 출력함
                        # 버프 스킬을 사용한 경우 BuffManager에 등록함
                        logs = []
                        
                        if isinstance(NextSkill, SummonAttribute):
                            self.Character.SummonManager.Add(NextSkill)
                        elif isinstance(NextSkill, KeydownSkill):
                            KeydownInterval = deepcopy(NextSkill.Interval)
                            keydownTime = int(NextSkill.KeydownTime.total_seconds()/TIME_UNIT.total_seconds())
                            startTime = int(NextSkill.Interval.total_seconds()/TIME_UNIT.total_seconds())
                            for i in range(0, keydownTime -1):                                
                                if KeydownInterval == TIME_ZERO:
                                    logs = NextSkill.UseSkill()
                                    self.Timestamping(logs)
                                    KeydownInterval = deepcopy(NextSkill.Interval)
                                KeydownInterval.update()
                                self.Tick()
                            self.Timestamping(NextSkill.Finish())
                        elif isinstance(NextSkill, OriginSkill):
                            nextInterval = NextSkill.TimingTable[NextSkill.index]
                            NextSkill.index += 1
                            SceneDuration = int(NextSkill.AttackDelay.total_seconds()/TIME_UNIT.total_seconds())
                            if hasattr(NextSkill, "Before"):
                                NextSkill.Before()
                            for i in range(0, SceneDuration):
                                if nextInterval == TIME_ZERO:
                                    logs = NextSkill.UseSkill()
                                    self.Timestamping(logs)
                                    nextInterval = NextSkill.TimingTable[NextSkill.index]
                                    NextSkill.index += 1

                                nextInterval.update()
                                self.Tick()
                            # 후딜없음
                            NextSkill.Finish()
                            NextSkill.AttackDelay = Cooldown()
                            

                        elif isinstance(NextSkill, DamageAttribute):
                            self.Timestamping(NextSkill.UseSkill())
                        elif isinstance(NextSkill, BuffAttribute):
                            self.Character.BuffManager.Add(NextSkill)
                        

                        # 스킬에 후딜이 있다면, 캐릭터 딜레이 정보 입력
                        if isinstance(NextSkill, SkillDelayAttribute):
                            # 공속에 따라 스킬 딜레이 감소 - 스킬 정보 입력 단계에서 최고 공속으로 설정
                            self.Character.Delay = deepcopy(NextSkill.AttackDelay)
                        else:
                            self.Character.Delay = Cooldown()
                        # 해당 스킬 사용 후 종료
                        break
                        
            ## 스킬 사용 완료 후 정리 ## -----------------------
            # 시간 경과, 다음 사용 스킬 받아옴
            self.Tick()
        self.EndSimulation(schedule)
        
            
        
    def EndSimulation(self, schedule: SkillSchedule):
        
        TotalDamage = 0
        i = 0
        max_damage = 0
        max_interval = None
        start = 0
        end = 0
        total_damage = 0
        skillCount = defaultdict(int)
        charName = self.Character._JobName.value[JobNameInfo.name.value]

        with open(self.savepath + charName + ".txt", 'w') as f:
            f.write(charName)
            f.write("\n현재 캐릭터의 기본 스펙(도핑, 패시브 포함)\n")
            f.write(str(self.Character.TotalSpec) + "\n\n")
            f.write("### 딜사이클 ###:\n" + str(schedule))
            f.write("\n\n###데미지 로그###\n")

            for log in self.SimulationLog:
                # Add the damage of the current log and move the end pointer
                total_damage += log._Damage
                end += 1

                # Find the maximum index within 15 seconds
                while log._Timestamp - self.SimulationLog[start]._Timestamp > timedelta(seconds=15):
                    # Subtract the damage of the start log and move the start pointer
                    total_damage -= self.SimulationLog[start]._Damage
                    start += 1

                # Update maximum damage and interval
                if total_damage > max_damage:
                    max_damage = total_damage
                    max_interval = (start, end - 1)

                if log is not self.nothing:
                    skillCount[log._SkillName] += 1
                    f.write(f"Attack No. {i+1} (this skill No. {skillCount[log._SkillName]})\n")
                    i += 1
                    f.write(str(log) + '\n')
                    TotalDamage += log._Damage

            f.write(f"최대 데미지를 기록한 15초 구간: {self.SimulationLog[max_interval[0]]._Timestamp} ~ {self.SimulationLog[max_interval[1]]._Timestamp}\n")
            f.write(f"그 시간 구간 동안의 총 데미지: {max_damage:,}\n")
            f.write(f"총 시뮬레이션 시간: {log._Timestamp}\n")
            f.write(f"총 데미지: {TotalDamage:,}\n")

    

    def Tick(self):
        logs = self.DummyTarget.Tick()
        logs = self.Character.Tick()
        if len(logs) > 0:
            self.Timestamping(logs)
        for buff in  self.petBuffList:
            # 메르, 쿨감모 옵션에 따라 스킬 쿨타임 설정
            if issubclass(buff, CooldownAttribute):
                if self.Character.CooldownManager.Count(buff):
                    if issubclass(buff, OnPressSkill):
                        self.Character.BuffManager.Add(buff())
        
                   

            
        self.CurrentTime += TIME_UNIT
        
    def Timestamping(self, logs:list):
        if len(logs) == 0:
            return 
        if (not isinstance(logs, list)):
            raise TypeError("logs 는 DamageLog의 리스트")
        if not all(isinstance(log, (DamageLog, type(None))) for log in logs):
            raise TypeError("logs 는 DamageLog의 리스트")
        
        for log in logs:
            if log is not None:
                log.Timestamp = self.CurrentTime
                if log is not self.nothing:
                    print(log)
                bisect.insort(self.SimulationLog, log, key=lambda log: log.Timestamp)
    
    


    

    def ShowStackedBar(self):
        rc('font', family='AppleGothic')
        plt.rcParams['axes.unicode_minus'] = False

        damage_logs = self.SimulationLog

        damage_accumulation = defaultdict(float)
        time_skill_damage = []

        for damage_log in damage_logs:
            skill_name = str(damage_log._SkillName)
            damage_accumulation[skill_name] += damage_log._Damage
            time_skill_damage.append((damage_log.Timestamp.total_seconds(), damage_log._Damage, skill_name))

        df = pd.DataFrame(time_skill_damage, columns=['Time', 'Skill Damage', 'Skill'])

        df.sort_values('Time', inplace=True)

        time_list = np.arange(math.floor(df['Time'].min()), df['Time'].max() + 1, 1)  # Create a time list that includes every second
        skill_cumulative_damage = []

        for skill_name in damage_accumulation.keys():
            skill_df = df[df['Skill'] == skill_name].copy()

            # Round the time values to the nearest second and group by the rounded time
            skill_df['Rounded Time'] = skill_df['Time'].apply(math.ceil)
            skill_df = skill_df.groupby('Rounded Time')['Skill Damage'].sum().reset_index()

            # Create a full DataFrame that includes every second, and merge it with the skill DataFrame
            full_df = pd.DataFrame(time_list, columns=['Rounded Time'])
            skill_df = pd.merge(full_df, skill_df, on='Rounded Time', how='outer').fillna(0)

            damage_list = skill_df['Skill Damage'].tolist()

            # Make sure all lists have the same length by padding with 0
            if len(damage_list) < len(time_list):
                padding = [0] * (len(time_list) - len(damage_list))
                damage_list.extend(padding)

            skill_cumulative_damage.append(damage_list)

        # Instead of using a stackplot, we use a bar plot for each skill's damage
        cumul = np.array([0.0] * len(time_list))

        for i, damage_list in enumerate(skill_cumulative_damage):
            plt.bar(time_list, damage_list, bottom=cumul, label=list(damage_accumulation.keys())[i])
            cumul += np.array(damage_list)

        plt.xlabel('Time (seconds)')
        plt.ylabel('Damage')
        plt.title('Damage over Time')
        plt.legend()

        plt.show()

    
    
    def ShowStackedCumulativePlot(self):
        rc('font', family='AppleGothic')
        plt.rcParams['axes.unicode_minus'] = False

        damage_logs = self.SimulationLog

        damage_accumulation = defaultdict(float)
        time_skill_damage = []

        for damage_log in damage_logs:
            #print(damage_log._Damage)
            skill_name = str(damage_log._SkillName)
            damage_accumulation[skill_name] += damage_log._Damage
            time_skill_damage.append((damage_log.Timestamp.total_seconds(), damage_log._Damage, skill_name))

        df = pd.DataFrame(time_skill_damage, columns=['Time', 'Skill Damage', 'Skill'])

        df.sort_values('Time', inplace=True)

        time_list = np.arange(math.floor(df['Time'].min()), df['Time'].max() + 1, 1)  # Create a time list that includes every second
        skill_cumulative_damage = []

        for skill_name in damage_accumulation.keys():
            skill_df = df[df['Skill'] == skill_name].copy()

            # Round the time values to the nearest second and group by the rounded time
            skill_df['Rounded Time'] = skill_df['Time'].round()
            skill_df = skill_df.groupby('Rounded Time')['Skill Damage'].sum().reset_index()

            # Create a full DataFrame that includes every second, and merge it with the skill DataFrame
            full_df = pd.DataFrame(time_list, columns=['Rounded Time'])
            skill_df = pd.merge(full_df, skill_df, on='Rounded Time', how='outer').fillna(0)

            damage_list = skill_df['Skill Damage'].tolist()
            damage_cumulative = np.cumsum(damage_list).tolist()

            # Make sure all lists have the same length by padding with the last value
            if len(damage_cumulative) < len(time_list):
                last_value = damage_cumulative[-1]
                padding = [last_value] * (len(time_list) - len(damage_cumulative))
                damage_cumulative.extend(padding)

            skill_cumulative_damage.append(damage_cumulative)


        for i, damage_list in enumerate(skill_cumulative_damage):
            #print(f"Skill {i+1} Damage List: {damage_list}")
            pass

        rc('TkAgg')
        plt.stackplot(time_list, skill_cumulative_damage, labels=damage_accumulation.keys())

        plt.xlabel('Time (seconds)')
        plt.ylabel('Damage')
        plt.title('Cumulative Damage over Time')
        plt.legend()

        plt.show()
