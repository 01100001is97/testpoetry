from Core.ABCSkill import PassiveSkill, SkillAdvance, OnPressSkill, KeydownSkill, AutomateActivativeSkill, OriginSkill
from Core.SpecElements import SpecVector, CoreStat, CreateSpecVector
from Skill.Attributes import *
from Skill.Adventurer.Bowman.Archer import *
from Core.Condition import ConditionEnum
from Core.Probability import SuccessProbability
from random import random
from Character.ABCCharacter import ABCCharacter
from Dummy.Dummy import Dummy, DummySize
from datetime import timedelta
import random
import math
from Skill.CommonSkill import 스파이더_인_미러, 스파이더_인_미러_거울속의_거미, 크레스트_오브_더_솔라, 크레스트_오브_더_솔라_불꽃의_문양
from enum import Enum



class RelicSymbol(Enum):
    discharge = 0
    blast = 1
    transition = 2



class 렐릭_차지_컨트롤러:
    def __init__(self) -> None:
        self._Guage = 1000
        self._MaxRelicGuage = 1000
        self._Symbol = RelicSymbol.discharge
        self._Enchant = RelicSymbol.blast
        

    @property
    def Enchant(self):
        return self._Enchant
    
    @Enchant.setter
    def Enchant(self, symbol:RelicSymbol):
        if not isinstance(symbol, RelicSymbol):
            raise ValueError("심볼은 디스차지, 블래스트, 트랜지션 세 가지 중 하나임")
        self._Enchant = symbol

    @property
    def Guage(self):
        if 0 <= self._Guage <= self._MaxRelicGuage:
            return self._Guage
        else:
            raise AttributeError("Guage 값의 범위는 0~10")
    
    @Guage.setter
    def Guage(self, guage:int):
        if 0 <= guage <= self._MaxRelicGuage and 0 <= self._Guage + guage <= self._MaxRelicGuage:
            self._Guage = guage
        else:
            self._Guage = min(guage, self._MaxRelicGuage)
            
    @property
    def Symbol(self):
        return self._Symbol
    
    @Symbol.setter
    def Symbol(self, symbol:RelicSymbol):
        if not isinstance(symbol, RelicSymbol):
            raise ValueError("심볼은 디스차지, 블래스트, 트랜지션 세 가지 중 하나임")
        self._Symbol = symbol
   
   
    
렐릭_차지 = 렐릭_차지_컨트롤러()

class PathFinderSkill(DamageAttribute):
    def __init__(self, damage_point: int, line: int, castingCount: int = 1):
        self.RelicController = 렐릭_차지
        
        self.RelicDiff = 0
        
        super().__init__(damage_point, line, castingCount)

    def GetCurseTransitionBuff(self):
        if self.Owner.BuffManager.isRegistered(포세이큰_렐릭_렐릭해방):
            if self.Owner.CooldownManager.isReady(포세이큰_렐릭_고대의분노):
                summon = 포세이큰_렐릭_고대의분노()
                summon.Owner = self.Owner
                summon.Target = self.Target

                self.Owner.ProjectileManager.Add(summon, isImmediate=True)
                self.Owner.CooldownManager.Count(포세이큰_렐릭_고대의분노)

        if self.Target.Condition[ConditionEnum.커스_트랜지션] >= 0:
            return CreateSpecVector([CoreStat.CRITICAL_DAMAGE], self.Target.Condition[ConditionEnum.커스_트랜지션]* 4)
        else:
            return SpecVector()

    def IncrementCurseStack(self, prob = 0.4):
        add = 0
        if 카디널_포스_에디셔널_인핸스 in self.Owner._PassiveSkillList:
            add = 0.1
        if random.random() < prob + add:
            self.Target.increment_condition(ConditionEnum.커스_트랜지션)

    

    @property
    def AncientGuidance(self):
        return 가이던스._AncientGuidance
    
    @AncientGuidance.setter
    def AncientGuidance(self, guage):
        if not isinstance(guage, int):
            raise ValueError("렐릭 게이지 입력값이 잘못됨")
        가이던스._AncientGuidance = guage

        if 가이던스._AncientGuidance >= 500:
            self.Owner.BuffManager.Add(에인션트_가이던스_버프())
            가이던스._AncientGuidance = 0



    @property
    def RelicGuage(self):
        return self.RelicController.Guage
    
    @RelicGuage.setter
    def RelicGuage(self, guage):
        if not isinstance(guage, int):
            raise ValueError("렐릭 게이지 입력값이 잘못됨")
        
        self.RelicController.Guage = guage

    def ChargeRelicGuage(self, guage):
        """ 렐릭 게이지의 충전은 엔시언트 가이던스에서 요구하는 게이지 증감량을 반영함
        """
        beforeRelicGuage = self.RelicGuage
        self.RelicGuage = self.RelicGuage + guage
        afterRelicGuage = self.RelicGuage
        self.AncientGuidance = self.AncientGuidance + afterRelicGuage - beforeRelicGuage


class 에인션트_포스(PathFinderSkill):
    def __init__(self, damage_point: int, line: int, castingCount: int = 1):
        super().__init__(damage_point, line, castingCount)

    def GetAncientForceBuff(self):
        result = SpecVector()
        if 에인션트_포스_보스킬러 in self.Owner._PassiveSkillList:
            result[CoreStat.DAMAGE_PERCENTAGE_BOSS] += 20
        
        if 에인션트_포스_이그노어_가드 in self.Owner._PassiveSkillList:
            result[CoreStat.IGNORE_GUARD_PERCENTAGE] = 20

        if self.Owner.BuffManager.isRegistered(포세이큰_렐릭_렐릭해방):
            result[CoreStat.FINAL_DAMAGE_PERCENT] = 15

        return result

    def GetAncientArcheryBuff(self):
        archery = 에인션트_아처리()
        archery.ApplyCombat(isOriginal= False)
        addSpec = SpecVector()
        addSpec[CoreStat.FINAL_DAMAGE_PERCENT] = math.floor(archery.Level/3)
        addSpec[CoreStat.DAMAGE_PERCENTAGE_BOSS] = archery.Level + 20
        return addSpec

class 에인션트_포스_보스킬러(PassiveSkill):
    def __init__(self):
        PassiveSkill.__init__(
            self=self,
            advanced=SkillAdvance.Hyper,
            level=1,
            max=1
        )

class 에인션트_포스_이그노어_가드(PassiveSkill):
    def __init__(self):
        PassiveSkill.__init__(
            self=self,
            advanced=SkillAdvance.Hyper,
            level=1,
            max=1
        )


class 인챈트_포스(PathFinderSkill):
    def __init__(self, damage_point: int, line: int, castingCount: int = 1):

        super().__init__(damage_point, line, castingCount)

    def GetEnchant(self):
        return self.RelicController.Enchant
    
    def SetEnchant(self, symbol):
        self.RelicController.Enchant = symbol

    def GetEnchantForceBuff(self):
        result = SpecVector()
        if 에인션트_포스_보스킬러 in self.Owner._PassiveSkillList:
            result[CoreStat.DAMAGE_PERCENTAGE_BOSS] += 20
        
        if 에인션트_포스_이그노어_가드 in self.Owner._PassiveSkillList:
            result[CoreStat.IGNORE_GUARD_PERCENTAGE] = 20

        if self.Owner.BuffManager.isRegistered(포세이큰_렐릭_렐릭해방):
            result[CoreStat.FINAL_DAMAGE_PERCENT] = 15
        return result

    
    def GetAncientArcheryBuff(self):
        archery = 에인션트_아처리()
        archery.ApplyCombat(isOriginal= False)
        addSpec = SpecVector()
        addSpec[CoreStat.FINAL_DAMAGE_PERCENT] = math.floor(archery.Level/3)
        addSpec[CoreStat.DAMAGE_PERCENTAGE_BOSS] = archery.Level + 20
        return addSpec



class 에인션트_보우_액셀레이션(PassiveSkill, BuffAttribute):
    def __init__(self, level=10):
        max = 10
        stat = SpecVector()
        stat[CoreStat.STAT_DEX] = 2* level
        
        PassiveSkill.__init__(self=self, advanced=SkillAdvance.Second, level=level, max=max)
        BuffAttribute.__init__(self=self, stat=stat)


class 에인션트_보우_마스터리(PassiveSkill, BuffAttribute):
    # 마스터리 상승으로 되어있으나, 에인션트_보우_엑스퍼트 스킬에서 오르는 수치로 재조정되므로 패스함
    def __init__(self, level=10):
        max = 10
        stat = SpecVector()
        stat[CoreStat.ATTACK_PHYSICAL] = 3 * level
        

        PassiveSkill.__init__(self=self, advanced=SkillAdvance.Third, level=level, max=max)
        BuffAttribute.__init__(self=self, stat=stat)
       




