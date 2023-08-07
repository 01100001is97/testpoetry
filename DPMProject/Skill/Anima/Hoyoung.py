from typing import Any
from Core.ABCSkill import PassiveSkill, SkillAdvance, OnPressSkill, KeydownSkill, AutomateActivativeSkill, OriginSkill
from Core.SpecElements import SpecVector, CoreStat, CreateSpecVector
from Skill.Attributes import *
from Skill.CommonSkill import 쓸만한_컴뱃오더스, 그란디스_여신의_축복
from Core.Cooldown import TIME_ZERO
from Core.Condition import ConditionEnum
from Core.Probability import SuccessProbability
from random import random
from Character.ABCCharacter import CharacterStatus
from Dummy.Dummy import Dummy, DummySize
from datetime import timedelta
from enum import Enum
import random
import math

class 천지인_속성(Enum):
    천 = 0
    지 = 1
    인 = 2
    허 = 3

class 부적_도력:
    def __init__(self) -> None:
        self._AmuletGuage = 100
        self._MaxAmuletGuage = 100
        self._NowCombo = 0
        self.MaxCombo = 3
        self.천 = False
        self.지 = False
        self.인 = False
        self.허 = False
        # 방금 사용한 스킬의 속성
        self._now = None
        # 3단계 연계 성공 여부
        self.OnSuccess = False
        self.successStack = 0
        self.Owner = None


    @property
    def AmuletGuage(self):
        return self._AmuletGuage
    
    @AmuletGuage.setter
    def AmuletGuage(self, num):
        num = max(0,min(num, self._MaxAmuletGuage))
        
        self._AmuletGuage = num

    @property
    def NowCombo(self):
        return self._NowCombo
    
    @NowCombo.setter
    def NowCombo(self, num:int):
        
        combo1 = 10
        combo2 = 15
        combo3 = 20
        scroll = 15
        if self.Owner.BuffManager.isRegistered(그란디스_여신의_축복):
            combo1 *= 1.75
            combo2 *= 1.75
            combo3 *= 1.75
            scroll *= 1.75

        if num != 1:
            raise ValueError("콤보는 한번에 1씩 올라감")
        
        self._NowCombo += 1

        if self._NowCombo == 1:
            # 게이지 상승
            self.AmuletGuage += combo1
        elif self._NowCombo == 2:
            self.AmuletGuage += combo2
        elif self._NowCombo == 3:
            self.AmuletGuage += combo3
            # 연계 성공 시 효과
            self._NowCombo = 0
            
        
        # 속성 공격시 두루마리 게이지 상승
        두루마리.ScrollGuage += scroll
        
        combo1 = 10
        combo2 = 15
        combo3 = 20
        scroll = 15

    @property
    def Status(self):
        return (self.천, self.지, self.인)
    
    @property
    def Now(self):
        return self._now
    
    @Now.setter
    def Now(self, elemental:천지인_속성):
        if not isinstance(elemental, 천지인_속성):
            raise TypeError('호영 스킬 속성은 천지인 속성 중 하나임')
        nowStatus = self.Status

        # 현재 사용하는 속성을 기록함
        if elemental == 천지인_속성.허:
            return
        # TODO: 속성 설정시 도력 증가 설정
        if elemental == 천지인_속성.천:
            self.천 = True
        elif elemental == 천지인_속성.지:
            self.지 = True
        elif elemental == 천지인_속성.인:
            self.인 = True

        #천지인 속성에 변화가 있는 경우 콤보 증가
        for i in [천지인_속성.천, 천지인_속성.지, 천지인_속성.인]:
            if nowStatus[i.value] != self.Status[i.value]:
                self.NowCombo = 1

        # 방금 사용한 스킬 속성을 기록
        self._now = elemental

        
        if self.천 and self.지 and self.인:
            self.천 = False
            self.지 = False
            self.인 = False
            self.OnSuccess = True
            self.successStack += 1
            if self.Owner.BuffManager.isRegistered(선기_천지인_환영_버프):
                for skill in [금고봉_인, 지진쇄_지, 멸화염_천]:
                    if self.Owner.CooldownManager.ReduceCooldown(skill, Cooldown(seconds=15)):
                        break
        
class 두루마리_도력:
    def __init__(self) -> None:
        self._ScrollGuage = 900
        self.MaxScrollGuage = 900
        self.Owner = None
        # 천지인 속성 공격시 도력 15충전 - 부적도력 combo 부분
        # 부적 도술 사용시 두루마리 도력 200 충전

    @property
    def ScrollGuage(self):
        return self._ScrollGuage
    
    @ScrollGuage.setter
    def ScrollGuage(self, num:int):
        if self.Owner.BuffManager.isRegistered(그란디스_여신의_축복):
            num = self.ScrollGuage + (num - self.ScrollGuage) * 1.75
        num = max(0,min(num, self.MaxScrollGuage))
        
        self._ScrollGuage = num

부적 = 부적_도력()
두루마리 = 두루마리_도력()

class 정령친화(PassiveSkill):
    def __init__(self,level = 1):
        self.SummonDuration = 10
        PassiveSkill.__init__(
            self=self,
            advanced=SkillAdvance.Zero,
            level=level,
            max=1
        )

class 괴이봉인(PassiveSkill, BuffAttribute):
    def __init__(self, level=1):
        max = 1
        stat = SpecVector()
        stat[CoreStat.ATTACK_PHYSICAL_PERCENTAGE] = 10
        stat[CoreStat.FINAL_DAMAGE_PERCENT] = 10

        PassiveSkill.__init__(self, advanced=SkillAdvance.Zero, level=level, max=max)
        BuffAttribute.__init__(self, stat=stat)

# 공속증가 효과가 있지만 이미 모델링되어 있으므로 하지않음
class 부채가속(OnPressSkill):
    def __init__(self, level = 10):
        max = 10
        PassiveSkill.__init__(
            self=self,
            advanced=SkillAdvance.Second,
            level=level,
            max=max
        )

class 부채_숙련(PassiveSkill, BuffAttribute):
    def __init__(self, level=10):
        max = 10
        stat = SpecVector()
        stat[CoreStat.ATTACK_PHYSICAL] = self.set_attack_power(level)

        PassiveSkill.__init__(self=self, advanced=SkillAdvance.Second, level=level, max=max)
        BuffAttribute.__init__(self=self, stat=stat)
        

    def set_mastery(self, level:int):
        return 50

    def set_attack_power(self, level:int):
        return 25

class 심안(PassiveSkill, BuffAttribute):
    def __init__(self, level=10):
        max = 10
        stat = SpecVector()

        stat[CoreStat.CRITICAL_PERCENTAGE] = 30
        stat[CoreStat.CRITICAL_DAMAGE] = 10

        PassiveSkill.__init__(self=self, advanced=SkillAdvance.Second, level=level, max=max)
        BuffAttribute.__init__(self=self, stat=stat)

class 신체_단련(PassiveSkill, BuffAttribute):
    def __init__(self, level=5):
        max = 5
        stat = SpecVector()

        stat[CoreStat.STAT_LUK] = 60

        PassiveSkill.__init__(self=self, advanced=SkillAdvance.Second, level=level, max=max)
        BuffAttribute.__init__(self=self, stat=stat)

class 고급_부채_숙련(PassiveSkill, MasteryAttribute, BuffAttribute, CombatOrdersAttribute):
    def __init__(self, level=30):
        max = 30
        stat = SpecVector()
        advancedMastery = self.set_mastery(level)

        stat[CoreStat.ATTACK_PHYSICAL] = self.set_attack_power(level)
        stat[CoreStat.FINAL_DAMAGE_PERCENT] = self.set_final_damage(level)

        PassiveSkill.__init__(self=self, advanced=SkillAdvance.Fourth, level=level, max=max)
        BuffAttribute.__init__(self=self, stat=stat)
        MasteryAttribute.__init__(self=self, mastery= advancedMastery)
        CombatOrdersAttribute.__init__(self)

    def set_mastery(self, level:int):
        return 55+math.ceil(level/2)

    def set_attack_power(self, level:int):
        return level + 10

    def set_final_damage(self, level:int):
        return 14 + math.floor(level/2)

    @property
    def Level(self):
        return self._level
    
    @Level.setter
    def Level(self, level:int):
        if not isinstance(level, int) or level < 0:
            raise ValueError("Level must be a non-negative integer")
        if level > self.MaxLevel:
            self._level = level
        self._level = level
        self.Mastery = self.set_mastery(level)
        self.BuffStat[CoreStat.ATTACK_PHYSICAL] = self.set_attack_power(level)
        self.BuffStat[CoreStat.FINAL_DAMAGE_PERCENT] = self.set_final_damage(level)

class 점정(PassiveSkill, BuffAttribute, CombatOrdersAttribute):
    def __init__(self, level=10):
        max = 10
        stat = SpecVector()

        stat[CoreStat.ATTACK_PHYSICAL] = self.set_attack_power(level)
        stat[CoreStat.FINAL_DAMAGE_PERCENT] = self.set_final_damage(level)
        stat[CoreStat.CRITICAL_PERCENTAGE] = self.set_critical_rate(level)
        stat[CoreStat.CRITICAL_DAMAGE] = self.set_critical_damage(level)
        stat[CoreStat.IGNORE_GUARD_PERCENTAGE] = self.set_ignore_defense(level)
        
        PassiveSkill.__init__(self=self, advanced=SkillAdvance.Fourth, level=level, max=max)
        BuffAttribute.__init__(self=self, stat=stat)
        CombatOrdersAttribute.__init__(self)

    def set_attack_power(self, level:int):
        return level

    def set_final_damage(self, level:int):
        return level

    def set_critical_rate(self, level:int):
        return level

    def set_critical_damage(self, level:int):
        return level

    def set_ignore_defense(self, level:int):
        return level

    @property
    def Level(self):
        return self._level
    
    @Level.setter
    def Level(self, level:int):
        if not isinstance(level, int) or level < 0:
            raise ValueError("Level must be a non-negative integer")
        if level > self.MaxLevel:
            self._level = level
        self._level = level
        self._BuffStat[CoreStat.ATTACK_PHYSICAL] = self.set_attack_power(level)
        self._BuffStat[CoreStat.FINAL_DAMAGE_PERCENT] = self.set_final_damage(level)
        self._BuffStat[CoreStat.CRITICAL_PERCENTAGE] = self.set_critical_rate(level)
        self._BuffStat[CoreStat.CRITICAL_DAMAGE] = self.set_critical_damage(level)
        self._BuffStat[CoreStat.IGNORE_GUARD_PERCENTAGE] = self.set_ignore_defense(level)
        
