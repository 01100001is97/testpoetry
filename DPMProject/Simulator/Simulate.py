from datetime import timedelta
from enum import Enum
from Dummy.Dummy import Dummy
from Character.ABCCharacter import ABCCharacter, CharacterStatus
from Core.Cooldown import Cooldown, TIME_UNIT, TIME_ZERO
from Core.ABCSkill import *
from Skill.Attributes import *
from Skill.CommonSkill import 쓸만한_샤프아이즈, 쓸만한_컴뱃오더스
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
from datetime import datetime


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
    def Cumulative(self):
        """DPM 시뮬레이션 시 데미지 누적값

        Returns:
            _type_: _description_
        """
        return self._Cumulative

    @Cumulative.setter
    def Cumulative(self,damage:int):
        if not isinstance(damage, int):
            raise TypeError("Damage must be an instance of int")
        
        if damage < 0:
            raise ValueError("damage must positive")
        
        self._Cumulative = damage

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

    def Simulate(self, duration:timedelta, schedule: SkillSchedule):
        """캐릭터와 더미를 대상으로 DPM 시뮬레이션을 수행함

        Args:
            duration (timedelta): _description_
        """
        nextSkill = None
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
            if not callable(nextSkill):
                nextSkill = schedule.Next()
            
            if nextSkill == None:
                self.EndSimulation()
                break
            
            # 스킬 후딜 중인지 체크함
            isSkipable = False
            if self.Character.Status in [CharacterStatus.Using_Skill]:
                # TODO: 현재 사용할 스킬이 사용중인 스킬을 스킵할 수 있는지 확인(연계)
                pass
            
            # 스킬 사용 가능 조건: 캐릭터의 휴식 혹은 다음 스킬 차례가 연계 가능한 스킬
            if self.Character.Status in [CharacterStatus.Idle] or isSkipable:
                for skill in self.Character._OnPressSkillList + self.Character._KeydownSkillList:
                    if skill == nextSkill:
                        # 만약 예약된 스킬이 쿨타임중이라면 다음 기회로 넘김
                        if issubclass(nextSkill, CooldownAttribute):
                            if not self.Character.ReadyFor(skill):
                                break
                        
                        # 스킬 인스턴스 설정
                        nextSkill = nextSkill()

                        # 스킬의 사용자, 타겟 설정
                        nextSkill._Owner = self.Character
                        nextSkill._Target = self.DummyTarget

                        # 컴뱃오더스가 사용중이라면 스킬에 적용
                        if issubclass(type(nextSkill), CombatOrdersAttribute):  
                            if not self.Character._JobName == JobName.Paladin:  
                                nextSkill.ApplyCombat(isOriginal = 쓸만한_컴뱃오더스 not in self.petBuffList)
                            pass

                        # 메르, 쿨감모 옵션에 따라 스킬 쿨타임 설정
                        if isinstance(nextSkill, CooldownAttribute):
                            self.Character.CooldownManager.Count(type(nextSkill))

                        
                        # 소환수 스킬을 사용한 경우 SummonManager 에 등록함
                        # 공격 스킬을(소환수가 아닌) 사용한 경우 DamageLog 를 출력함
                        # 버프 스킬을 사용한 경우 BuffManager에 등록함
                        logs = []
                        if isinstance(nextSkill, SummonAttribute):
                            self.Character.SummonManager.Add(nextSkill)
                        elif isinstance(nextSkill, DamageAttribute):
                            logs = nextSkill.UseSkill()
                        #elif 버프 등록
                        self.Timestamping(logs)

                        # 스킬에 후딜이 있다면, 캐릭터 딜레이 정보 입력
                        if isinstance(nextSkill, SkillDelayAttribute):
                            # 공속에 따라 스킬 딜레이 감소 - 스킬 정보 입력 단계에서 최고 공속으로 설정
                            self.Character.Delay = nextSkill.AttackDelay

                        # 해당 스킬을 찾은 시점에서 루프 종료
                        break
                        
            ## 스킬 사용 완료 후 정리 ## -----------------------
            # 시간 경과, 다음 사용 스킬 받아옴
            self.Tick()
        self.EndSimulation()
        
            
    def EndSimulation(self):
        i = 0
        skillCount = defaultdict(int)
        for log in self.SimulationLog:
            skillCount[log._SkillName] += 1
            print(f"Skill No. {i} (this skill No. {skillCount[log._SkillName]})")
            i += 1
            print(log)

    def Tick(self):
        logs = self.Character.Tick()
        if len(logs) > 0:
            self.Timestamping(logs)
        
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
                #print(log)
                bisect.insort(self.SimulationLog, log, key=lambda log: log.Timestamp)
    
    
    
    def Show_bar(self):
        rc('font', family='AppleGothic')
        plt.rcParams['axes.unicode_minus'] = False

        damage_logs = self.SimulationLog

        damage_accumulation = defaultdict(float)
        time_skill_damage = []

        for damage_log in damage_logs:
            skill_name = str(damage_log._SkillName)
            damage_value = damage_log._Damage
            print(f"Skill: {skill_name}, Damage: {damage_value}")
            damage_accumulation[skill_name] += damage_value
            time_skill_damage.append((damage_log.Timestamp.total_seconds(), damage_value, skill_name))
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

        # Calculate the per-second damage for each skill
        skill_per_second_damage = []
        for damage_list in skill_cumulative_damage:
            per_second_damage = np.diff(damage_list)
            skill_per_second_damage.append(per_second_damage)

        cumul = np.array([0.0 for _ in skill_per_second_damage[0]])
        for i, damage_list in enumerate(skill_per_second_damage):
            x = np.arange(len(damage_list))  # 시간대를 인덱스로 사용
            #y = [damage_list[j] for j in range(len(damage_list))]  # 스킬별로 해당 시간대의 초당 데미지 값 가져오기
            
            y = np.array(damage_list)
            
            skill_name = list(damage_accumulation.keys())[i]

            plt.bar(x, y, label=skill_name, bottom=cumul)
            cumul += y
            



        plt.xlabel('Time (seconds)')
        plt.ylabel('Damage per Second')
        plt.title('Per-Second Damage by Skill')
        plt.legend()

        plt.show()


        
    
    def ShowCumulative_line(self):
        rc('font', family='AppleGothic')
        plt.rcParams['axes.unicode_minus'] = False

        damage_logs = self.SimulationLog

        damage_accumulation = defaultdict(float)
        time_skill_damage = []

        for damage_log in damage_logs:
            print(damage_log._Damage)
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
            print(f"Skill {i+1} Damage List: {damage_list}")

        rc('TkAgg')
        plt.stackplot(time_list, skill_cumulative_damage, labels=damage_accumulation.keys())

        plt.xlabel('Time (seconds)')
        plt.ylabel('Damage')
        plt.title('Cumulative Damage over Time')
        plt.legend()

        plt.show()

    def ShowCumulative_bar(self):
        rc('font', family='AppleGothic')
        plt.rcParams['axes.unicode_minus'] = False

        damage_logs = self.SimulationLog

        damage_accumulation = defaultdict(float)
        time_skill_damage = []

        for damage_log in damage_logs:
            skill_name = str(damage_log._SkillName)
            damage_value = damage_log._Damage
            print(f"Skill: {skill_name}, Damage: {damage_value}")
            damage_accumulation[skill_name] += damage_value
            time_skill_damage.append((damage_log.Timestamp.total_seconds(), damage_value, skill_name))
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
            damage_cumulative = np.cumsum(damage_list)

            # Make sure all lists have the same length by padding with the last value
            if len(damage_cumulative) < len(time_list):
                last_value = damage_cumulative[-1]
                padding = [last_value] * (len(time_list) - len(damage_cumulative))
                damage_cumulative.extend(padding)

            skill_cumulative_damage.append(damage_cumulative)

        # Plot the cumulative bar graph
        for i, damage_list in enumerate(skill_cumulative_damage):
            x = np.arange(len(damage_list))  # 시간대를 인덱스로 사용
            y = [damage_list[j] for j in range(len(damage_list))]  # 스킬별로 해당 시간대의 누적 데미지 값 가져오기
            skill_name = list(damage_accumulation.keys())[i]

            plt.bar(x, y, label=skill_name)

        plt.xlabel('Time (seconds)')
        plt.ylabel('Cumulative Damage')
        plt.title('Cumulative Damage by Skill')
        plt.legend()

        plt.show()