class 에인션트_가이던스(PassiveSkill, BuffAttribute):
    def __init__(self, level=10):
        max = 10
        stat = SpecVector()
        stat[CoreStat.STAT_HP_PERCENTAGE] = 50
        stat[CoreStat.FINAL_DAMAGE_PERCENT] = 2 * level
        self._AncientGuidance = 0
        
        PassiveSkill.__init__(self=self, advanced=SkillAdvance.Third, level=level, max=max)
        BuffAttribute.__init__(self=self, stat=stat)
        

가이던스 = 에인션트_가이던스()


class 에인션트_가이던스_버프(PassiveSkill, BuffAttribute, DurationAttribute):
    def __init__(self, level=10):
        max = 10
        stat = SpecVector()
        stat[CoreStat.FINAL_DAMAGE_PERCENT] = 8
        
        buffduration = Cooldown(seconds=40)
        PassiveSkill.__init__(self=self, advanced=SkillAdvance.Third, level=level, max=max)
        BuffAttribute.__init__(self=self, stat=stat)
        DurationAttribute.__init__(
            self=self,
            duration=buffduration,
            serverlack=True,
            isbuffmult=False
        )

# 4차. 컴뱃오더스와 렙당 1의 효과를 받음
class 에센스_오브_아처(PassiveSkill, BuffAttribute, CombatOrdersAttribute):
    def __init__(self, level=10):
        max = 10
        stat = self.GetBuffStat(level)
       
        PassiveSkill.__init__(self=self, advanced=SkillAdvance.Fourth, level=level, max=max)
        BuffAttribute.__init__(self=self, stat=stat)
        CombatOrdersAttribute.__init__(self=self)

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
        self._BuffStat = self.GetBuffStat(level=level)

    def GetBuffStat(self, level):
        stat = SpecVector()
        stat[CoreStat.CRITICAL_PERCENTAGE] = level
        stat[CoreStat.DAMAGE_PERCENTAGE] = level
        stat[CoreStat.IGNORE_GUARD_PERCENTAGE] = 3 * level
        return stat
    

class 에인션트_보우_엑스퍼트(PassiveSkill, BuffAttribute, CombatOrdersAttribute, MasteryAttribute):
    def __init__(self, level=30):
        max = 30
        stat = SpecVector()
        ancientMastery = self.set_mastery(level)
        
        stat[CoreStat.ATTACK_PHYSICAL] = self.set_attack_power(level)
        stat[CoreStat.CRITICAL_DAMAGE] = self.set_critical_damage(level=level)

        PassiveSkill.__init__(self=self, advanced=SkillAdvance.Fourth, level=level, max=max)
        BuffAttribute.__init__(self=self, stat=stat)
        CombatOrdersAttribute.__init__(self=self)
        MasteryAttribute.__init__(self=self, mastery= ancientMastery)

    def set_mastery(self, level:int):
        return 55 + math.ceil(level/2)

    def set_attack_power(self, level:int):
        return level * 2

    def set_critical_damage(self, level:int):
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
        self.Mastery = self.set_mastery(level)
        self._BuffStat[CoreStat.ATTACK_PHYSICAL] = self.set_attack_power(level)
        self._BuffStat[CoreStat.CRITICAL_DAMAGE] = self.set_critical_damage(level)


class 일루전_스탭(PassiveSkill, BuffAttribute, CombatOrdersAttribute):
    def __init__(self, level=30):
        max = 30
        stat = SpecVector()
        stat[CoreStat.STAT_DEX] = self.set_agility(level)

        PassiveSkill.__init__(self=self, advanced=SkillAdvance.Fourth, level=level, max=max)
        BuffAttribute.__init__(self=self, stat=stat)
        CombatOrdersAttribute.__init__(self)

    def set_agility(self, level:int):
        return 20 + 3*level

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
        self._BuffStat[CoreStat.STAT_DEX] = self.set_agility(level=level)


class 어드밴스드_카디널_포스(PassiveSkill, CombatOrdersAttribute):

    def __init__(self, level=21):
        self.Level = level
        max = 21
        PassiveSkill.__init__(
            self=self,
            advanced=SkillAdvance.Fourth,
            level=level,
            max=max
        )
        CombatOrdersAttribute.__init__(self)

    # Get the damage for Cardinal Discharge
    def GetCardinalDischargeDamage(self):
        return 200+5*self.Level
    
    # Get the number of attack lines for Cardinal Discharge
    def GetCardinalDischargeAttackLine(self):
        return 5

    # Get the number of attack count for Cardinal Discharge
    def GetCardinalDischargeAttackCount(self):
        return 2

    # Get the damage for Cardinal Blast
    def GetCardinalBlastDamage(self):
        return 300+15*self.Level

    # Get the number of attack lines for Cardinal Blast
    def GetCardinalBlastAttackLine(self):
        return 5

    # Get the number of attack count for Cardinal Blast
    def GetCardinalBlastAttackCount(self):
        return 1

    # Get the damage for Cardinal Transition
    def GetCardinalTransitionDamage(self):
        return 400 + 7 * self.Level

    # Get the number of attack lines for Cardinal Transition
    def GetCardinalTransitionAttackLine(self):
        return 5
    # Get the number of attack count for Cardinal Transition
    def GetCardinalTransitionAttackCount(self):
        return 1
    
class 에디셔널_트랜지션(PassiveSkill, BuffAttribute, CombatOrdersAttribute):
    def __init__(self, level= 20):
        max = 20
        BuffStat= self.GetAtkPer(level)
        PassiveSkill.__init__(
            self=self,
            advanced=SkillAdvance.Fourth,
            level=level,
            max=max
        )
        BuffAttribute.__init__(
            self=self,
            stat=BuffStat
        )
        CombatOrdersAttribute.__init__(self)

    def GetAtkPer(self, level):
        return CreateSpecVector([CoreStat.ATTACK_PHYSICAL_PERCENTAGE], level)
    
    @property
    def Level(self):
        return super().Level
    
    # Skill 의 Level setter 재정의 - 스킬 레벨의 변화와 데미지 계산 바인딩
    @Level.setter
    def Level(self, level:int):
        # 검사 로직: 여기에서는 level이 0 이상의 정수인지 확인합니다.
        if not isinstance(level, int) or level < 0:
            raise ValueError("Level must be a non-negative integer")
        # 추가 로직: level이 MaxLevel 보다 큰 경우 값을 절삭함
        if level > self.MaxLevel:
            self._level = level
        self._level = level

        self.BuffStat = self.GetAtkPer(level)

    
class 에인션트_아처리(PassiveSkill, CombatOrdersAttribute):
    def __init__(self, level=30):
        max = 30
        PassiveSkill.__init__(
            self=self,
            advanced=SkillAdvance.Fourth,
            level=level,
            max=max
        )
        CombatOrdersAttribute.__init__(self=self)

    def AdditionalDischargeDamageUpgrade(self, level=31):
        return 35 + level
    
    def AdditionalBlastDamageUpgrade(self, level=31):
        return 40 + level
    
    # 스플릿 미스텔 패스함
        


class 카디널_포스(PathFinderSkill):
    def __init__(self, damage_point: int, line: int, attackSymbol:RelicSymbol, castingCount: int = 1 ):
        if not  isinstance(attackSymbol, RelicSymbol):
            raise ValueError("심볼 입력은 디스차지, 블래스트, 트랜지션 중 하나")
        self.AttackSymbol = attackSymbol
        PathFinderSkill.__init__(
            self=self,
            damage_point=damage_point,
            line=line,
            castingCount=castingCount
        )

    def RelicIsDifferent(self):
        
        if self.RelicController.Symbol is not self.AttackSymbol:
            self.Owner.CooldownManager.ReduceCooldown(에인션트_포스, Cooldown(seconds=1))
            self.Owner.CooldownManager.ReduceCooldown(인챈트_포스, Cooldown(seconds=1))

            if self.Owner.BuffManager.isRegistered(포세이큰_렐릭_렐릭해방):
                summon = 포세이큰_렐릭_렐릭해방()
                summon.Owner = self.Owner
                summon.Target = self.Target
                self.Owner.ProjectileManager.Add(summon)
       
            return True
        else:
            return False

    def GetCardinalForceReinforceBuff(self):
        result = SpecVector()
        if 카디널_포스_리인포스 in self.Owner._PassiveSkillList:
            result[CoreStat.DAMAGE_PERCENTAGE] += 20
        
        return result

    
    def CardinalBlastRelicCharge(self):
        
        self.ChargeRelicGuage(20)

    def CardinalDischargeArrowCharge(self):
        
        self.ChargeRelicGuage(10)

    def RavenCharge(self):
        self.ChargeRelicGuage(10)

    def CooldownAncientSkill(self):
        # TODO: 직전과 다른 카디널포스 사용시 애인션트/인챈트포스 스킬 쿨다운 1초
        pass

    # 직전과 다른 카디널 포스 스킬 사용시 5차 제외 에인션트 포스 스킬 쿨감 0.5초
        