class 수라(PassiveSkill, BuffAttribute):
    def __init__(self, level=10):
        max_level = 10
        stat = SpecVector()

        stat[CoreStat.ATTACK_PHYSICAL] = 50
        stat[CoreStat.CRITICAL_PERCENTAGE] = 10
        stat[CoreStat.CRITICAL_DAMAGE] = 20
        stat[CoreStat.DAMAGE_PERCENTAGE_BOSS] = 20
        stat[CoreStat.IGNORE_GUARD_PERCENTAGE] = 10

        PassiveSkill.__init__(self=self, advanced=SkillAdvance.Second, level=level, max=max_level)
        BuffAttribute.__init__(self=self, stat=stat)

class 득의(PassiveSkill):
    def __init__(self, level=19):
        PassiveSkill.__init__(
            self=self,
            advanced=SkillAdvance.Third,
            level=level,
            max=19
        )
    
    def DamagePoint_여의선(self):
        return 205
    def DamagePoint_토파류(self):
        return 100
    def DamagePoint_마봉_호로부(self):
        return 200
    def DamagePoint_환영_분신부(self):
        return 60
        
class 득도(PassiveSkill, BuffAttribute, CombatOrdersAttribute):
    def __init__(self, level=20):
        Buff = CreateSpecVector([CoreStat.DAMAGE_PERCENTAGE], math.floor(level/2))
        PassiveSkill.__init__(
            self=self,
            advanced=SkillAdvance.Fourth,
            level=level,
            max=20
        )
        BuffAttribute.__init__(
            self=self,
            stat=Buff
        )
        CombatOrdersAttribute.__init__(self)
    
    @property
    def Level(self):
        return super().Level
    
    @Level.setter
    def Level(self, level:int):
        if not isinstance(level, int) or level < 0:
            raise ValueError("Level must be a non-negative integer")
        if level > self.MaxLevel:
            self._level = level
        self._level = level

        self.BuffStat[CoreStat.DAMAGE_PERCENTAGE] = math.floor(level/2)


    def DamagePoint_여의선(self):
        return 207 + 5 * self.Level

    def DamagePoint_토파류(self):
        return 120 + 5 * self.Level

    def DamagePoint_파초풍(self):
        return 101 + 2 * self.Level

    def DamagePoint_지진쇄(self):
        return 145 + 5 * self.Level

    def DamagePoint_마봉_호로부(self):
        return 350 + 10 * self.Level

    def DamagePoint_환영_분신부(self):
        return 70 + 2 * self.Level

    def DamagePoint_추적_귀화부(self):
        return self.Level * 5 + 115

# 패시브 스킬-----------------------------

class HoyoungSkill(DamageAttribute):
    
    def __init__(self, damage_point: int, line: int, castingCount: int = 1):
        DamageAttribute.__init__(self, damage_point, line, castingCount)

    def ActiveOnHit(self):
        self.분신부_트리거()
        self.호접지몽_트리거()
        self.괴력난신_트리거()

        # 천지인환영
        if hasattr(self, 'Elemental'):
            if self.Elemental != 천지인_속성.허:
                if self.Owner.CooldownManager.isReady(선기_천지인_환영):
                    if not self.Owner.ProjectileManager.isRegistered(선기_천지인_환영):                
                        summon = 선기_천지인_환영()
                        summon.Owner = self.Owner
                        summon.Target = self.Target

                        available = [천지인_속성.천, 천지인_속성.지, 천지인_속성.인]
                        available.remove(self.Elemental)
                        random.shuffle(available)
                        if isinstance(self, 선기_파천황):
                            summon.Minimum = 0.2
                            summon.Maximum = 0.3
                        elif isinstance(self, 금고봉_인):
                            summon.Minimum = 0.34
                            summon.Maximum = 0.4

                        for attribute in available:
                            if not 부적.Status[attribute.value]:
                                summon.attribute = attribute
                        if summon.attribute in available:
                            self.Owner.ProjectileManager.Add(summon, isImmediate=False)
                            # 쿨타임 등록은 해당 클래스의 UseSkill 메소드에서 수행
            

        # 멸화염 불꽃의 문양
        if self.Owner.BuffManager.isRegistered(멸화염_문양_폭발) and hasattr(self, 'Elemental'):
            if self.Elemental in [천지인_속성.천, 천지인_속성.지, 천지인_속성.인]:
                멸화염_문양_폭발.count += 1
                if 멸화염_문양_폭발.count == 3:
                    summon = 멸화염_문양_폭발(level=멸화염_천().Level)
                    summon.Owner = self.Owner
                    summon.Target = self.Target
                    self.Owner.ProjectileManager.Add(summon, isImmediate=True)
                    멸화염_문양_폭발.count = 0
        
    def 괴력난신_트리거(self):
        # 괴력난신
        if self.Owner.BuffManager.isRegistered(선기_강림_괴력난신):
            선기_강림_괴력난신_신들의_일격.count += 1
            if self.Owner.CooldownManager.isReady(선기_강림_괴력난신_신들의_일격) and 선기_강림_괴력난신_신들의_일격.count >= 12:
                summon = 선기_강림_괴력난신_신들의_일격()
                summon.Owner = self.Owner
                summon.Target = self.Target
                self.Owner.ProjectileManager.Add(summon, isImmediate=True)
                self.Owner.CooldownManager.Count(선기_강림_괴력난신_신들의_일격)
                선기_강림_괴력난신_신들의_일격.count = 0
                
    def 호접지몽_트리거(self):
         # 호접지몽 on?
        if self.Owner.BuffManager.isRegistered(권술_호접지몽):
            if self.Owner.CooldownManager.isReady(권술_호접지몽_나비):
                
                for _ in range(0, 권술_호접지몽_나비().CastingCount):
                    summon = 권술_호접지몽_나비()
                    summon.Owner = self.Owner
                    summon.Target = self.Target
                    summon.ApplyCombat(isOriginal=False)
                    self.Owner.ProjectileManager.Add(summon, isImmediate=False)
                self.Owner.CooldownManager.Count(권술_호접지몽_나비)

    def 분신부_트리거(self):
        # 분신부가 활성화되어 있으면
        if self.Owner.BuffManager.isRegistered(환영_분신부):
            if self.Owner.CooldownManager.isReady(환영_분신부_분신):
                # 분신난무가 켜져있나?
                nanmuCount = 0
                if self.Owner.BuffManager.isRegistered(선기_극대_분신난무):
                    nanmuCount = 7
                # 분신 갯수만큼 공격함. 단, 사출기에
                
                for _ in range(0, 환영_분신부_분신().CastingCount + nanmuCount):
                    summon = 환영_분신부_분신()
                    summon.Owner = self.Owner
                    summon.Target = self.Target
                    self.Owner.ProjectileManager.Add(summon, isImmediate=False)
                self.Owner.CooldownManager.Count(환영_분신부_분신)



class 천지인_스킬(HoyoungSkill):
    def __init__(self, damage_point: int, line: int, elemental:천지인_속성, castingCount: int = 1):
        self.부적 = 부적
        if not isinstance(elemental, 천지인_속성):
            raise ValueError("천지인 스킬은 속성 지정이 필요함")
        self.Elemental = elemental

        HoyoungSkill.__init__(self, damage_point, line, castingCount)

    def GetCheonjiinBuff(self):
        """천지인 스킬 전용 버프를 얻어욤. 또한, 해당 스킬의 속성을 부적에서 사용표시로 전환함

        Returns:
            _type_: _description_
        """
        buff = SpecVector()

        if 천지인_리인포스 in self.Owner._PassiveSkillList:
            buff[CoreStat.DAMAGE_PERCENTAGE] += 10

        if 천지인_보스킬러 in self.Owner._PassiveSkillList:
            buff[CoreStat.DAMAGE_PERCENTAGE_BOSS] += 15

        if 선기_강림_괴력난신_버프 in self.Owner._PassiveSkillList:
            buff += 선기_강림_괴력난신_버프().elementalbuff

        now = self.부적.Now
        # 이전 속성과 다른 속성의 공격으로 연계할 경우 최종데미지 5%
        if now is not None and now != self.Elemental and self.Elemental is not 천지인_속성.허:
            buff[CoreStat.FINAL_DAMAGE_PERCENT] += 5
            # 다음 연계되는 허 스킬의 최종데미지 5% 증가
            self.부적.허 = True

        # 허스킬인 경우, 이전 스킬이 최종데미지 버프를 받았을 경우
        if self.Elemental == 천지인_속성.허 and self.부적.허:
            buff[CoreStat.FINAL_DAMAGE_PERCENT] += 5
            # 최종데미지 버프 받은 기록 초기화
            self.부적.허 = False
        
        if not (isinstance(self, 금고봉_인) and 금고봉_인.isFirst):
            self.부적.Now = self.Elemental

        # 천지만물
        if 천지만물 in self.Owner._PassiveSkillList:
            if self.Owner.CooldownManager.isReady(천지만물):
                if 부적.successStack >= 3:
                    self.Owner.BuffManager.Add(천지만물())
                    self.Owner.CooldownManager.Count(천지만물)
                    천지만물.ReinforceSkill = True
                    부적.successStack = 0

        # 공격 시 자동 발동 타격들 실행
        self.ActiveOnHit()

        
        return buff
       
    
class 천지인_리인포스(PassiveSkill):
    def __init__(self, level=1):
        PassiveSkill.__init__(
            self=self,
            advanced=SkillAdvance.Hyper,
            level=level,
            max=1
        )

class 천지인_보스킬러(PassiveSkill):
    def __init__(self, level=1):
        PassiveSkill.__init__(
            self=self,
            advanced=SkillAdvance.Hyper,
            level=level,
            max=1
        )

class 추적귀화부_헤이스트(PassiveSkill):
    def __init__(self, level=1):
        PassiveSkill.__init__(
            self=self,
            advanced=SkillAdvance.Hyper,
            level=level,
            max=1
        )

class 환영분신부_이그노어가드(PassiveSkill):
    def __init__(self, level=1):
        PassiveSkill.__init__(
            self=self,
            advanced=SkillAdvance.Hyper,
            level=level,
            max=1
        )

class 권술_흡성와류_헤이스트(PassiveSkill):
    def __init__(self, level=1):
        PassiveSkill.__init__(
            self=self,
            advanced=SkillAdvance.Hyper,
            level=level,
            max=1
        )

# 액티브 스킬 -------------------------