class 카디널_포스_리인포스(PassiveSkill):
    def __init__(self):
        PassiveSkill.__init__(
            self=self,
            advanced=SkillAdvance.Hyper,
            level=1,
            max=1
        )

class 카디널_포스_에디셔널_인핸스(PassiveSkill):
    def __init__(self):
        PassiveSkill.__init__(
            self=self,
            advanced=SkillAdvance.Hyper,
            level=1,
            max=1
        )

class 카디널_포스_보너스_어택(PassiveSkill):
    def __init__(self):
        PassiveSkill.__init__(
            self=self,
            advanced=SkillAdvance.Hyper,
            level=1,
            max=1
        )


class 카디널_디스차지(OnPressSkill, 카디널_포스, SkillDelayAttribute, SkipableAttribute):
    def __init__(self, level = 20):
        CardinalMax = 20
        CardinalDischargeIcon = None

        cardinalDischargeDamage = self.GetSkillDamage(level=level)
        cardinalDischargeAttackLine = self.GetSkillAttackLine()
        cardinalDischargeAttackCount = self.GetSkillAttackCount()

        cardinalSkillDelay = Cooldown(milliseconds=480)
        cardinalDischargeSkipList = [
            카디널_블래스트,
            카디널_트랜지션
        ]
        cardinalDischargeSkipTiming = [
            Cooldown(milliseconds=270)
        ]

        OnPressSkill.__init__(
            self=self,
            icon = CardinalDischargeIcon,
            advanced=SkillAdvance.Fourth,
            level=level,
            max=CardinalMax
        )
        카디널_포스.__init__(
            self=self,
            damage_point=cardinalDischargeDamage,
            line=cardinalDischargeAttackLine,
            attackSymbol= RelicSymbol.discharge,
            castingCount= cardinalDischargeAttackCount
        )
        SkillDelayAttribute.__init__(
            self=self,
            casting_delay=cardinalSkillDelay,
            applyAttackSpeed=False,
            special=False
        )
        SkipableAttribute.__init__(
            self=self,
            combo_skill_list=cardinalDischargeSkipList,
            skip=cardinalDischargeSkipTiming
        )


    def GetSkillDamage(self, level):
        return 어드밴스드_카디널_포스().GetCardinalDischargeDamage()
        

    def GetSkillAttackLine(self):
        return 어드밴스드_카디널_포스().GetCardinalDischargeAttackLine()
        

    def GetSkillAttackCount(self):
        return 어드밴스드_카디널_포스().GetCardinalDischargeAttackCount()
        
    
    def UseSkill(self):
        # 카디널 포스의 효과 
        # 렐릭 게이지 참조
        # 공격
        # 사출기 매니저에 등록
        # 리턴: 스킬 로그
        self.IncrementCurseStack()
        addBuff = self.GetCardinalForceReinforceBuff()
        
        add = 0
        if 카디널_포스_보너스_어택 in self.Owner._PassiveSkillList:
            add = 1
            self.AttackLine = self.GetSkillAttackLine() + add
        
        if 카디널_디스차지_강화_5th in self.Owner._PassiveSkillList:
            addBuff += 카디널_디스차지_강화_5th().CardinalCoreReinforce
        

        result = []
        for _ in range(0, self.GetSkillAttackCount()):
            addCurse = self.GetCurseTransitionBuff()
            dischargeLog = self.Target.TakeAttack(char=self.Owner, skill=self, add = addBuff + addCurse)
            result.append(dischargeLog)
            self.CardinalDischargeArrowCharge()

        # 만약 카디널 디스차지 사용 중 렐릭 문양이 블래스트라면 "에디셔널 블래스트"를 발동함
        
        if self.RelicIsDifferent():
            addBlast = 에디셔널_블래스트()
            addBlast.Owner = self.Owner
            addBlast.Target = self.Target
            self.Owner.ProjectileManager.Add(addBlast)


        self.RelicController.Symbol = self.AttackSymbol

        return result

class 카디널_디스차지_강화_5th(PassiveSkill):
    def __init__(self, level=60):
        self.CardinalCoreReinforce = CreateSpecVector([CoreStat.FINAL_DAMAGE_PERCENT], level * 카디널_디스차지().Advanced.value)
        self.CardinalCoreReinforce[CoreStat.IGNORE_GUARD_PERCENTAGE] = 20
        PassiveSkill.__init__(
            self=self,
            advanced=SkillAdvance.Fifth,
            level=level,
            max=60
        )

class 카디널_블래스트(OnPressSkill, 카디널_포스, SkillDelayAttribute, SkipableAttribute):
    def __init__(self, level=20):
        CardinalMax = 20
        CardinalBlastIcon = None

        cardinalBlastDamage = self.GetSkillDamage(level=level)
        cardinalBlastAttackLine = self.GetSkillAttackLine()
        cardinalBlastAttackCount = self.GetSkillAttackCount()
        blastSymbol = RelicSymbol.blast
        cardinalSkillDelay = Cooldown(milliseconds=480)
        cardinalBlastSkipList = [
            카디널_디스차지,
            카디널_트랜지션
        ]
        cardinalBlastSkipTiming = [
            Cooldown(milliseconds=210)
        ]

        OnPressSkill.__init__(
            self=self,
            icon=CardinalBlastIcon,
            advanced=SkillAdvance.Fourth,
            level=level,
            max=CardinalMax
        )
        카디널_포스.__init__(
            self=self,
            damage_point=cardinalBlastDamage,
            line=cardinalBlastAttackLine,
            attackSymbol= blastSymbol,
            castingCount=cardinalBlastAttackCount
        )
        SkillDelayAttribute.__init__(
            self=self,
            casting_delay=cardinalSkillDelay,
            applyAttackSpeed=False,
            special=False
        )
        SkipableAttribute.__init__(
            self=self,
            combo_skill_list=cardinalBlastSkipList,
            skip=cardinalBlastSkipTiming
        )

    def GetSkillDamage(self, level):
        return 어드밴스드_카디널_포스().GetCardinalBlastDamage()
        
    def GetSkillAttackLine(self):
        
        return 어드밴스드_카디널_포스().GetCardinalBlastAttackLine()

    def GetSkillAttackCount(self):
        return 어드밴스드_카디널_포스().GetCardinalBlastAttackCount()
        


    def UseSkill(self):
        # 카디널 포스의 효과 
        # 렐릭 게이지 참조
        # 공격
        # 사출기 매니저에 등록
        # 리턴: 스킬 로그
        
        self.IncrementCurseStack()
        addbuff = self.GetCardinalForceReinforceBuff()

        add = 0
        if 카디널_포스_보너스_어택 in self.Owner._PassiveSkillList:
            add = 1
            self.AttackLine = self.GetSkillAttackLine() + add
        
        if 카디널_블래스트_6th in self.Owner._PassiveSkillList:
            self.DamagePoint = 카디널_블래스트_6th().CardinalBlast6thDamage
            self.AttackLine = 카디널_블래스트_6th().CardinalBlast6thAttackLine + add
        
        if 카디널_블래스트_강화_5th in self.Owner._PassiveSkillList:
            addbuff += 카디널_블래스트_강화_5th().CardinalCoreReinforce
        


        result = []
        for _ in range(0, self.GetSkillAttackCount()):
            cursebuff = self.GetCurseTransitionBuff()
            dischargeLog = self.Target.TakeAttack(char=self.Owner, skill=self, add = cursebuff + addbuff)
            result.append(dischargeLog)
            self.CardinalBlastRelicCharge()

        # 블래스트 스킬 사용 시 문양이 디스차지라면 "에디셔널 디스차지" 를 발동함
        if self.RelicIsDifferent():
            addDischarge = 에디셔널_디스차지()
            addDischarge.Owner = self.Owner
            addDischarge.Target = self.Target
            self.Owner.ProjectileManager.Add(addDischarge)

        self.RelicController.Symbol = self.AttackSymbol
        return result
    