class 여의선_인(OnPressSkill, 천지인_스킬, SkillDelayAttribute, BuffAttribute):
    def __init__(self, level=20):
        MasterLevel = 20
        YeoiseonInIcon = None

        yeoiseonInDamage = 0
        yeoiseonInAttackLine = 5
        yeoiseonInAttackCount = 1
        inSymbol = 천지인_속성.인
        yeoiseonSkillDelay = Cooldown(milliseconds=690) 
        yeoBuff = CreateSpecVector([CoreStat.FINAL_DAMAGE_PERCENT], 5)
        OnPressSkill.__init__(
            self=self,
            icon=YeoiseonInIcon,
            advanced=SkillAdvance.Fourth,
            level=level,
            max=MasterLevel
        )
        천지인_스킬.__init__(
            self=self,
            damage_point=yeoiseonInDamage,
            line=yeoiseonInAttackLine,
            elemental=inSymbol,
            castingCount=yeoiseonInAttackCount
        )
        SkillDelayAttribute.__init__(
            self=self,
            casting_delay=yeoiseonSkillDelay,
            applyAttackSpeed=True,
            special=False
        )
        BuffAttribute.__init__(
            self=self,
            stat=yeoBuff
        )

    def GetSkillDamage(self):
        point = 90

        if 득의 in self.Owner._PassiveSkillList:
            reinforce = 득의()
            point += reinforce.DamagePoint_여의선()
            
        if 득도 in self.Owner._PassiveSkillList:
            reinforce = 득도()
            reinforce.ApplyCombat(False)
            if self._Owner._IsPassiveLevel:
                reinforce.ApplyPassiveLevel1()
            point += reinforce.DamagePoint_여의선()
        return point
        
    def GetSkillAttackLine(self):
        return 5

    def UseSkill(self):
        # 천지인 스킬의 효과
        # 렐릭 게이지 참조
        # 공격
        # 사출기 매니저에 등록
        # 리턴: 스킬 로그
        
        
        addbuff = self.GetCheonjiinBuff()
        self.DamagePoint = self.GetSkillDamage()
        self.AttackLine = self.GetSkillAttackLine()

        
        if 여의선_인_강화_5th in self.Owner._PassiveSkillList:
            addbuff += 여의선_인_강화_5th().CheonjiinCoreReinforce
        
        
        seonLog = self.Target.TakeAttack(char=self.Owner, skill=self, add = addbuff + self.BuffStat)
    
        return [seonLog]

class 여의선_인_강화_5th(PassiveSkill):

    def __init__(self, level=60):
        self.CheonjiinCoreReinforce = CreateSpecVector([CoreStat.FINAL_DAMAGE_PERCENT], level*2)
        self.CheonjiinCoreReinforce[CoreStat.IGNORE_GUARD_PERCENTAGE] = 20
        PassiveSkill.__init__(
            self=self,
            advanced=SkillAdvance.Fifth,
            level=level,
            max= 60
        )

class 토파류_지(OnPressSkill, 천지인_스킬, SkillDelayAttribute):
    def __init__(self, level=20):
        MasterLevel = 20
        ToparyuJiIcon = None

        toparyuJiDamage = 0
        toparyuJiAttackLine = 4
        toparyuJiAttackCount = 6
        jiSymbol = 천지인_속성.지
        toparyuSkillDelay = Cooldown(milliseconds=570)
        
        OnPressSkill.__init__(
            self=self,
            icon=ToparyuJiIcon,
            advanced=SkillAdvance.Fourth,
            level=level,
            max=MasterLevel
        )
        천지인_스킬.__init__(
            self=self,
            damage_point=toparyuJiDamage,
            line=toparyuJiAttackLine,
            elemental=jiSymbol,
            castingCount=toparyuJiAttackCount
        )
        SkillDelayAttribute.__init__(
            self=self,
            casting_delay=toparyuSkillDelay,
            applyAttackSpeed=False,
            special=True
        )

    def GetSkillDamage(self):
        point = 100

        if 득의 in self.Owner._PassiveSkillList:
            reinforce = 득의()
            point += reinforce.DamagePoint_토파류()
            
        if 득도 in self.Owner._PassiveSkillList:
            reinforce = 득도()
            reinforce.ApplyCombat(False)
            if self._Owner._IsPassiveLevel:
                reinforce.ApplyPassiveLevel1()
            point += reinforce.DamagePoint_토파류()
        return point
        
    def GetSkillAttackLine(self):
        return 4

    def UseSkill(self):
        addbuff = self.GetCheonjiinBuff()
        self.DamagePoint = self.GetSkillDamage()
        self.AttackLine = self.GetSkillAttackLine()
        
        if 토파류_강화_5th in self.Owner._PassiveSkillList:
            addbuff += 토파류_강화_5th().reinforce_ratio

        ryuLog = self.Target.TakeAttack(char=self.Owner, skill=self, add =addbuff)

        summon = 토파류_허실()
        summon.Owner = self.Owner
        summon.Target = self.Target
        self.Owner.ProjectileManager.Add(summon, ForcedDelay=self.AttackDelay - summon.AttackDelay)

        return [ryuLog]
    
class 토파류_허실(OnPressSkill, 천지인_스킬, SkillDelayAttribute):
    def __init__(self, level=20):
        MasterLevel = 20
        ToparyuJiIcon = None

        toparyuJiDamage = 0
        toparyuJiAttackLine = 4
        toparyuJiAttackCount = 6
        jiSymbol = 천지인_속성.허
        toparyuSkillDelay = Cooldown(milliseconds=30)
        
        OnPressSkill.__init__(
            self=self,
            icon=ToparyuJiIcon,
            advanced=SkillAdvance.Fourth,
            level=level,
            max=MasterLevel
        )
        천지인_스킬.__init__(
            self=self,
            damage_point=toparyuJiDamage,
            line=toparyuJiAttackLine,
            elemental=jiSymbol,
            castingCount=toparyuJiAttackCount
        )
        SkillDelayAttribute.__init__(
            self=self,
            casting_delay=toparyuSkillDelay,
            applyAttackSpeed=False,
            special=True
        )

    def GetSkillDamage(self):
        point = 100

        if 득의 in self.Owner._PassiveSkillList:
            reinforce = 득의()
            point += reinforce.DamagePoint_토파류()
            
        if 득도 in self.Owner._PassiveSkillList:
            reinforce = 득도()
            reinforce.ApplyCombat(False)
            if self._Owner._IsPassiveLevel:
                reinforce.ApplyPassiveLevel1()
            point += reinforce.DamagePoint_토파류()
        return point
        
    def GetSkillAttackLine(self):
        return 4

    def UseSkill(self):
        addbuff = self.GetCheonjiinBuff()
        self.DamagePoint = self.GetSkillDamage()
        self.AttackLine = self.GetSkillAttackLine()
        if 토파류_강화_5th in self.Owner._PassiveSkillList:
            addbuff += 토파류_강화_5th().reinforce_ratio

        ryuLog = self.Target.TakeAttack(char=self.Owner, skill=self, add =addbuff)

        # 토파류: 허 소환
        return [ryuLog]

class 토파류_강화_5th(PassiveSkill):
    def __init__(self, level=60):
        super().__init__(SkillAdvance.Fifth, level, level)
        self.reinforce_ratio = CreateSpecVector([CoreStat.FINAL_DAMAGE_PERCENT], level*2)
        self.reinforce_ratio[CoreStat.IGNORE_GUARD_PERCENTAGE] = 20

class 지진쇄_지(OnPressSkill, 천지인_스킬, SkillDelayAttribute, CooldownAttribute):
    def __init__(self, level=20):
        MasterLevel = 20
        JijinJiIcon = None

        jijinJiDamage = 0
        jijinJiAttackLine = 6
        jijinJiAttackCount = 1
        jiSymbol = 천지인_속성.지
        jijinSkillDelay = Cooldown(milliseconds=540)
        jijinSkillCooldown = Cooldown(seconds=6)
        OnPressSkill.__init__(
            self=self,
            icon=JijinJiIcon,
            advanced=SkillAdvance.Fourth,
            level=level,
            max=MasterLevel
        )
        천지인_스킬.__init__(
            self=self,
            damage_point=jijinJiDamage,
            line=jijinJiAttackLine,
            elemental=jiSymbol
        )
        SkillDelayAttribute.__init__(
            self=self,
            casting_delay=jijinSkillDelay,
            applyAttackSpeed=False,
            special=True
        )
        CooldownAttribute.__init__(
            self=self,
            cooldown=jijinSkillCooldown,
            isresetable=True
        )

    def GetSkillDamage(self):
        point = 180

            
        if 득도 in self.Owner._PassiveSkillList:
            reinforce = 득도()
            reinforce.ApplyCombat(False)
            # TODO: 패시브 레벨1
            if self._Owner._IsPassiveLevel:
                reinforce.ApplyPassiveLevel1()
            point += reinforce.DamagePoint_지진쇄()

        if 지진쇄_강화_6th in self.Owner._PassiveSkillList:
            if 천지만물.ReinforceSkill:
                point = 740 + 9 * 30
            else:
                point = 지진쇄_강화_6th().jijinDamage        
        return point
    
    
        
    def GetSkillAttackLine(self):
        return 6

    def UseSkill(self):
        addlog = []
        addbuff = self.GetCheonjiinBuff()
        self.DamagePoint = self.GetSkillDamage()
        self.AttackLine = self.GetSkillAttackLine()
        if 지진쇄_강화_5th in self.Owner._PassiveSkillList:
            addbuff += 지진쇄_강화_5th().reinforce_ratio

        jijinLog = self.Target.TakeAttack(char=self.Owner, skill=self, add=addbuff)

        if 천지만물.ReinforceSkill:
            addhit = 지진쇄_고고한_청월(level=self.Level)
            addlog = addhit.UseSkill(buff = addbuff)
            천지만물.ReinforceSkill = False

        summon = 지진쇄_허실()
        summon.Owner = self.Owner
        summon.Target = self.Target
        self.Owner.ProjectileManager.Add(summon, ForcedDelay=self.AttackDelay - summon.AttackDelay)

        return [jijinLog] + addlog

class 지진쇄_허실(OnPressSkill, 천지인_스킬, SkillDelayAttribute):
    def __init__(self, level=20):
        MasterLevel = 20
        JijinHeoIcon = None

        jijinHeoDamage = 0
        jijinHeoAttackLine = 6
        jijinHeoAttackCount = 1
        heoSymbol = 천지인_속성.허
        jijinSkillDelay = Cooldown(milliseconds=30)
        

        OnPressSkill.__init__(
            self=self,
            icon=JijinHeoIcon,
            advanced=SkillAdvance.Fourth,
            level=level,
            max=MasterLevel
        )
        천지인_스킬.__init__(
            self=self,
            damage_point=jijinHeoDamage,
            line=jijinHeoAttackLine,
            elemental=heoSymbol
        )
        SkillDelayAttribute.__init__(
            self=self,
            casting_delay=jijinSkillDelay,
            applyAttackSpeed=False,
            special=True
        )
        

    def GetSkillDamage(self):
        point = 180

        if 득도 in self.Owner._PassiveSkillList:
            reinforce = 득도()
            reinforce.ApplyCombat(False)
            # TODO: 패시브 레벨1
            if self._Owner._IsPassiveLevel:
                reinforce.ApplyPassiveLevel1()
            point += reinforce.DamagePoint_지진쇄()

        if 지진쇄_강화_6th in self.Owner._PassiveSkillList:
            if 천지만물.ReinforceSkill:
                point = 810 + 10*30
            else:
                point = 지진쇄_강화_6th().jijinDamage
        return point

    def GetSkillAttackLine(self):
        return 6

    def UseSkill(self):
        addbuff = self.GetCheonjiinBuff()
        self.DamagePoint = self.GetSkillDamage()
        self.AttackLine = self.GetSkillAttackLine()

        if 지진쇄_강화_5th in self.Owner._PassiveSkillList:
            addbuff += 지진쇄_강화_5th().reinforce_ratio

        jijinLog = self.Target.TakeAttack(char=self.Owner, skill=self, add=addbuff)
        return [jijinLog]

class 지진쇄_강화_5th(PassiveSkill):
    def __init__(self, level=60):
        super().__init__(SkillAdvance.Fifth, level, level)
        self.reinforce_ratio = CreateSpecVector([CoreStat.FINAL_DAMAGE_PERCENT], level*2)
        self.reinforce_ratio[CoreStat.IGNORE_GUARD_PERCENTAGE] = 20

class 지진쇄_강화_6th(PassiveSkill):
    def __init__(self, level=30):
        self.jijinDamage = 650
        super().__init__(SkillAdvance.Sixth, level, 30)

class 지진쇄_고고한_청월(OnPressSkill, 천지인_스킬, SummonAttribute):
    def __init__(self, level):
        OnPressSkill.__init__(
            self=self,
            icon=Any,
            advanced=SkillAdvance.Sixth,
            level=level,
            max=30
        )
        천지인_스킬.__init__(
            self=self,
            damage_point= self.GetDamagePoint(level),
            line=5,
            elemental=천지인_속성.지
        )
        SummonAttribute.__init__(
            self=self,
            duration=Cooldown(seconds=5),
            interval=Cooldown(milliseconds=900),
            mult=False
        )

    def GetDamagePoint(self, level):
        return 520+7*level
    
    def UseSkill(self, buff=SpecVector()):
        return [self.Target.TakeAttack(char=self.Owner, skill=self, add=buff)]

class 파초풍_천(OnPressSkill, 천지인_스킬, SkillDelayAttribute):
    def __init__(self, level=20):
        MasterLevel = 20
        PachoCheonIcon = None

        pachoCheonDamage = 0
        pachoCheonAttackLine = 5
        
        cheonSymbol = 천지인_속성.천
        pachoSkillDelay = Cooldown(milliseconds=660)
        

        OnPressSkill.__init__(
            self=self,
            icon=PachoCheonIcon,
            advanced=SkillAdvance.Fourth,
            level=level,
            max=MasterLevel
        )
        천지인_스킬.__init__(
            self=self,
            damage_point=pachoCheonDamage,
            line=pachoCheonAttackLine,
            elemental=cheonSymbol
        )
        SkillDelayAttribute.__init__(
            self=self,
            casting_delay=pachoSkillDelay,
            applyAttackSpeed=False,
            special=True
        )

    def GetSkillDamage(self):
        point = 150

        if 득도 in self.Owner._PassiveSkillList:
            reinforce = 득도()
            reinforce.ApplyCombat(False)
            # TODO: 패시브 레벨1
            if self._Owner._IsPassiveLevel:
                reinforce.ApplyPassiveLevel1()
            point += reinforce.DamagePoint_파초풍()
        return point

    def GetSkillAttackLine(self):
        return 5

    def UseSkill(self):
        self.Owner._Jump = Cooldown(seconds=1)

        addbuff = self.GetCheonjiinBuff()
        self.DamagePoint = self.GetSkillDamage()
        self.AttackLine = self.GetSkillAttackLine()
        if 파초풍_강화_5th in self.Owner._PassiveSkillList:
            addbuff += 파초풍_강화_5th().reinforce_ratio

        summon = 파초풍_허실()
        summon.Owner = self.Owner
        summon.Target = self.Target
        self.Owner.ProjectileManager.Add(summon, ForcedDelay=self.AttackDelay - summon.AttackDelay)

        pachoLog = self.Target.TakeAttack(char=self.Owner, skill=self, add=addbuff)
        return [pachoLog]

class 파초풍_허실(OnPressSkill, 천지인_스킬, SkillDelayAttribute):
    def __init__(self, level=20):
        MasterLevel = 20
        PachoHeoSilIcon = None

        pachoHeoSilDamage = 0
        pachoHeoSilAttackLine = 5
        
        heoSilSymbol = 천지인_속성.허
        pachoSkillDelay = Cooldown(milliseconds=30)

        OnPressSkill.__init__(
            self=self,
            icon=PachoHeoSilIcon,
            advanced=SkillAdvance.Fourth,
            level=level,
            max=MasterLevel
        )
        천지인_스킬.__init__(
            self=self,
            damage_point=pachoHeoSilDamage,
            line=pachoHeoSilAttackLine,
            elemental=heoSilSymbol
        )
        SkillDelayAttribute.__init__(
            self=self,
            casting_delay=pachoSkillDelay,
            applyAttackSpeed=False,
            special=True
        )

    def GetSkillDamage(self):
        point = 150

        if 득도 in self.Owner._PassiveSkillList:
            reinforce = 득도()
            reinforce.ApplyCombat(False)
            # TODO: 패시브 레벨1
            if self._Owner._IsPassiveLevel:
                reinforce.ApplyPassiveLevel1()
            point += reinforce.DamagePoint_파초풍()
        return point

    def GetSkillAttackLine(self):
        return 5

    def UseSkill(self):
        addbuff = self.GetCheonjiinBuff()
        self.DamagePoint = self.GetSkillDamage()
        self.AttackLine = self.GetSkillAttackLine()
        if 파초풍_강화_5th in self.Owner._PassiveSkillList:
            addbuff += 파초풍_강화_5th().reinforce_ratio


        pachoLog = self.Target.TakeAttack(char=self.Owner, skill=self, add=addbuff)
        return [pachoLog]

class 파초풍_강화_5th(PassiveSkill):
    def __init__(self, level=60):
        super().__init__(SkillAdvance.Fifth, level, level)
        self.reinforce_ratio = CreateSpecVector([CoreStat.FINAL_DAMAGE_PERCENT], level*2)
        self.reinforce_ratio[CoreStat.IGNORE_GUARD_PERCENTAGE] = 20

class 멸화염_천(OnPressSkill, 천지인_스킬, SkillDelayAttribute, CooldownAttribute, CombatOrdersAttribute):
    def __init__(self, level=30):
        MasterLevel = 30
        MyeolhwaIcon = None

        myeolhwaDamage = 0
        myeolhwaAttackLine = 6
        
        cheonSymbol = 천지인_속성.천
        myeolhwaSkillDelay = Cooldown(milliseconds=450)
        myeolhwaSkillCooldown = Cooldown(seconds=8)
        OnPressSkill.__init__(
            self=self,
            icon=MyeolhwaIcon,
            advanced=SkillAdvance.Fourth,
            level=level,
            max=MasterLevel
        )
        천지인_스킬.__init__(
            self=self,
            damage_point=myeolhwaDamage,
            line=myeolhwaAttackLine,
            elemental=cheonSymbol
        )
        SkillDelayAttribute.__init__(
            self=self,
            casting_delay=myeolhwaSkillDelay,
            applyAttackSpeed=False,
            special=True
        )
        CooldownAttribute.__init__(
            self=self,
            cooldown=myeolhwaSkillCooldown,
            isresetable=False
        )
        CombatOrdersAttribute.__init__(self)

    def GetSkillDamage(self, level):
        if 천지만물.ReinforceSkill:
            return 600+7*30
        else:
            return 310 + 2 * level

    @property
    def Level(self):
        return super().Level
    
    @Level.setter
    def Level(self, level:int):
        if not isinstance(level, int) or level < 0:
            raise ValueError("Level must be a non-negative integer")
        if level > self.MaxLevel:
            self._level = level
        self._level = level

        self.DamagePoint = self.GetSkillDamage(level)

    def GetSkillAttackLine(self):
        return 6

    def UseSkill(self):
        if not self.Owner._Jump > TIME_ZERO:
            raise AttributeError("공중에 뜨지 않으면 사용 불가함")
        addbuff = self.GetCheonjiinBuff()
        
        if 멸화염_강화_5th in self.Owner._PassiveSkillList:
            addbuff += 멸화염_강화_5th().reinforce_ratio

        if 멸화염_강화_6th in self.Owner._PassiveSkillList:
            self.DamagePoint = 멸화염_강화_6th().myulDamage
            if 천지만물 in self.Owner._PassiveSkillList and 천지만물.ReinforceSkill:
                self.DamagePoint = self.GetSkillDamage(level=30)

                
        myeolhwaLog = self.Target.TakeAttack(char=self.Owner, skill=self, add=addbuff)

        summon = 멸화염_허실()
        summon.Owner = self.Owner
        summon.Target = self.Target
        self.Owner.ProjectileManager.Add(summon, ForcedDelay=self.AttackDelay - summon.AttackDelay)

        return [myeolhwaLog]

class 멸화염_허실(OnPressSkill, 천지인_스킬, SkillDelayAttribute, CombatOrdersAttribute):
    def __init__(self, level=30):
        MasterLevel = 30
        MyeolhwaHeoIcon = None

        myeolhwaHeoDamage = 0
        myeolhwaHeoAttackLine = 6
        heoSymbol = 천지인_속성.허
        myeolhwaHeoSkillDelay = Cooldown(milliseconds=30)

        OnPressSkill.__init__(
            self=self,
            icon=MyeolhwaHeoIcon,
            advanced=SkillAdvance.Fourth,
            level=level,
            max=MasterLevel
        )
        천지인_스킬.__init__(
            self=self,
            damage_point=myeolhwaHeoDamage,
            line=myeolhwaHeoAttackLine,
            elemental=heoSymbol
        )
        SkillDelayAttribute.__init__(
            self=self,
            casting_delay=myeolhwaHeoSkillDelay,
            applyAttackSpeed=False,
            special=True
        )
        CombatOrdersAttribute.__init__(self)

    def GetSkillDamage(self, level):
        if 천지만물.ReinforceSkill:
            return 600+7*30
        else:
            return 310 + 2 * level

    @property
    def Level(self):
        return super().Level
    
    @Level.setter
    def Level(self, level:int):
        if not isinstance(level, int) or level < 0:
            raise ValueError("Level must be a non-negative integer")
        if level > self.MaxLevel:
            self._level = level
        self._level = level

        self.DamagePoint = self.GetSkillDamage(level)

    def GetSkillAttackLine(self):
        return 6

    def UseSkill(self):
        addbuff = self.GetCheonjiinBuff()

        if 멸화염_강화_5th in self.Owner._PassiveSkillList:
            addbuff += 멸화염_강화_5th().reinforce_ratio
        
        if 멸화염_강화_6th in self.Owner._PassiveSkillList:
            self.DamagePoint = 멸화염_강화_6th().myulDamage
            if 천지만물 in self.Owner._PassiveSkillList and 천지만물.ReinforceSkill:
                self.DamagePoint = self.GetSkillDamage(level=30)

                self.Owner.BuffManager.Add(멸화염_문양_폭발(level=self.Level))
                천지만물.ReinforceSkill = False
        myeolhwaHeoLog = self.Target.TakeAttack(char=self.Owner, skill=self, add=addbuff)
        return [myeolhwaHeoLog]