class 카디널_블래스트_강화_5th(PassiveSkill):
    def __init__(self, level=60):
        self.CardinalCoreReinforce = CreateSpecVector([CoreStat.FINAL_DAMAGE_PERCENT], level * 카디널_블래스트().Advanced.value)
        self.CardinalCoreReinforce[CoreStat.IGNORE_GUARD_PERCENTAGE] = 20

        PassiveSkill.__init__(
            self=self,
            advanced=SkillAdvance.Fifth,
            level=level,
            max=max
        )

class 카디널_트랜지션(OnPressSkill, 카디널_포스, SkillDelayAttribute, SkipableAttribute):
    def __init__(self, level=20):
        CardinalMax = 30
        CardinalTransitionIcon = None

        cardinalTransitionDamage = self.GetSkillDamage(level=level)
        cardinalTransitionAttackLine = self.GetSkillAttackLine()
        cardinalTransitionAttackCount = self.GetSkillAttackCount()

        cardinalSkillDelay = Cooldown(milliseconds=480)
        cardinalTransitionSkipList = [
            #
        ]
        cardinalTransitionSkipTiming = [
            #Cooldown(milliseconds=270)
        ]

        OnPressSkill.__init__(
            self=self,
            icon=CardinalTransitionIcon,
            advanced=SkillAdvance.Fourth,
            level=level,
            max=CardinalMax
        )
        카디널_포스.__init__(
            self=self,
            damage_point=cardinalTransitionDamage,
            line=cardinalTransitionAttackLine,
            attackSymbol= RelicSymbol.transition,
            castingCount=cardinalTransitionAttackCount
        )
        SkillDelayAttribute.__init__(
            self=self,
            casting_delay=cardinalSkillDelay,
            applyAttackSpeed=True,
            special=False
        )
        SkipableAttribute.__init__(
            self=self,
            combo_skill_list=cardinalTransitionSkipList,
            skip=cardinalTransitionSkipTiming
        )

    def GetSkillDamage(self, level):
        return 어드밴스드_카디널_포스().GetCardinalTransitionDamage(level=level)
        

    def GetSkillAttackLine(self):
        return 어드밴스드_카디널_포스().GetCardinalTransitionAttackLine()
        

    def GetSkillAttackCount(self):
        return 어드밴스드_카디널_포스().GetCardinalTransitionAttackCount()
    

    def UseSkill(self):
        # 고대의 저주 디버프 1중첩
        # 카디널 포스의 효과 
        # 신속의 기운 참조
        # 공격
        # 사출기 매니저에 등록
        # 리턴: 스킬 로그


        addbuff = self.GetCardinalForceReinforceBuff()

        add = 0
        if 카디널_포스_보너스_어택 in self.Owner._PassiveSkillList:
            add = 1
            self.AttackLine = self.GetSkillAttackLine() + add
        
        
        return


# 에디셔널류 스킬
class 에디셔널_디스차지(OnPressSkill, PathFinderSkill, ProjectileAttribute, CombatOrdersAttribute):
    def __init__(self, level = 20):
        max = 20
        OnPressSkill.__init__(
            self=self,
            icon=None,
            advanced=SkillAdvance.Fourth,
            level=level,
            max=max
        )
        PathFinderSkill.__init__(
            self=self,
            damage_point=self.CalcDamagePoint(level),
            line=self.CalcAttackLine(),
            castingCount=self.CalcAttackCount()
        )
        ProjectileAttribute.__init__(
            self=self,
            maximumTime=0.5
        )
        CombatOrdersAttribute.__init__(
            self=self
        )

    def CalcDamagePoint(self, level):
        return 60 + 2*level + 에인션트_아처리().AdditionalDischargeDamageUpgrade()   
    def CalcAttackCount(self):
        return 3
    def CalcAttackLine(self):
        return 3
    
    def AddDischargeProb(self):
        
        addprob = 0
        if 카디널_포스_에디셔널_인핸스 in self.Owner._PassiveSkillList:
            addprob += 0.1
        return 40/100 + addprob

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

        self.DamagePoint = self.CalcDamagePoint(level)

    def UseSkill(self):
       
        result = []
        # 코어강화 방무 추가해야함

        addCount = 0
        if self.Owner.BuffManager.isRegistered(렐릭_에볼루션):
            addCount = 1
        addBuff = SpecVector()
        if 에디셔널_디스차지_강화_5th in self.Owner._PassiveSkillList:
            addBuff = 에디셔널_디스차지_강화_5th().dischargeCoreReinforce
        

        if random.random() < self.AddDischargeProb():
            for _ in range(0, self.CalcAttackCount()+addCount):
                result.append(self.Target.TakeAttack(char=self.Owner, skill=self, add = addBuff))
            

        return result
        
class 에디셔널_디스차지_강화_5th(PassiveSkill):
    def __init__(self, level=60):
        self.dischargeCoreReinforce = CreateSpecVector([CoreStat.FINAL_DAMAGE_PERCENT], level * 에디셔널_디스차지().Advanced.value)
        self.dischargeCoreReinforce[CoreStat.IGNORE_GUARD_PERCENTAGE] = 20
        PassiveSkill.__init__(
            self=self,
            advanced=SkillAdvance.Fifth,
            level=level,
            max = 60
        )