class 멸화염_강화_5th(PassiveSkill):
    def __init__(self, level=60):
        super().__init__(SkillAdvance.Fifth, level, level)
        self.reinforce_ratio = CreateSpecVector([CoreStat.FINAL_DAMAGE_PERCENT], level*2)
        self.reinforce_ratio[CoreStat.IGNORE_GUARD_PERCENTAGE] = 20

class 멸화염_강화_6th(PassiveSkill):
    def __init__(self, level=30):
        self.myulDamage = 555
        super().__init__(SkillAdvance.Sixth, level, 30)

class 멸화염_문양_폭발(OnPressSkill, 천지인_스킬, BuffAttribute, DurationAttribute):
    count = 0
    def __init__(self, level: int):
        OnPressSkill.__init__(
            self=self,
            icon=Any,
            advanced=SkillAdvance.Sixth,
            level=level,
            max=30
        )
        천지인_스킬.__init__(
            self=self,
            damage_point=self.GetDamagePoint(level),
            line=5,
            elemental=천지인_속성.천
        )
        BuffAttribute.__init__(
            self=self,
            stat=SpecVector()
        )
        DurationAttribute.__init__(
            self=self,
            duration=Cooldown(seconds=15),
            serverlack=False,
            isbuffmult=False
        )

    def GetDamagePoint(self, level):
        return 505 + level*6

    def UseSkill(self, addbuff=SpecVector()):
        return [self.Target.TakeAttack(char=self.Owner, skill=self, add=addbuff)]
    
class 금고봉_인(OnPressSkill, 천지인_스킬, SkillDelayAttribute, CooldownAttribute, CombatOrdersAttribute, BuffAttribute):
    isFirst = True
    secondBuff = SpecVector()
    def __init__(self, level=30):
        MasterLevel = 30
        GeumgobongIcon = None

        geumgobongDamage1 = 282
        
        geumgobongAttackLine1 = 10
        
        inSymbol = 천지인_속성.인
        addBuff = SpecVector()
        addBuff[CoreStat.DAMAGE_PERCENTAGE_BOSS] = 30

        geumgobongSkillDelay = Cooldown(milliseconds=690)
        geumgobongSkillCooldown = Cooldown(seconds=11)
        OnPressSkill.__init__(
            self=self,
            icon=GeumgobongIcon,
            advanced=SkillAdvance.Fourth,
            level=level,
            max=MasterLevel
        )
        천지인_스킬.__init__(
            self=self,
            damage_point=geumgobongDamage1,
            line=geumgobongAttackLine1,
            elemental=inSymbol
        )
        SkillDelayAttribute.__init__(
            self=self,
            casting_delay=geumgobongSkillDelay,
            applyAttackSpeed=False,
            special=True
        )
        CooldownAttribute.__init__(
            self=self,
            cooldown=geumgobongSkillCooldown,
            isresetable=True
        )
        CombatOrdersAttribute.__init__(self)
        BuffAttribute.__init__(
            self=self,
            stat=addBuff
        )

    def GetSkillDamage1(self, level):
        point = 192 + 3 * level
        if 금고봉_강화_6th in self.Owner._PassiveSkillList:
            point = 455
        
        if 천지만물.ReinforceSkill:
            point = 725
        return point
    def GetSkillDamage2(self, level):
        point = 398 + 2 * level
        if 금고봉_강화_6th in self.Owner._PassiveSkillList:
            point = 830
        if 천지만물.ReinforceSkill:
            point = 1320
        return point
        
    def GetSkillAttackLine1(self):
        return 10
    
    def GetSkillAttackLine2(self):
        return 8

    @property
    def Level(self):
        return super().Level

    @Level.setter
    def Level(self, level:int):
        if not isinstance(level, int) or level < 0:
            raise ValueError("Level must be a non-negative integer")
        if level > self.MaxLevel:
            self._level = level
        self._level = level

    

    def GetSkillAttackLine(self):
        return self.Line

    def UseSkill(self):
        addlog = []
        addbuff = self.GetCheonjiinBuff()
        if 금고봉_강화_5th in self.Owner._PassiveSkillList:
            addbuff += 금고봉_강화_5th().reinforce_ratio
        if 금고봉_인.isFirst:
            
            self.DamagePoint = self.GetSkillDamage1(self.Level)
            
            금고봉_인.isFirst = False
            self.AttackLine = self.GetSkillAttackLine1()
            self.Owner.ProjectileManager.Add(self, isImmediate=True, ForcedDelay = Cooldown(milliseconds=360))
        else:
            self.DamagePoint = self.GetSkillDamage2(self.Level)
            금고봉_인.isFirst = True
            self.AttackLine = self.GetSkillAttackLine2()

            if 천지만물.ReinforceSkill:
                addhit = 금고봉_도깨비의_기운(level=self.Level)
                addhit.Owner = self.Owner
                addhit.Target = self.Target
                # 도깨비 기운도 금고봉이 받는 데미지 버프 그대로 받음
                addlog = addhit.UseSkill(buff = self.BuffStat + addbuff)

                천지만물.ReinforceSkill = False

        geumgobongLog = self.Target.TakeAttack(char=self.Owner, skill=self, add=addbuff + self.BuffStat)
        
        return [geumgobongLog] + addlog

class 금고봉_강화_5th(PassiveSkill):
    def __init__(self, level=60):
        super().__init__(SkillAdvance.Fifth, level, level)
        self.reinforce_ratio = CreateSpecVector([CoreStat.FINAL_DAMAGE_PERCENT], level*2)
        self.reinforce_ratio[CoreStat.IGNORE_GUARD_PERCENTAGE] = 20

class 금고봉_강화_6th(PassiveSkill):
    def __init__(self, level=30):
        super().__init__(SkillAdvance.Sixth, level, 30)

class 금고봉_도깨비의_기운(OnPressSkill, 천지인_스킬):
    def __init__(self, level: int):
        max = 30

        OnPressSkill.__init__(
            self=self,
            icon=Any,
            advanced= SkillAdvance.Sixth,
            level=level,
            max = max
        )
        천지인_스킬.__init__(
            self=self,
            damage_point= self.GetDamagePoint(level),
            line=8,
            elemental=천지인_속성.인
        )

    def GetDamagePoint(self, level):
        return level*11 + 495

    def UseSkill(self, buff:SpecVector):
        return [self.Target.TakeAttack(char=self.Owner, skill=self, add=buff)]
# 부적 스킬 ------------------------------

class 부적_스킬(HoyoungSkill):
    def __init__(self, damage_point: int, line: int, castingCount: int = 1):
        self.부적 = 부적 
        self.두루마리 = 두루마리
        HoyoungSkill.__init__(self, damage_point, line, castingCount)

    def UseAmulet(self):
        self.두루마리.ScrollGuage += 200

class 추적_귀화부(OnPressSkill, 부적_스킬, SummonAttribute, SkillDelayAttribute):
    isFirst = True
    def __init__(self, level = 20):
        chasingIcon = None
        chasingDuration = Cooldown(seconds=40)
        self.chasingInterval = Cooldown(milliseconds=1800)
        chasingDelay = Cooldown(milliseconds=630)
        chasingDamage = 0
        chasingAttackLine = 5

        OnPressSkill.__init__(
            self=self,
            icon=chasingIcon,
            advanced=SkillAdvance.Third,
            level=level,
            max=20
        )
        부적_스킬.__init__(
            self=self,
            damage_point=chasingDamage,
            line=chasingAttackLine
        )
        SummonAttribute.__init__(
            self=self,
            duration=chasingDuration,
            interval=self.chasingInterval,
            mult=True
        )
        SkillDelayAttribute.__init__(
            self=self,
            casting_delay=chasingDelay,
            applyAttackSpeed=False
        )

        if 추적_귀화부.isFirst and 부적.AmuletGuage >=100:
            부적.AmuletGuage -= 100
            추적_귀화부.isFirst = False
        elif 부적.AmuletGuage < 100:
            raise ValueError("스킬 사용에 필요한 부적도력이 부족함")
        


    def GetSkillDamage(self,level):
        point = 210
        if 득도 in self.Owner._PassiveSkillList:
            reinforce = 득도()
            if 쓸만한_컴뱃오더스 in self.Owner._PassiveSkillList:
                reinforce.ApplyCombat(False)
            if self._Owner._IsPassiveLevel:
                reinforce.ApplyPassiveLevel1()
            point += reinforce.DamagePoint_추적_귀화부()
        return point
    
    def UseSkill(self):
        self.UseAmulet()
        if 추적귀화부_헤이스트 in self.Owner._PassiveSkillList:
            self.Interval = self.chasingInterval * 0.75
        
        self.DamagePoint = self.GetSkillDamage(self.Level)

        add = SpecVector()
        if 추적_귀화부_강화_5th in self.Owner._PassiveSkillList:
            add = 추적_귀화부_강화_5th().reinforce_ratio

        amuletLog = self.Target.TakeAttack(char=self.Owner, skill=self, add = add)
        추적_귀화부.isFirst = True
        return [amuletLog]

class 추적_귀화부_강화_5th(PassiveSkill):
    
    def __init__(self, level=60):
        super().__init__(SkillAdvance.Fifth, level, level)
        self.reinforce_ratio = CreateSpecVector([CoreStat.FINAL_DAMAGE_PERCENT], level*2)
        self.reinforce_ratio[CoreStat.IGNORE_GUARD_PERCENTAGE] = 20

class 환영_분신부(OnPressSkill, BuffAttribute, DurationAttribute, SkillDelayAttribute):
    isFirst = True
    def __init__(self, level=20):
        illusionDuration = Cooldown(seconds=200)
        illusionIcon = None
        
        illusionCastingDelay = Cooldown(milliseconds=900)
        OnPressSkill.__init__(
            self=self,
            icon=illusionIcon,
            advanced=SkillAdvance.Fourth,
            level=level,
            max=20
        )
        DurationAttribute.__init__(
            self=self,
            duration=illusionDuration,
            serverlack=True,
            isbuffmult=True
        )
        BuffAttribute.__init__(
            self=self,
            stat=SpecVector()
        )
        SkillDelayAttribute.__init__(
            self=self,
            casting_delay=illusionCastingDelay,
            applyAttackSpeed=True
        )
        if 환영_분신부.isFirst and 부적.AmuletGuage >= 100:
            부적.AmuletGuage -= 100
            두루마리.ScrollGuage += 200
            환영_분신부.isFirst = False
        elif 부적.AmuletGuage < 100:
            raise ValueError("스킬 사용에 필요한 부적도력이 부족함")
        

    def UseSkill(self):
        
        return []
        