class 에디셔널_블래스트(OnPressSkill, PathFinderSkill, ProjectileAttribute, CombatOrdersAttribute):
    def __init__(self, level = 20):
        max = 20

        OnPressSkill.__init__(
            self=self,
            icon=None,
            advanced=SkillAdvance.Fourth,
            level=level,
            max = max
        )
        PathFinderSkill.__init__(
            self=self,
            damage_point=self.CalcDamagePoint(level=level),
            line=self.CalcAttackLine(),
            castingCount=2
        )
        ProjectileAttribute.__init__(
            self=self,
            maximumTime=0.5
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

        self.DamagePoint = self.CalcDamagePoint(level)

    def CalcDamagePoint(self, level):
        return 70 + 4 * level + 에인션트_아처리().AdditionalBlastDamageUpgrade()
    def CalcAttackCount(self):
        if 에디셔널_블래스트_6th in self.Owner._PassiveSkillList:
            return 3
        else:
            return 2
    def CalcAttackLine(self):
        return 3
    
    def AddBlastProb(self):
        addprob = 0
        if 카디널_포스_에디셔널_인핸스 in self.Owner._PassiveSkillList:
            addprob += 0.1
        if 에디셔널_블래스트_6th in self.Owner._PassiveSkillList:
            return 50/100 + addprob
        else:
            return 40/100 + addprob

    def UseSkill(self):
        result = []
        # TODO:코어강화 방무 추가해야함

        addCount = 0
        if self.Owner.BuffManager.isRegistered(렐릭_에볼루션):
            addCount = 1
        
        if 에디셔널_블래스트_강화_5th in self.Owner._PassiveSkillList:
            addbuff = 에디셔널_블래스트_강화_5th().additionalCoreReinforce

        if 에디셔널_블래스트_6th in self.Owner._PassiveSkillList:
            self.DamagePoint = 에디셔널_블래스트_6th().AdditionalBlast6thDamage
            self.AttackLine = 에디셔널_블래스트_6th().AdditionalBlast6thAttackLine

        isFirst = True
        if random.random() < self.AddBlastProb():
            for _ in range(0, self.CalcAttackCount()+addCount):
                if isFirst:
                    result.append(self.Target.TakeAttack(char=self.Owner, skill=self, add = addbuff))
                    isFirst = False
                    self.DamagePoint *= 0.7
                else:
                    result.append(self.Target.TakeAttack(char=self.Owner, skill=self, add = addbuff))
            
       
        if self.Owner.CooldownManager.isReady(에디셔널_블래스트_저주화살):
            
            for _ in range(0, 에디셔널_블래스트_저주화살().CastingCount):
                summon = 에디셔널_블래스트_저주화살()
                
                summon.Owner = self.Owner
                summon.Target= self.Target
                
                self.Owner.ProjectileManager.Add(summon)
            self.Owner.CooldownManager.Count(에디셔널_블래스트_저주화살)

        return result


class 에디셔널_블래스트_강화_5th(PassiveSkill):
    def __init__(self, level=60):
        self.additionalCoreReinforce = CreateSpecVector([CoreStat.FINAL_DAMAGE_PERCENT], level * 에디셔널_블래스트().Advanced.value)
        self.additionalCoreReinforce[CoreStat.IGNORE_GUARD_PERCENTAGE] = 20


class 렐릭_에볼루션(OnPressSkill, PathFinderSkill, DurationAttribute, BuffAttribute, SkipableAttribute):
    def __init__(self):
        max = 1
        level = 1
        RelicEvolutionIcon = None

        
        OnPressSkill.__init__(
            self=self,
            icon=RelicEvolutionIcon,
            advanced=SkillAdvance.Hyper,
            level=level,
            max=max
        )
        DurationAttribute.__init__(
            self=self,
            duration=Cooldown(seconds=30),
            serverlack=True,
            isbuffmult=False
        )
        BuffAttribute.__init__(
            self=self, stat=SpecVector()
        )
        PathFinderSkill.__init__(
            self=self,
            damage_point=0,
            line=0
        )
        SkipableAttribute.__init__(
            self=self,
            combo_skill_list=[
                얼티밋_블래스트
            ],
            skip=[
                Cooldown()
            ]
        )

    def UseSkill(self):
        self.ChargeRelicGuage(1000)

        self.Owner.BuffManager.Add(self)
        return []
        
class 레이븐_강화_5th(PassiveSkill):
    def __init__(self, level=60):
        self.RavenCoreReinforce = CreateSpecVector([CoreStat.FINAL_DAMAGE_PERCENT], level * 레이븐().Advanced.value)
        self.RavenCoreReinforce[CoreStat.IGNORE_GUARD_PERCENTAGE] = 20
        PassiveSkill.__init__(
            self=self,
            advanced=SkillAdvance.Third,
            level=level,
            max=max
        )

class 레이븐(OnPressSkill,PathFinderSkill, SummonAttribute, SkillDelayAttribute):
    # TODO: 이볼브랑 교체하기
    def __init__(self, level = 10):
        max = 10
        RavenIcon = None

        RavenDamage = 390
      
        RavenDamageLine = 1

        RavenAttackDelay = Cooldown(milliseconds=600)
        RavenInterval = Cooldown(milliseconds=570)
        RavenDuration = Cooldown(seconds=220)

        OnPressSkill.__init__(
            self=self,
            icon=RavenIcon,
            advanced=SkillAdvance.Third,
            level=level,
            max=max
        )
        PathFinderSkill.__init__(
            self=self,
            damage_point=RavenDamage,
            line=RavenDamageLine
        )
        SummonAttribute.__init__(
            self=self,
            duration=RavenDuration,
            interval=RavenInterval,
            mult=True
        )
        SkillDelayAttribute.__init__(
            self=self,
            casting_delay=RavenAttackDelay,
            applyAttackSpeed=False
        )
        
    def UseSkill(self):
        if not isinstance(self.Owner, ABCCharacter):
            raise TypeError("스킬의 소유자가 설정되지 않앗음")
        
        if not isinstance(self.Target, Dummy):
            raise TypeError("더미 입력값이 잘못되었음")
        
        addbuff = SpecVector()
        if 레이븐_강화_5th in self.Owner._PassiveSkillList:
            addbuff = 레이븐_강화_5th().RavenCoreReinforce
        
        RavenLog = self.Target.TakeAttack(
            char=self.Owner,
            skill=self,
            add=addbuff
        )
        self.ChargeRelicGuage(10)

        return [RavenLog]
    
class 커스_인챈트_블래스트(OnPressSkill,PathFinderSkill):
    def __init__(self):
        렐릭_차지.Enchant = RelicSymbol.blast
        OnPressSkill.__init__(
            self=self,
            icon=None,
            advanced=SkillAdvance.Fourth,
            level=1,
            max=1
        )

    def UseSkill(self):
        return []

class 커스_인챈트_디스차지(OnPressSkill,PathFinderSkill):
    def __init__(self):
        렐릭_차지.Enchant = RelicSymbol.discharge
        OnPressSkill.__init__(
            self=self,
            icon=None,
            advanced=SkillAdvance.Fourth,
            level=1,
            max=1
        )

    def UseSkill(self):
        return []

class 커스_인챈트_트랜지션(OnPressSkill,PathFinderSkill):
    def __init__(self):
        렐릭_차지.Enchant = RelicSymbol.transition
        OnPressSkill.__init__(
            self=self,
            icon=None,
            advanced=SkillAdvance.Fourth,
            level=1,
            max=1
        )

    def UseSkill(self):
        return []





class 엣지_오브_레조넌스(OnPressSkill, 에인션트_포스, SkipableAttribute, CooldownAttribute, CombatOrdersAttribute):
    def __init__(self, level = 30):
        max = 30
        ResonanceIcon = None

        ResonanceSkipList = [
            카디널_디스차지,
            카디널_블래스트,
            카디널_트랜지션
        ]
        ResonanceSkipTiming = [
            Cooldown(),
            Cooldown(),
            Cooldown()
        ]

        OnPressSkill.__init__(
            self=self,
            icon=ResonanceIcon,
            advanced=SkillAdvance.Fourth,
            level=level,
            max=max
        )
        에인션트_포스.__init__(
            self=self,
            damage_point= self.CalcDamagePoint(level),
            line= self.CalcAttackLine()
        )
        SkipableAttribute.__init__(
            self=self,
            combo_skill_list=ResonanceSkipList,
            skip=ResonanceSkipTiming
        )
        CooldownAttribute.__init__(
            self=self,
            cooldown=Cooldown(seconds=15),
            isresetable=True
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
        self.DamagePoint = self.CalcDamagePoint(level)
       

    def CalcDamagePoint(self, level):
        return 430 + 15 * level
    def CalcAttackLine(self):
        return 6


    def UseSkill(self):
        # 카디널 포스의 효과 
        # 렐릭 게이지 참조
        # 공격
        # 사출기 매니저에 등록
        # 리턴: 스킬 로그
        self.IncrementCurseStack()
        cursebuff = self.GetCurseTransitionBuff()

        # 에이션트 스킬 버프 효과
        ancientbuff = self.GetAncientForceBuff()
        ancientbuff += self.GetAncientArcheryBuff()

        if self.RelicController.Guage < 100:
            raise AttributeError("게이지가 부족하여 스킬을 사용할 수 없음")
        self.RelicController.Guage -= 100  # 렐릭 게이지 300 소비
      
        coreBuff = SpecVector()
        if 엣지_오브_레조넌스_강화_5th in self.Owner._PassiveSkillList:
            coreBuff = 엣지_오브_레조넌스_강화_5th().ResonanceCoreReinforce

        mul = self.Target.Condition[ConditionEnum.커스_트랜지션]
        mul = 1.1 ** mul - 1

        resuFinalDamage = CreateSpecVector([CoreStat.FINAL_DAMAGE_PERCENT], mul * 100)

        ResonanceLog = self.Target.TakeAttack(
            char=self.Owner,
            skill=self,
            add=cursebuff + ancientbuff + resuFinalDamage + coreBuff
        )
         
        return [ResonanceLog]

class 엣지_오브_레조넌스_강화_5th(PassiveSkill):
    def __init__(self, level=60):
        self.ResonanceCoreReinforce = CreateSpecVector([CoreStat.FINAL_DAMAGE_PERCENT], level * 엣지_오브_레조넌스().Advanced.value)
        self.ResonanceCoreReinforce[CoreStat.IGNORE_GUARD_PERCENTAGE] = 20
        PassiveSkill.__init__(
            self=self,
            advanced=SkillAdvance.Fifth,
            level=level,
            max = 60
        )

# 트임은 3차스킬이지만(컴뱃오더스 X) 코강은 4차적용받음
class 트리플_임팩트(OnPressSkill, 에인션트_포스, CooldownAttribute, SkillDelayAttribute):
    def __init__(self, level = 20):
        max = 20
        TripleIcon = None
        TripleDelay = Cooldown(milliseconds=540)
       

        OnPressSkill.__init__(
            self=self,
            icon=TripleIcon,
            advanced=SkillAdvance.Fourth,
            level=level,
            max=max
        )
        에인션트_포스.__init__(
            self=self,
            damage_point= self.CalcDamagePoint(level),
            line= self.CalcAttackLine()
        )
        CooldownAttribute.__init__(
            self=self,
            cooldown=Cooldown(seconds=10),
            isresetable=True
        )
        SkillDelayAttribute.__init__(
            self=self,
            casting_delay=TripleDelay,
            applyAttackSpeed=True
        )

    def CalcDamagePoint(self, level):
        return 265
    def CalcAttackLine(self):
        return 5
    
    def UseSkill(self):
        # 카디널 포스의 효과 
        # 렐릭 게이지 참조
        # 공격
        # 사출기 매니저에 등록
        # 리턴: 스킬 로그
        self.IncrementCurseStack()
        cursebuff = self.GetCurseTransitionBuff()

        # 에이션트 스킬 버프 효과
        ancientbuff = self.GetAncientForceBuff()
        ancientbuff += self.GetAncientArcheryBuff()

        if self.RelicController.Guage < 100:
            raise AttributeError("게이지가 부족하여 스킬을 사용할 수 없음")
        self.RelicController.Guage -= 100  # 렐릭 게이지 300 소비
      

        coreBuff = SpecVector()
        if 트리플_임팩트_강화_5th in self.Owner._PassiveSkillList:
            coreBuff = 트리플_임팩트_강화_5th().CardinalCoreReinforce


        ResonanceLog = self.Target.TakeAttack(
            char=self.Owner,
            skill=self,
            add=cursebuff + ancientbuff + coreBuff
        )
         
        return [ResonanceLog]


class 트리플_임팩트_강화_5th(PassiveSkill):
    def __init__(self, level=60):
        self.CardinalCoreReinforce = CreateSpecVector([CoreStat.FINAL_DAMAGE_PERCENT], level * 트리플_임팩트().Advanced.value)
        self.CardinalCoreReinforce[CoreStat.IGNORE_GUARD_PERCENTAGE] = 20
        PassiveSkill.__init__(
            self=self,
            advanced=SkillAdvance,
            level=level,
            max=60
        )

# 5차 전직
class 얼티밋_블래스트(OnPressSkill, 에인션트_포스, CooldownAttribute, SkillDelayAttribute, SummonAttribute):
    isCost = None
    def __init__(self, level = 30):
        max = 30
        UltimateBlastIcon = None
        UltimateBlastDelay = Cooldown(milliseconds=1800)  # 재사용 대기시간 120초
        self.FirstAttackDelay = Cooldown(milliseconds=1340)
        OnPressSkill.__init__(
            self=self,
            icon=UltimateBlastIcon,
            advanced=SkillAdvance.Fifth,
            level=level,
            max=max
        )
        에인션트_포스.__init__(
            self=self,
            damage_point= self.CalcDamagePoint(level),
            line= self.CalcAttackLine(),
            castingCount=6
        )
        CooldownAttribute.__init__(
            self=self,
            cooldown=Cooldown(seconds=120),  # 재사용 대기시간 120초
            isresetable=True
        )
        SkillDelayAttribute.__init__(
            self=self,
            casting_delay=UltimateBlastDelay,
            applyAttackSpeed=True
        )
        SummonAttribute.__init__(
            self=self,
            duration=UltimateBlastDelay,
            interval=self.FirstAttackDelay,
            mult=False
        
        )
        

    def CalcDamagePoint(self, level):
        return 400 + 20 * level

    def CalcAttackLine(self):
        return 15

    def UseSkill(self):
        # 렐릭 게이지 참조
        # 공격
        # 사출기 매니저에 등록
        # 리턴: 스킬 로그

        if 얼티밋_블래스트.isCost is None:
            CostGuage = self.RelicController.Guage
            얼티밋_블래스트.isCost = CreateSpecVector([CoreStat.FINAL_DAMAGE_PERCENT],(CostGuage//250) * 25)
            얼티밋_블래스트.isCost[CoreStat.IGNORE_GUARD_PERCENTAGE] = 100
            self.RelicController.Guage = 0

            self.Owner.SummonManager.Add(self)
            return []
            
        self.IncrementCurseStack()
        cursebuff = self.GetCurseTransitionBuff()

        # 에이션트 스킬 버프 효과
        ancientbuff = self.GetAncientForceBuff()
        ancientbuff += self.GetAncientArcheryBuff()
        
        
        

        result = []
        for _ in range(0, self.CastingCount):
            UltimateBlastLog = self.Target.TakeAttack(
                char=self.Owner,
                skill=self,
                add=cursebuff + ancientbuff  + 얼티밋_블래스트.isCost
            )
            result.append(UltimateBlastLog)
         
        return result

"""
class 레이븐_템페스트(OnPressSkill, 에인션트_포스, SummonAttribute, CooldownAttribute, SkillDelayAttribute):
    isFirst = True
    def __init__(self, level = 30):
        max = 30
        self.verified = False
        RavenTempestIcon = None
        RavenTempestDamage = 400 + 20 * level
        RavenTempestInterval = Cooldown(milliseconds=360)  # 방향 전환 대기시간 2초
        RavenTempestDelay = Cooldown(milliseconds=720)  # 이볼브 클래스에서 가져온 값
        RavenTempestDuration = Cooldown(seconds=27)  # 27초 동안 유지
        RavenTempestCooldown = Cooldown(seconds=120)  # 재사용 대기시간 120초

        if 레이븐_템페스트.isFirst:
            if 렐릭_차지.Guage < 300:
                raise ValueError("게이지가 부족해 스킬 사용 불가")
            렐릭_차지.Guage -= 300
            레이븐_템페스트.isFirst= False

        

        OnPressSkill.__init__(
            self=self,
            icon=RavenTempestIcon,
            advanced=SkillAdvance.Fifth,
            level=level,
            max=max
        )
        에인션트_포스.__init__(
            self=self,
            damage_point= RavenTempestDamage,
            line= self.CalcAttackLine()
        )
        CooldownAttribute.__init__(
            self=self,
            cooldown=RavenTempestCooldown,
            isresetable=False
        )
        SkillDelayAttribute.__init__(
            self=self,
            casting_delay=RavenTempestDelay,
            applyAttackSpeed=True
        )
        SummonAttribute.__init__(
            self=self,
            duration=RavenTempestDuration,
            interval= RavenTempestInterval,
            mult= False
        )

    def CalcAttackLine(self):
        return 5  # 5번 공격

    def UseSkill(self):
        # 렐릭 게이지 참조
        # 공격
        # 사출기 매니저에 등록
        # 리턴: 스킬 로그
        if self.verified or self.Owner.SummonManager.isSummoned(이볼브):
            for key, value in list(self.Owner.SummonManager.Summons.items()):
                if isinstance(key.Skill, 이볼브):
                    del self.Owner.SummonManager.Summons[key]
            self.verified = True

        cursebuff = self.GetCurseTransitionBuff()

        # 에이션트 스킬 버프 효과
        ancientbuff = self.GetAncientForceBuff()
        ancientbuff += self.GetAncientArcheryBuff()


        RavenTempestLog = self.Target.TakeAttack(
            char=self.Owner,
            skill=self,
            add=cursebuff + ancientbuff 
        )
         
        return [RavenTempestLog]
    
    def EndSummon(self):
        레이븐_템페스트.isFirst = True
"""

class 이볼브_템페스트(OnPressSkill, 에인션트_포스, SummonAttribute, CooldownAttribute, SkillDelayAttribute):
    isFirst = True
    EvolceCool = Cooldown()
    def __init__(self, level = 30):
        max = 30
        EvolveTempestIcon = None
        self.verified = False
        EvolveTempestDamage = 400 + 20 * level # 레벨에 따라 대미지가 증가한다.
        EvolveTempestInterval = Cooldown(milliseconds=120) # 방향 전환 대기시간 2초
        EvolveTempestDelay = Cooldown(milliseconds=720) # 이볼브 클래스에서 가져온 값
        EvolveTempestDuration = Cooldown(seconds=10) # 10초 동안 유지
        EvolveTempestCooldown = Cooldown(seconds=120) # 재사용 대기시간 120초


        if 이볼브_템페스트.isFirst:
            if 렐릭_차지.Guage < 300:
                raise ValueError("게이지가 부족해 스킬 사용 불가")
            렐릭_차지.Guage -= 300
            이볼브_템페스트.isFirst= False



        OnPressSkill.__init__(
            self=self,
            icon=EvolveTempestIcon,
            advanced=SkillAdvance.Fifth,
            level=level,
            max=max
        )
        에인션트_포스.__init__(
            self=self,
            damage_point= EvolveTempestDamage,
            line= self.CalcAttackLine()
        )
        CooldownAttribute.__init__(
            self=self,
            cooldown=EvolveTempestCooldown,
            isresetable=False
        )
        SkillDelayAttribute.__init__(
            self=self,
            casting_delay=EvolveTempestDelay,
            applyAttackSpeed=True
        )
        SummonAttribute.__init__(
            self=self,
            duration=EvolveTempestDuration,
            interval= EvolveTempestInterval,
            mult= False
        )

    def CalcAttackLine(self):
        return 6  # 6번 공격

    def UseSkill(self):
        # 렐릭 게이지 참조
        # 공격
        # 사출기 매니저에 등록
        # 리턴: 스킬 로그
        self.IncrementCurseStack()
        if self.verified or self.Owner.SummonManager.isSummoned(이볼브):
            for key, value in list(self.Owner.SummonManager.Summons.items()):
                if isinstance(key.Skill, 이볼브):
                    이볼브_템페스트.EvolceCool = value
                    del self.Owner.SummonManager.Summons[key]
            self.verified = True
        

        cursebuff = self.GetCurseTransitionBuff()

        # 에이션트 스킬 버프 효과
        ancientbuff = self.GetAncientForceBuff()
        ancientbuff += self.GetAncientArcheryBuff()


        EvolveTempestLog = self.Target.TakeAttack(
            char=self.Owner,
            skill=self,
            add=cursebuff + ancientbuff 
        )
        self.ChargeRelicGuage(20)
        return [EvolveTempestLog]
    
    def EndSummon(self):
        이볼브_템페스트.isFirst = True
        summon = 이볼브()
        summon.Owner = self.Owner
        summon.Target = self.Target

        summon.Duration = 이볼브_템페스트.EvolceCool
        self.Owner.SummonManager.Add(summon)


class 옵시디언_배리어(OnPressSkill, 인챈트_포스, SummonAttribute, CooldownAttribute, SkillDelayAttribute):
    isFirst = True
    

    def __init__(self, level = 30):
        max = 30
        
        BarrierIcon = None
        BarrierInterval = Cooldown(milliseconds=510) # 방향 전환 대기시간 2초
        BarrierDelay = Cooldown(milliseconds=720) # 이볼브 클래스에서 가져온 값
        BarrierDuration = Cooldown(seconds=12) # 10초 동안 유지
        BarrierCooldown = Cooldown(seconds=120) # 재사용 대기시간 120초
        BarrierAttackLine = 4

        if 옵시디언_배리어.isFirst == True:
            if 렐릭_차지.Guage < 300:
                raise AttributeError("게이지가 부족하여 스킬을 사용할 수 없음")
            렐릭_차지.Guage -= 300  # 렐릭 게이지 300 소비
            옵시디언_배리어.isFirst = False
       
        if 렐릭_차지.Enchant is RelicSymbol.blast:
            BarrierDamage = 500 + 18 * level # 레벨에 따라 대미지가 증가한다.
            
        elif 렐릭_차지.Enchant is RelicSymbol.discharge:
            BarrierDamage = 0
        elif 렐릭_차지.Enchant is RelicSymbol.transition:
            BarrierDamage = 500 + 18 * level # 레벨에 따라 대미지가 증가한다.
        else:
            raise ValueError("렐릭 문양 3가지 이외에는 없음")
            
        OnPressSkill.__init__(
            self=self,
            icon=BarrierIcon,
            advanced=SkillAdvance.Fifth,
            level=level,
            max=max
        )
        인챈트_포스.__init__(
            self=self,
            damage_point= BarrierDamage,
            line= self.CalcAttackLine()
        )
        CooldownAttribute.__init__(
            self=self,
            cooldown=BarrierCooldown,
            isresetable=False
        )
        SkillDelayAttribute.__init__(
            self=self,
            casting_delay=BarrierDelay,
            applyAttackSpeed=True
        )
        SummonAttribute.__init__(
            self=self,
            duration=BarrierDuration,
            interval= BarrierInterval,
            mult= False
        )

 
    def CalcAttackLine(self):
        return 4  # 6번 공격

    def UseSkill(self):
        # 렐릭 게이지 참조
        # 공격
        # 사출기 매니저에 등록
        # 리턴: 스킬 로그
        self.IncrementCurseStack()
        cursebuff = self.GetCurseTransitionBuff()

        
        ancientbuff = self.GetAncientArcheryBuff()
        ancientbuff += self.GetEnchantForceBuff()
        

        EvolveTempestLog = self.Target.TakeAttack(
            char=self.Owner,
            skill=self,
            add=cursebuff + ancientbuff 
        )
        
        return [EvolveTempestLog]

    def EndSummon(self):
        옵시디언_배리어.isFirst = True

class 렐릭_언바운드(OnPressSkill, 인챈트_포스, SummonAttribute, CooldownAttribute, SkillDelayAttribute, SkipableAttribute):
    isFirst = True
    def __init__(self, level=30):
        max = 30
        
        if 렐릭_언바운드.isFirst:
            if 렐릭_차지.Guage < 250:
                raise AttributeError("게이지가 부족하여 스킬을 사용할 수 없음")
            
            렐릭_차지.Guage -= 250
            렐릭_언바운드.isFirst = False

        UnboundIcon = None
        UnboundDamage = None
        UnboundInterval = Cooldown(milliseconds=0)  # 정보 부족으로 공란
        self.FirstAttackDelay = Cooldown(milliseconds=500)
        UnboundDelay = Cooldown(milliseconds=490)  # 정보 부족으로 공란
        UnboundDuration = Cooldown(seconds=0)  # 정보 부족으로 공란
        UnboundCooldown = Cooldown(seconds=120)  # 재사용 대기시간 120초
        UnboundAttackLine = 0  # 정보 부족으로 공란
        self.Unboundcount = 4

        if 렐릭_차지.Enchant is RelicSymbol.blast:
            UnboundDamage = 625 + 25 * level  # 레벨에 따라 대미지가 증가한다. 대략적인 추정치
            UnboundAttackLine = 8
            UnboundDuration = Cooldown(seconds=7)
            UnboundInterval = Cooldown(seconds=2)

            
        elif 렐릭_차지.Enchant is RelicSymbol.discharge:
            UnboundDamage = 1100 + 44 * level  # 레벨에 따라 대미지가 증가한다. 대략적인 추정치
            UnboundAttackLine = 0  # 정보 부족으로 공란
            UnboundDuration = Cooldown(seconds=22)
            
        elif 렐릭_차지.Enchant is RelicSymbol.transition:
            UnboundDamage = 1540 + 62 * level  # 레벨에 따라 대미지가 증가한다. 대략적인 추정치
            UnboundAttackLine = 5
            UnboundDuration = Cooldown(seconds=40)
        else:
            raise ValueError("심볼문양 3가지 외에 스킬은 없음")
            
        OnPressSkill.__init__(
            self=self,
            icon=UnboundIcon,
            advanced=SkillAdvance.Fifth,
            level=level,
            max=max
        )
        인챈트_포스.__init__(
            self=self,
            damage_point= UnboundDamage,
            line= UnboundAttackLine
        )
        CooldownAttribute.__init__(
            self=self,
            cooldown=UnboundCooldown,
            isresetable=False
        )
        SkillDelayAttribute.__init__(
            self=self,
            casting_delay=UnboundDelay,
            applyAttackSpeed=True
        )
        SummonAttribute.__init__(
            self=self,
            duration=UnboundDuration,
            interval= UnboundInterval,
            mult= False
        )
        SkipableAttribute.__init__(
            self=self,
            combo_skill_list=[
                얼티밋_블래스트,
                이볼브_템페스트
            ],
            skip=[
                Cooldown(),
                Cooldown(),
            ]
        )

    def UseSkill(self):
        # 렐릭 게이지 참조
        # 공격
        # 사출기 매니저에 등록
        # 리턴: 스킬 로그
        self.IncrementCurseStack()
        cursebuff = self.GetCurseTransitionBuff()

        
        ancientbuff = self.GetAncientArcheryBuff()
        ancientbuff += self.GetEnchantForceBuff()

        
        result = []
        for _ in range(0, self.Unboundcount):
            UnboundLog = self.Target.TakeAttack(
                char=self.Owner,
                skill=self,
                add=cursebuff + ancientbuff 
            )
            result.append(UnboundLog)
        
        return result

    def EndSummon(self):
        렐릭_언바운드.isFirst = True

# 6차 전직

class 카디널_블래스트_6th(PassiveSkill):
    def __init__(self, level=30):
        max = 30
        self.CardinalBlast6thDamage = 990
        self.CardinalBlast6thAttackLine = 5
        

        PassiveSkill.__init__(
            self=self,
            advanced=SkillAdvance.Sixth,
            level=level,
            max=max
        )


class 에디셔널_블래스트_6th(PassiveSkill):
    def __init__(self, level=30):
        max = 30
        self.AdditionalBlast6thDamage = 330
        self.AdditionalBlast6thAttackLine = 3
        

        PassiveSkill.__init__(
            self=self,
            advanced=SkillAdvance.Sixth,
            level=level,
            max=max
        )

class 에디셔널_블래스트_저주화살(OnPressSkill, DamageAttribute, CooldownAttribute, ProjectileAttribute):
    def __init__(self, level=30):
        max=30
        curseArrowDamage = 180
        curseArrowAttackLine = 4
        curseArrowAttackCount = 16

        OnPressSkill.__init__(
            self=self,
            icon=None,
            advanced=SkillAdvance.Sixth,
            level=level,
            max=max
        )
        DamageAttribute.__init__(
            self=self,
            damage_point=curseArrowDamage,
            line=curseArrowAttackLine,
            castingCount=curseArrowAttackCount
        )
        CooldownAttribute.__init__(
            self=self,
            cooldown=Cooldown(seconds=20),
            isresetable=False
        )
        ProjectileAttribute.__init__(
            self=self,
            maximumTime=0.5
        )


    def UseSkill(self):
        add=SpecVector()
        if 에디셔널_블래스트_강화_5th in self.Owner._PassiveSkillList:
            add = 에디셔널_블래스트_강화_5th().additionalCoreReinforce
        return [self.Target.TakeAttack(char=self.Owner, skill=self, add = add)]
        

class 포세이큰_렐릭(OriginSkill, PathFinderSkill, CooldownAttribute, SkillDelayAttribute):
    def __init__(self, level= 30):
        RelicIcon = None
        max = 30
        Relic1stDamage = 3600
        Relic1stDamageLine = 8
        self.Relic1stCount = 3

        self.relic2ndDamage = 3600
        self.relic2ndDamageLine = 8
        self.Relic2ndCount = 2

        self.Relic3rdDamage = 5400
        self.Relic3rdtDamageLine = 12
        self.Relic3rdCount = 5
        


        Relic1stCastingdelay = Cooldown(milliseconds=6540)
        RelicTimingTable = [Cooldown(seconds=1)] + [Cooldown(milliseconds=30) for _ in range(0, self.Relic1stCount-1)] \
        + [Cooldown(seconds=3)] + [Cooldown(milliseconds=30) for _ in range(0, self.Relic2ndCount-1)] \
        + [Cooldown(milliseconds=2300)] + [Cooldown(milliseconds=30) for _ in range(0, self.Relic3rdCount)]
        
        RelicCooldown = Cooldown(seconds=360)

        OriginSkill.__init__(
            self=self,
            icon=RelicIcon,
            advanced=SkillAdvance.Sixth,
            level=level,
            max=max,
            timingTable=RelicTimingTable
        )
        PathFinderSkill.__init__(
            self=self,
            damage_point=Relic1stDamage,
            line=Relic1stDamageLine,
            castingCount=self.Relic1stCount
        )
        SkillDelayAttribute.__init__(
            self=self,
            casting_delay=Relic1stCastingdelay,
            applyAttackSpeed=False
        )
        CooldownAttribute.__init__(
            self=self,
            cooldown=RelicCooldown,
            isresetable=False
        )

    def UseSkill(self):
        if not isinstance(self.Target, Dummy):
            raise TypeError("더미 입력값이 잘못되었음")
        
        
        buff = self.GetCurseTransitionBuff()
        
        if self.index > self.Relic1stCount + self.Relic2ndCount:
            self.DamagePoint = self.Relic3rdDamage
            self.AttackLine = self.Relic3rdtDamageLine
            


        RelicLog = self.Target.TakeAttack(char=self.Owner, skill=self, add = buff)

        return [RelicLog]


    def Finish(self):
        pass

    def Before(self):

        summon = 포세이큰_렐릭_렐릭해방()
        summon.Owner = self.Owner
        summon.Target = self.Target
        self.Owner.BuffManager.Add(summon)

         

class 포세이큰_렐릭_렐릭해방(OnPressSkill, PathFinderSkill, BuffAttribute, DurationAttribute, ProjectileAttribute):
    def __init__(self, level = 30):
        max = 30

        OnPressSkill.__init__(
            self=self,
            icon=None,
            advanced=SkillAdvance.Sixth,
            level=level,
            max=max
        )
        BuffAttribute.__init__(
            self=self,
            stat=SpecVector()
        )
        DurationAttribute.__init__(
            self=self,
            duration=Cooldown(seconds=30),
            # TODO: 서버렉 여부 확인
            serverlack=False,
            isbuffmult=False
        )
        ProjectileAttribute.__init__(
            self=self,
            maximumTime=0.5
        )
        PathFinderSkill.__init__(
            self=self,
            damage_point=1080,
            line=3
        )


    def UseSkill(self):
        addbuff = self.GetCurseTransitionBuff()

        ArrowLog = self.Target.TakeAttack(char=self.Owner, skill=self, add = addbuff)
        return [ArrowLog]
    
class 포세이큰_렐릭_고대의분노(OnPressSkill, 에인션트_포스, CooldownAttribute,ProjectileAttribute):
    def __init__(self, level=30):
        max = 30
        relicicon = None

        RelicAddDamage = 1200
        RelicAddAttackLine = 8
        RelicAddCooldown = Cooldown(seconds=10)
        AttCount = 3
        OnPressSkill.__init__(
            self=self,
            advanced=SkillAdvance.Sixth,
            level=level,
            max=max,
            icon=relicicon
        )
        에인션트_포스.__init__(
            self=self,
            damage_point=RelicAddDamage,
            line=RelicAddAttackLine,
            castingCount=AttCount
        )
        CooldownAttribute.__init__(
            self=self,
            cooldown=RelicAddCooldown,
            isresetable=False
        )
        ProjectileAttribute.__init__(
            self=self,
            maximumTime=0
        )
        
    def UseSkill(self):
        if not isinstance(self.Owner, ABCCharacter):
            raise TypeError("스킬의 소유자가 설정되지 않았음")
        
        if not isinstance(self.Target, Dummy):
            raise TypeError("더미 입력값이 잘못되었음")
        
        # 에인션트_포스 스킬 시 공격 카운트에 따른 버프 효과를 받아옴
        
        
        cursebuff = self.GetCurseTransitionBuff()

        # 에이션트 스킬 버프 효과
        ancientbuff = self.GetAncientForceBuff()
        ancientbuff += self.GetAncientArcheryBuff()
        
        result = []
        for _ in range(0, self.CastingCount):
            subRelicLog = self.Target.TakeAttack(char=self.Owner, skill=self, add = cursebuff + ancientbuff)
            result.append(subRelicLog)

        return result
    


class 스파이더_인_미러_패스파인더(스파이더_인_미러, PathFinderSkill):
    def __init__(self, level=30):
        스파이더_인_미러.__init__(self,level)

    # 패스파인더의의 스파이더 인 미러는 커스 트랜지션의 효과를 받음
    def UseSkill(self):

        if not isinstance(self.Target, Dummy):
            raise TypeError("더미 입력값이 잘못되었음")
        stat = self.GetCurseTransitionBuff()

        spiderInMirrorLog = self.Target.TakeAttack(
            char = self.Owner,
            skill=self,
            add=stat
        )

        # 스인미 거울속의 거미 소환
        summon = 스파이더_인_미러_거울속의_거미_패스파인더()
        summon.Owner = self.Owner
        summon.Target = self.Target

        self.Owner.SummonManager.Add(summon)


        return [spiderInMirrorLog]
    


class 스파이더_인_미러_거울속의_거미_패스파인더(스파이더_인_미러_거울속의_거미, PathFinderSkill):
 
    def __init__(self, level=30):
        스파이더_인_미러_거울속의_거미.__init__(
            self=self,
            level=level
        )
    

    def UseSkill(self):
        if not isinstance(self.Target, Dummy):
            raise TypeError("더미 입력값이 잘못되었음")
        stat = self.GetCurseTransitionBuff()


        spiderInMirrorLog = self.Target.TakeAttack(
            char = self.Owner,
            skill=self,
            add=stat
        )
        return [spiderInMirrorLog]
    
class 크레스트_오브_더_솔라_패스파인더(크레스트_오브_더_솔라, PathFinderSkill):
    def __init__(self):
        크레스트_오브_더_솔라.__init__(self=self)

    def UseSkill(self):
        stat = self.GetCurseTransitionBuff()
        if not isinstance(self.Target, Dummy):
            raise TypeError("더미 입력값이 잘못되었음")
        

        SunRiseLog = self.Target.TakeAttack(
            char = self.Owner,
            skill=self,
            add=stat
        )

        # 스인미 거울속의 거미 소환
        summon = 크레스트_오브_더_솔라_불꽃의_문양_패스파인더()
        summon.Owner = self.Owner
        summon.Target = self.Target

        self.Owner.SummonManager.Add(summon)


        return [SunRiseLog]
    

class 크레스트_오브_더_솔라_불꽃의_문양_패스파인더(크레스트_오브_더_솔라_불꽃의_문양, PathFinderSkill):
    def __init__(self):
        크레스트_오브_더_솔라_불꽃의_문양.__init__(
            self=self
            
        )

    def UseSkill(self):
        
        stat = self.GetCurseTransitionBuff()

        if not isinstance(self.Target, Dummy):
            raise TypeError("더미 입력값이 잘못되었음")
        

        SunRiseLog = self.Target.TakeAttack(
            char = self.Owner,
            skill=self,
            add=stat
        )
        return [SunRiseLog]