class 환영_분신부_분신(AutomateActivativeSkill, 부적_스킬, ProjectileAttribute, CooldownAttribute):
    def __init__(self, level = 20):
        illusionIcon = None
        illusionDamage = 0
        illusionAttakLine = 4
        illusionCount =3
        self.Maximum = 0.1
        illusionCooldown = Cooldown(milliseconds=1500)
        
        AutomateActivativeSkill.__init__(
            self=self,
            advanced=SkillAdvance.Fourth,
            level=level,
            max=20
        )
        부적_스킬.__init__(
            self=self,
            damage_point=illusionDamage,
            line=illusionAttakLine,
            castingCount=illusionCount
        )
        ProjectileAttribute.__init__(
            self=self,
            maximumTime= 0.5
        )
        CooldownAttribute.__init__(
            self=self,
            cooldown=illusionCooldown,
            isresetable=True
        )

    def GetSkillDamage(self):
        point = 60
        if 득의 in self.Owner._PassiveSkillList:
            point += 득의().DamagePoint_환영_분신부()

        if 득도 in self.Owner._PassiveSkillList:
            reinforce = 득도()
            if 쓸만한_컴뱃오더스 in self.Owner._PassiveSkillList:
                reinforce.ApplyCombat(False)
            if self._Owner._IsPassiveLevel:
                reinforce.ApplyPassiveLevel1()
            point += reinforce.DamagePoint_환영_분신부()

        if self.Owner.BuffManager.isRegistered(선기_극대_분신난무):
            if 선기_극대_분신난무_강화_6th in self.Owner._PassiveSkillList:
                point += 선기_극대_분신난무_강화_6th().AddDamagePoint
            else:
                point += 선기_극대_분신난무().Damage
        return point

    def UseSkill(self):
        self.괴력난신_트리거()
        환영_분신부.isFirst = True
        addBuff = SpecVector()


        self.DamagePoint = self.GetSkillDamage()

        if 환영분신부_이그노어가드 in self.Owner._PassiveSkillList:
            addBuff[CoreStat.IGNORE_GUARD_PERCENTAGE] = 20

        if 환영_분신부_강화_5th in self.Owner._PassiveSkillList:
            addBuff += 환영_분신부_강화_5th().reinforce_ratio

        return [self.Target.TakeAttack(char=self.Owner, skill=self, add = addBuff)]
    
    def active(self):
        return super().active()

class 환영_분신부_강화_5th(PassiveSkill):
    def __init__(self, level=60):
        super().__init__(SkillAdvance.Fifth, level, level)
        self.reinforce_ratio = CreateSpecVector([CoreStat.FINAL_DAMAGE_PERCENT], level*2)
        self.reinforce_ratio[CoreStat.IGNORE_GUARD_PERCENTAGE] = 20

class 마봉_호로부(OnPressSkill, 부적_스킬, SkillDelayAttribute, BuffAttribute):
    isFirst = True
    def __init__(self, level=20):
        max = 20
        horobuIcon = None
        horobuAttackLine = 6
        horobuDelay = Cooldown(milliseconds=570)
        horobuBuff = CreateSpecVector([CoreStat.DAMAGE_PERCENTAGE_BOSS], 20)
        OnPressSkill.__init__(
            self=self,
            icon= horobuIcon,
            advanced=SkillAdvance.Fourth,
            level=level,
            max=max
        )
        부적_스킬.__init__(
            self=self,
            damage_point=0,
            line=horobuAttackLine
        )
        SkillDelayAttribute.__init__(
            self=self,
            casting_delay=horobuDelay,
            applyAttackSpeed=True
        )
        BuffAttribute.__init__(
            self=self,
            stat=horobuBuff
        )

        if 마봉_호로부.isFirst and self.부적.AmuletGuage >= 100:
            self.부적.AmuletGuage -= 100
            마봉_호로부.isFirst = False
        elif self.부적.AmuletGuage < 100:
            raise ValueError("스킬 사용에 필요한 부적도력이 부족함")
        

    def GetSkillDamage(self):
        point = 250

        if 득의 in self.Owner._PassiveSkillList:
            reinforce = 득의()
            point += reinforce.DamagePoint_마봉_호로부()
            
        if 득도 in self.Owner._PassiveSkillList:
            reinforce = 득도()
            reinforce.ApplyCombat(False)
            if self._Owner._IsPassiveLevel:
                reinforce.ApplyPassiveLevel1()
            point += reinforce.DamagePoint_마봉_호로부()
        return point
    
    def UseSkill(self):
        self.괴력난신_트리거()
        addbuff = SpecVector()
        self.DamagePoint = self.GetSkillDamage()

        if 마봉_호로부_강화_5th in self.Owner._PassiveSkillList:
            addbuff += 마봉_호로부_강화_5th().reinforce

        horobuLog = self.Target.TakeAttack(char=self.Owner, skill=self, add=addbuff + self.BuffStat)

        self.ActiveOnHit()
        마봉_호로부.isFirst = True
        return [horobuLog]

class 마봉_호로부_강화_5th(PassiveSkill):
    def __init__(self, level=60):
        self.reinforce = CreateSpecVector([CoreStat.FINAL_DAMAGE_PERCENT], 2*level)
        self.reinforce[CoreStat.IGNORE_GUARD_PERCENTAGE] = 20
        
        PassiveSkill.__init__(
            self=self,
            advanced=SkillAdvance.Fifth,
            level=level,
            max=max
        )

class 두루마리_스킬(HoyoungSkill):
    def __init__(self, damage_point: int, line: int, castingCount: int = 1):
        self.두루마리 = 두루마리
        DamageAttribute.__init__(self, damage_point, line, castingCount)

    def GetDurumariBuff(self):
        return
    
class 권술_흡성와류(OnPressSkill, 두루마리_스킬, SummonAttribute, SkillDelayAttribute, CombatOrdersAttribute):
    isFirst = True
    def __init__(self, level=30):
        suckingIcon = None
        suckingDuration = Cooldown(seconds=40)
        self.suckingInterval = Cooldown(milliseconds=1200)
        suckingDelay = Cooldown(milliseconds=750)
        suckingDamage = 0
        suckingAttackLine = 6
        self.FirstAttackDelay = Cooldown(milliseconds=600)

        OnPressSkill.__init__(
            self=self,
            icon=suckingIcon,
            advanced=SkillAdvance.Fourth,
            level=level,
            max=30
        )
        두루마리_스킬.__init__(
            self=self,
            damage_point=suckingDamage,
            line=suckingAttackLine
        )
        SummonAttribute.__init__(
            self=self,
            duration=suckingDuration,
            interval=self.suckingInterval,
            mult=True
        )
        SkillDelayAttribute.__init__(
            self=self,
            casting_delay=suckingDelay,
            applyAttackSpeed=False
        )
        CombatOrdersAttribute.__init__(self)

        if 권술_흡성와류.isFirst and 두루마리.ScrollGuage >= 900:
            두루마리.ScrollGuage -= 900
            권술_흡성와류.isFirst = False
        elif 두루마리.ScrollGuage < 900:
            raise ValueError("스킬 사용에 필요한 부적도력이 부족함")

    def GetSkillDamage(self, level):
        point = 136 + 4 * level
        
        return point
    
    def UseSkill(self):
        
        if 권술_흡성와류_헤이스트 in self.Owner._PassiveSkillList:
            self.Interval = self.suckingInterval * 0.75
        
        self.DamagePoint = self.GetSkillDamage(self.Level)

        add = SpecVector()
        if 권술_흡성와류_강화_5th in self.Owner._PassiveSkillList:
            add = 권술_흡성와류_강화_5th().reinforce

        amuletLog = self.Target.TakeAttack(char=self.Owner, skill=self, add = add)
        권술_흡성와류.isFirst = True
        return [amuletLog]

class 권술_흡성와류_강화_5th(PassiveSkill):
    def __init__(self, level=60):
        self.reinforce = CreateSpecVector([CoreStat.FINAL_DAMAGE_PERCENT] , 2* level)
        self.reinforce[CoreStat.IGNORE_GUARD_PERCENTAGE] = 20
        super().__init__(SkillAdvance.Fifth, level, 60)

class 권술_미생강변(OnPressSkill, 두루마리_스킬, SkillDelayAttribute, DebuffAttribute, DurationAttribute, BuffAttribute):
    isFirst = True
    def __init__(self, level=20):
        mutationIcon = None
        mutationDuration = Cooldown(seconds=60)
        mutationDebuff = CreateSpecVector([CoreStat.IGNORE_GUARD_PERCENTAGE], 20)
        
        mutationDelay = Cooldown(milliseconds=630)
        mutationDamage = 0
        mutationAttackLine = 8
        mutationBuff = CreateSpecVector([CoreStat.DAMAGE_PERCENTAGE_BOSS], 20)

        OnPressSkill.__init__(
            self=self,
            icon=mutationIcon,
            advanced=SkillAdvance.Fourth,
            level=level,
            max=20
        )
        부적_스킬.__init__(
            self=self,
            damage_point=mutationDamage,
            line=mutationAttackLine
        )
        SkillDelayAttribute.__init__(
            self=self,
            casting_delay=mutationDelay,
            applyAttackSpeed=True
        )
        DebuffAttribute.__init__(
            self=self,
            debuff_stat=mutationDebuff,
            condition=[]
        )
        DurationAttribute.__init__(
            self=self,
            duration=mutationDuration,
            serverlack=False,
            isbuffmult=False
        )
        BuffAttribute.__init__(
            self=self,
            stat=mutationBuff
        )

        if 권술_미생강변.isFirst and self.두루마리.ScrollGuage>= 900:
            self.두루마리.ScrollGuage -= 900
            권술_미생강변.isFirst = False
        elif self.두루마리.ScrollGuage < 900:
            raise ValueError("스킬 사용에 필요한 부적도력이 부족함")

    def GetSkillDamage(self, level):
        point = 450 + 280 + 4 * level
        
        return point

    def UseSkill(self):
        self.괴력난신_트리거()
        권술_미생강변.isFirst = True
        
        self.DamagePoint = self.GetSkillDamage(self.Level)

        self.Target._DebuffManager.Add(self)

        add = SpecVector()
        if 권술_미생강변_강화_5th in self.Owner._PassiveSkillList:
            add = 권술_미생강변_강화_5th().reinforce

        amuletLog = self.Target.TakeAttack(char=self.Owner, skill=self, add = add+self.BuffStat)
        
    
        return [amuletLog]

class 권술_미생강변_강화_5th(PassiveSkill):
    def __init__(self, level=60):
        self.reinforce = CreateSpecVector([CoreStat.FINAL_DAMAGE_PERCENT] , 2* level)
        self.reinforce[CoreStat.IGNORE_GUARD_PERCENTAGE] = 20
        super().__init__(SkillAdvance.Fifth, level, 60)    

class 권술_호접지몽(OnPressSkill, BuffAttribute, DurationAttribute, SkillDelayAttribute, CombatOrdersAttribute):
    isFirst = True
    def __init__(self, level=30):
        butterflyDuration = Cooldown(seconds=100)
        butterflyIcon = None
        butterflyBuff = CreateSpecVector([CoreStat.FINAL_DAMAGE_PERCENT], 10)
        #self.Minimum = 0.7
        butterflyCastingDelay = Cooldown(milliseconds=600)
        OnPressSkill.__init__(
            self=self,
            icon=butterflyIcon,
            advanced=SkillAdvance.Fourth,
            level=level,
            max=30
        )
        DurationAttribute.__init__(
            self=self,
            duration=butterflyDuration,
            serverlack=True,
            isbuffmult=True
        )
        BuffAttribute.__init__(
            self=self,
            stat=butterflyBuff
        )
        SkillDelayAttribute.__init__(
            self=self,
            casting_delay=butterflyCastingDelay,
            applyAttackSpeed=False
        )
        CombatOrdersAttribute.__init__(self)
        
        if 권술_호접지몽.isFirst and 두루마리.ScrollGuage >= 900:
            두루마리.ScrollGuage -= 900
            권술_호접지몽.isFirst = False
        elif 두루마리.ScrollGuage < 900:
            raise ValueError("스킬 사용에 필요한 부적도력이 부족함")
        

    def UseSkill(self):
        self.isFirst = True
        return []
        
class 권술_호접지몽_나비(AutomateActivativeSkill, 두루마리_스킬, ProjectileAttribute, CooldownAttribute, CombatOrdersAttribute):
    def __init__(self, level = 30):
        butterflyIcon = None
        butterflyDamage = 0
        butterflyAttackLine = 1
        butterflyCount = 5 
        self.Minimum = 0.2
        self.Maximum = 1
        butterflyCooldown = Cooldown(seconds=1)
        
        AutomateActivativeSkill.__init__(
            self=self,
            advanced=SkillAdvance.Fourth,
            level=level,
            max=30
        )
        두루마리_스킬.__init__(
            self=self,
            damage_point=butterflyDamage,
            line=butterflyAttackLine,
            castingCount=butterflyCount
        )
        ProjectileAttribute.__init__(
            self=self,
            maximumTime= 1
        )
        CooldownAttribute.__init__(
            self=self,
            cooldown=butterflyCooldown,
            isresetable=False
        )
        CombatOrdersAttribute.__init__(self)


    def GetSkillDamage(self, level):
        point = 207 + 3 * level
        
        return point

    def UseSkill(self):
        self.괴력난신_트리거()
        addBuff = SpecVector()

        self.DamagePoint = self.GetSkillDamage(self.Level)

        if 권술_호접지몽_강화_5th in self.Owner._PassiveSkillList:
            addBuff += 권술_호접지몽_강화_5th().reinforce

        return [self.Target.TakeAttack(char=self.Owner, skill=self, add = addBuff)]
    
    def active(self):
        return super().active()

class 권술_호접지몽_강화_5th(PassiveSkill):
    def __init__(self, level=60):
        self.reinforce = CreateSpecVector([CoreStat.FINAL_DAMAGE_PERCENT], 2*level)
        self.reinforce[CoreStat.IGNORE_GUARD_PERCENTAGE] = 20
        
        PassiveSkill.__init__(
            self=self,
            advanced=SkillAdvance.Fifth,
            level=level,
            max=max
        )

class 선기_영약_태을선단(OnPressSkill, SummonAttribute, SkillDelayAttribute):
    def __init__(self, level=1):
        max = 1
        icon = None
        OnPressSkill.__init__(
            self=self,
            icon=icon,
            advanced=SkillAdvance.Hyper,
            level=level,
            max=max
        )
        SummonAttribute.__init__(
            self=self,
            duration=Cooldown(seconds=12),
            interval=Cooldown(seconds=1),
            mult=False
        )
        SkillDelayAttribute.__init__(
            self=self,
            casting_delay=Cooldown(milliseconds=540),
            applyAttackSpeed=False
        )
       

        부적.AmuletGuage = 부적._MaxAmuletGuage
        두루마리.ScrollGuage = 두루마리.MaxScrollGuage

    def UseSkill(self):
        부적.AmuletGuage += 35
        두루마리.ScrollGuage += 350
        return []

class 선기_극대_분신난무(OnPressSkill, BuffAttribute, SkillDelayAttribute, DurationAttribute, CooldownAttribute):
    def __init__(self, level=30):
        maxlevel = 30
        self.bunshinNum = 10
        self.Damage = 440
        OnPressSkill.__init__(
            self=self,
            icon=Any,
            advanced=SkillAdvance.Fifth,
            level=level,
            max=maxlevel
        )
        BuffAttribute.__init__(
            self=self,
            stat=SpecVector()
        )
        SkillDelayAttribute.__init__(
            self=self,
            casting_delay=Cooldown(milliseconds=900),
            applyAttackSpeed=False
        )
        DurationAttribute.__init__(
            self=self,
            duration=Cooldown(seconds=30),
            serverlack=False,
            isbuffmult=False
        )
        CooldownAttribute.__init__(
            self=self,
            cooldown=Cooldown(seconds=180),
            isresetable=False
        )
    def UseSkill(self):
        return []

class 선기_극대_분신난무_강화_6th(PassiveSkill):
    def __init__(self, level = 30):
        self.AddDamagePoint = 440+ level * 12
        PassiveSkill.__init__(
            self=self,
            advanced=SkillAdvance.Sixth,
            level=level,
            max=30
        )

class 권술_산령소환(OnPressSkill, 두루마리_스킬, SummonAttribute, SkillDelayAttribute, CooldownAttribute):
    isFirst = True
    def __init__(self, level=30):
        maxlevel = 30
        self.FirstAttackDelay = Cooldown(seconds=0.6)
        OnPressSkill.__init__(
            self=self,
            icon=Any,
            advanced=SkillAdvance.Fifth,
            level=level,
            max=maxlevel
        )
        HoyoungSkill.__init__(
            self=self,
            damage_point=1980,
            line=8,
            castingCount=1
        )
        SummonAttribute.__init__(
            self=self,
            duration= Cooldown(seconds=30 + level),
            interval=Cooldown(seconds=3),
            mult=False
        )
        SkillDelayAttribute.__init__(
            self=self,
            casting_delay=Cooldown(milliseconds=900),
            applyAttackSpeed=False
        )
        CooldownAttribute.__init__(
            self=self,
            cooldown=Cooldown(seconds=180),
            isresetable=False
        )

        if 권술_산령소환.isFirst and 두루마리.ScrollGuage >= 900:
            두루마리.ScrollGuage -= 900
            권술_산령소환.isFirst = False
        elif 두루마리.ScrollGuage < 900 and 권술_산령소환.isFirst:
            raise ValueError("스킬 사용에 필요한 부적도력이 부족함")

    def GetDamagePoint(self, level):
        return 900 + 36 * level

    def UseSkill(self):
        self.isFirst = True
        addbuff = SpecVector()
        if 권술_산령소환_강화_6th in self.Owner._PassiveSkillList:
            addbuff = 권술_산령소환_강화_6th().AddBuff

        if 부적.OnSuccess:
            self.DamagePoint = 350 + 14 *self.Level
            self.CastingCount = 4
            부적.OnSuccess = False
        else:
            self.DamagePoint = 1980
            self.CastingCount = 1
        log = []
        for _ in range(0, self.CastingCount):
            log.append(self.Target.TakeAttack(char=self.Owner, skill=self, add =addbuff))
        
        return log
    
class 권술_산령소환_강화_6th(PassiveSkill):
    def __init__(self, level = 30):
        self.AddBuff = SpecVector()
        base = 0
        if level == 1:
            base = 10
        elif level == 10:
            base = 25
        elif level == 20:
            base = 40
        elif level == 30:
            base = 60
        
        self.AddBuff[CoreStat.FINAL_DAMAGE_PERCENT] = base + level%10
        PassiveSkill.__init__(
            self=self,
            advanced=SkillAdvance.Sixth,
            level=level,
            max=30
        )

class 선기_강림_괴력난신(OnPressSkill, BuffAttribute, DurationAttribute, CooldownAttribute, SkillDelayAttribute):
    def __init__(self, level=30):
        icon = Any
        maxlevel = 30
        Buff = CreateSpecVector([CoreStat.DAMAGE_PERCENTAGE], 20+level*2)

        OnPressSkill.__init__(
            self=self,
            icon=icon,
            advanced=SkillAdvance.Fifth,
            level=level,
            max=maxlevel
        )
        BuffAttribute.__init__(
            self=self,
            stat=Buff
        )
        DurationAttribute.__init__(
            self=self,
            duration=Cooldown(seconds=30),
            serverlack=False,
            isbuffmult=False
        )
        CooldownAttribute.__init__(
            self=self,
            cooldown=Cooldown(seconds=180),
            isresetable=False
        )
        SkillDelayAttribute.__init__(
            self=self,
            casting_delay=Cooldown(seconds=0.9),
            applyAttackSpeed=False
        )


    def UseSkill(self):
        return []
    
class 선기_강림_괴력난신_신들의_일격(AutomateActivativeSkill, HoyoungSkill, CooldownAttribute):
    count = 0
    def __init__(self, level=30):
        maxlevel = 30

        AutomateActivativeSkill.__init__(
            self=self,
            advanced=SkillAdvance.Fifth,
            level=level,
            max=maxlevel            
        )
        HoyoungSkill.__init__(
            self=self,
            damage_point=self.GetDamagePoint(level),
            line=8
        )
        CooldownAttribute.__init__(
            self=self,
            cooldown=Cooldown(milliseconds=1500),
            isresetable=False
        )
        

    def GetDamagePoint(self,level):
        return 850 + 34*level
    
    def UseSkill(self):
        addbuff = SpecVector()
        if 선기_강림_괴력난신_강화_6th in self.Owner._PassiveSkillList:
            addbuff = 선기_강림_괴력난신_강화_6th().AddBuff
        return [self.Target.TakeAttack(char=self.Owner, skill=self, add = addbuff)]
    
    def active(self):
        return super().active()

class 선기_강림_괴력난신_신들의_강림(OnPressSkill, HoyoungSkill, SkillDelayAttribute, SummonAttribute):
    isCasting = True
    def __init__(self, level=30):
        maxlevel = 30
        self.FirstAttackDelay = Cooldown(milliseconds=3000)
        OnPressSkill.__init__(
            self=self,
            icon=Any,
            advanced=SkillAdvance.Fifth,
            level=level,
            max=maxlevel
        )
        HoyoungSkill.__init__(
            self=self,
            damage_point=self.GetDamagePoint(level),
            line= 15,
            castingCount=6
        )
        SkillDelayAttribute.__init__(
            self=self,
            casting_delay=Cooldown(milliseconds=3780),
            applyAttackSpeed=False
        )
        SummonAttribute.__init__(
            self=self,
            duration=Cooldown(milliseconds=3780),
            interval=self.FirstAttackDelay,
            mult=False,
        )

    def GetDamagePoint(self, level):
        return 1000 + 40 * level
    
    def UseSkill(self):
        if self.isCasting == False:
            addbuff = SpecVector()
            if 선기_강림_괴력난신_강화_6th in self.Owner._PassiveSkillList:
                addbuff = 선기_강림_괴력난신_강화_6th().AddBuff
            log = []
            for _ in range(0, self.CastingCount):
                log.append(self.Target.TakeAttack(char=self.Owner, skill=self, add = addbuff))
            return log
        else:

            self.Owner.BuffManager.Add(선기_강림_괴력난신_버프())
            self.isCasting = False
            # 난신 막타에 난신 데미지버프는 포함되지 않음.
            self.Owner.BuffManager.DeleteBuff(선기_강림_괴력난신())    
            
            
            self.Owner.SummonManager.Add(self)
            return []
                        
class 선기_강림_괴력난신_버프(OnPressSkill, BuffAttribute, DurationAttribute):
    def __init__(self, level=30):
        maxlevel = 30
        self.elementalbuff = CreateSpecVector([CoreStat.DAMAGE_PERCENTAGE], 20)
        OnPressSkill.__init__(
            self=self,
            icon=Any,
            advanced=SkillAdvance.Fifth,
            level=level,
            max=maxlevel
        )
        BuffAttribute.__init__(
            self=self,
            stat=SpecVector()
        )
        DurationAttribute.__init__(
            self=self,
            duration=Cooldown(seconds=30),
            serverlack=True,
            isbuffmult=False
        )

    def UseSkill(self):
        return []

class 선기_강림_괴력난신_강화_6th(PassiveSkill):
    def __init__(self, level = 30):
        self.AddBuff = SpecVector()
        base = 0
        if level == 1:
            base = 10
        elif level == 10:
            base = 25
        elif level == 20:
            base = 40
        elif level == 30:
            base = 60
        
        self.AddBuff[CoreStat.FINAL_DAMAGE_PERCENT] = base + level%10
        PassiveSkill.__init__(
            self=self,
            advanced=SkillAdvance.Sixth,
            level=level,
            max=30
        )

class 선기_천지인_환영(OnPressSkill, HoyoungSkill, CooldownAttribute):
    nowStack = 2
    def __init__(self, level=30):
        maxlevel = 30
        self.Maximum = 0.7
        self.Minimum = 0.6
        self.attribute = 천지인_속성.허
        OnPressSkill.__init__(
            self=self,
            icon=Any,
            advanced=SkillAdvance.Fifth,
            level=level,
            max=maxlevel
        )
        HoyoungSkill.__init__(
            self=self,
            damage_point=self.GetDamagePoint(level),
            line=6
        )
        CooldownAttribute.__init__(
            self=self,
            cooldown=Cooldown(seconds=5),
            isresetable=False
        )
    
    def GetDamagePoint(self, level):
        return 625 + 25*level
    
    def UseSkill(self):
        if not self.Owner.CooldownManager.isReady(선기_천지인_환영):
            return []
        num = sum([1 if e == False and e != 천지인_속성.허 else 0 for e in 부적.Status])

        log = []
        if 선기_천지인_환영.nowStack == 2:
            # 천지인 환영 버프가 있는 경우 미완성 속성 갯수만큼 연계함
            if self.Owner.BuffManager.isRegistered(선기_천지인_환영_버프):
                log.append(self.Attack())

                if sum([1 if e == False and e != 천지인_속성.허 else 0 for e in 부적.Status]) == 1:
                    summon = 선기_천지인_환영()
                    summon.Owner = self.Owner
                    summon.Target = self.Target
                    available = [천지인_속성.천, 천지인_속성.지, 천지인_속성.인]
                    
                    for e in available:
                        if not 부적.Status[e.value]:
                            summon.attribute = e
                    summon.Maximum = 0.3
                    summon.Minimum = 0.2
        

                    self.Owner.ProjectileManager.Add(summon)
            else:
                log.append(self.Attack())
                선기_천지인_환영.nowStack = 2
                self.Owner.CooldownManager.Count(선기_천지인_환영)
        elif 선기_천지인_환영.nowStack == 1:
            log.append(self.Attack())
 
        return log
    
    def Attack(self):
        self.괴력난신_트리거()
        선기_천지인_환영.nowStack -= 1
        if 선기_천지인_환영.nowStack == 0:
            self.Owner.CooldownManager.Count(선기_천지인_환영, forcedCooldown=Cooldown(seconds=2))
            선기_천지인_환영.nowStack = 2
        if 선기_천지인_환영_강화_6th in self.Owner._PassiveSkillList:
            addbuff = 선기_천지인_환영_강화_6th().AddBuff

        부적.Now = self.attribute


        return self.Target.TakeAttack(char=self.Owner, skill=self, add = addbuff)

class 선기_천지인_환영_버프(OnPressSkill, BuffAttribute, DurationAttribute, CooldownAttribute, SkillDelayAttribute):
    
    def __init__(self, level = 30):
        maxlevel = 30

        OnPressSkill.__init__(
            self=self,
            icon=Any,
            advanced=SkillAdvance.Fifth,
            level=level,
            max=maxlevel
        )
        CooldownAttribute.__init__(
            self=self,
            cooldown=Cooldown(seconds=2),
            isresetable=False
        )
        DurationAttribute.__init__(
            self=self,
            duration=Cooldown(seconds=30),
            # 서버렉 받으니까 수정좀 하지마 ㅅㅂ
            serverlack=True,
            isbuffmult=False
        )
        BuffAttribute.__init__(
            self=self, stat=SpecVector()
        )
        SkillDelayAttribute.__init__(
            self=self,
            casting_delay=Cooldown(milliseconds=720),
            applyAttackSpeed=False
        )
        
        
    
    def UseSkill(self):
        return []

class 선기_천지인_환영_강화_6th(PassiveSkill):
    def __init__(self, level = 30):
        self.AddBuff = SpecVector()
        base = 0
        if level == 1:
            base = 10
        elif level == 10:
            base = 25
        elif level == 20:
            base = 40
        elif level == 30:
            base = 60
        
        self.AddBuff[CoreStat.FINAL_DAMAGE_PERCENT] = base + level%10
        PassiveSkill.__init__(
            self=self,
            advanced=SkillAdvance.Sixth,
            level=level,
            max=30
        )
# --- 6차 스킬 -----
# 4차스킬 천지만물 강화스킬은 30초쿨타임마다 최종데미지 버프와 함께 공격스킬또한 30초쿨타임으로 강화함

class 천지만물(PassiveSkill, BuffAttribute, DurationAttribute, CooldownAttribute):
    ReinforceSkill = True
    def __init__(self, level=30):
        max = 30
        cool = Cooldown(seconds=30)
        dur = Cooldown(seconds=40)
        buff = CreateSpecVector([CoreStat.FINAL_DAMAGE_PERCENT], 5 + level//6)
        PassiveSkill.__init__(
            self=self,
            advanced=SkillAdvance.Sixth,
            level=level,
            max=max
        )
        BuffAttribute.__init__(
            self=self,
            stat=buff
        )
        DurationAttribute.__init__(
            self=self,
            duration=dur,
            serverlack=True,
            isbuffmult=False
        )
        CooldownAttribute.__init__(
            self=self,
            cooldown=cool,
            isresetable=False
        )
        
class 선기_파천황(OriginSkill, HoyoungSkill, SkillDelayAttribute, CooldownAttribute, BuffAttribute):
    def __init__(self, level=30):
        Icon = None
        max = 30
        pacheon1stDamage = 1350 + 45* level
        pacheon1stDamageLine = 3
        self.pacheon1stCount = 10

        self.pacheon2ndDamage = 1860 + 62 * level
        self.pacheon2ndDamageLine = 5
        self.pacheon2ndCount = 13

        self.pacheon3rdDamage = 4260 + 142* level
        self.pacheon3rdDamageLine = 12
        self.pacheon3rdCount = 9

        pacheonCastingDelay = Cooldown(milliseconds=7000)

        # 천지인 환영 발동을 위한 임시 로직
        self.Elemental = 천지인_속성.인

        pacheonTimingTable = [Cooldown(milliseconds=30)] + [Cooldown(milliseconds=210) for _ in range(0, self.pacheon1stCount -1)] \
        + [Cooldown(milliseconds=30)] + [Cooldown(milliseconds=180) for _ in range(0, self.pacheon2ndCount -1)] \
        + [Cooldown(milliseconds=320)] + [Cooldown(milliseconds=240) for _ in range(0, self.pacheon3rdCount -1)] + [Cooldown(milliseconds=770)] + [Cooldown(milliseconds=770)]
    
        pacheonCooldown = Cooldown(seconds=360)

        pacheonBuff = SpecVector()
        pacheonBuff += OriginSkill.CalculateBossDamage(level)
        pacheonBuff += OriginSkill.CalculateIgnoreGuard(level)


        OriginSkill.__init__(
            self=self,
            icon = Icon,
            advanced=SkillAdvance.Sixth,
            level=level,
            max=max,
            timingTable=pacheonTimingTable
        )
        HoyoungSkill.__init__(
            self=self,
            damage_point=pacheon1stDamage,
            line=pacheon1stDamageLine,
            castingCount=self.pacheon1stCount
        )
        SkillDelayAttribute.__init__(
            self=self,
            casting_delay=pacheonCastingDelay,
            applyAttackSpeed=False
        )
        CooldownAttribute.__init__(
            self=self,
            cooldown=pacheonCooldown,
            isresetable=False
        )
        BuffAttribute.__init__(
            self=self,
            stat = pacheonBuff
        )

    def UseSkill(self):
        for e in [천지인_속성.천, 천지인_속성.지, 천지인_속성.인]:
            if not 부적.Status[e.value]:
                self.Elemental = e
                break
        if not isinstance(self.Target, Dummy):
            raise TypeError("더미 입력값이 잘못되었음")
        
        self.ActiveOnHit()
        부적.Now = self.Elemental
        
        if self.index > self.pacheon1stCount:
            self.DamagePoint = self.pacheon2ndDamage
            self.AttackLine = self.pacheon2ndDamageLine
            if self.index > self.pacheon1stCount + self.pacheon2ndCount:
                self.DamagePoint = self.pacheon3rdDamage
                self.AttackLine = self.pacheon3rdDamageLine
            
        pacheonlog = self.Target.TakeAttack(char=self.Owner, skill=self, add = self.BuffStat)

        return [pacheonlog]
    
    def Finish(self):
        pass

    def Before(self):
        # 천지만물
        if 천지만물 in self.Owner._PassiveSkillList:
            self.Owner.BuffManager.Add(천지만물())
            

        

        