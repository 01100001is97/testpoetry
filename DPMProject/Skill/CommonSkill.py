from Core.ABCSkill import PassiveSkill, AutomateActivativeSkill, SkillAdvance, OnPressSkill
from Skill.Attributes import *
from Core.SpecElements import SpecVector, CoreStat, CreateSpecVector
from Item.ItemGroup import Weapon
from Core.ABCItem import ItemParts
from Core.Job import JobType, JobTypeInfo
from Dummy.Dummy import Dummy, DummySize
import math
from Dummy.Dummy import DamageLog
##-------------- 액티브 -------------------

class 연합의_의지(PassiveSkill, BuffAttribute):
    def __init__(self):
        passiveStat = SpecVector()
        passiveStat[CoreStat.STAT_ALL] = 5
        passiveStat[CoreStat.ATTACK_PHYSICAL] = 5
        passiveStat[CoreStat.ATTACK_SPELL] = 5
        PassiveSkill.__init__(self,advanced=SkillAdvance.Zero, level=1, max=1)
        BuffAttribute.__init__(self,stat=passiveStat)

    def DeleteBuff(self):
        return super().DeleteBuff()

# 패시브 스킬은 아니지만, DPM 계산 상 무한지속으로 간주 - 도핑리스트에 추가되었음
"""class 영웅의_메아리(PassiveSkill, BuffAttribute):
    def __init__(self):
        echoStat = SpecVector()
        echoStat[CoreStat.ATTACK_PHYSICAL_PERCENTAGE] = 4
        echoStat[CoreStat.ATTACK_SPELL_PERCENTAGE] = 4
        PassiveSkill.__init__(advanced=SkillAdvance.Zero, level=1, max=1)
        BuffAttribute.__init__(stat=echoStat)
"""

class 여제의_축복(PassiveSkill, BuffAttribute):
    def __init__(self):
        level = 30
        passiveStat = SpecVector()
        passiveStat[CoreStat.ATTACK_PHYSICAL] = level
        passiveStat[CoreStat.ATTACK_SPELL] = level
        PassiveSkill.__init__(self,advanced=SkillAdvance.Zero, level=level, max=30)
        BuffAttribute.__init__(self,stat=passiveStat)

    def DeleteBuff(self):
        return super().DeleteBuff()

# 패시브 스킬은 아니지만, DPM 계산 상 무한지속으로 간주 - 현재는 연금술 채택중이므로 누락
"""class 고급_무기_제련(PassiveSkill, BuffAttribute):
    def __init__(self):
        enchantStat = SpecVector()
        enchantStat[CoreStat.CRITICAL_DAMAGE] = 5
        PassiveSkill.__init__(advanced=SkillAdvance.Zero,level=1, max=1)
        BuffAttribute.__init__(stat=enchantStat)
"""
class 파괴의_얄다바오트(PassiveSkill, BuffAttribute):
    def __init__(self):
        enchantStat = SpecVector()
        enchantStat[CoreStat.FINAL_DAMAGE_PERCENT] = 10
        PassiveSkill.__init__(self,advanced=SkillAdvance.Zero, level=1, max=1)
        BuffAttribute.__init__(self,stat=enchantStat)

    def DeleteBuff(self):
        return super().DeleteBuff()
        
class 마약_버프(PassiveSkill, BuffAttribute):
    def __init__(self):
        passiveStat = SpecVector()
        # 마약 수치에 따라서 적용
        PassiveSkill.__init__(self,advanced=SkillAdvance.Zero,level=1, max=1)
        BuffAttribute.__init__(self,stat=passiveStat)

    def DeleteBuff(self):
        return super().DeleteBuff()

##-------------- 액티브 -------------------

class 리스트레인트링(OnPressSkill, BuffAttribute, CooldownAttribute, DurationAttribute, SkillDelayAttribute):
    def __init__(self, level = 4):
        buffStat = SpecVector()
        
        buffStat[CoreStat.ATTACK_PHYSICAL_PERCENTAGE] = level*25
        buffStat[CoreStat.ATTACK_SPELL_PERCENTAGE] = level*25
        OnPressSkill.__init__(self=self, icon=None, advanced=SkillAdvance.Zero, level=level, max=4)
        BuffAttribute.__init__(self=self, stat=buffStat)
        CooldownAttribute.__init__(self=self, cooldown=Cooldown(minutes=3),isresetable=False)
        DurationAttribute.__init__(self=self, duration=Cooldown(seconds=15), serverlack=False, isbuffmult=False)
        SkillDelayAttribute.__init__(self=self, casting_delay=Cooldown(milliseconds=30), applyAttackSpeed=False)

    @property
    def BuffStat(self):
        return self._BuffStat
    
    def UseSkill(self):
        return super().UseSkill()

        
        

class 웨폰퍼프_I링(OnPressSkill, BuffAttribute, CooldownAttribute, DurationAttribute, SkillDelayAttribute):
    def __init__(self, level = 4):
        multStat = SpecVector()
        #weaponSpec, _ = weapon.TotalSpec()
        
        multStat[CoreStat.STAT_INT] = level

        OnPressSkill.__init__(self=self, icon=None, advanced=SkillAdvance.Zero, level=level, max=4)
        BuffAttribute.__init__(self=self, stat=multStat)
        CooldownAttribute.__init__(self=self, cooldown=Cooldown(minutes=3),isresetable=False)
        DurationAttribute.__init__(self=self, duration=Cooldown(seconds=15), serverlack=True, isbuffmult=False)
        SkillDelayAttribute.__init__(self=self, casting_delay=Cooldown(milliseconds=30), applyAttackSpeed=False)

    @property
    def BuffStat(self):
        weapon = self.Owner.CharItemSlot.GetItem(part=ItemParts.Weapon)[0]
        spell, _ = weapon.TotalSpec()
        
        self._BuffStat[CoreStat.STAT_INT] = spell[CoreStat.ATTACK_SPELL] * 4
        return self._BuffStat
    
    def UseSkill(self):
        return super().UseSkill()

class 웨폰퍼프_D링(OnPressSkill, BuffAttribute, CooldownAttribute, DurationAttribute, SkillDelayAttribute):
    def __init__(self, level = 4):
        multStat = SpecVector()
        #weaponSpec, _ = weapon.TotalSpec()
        
        multStat[CoreStat.STAT_DEX] = level

        OnPressSkill.__init__(self=self, icon=None, advanced=SkillAdvance.Zero, level=level, max=4)
        BuffAttribute.__init__(self=self, stat=multStat)
        CooldownAttribute.__init__(self=self, cooldown=Cooldown(minutes=3),isresetable=False)
        DurationAttribute.__init__(self=self, duration=Cooldown(seconds=15), serverlack=True, isbuffmult=False)
        SkillDelayAttribute.__init__(self=self, casting_delay=Cooldown(milliseconds=30), applyAttackSpeed=False)

    @property
    def BuffStat(self):
        weapon = self.Owner.CharItemSlot.GetItem(part=ItemParts.Weapon)[0]
        spell, _ = weapon.TotalSpec()
        
        self._BuffStat[CoreStat.STAT_DEX] = spell[CoreStat.ATTACK_PHYSICAL] * 4
        return self._BuffStat
    
    def UseSkill(self):
        return super().UseSkill()

class 웨폰퍼프_S링(OnPressSkill, BuffAttribute, CooldownAttribute, DurationAttribute, SkillDelayAttribute):
    def __init__(self, level = 4):
        multStat = SpecVector()
        #weaponSpec, _ = weapon.TotalSpec()

        multStat[CoreStat.STAT_STR] = level

        OnPressSkill.__init__(self=self, icon=None, advanced=SkillAdvance.Zero, level=level, max=4)
        BuffAttribute.__init__(self=self, stat=multStat)
        CooldownAttribute.__init__(self=self, cooldown=Cooldown(minutes=3),isresetable=False)
        DurationAttribute.__init__(self=self, duration=Cooldown(seconds=15), serverlack=True, isbuffmult=False)
        SkillDelayAttribute.__init__(self=self, casting_delay=Cooldown(milliseconds=30), applyAttackSpeed=False)

    @property
    def BuffStat(self):
        weapon = self.Owner.CharItemSlot.GetItem(part=ItemParts.Weapon)[0]
        spell, _ = weapon.TotalSpec()
        
        self._BuffStat[CoreStat.STAT_STR] = spell[CoreStat.ATTACK_PHYSICAL] * 4
        return self._BuffStat
    
    def UseSkill(self):
        return super().UseSkill()

class 웨폰퍼프_L링(OnPressSkill, BuffAttribute, CooldownAttribute, DurationAttribute, SkillDelayAttribute):
    def __init__(self, level = 4):
        multStat = SpecVector()
        #weaponSpec, _ = weapon.TotalSpec()
        
        multStat[CoreStat.STAT_LUK] = level

        OnPressSkill.__init__(self=self, icon=None, advanced=SkillAdvance.Zero, level=level, max=4)
        BuffAttribute.__init__(self=self, stat=multStat)
        CooldownAttribute.__init__(self=self, cooldown=Cooldown(minutes=3),isresetable=False)
        DurationAttribute.__init__(self=self, duration=Cooldown(seconds=15), serverlack=True, isbuffmult=False)
        SkillDelayAttribute.__init__(self=self, casting_delay=Cooldown(milliseconds=30), applyAttackSpeed=False)

    @property
    def BuffStat(self):
        weapon = self.Owner.CharItemSlot.GetItem(part=ItemParts.Weapon)[0]
        spell, _ = weapon.TotalSpec()
        
        self._BuffStat[CoreStat.STAT_LUE] = spell[CoreStat.ATTACK_PHYSICAL] * 4
        return self._BuffStat
    
    def UseSkill(self):
        return super().UseSkill()
    
# 5차 쓸만한 스킬 -------------------------------------
# 샤프아이즈, 오더스, 윈드부스터 등은 무한지속 패시브 스킬로 간주함
class 쓸만한_샤프아이즈(PassiveSkill, BuffAttribute):
    def __init__(self, level = 1):
        sharpeyesStat = SpecVector()

        sharpeyesStat[CoreStat.CRITICAL_DAMAGE] = 8
        sharpeyesStat[CoreStat.CRITICAL_PERCENTAGE] = 10
        sharpeyesStat[CoreStat.STAT_ALL] = level

        PassiveSkill.__init__(
            self,
            advanced=SkillAdvance.Fifth,
            level=level,
            max=30
        )
        BuffAttribute.__init__(self, stat=sharpeyesStat)

    def DeleteBuff(self):
        return super().DeleteBuff()

class 쓸만한_컴뱃오더스(PassiveSkill):
    def __init__(self, level = 1):
        PassiveSkill.__init__(
            self, advanced=SkillAdvance.Fifth, level=level, max=30
        )
        
# 쓸어블, 쓸윈부

# 무한지속 패시브로 간주
class 메이플_용사(PassiveSkill, BuffAttribute, CombatOrdersAttribute):
    def __init__(self, level=30):
        max = 30
        
        buff = SpecVector()

        PassiveSkill.__init__(
            self=self,
            advanced=SkillAdvance.Fourth,
            level=level,
            max=max
        )
        BuffAttribute.__init__(
            self=self,
            stat=buff
        )
        CombatOrdersAttribute.__init__(self)

    def SetBuff(self,level:int):
        main = self.Owner.MainStat[0]
        result = SpecVector()
        result[main] = math.floor((self.Owner.Level *5 + 18)*round(level/2)/100)

        return result
        
    # Skill 의 Level getter 재정의
    @property
    def Level(self):
        return self._level
    
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
        self._BuffStat = self.SetBuff(level=level)

        

class 에픽_어드벤처(OnPressSkill, BuffAttribute, CooldownAttribute, DurationAttribute):
    def __init__(self, level=1):
        max = 1
        EpicIcon = None
        EpicStat = CreateSpecVector([CoreStat.DAMAGE_PERCENTAGE], 10)
        epicCool = Cooldown(seconds=120)
        epicDuration = Cooldown(seconds=60)

        OnPressSkill.__init__(
            self = self,
            icon = EpicIcon,
            advanced=SkillAdvance.Hyper,
            level=level,
            max=max
        )
        BuffAttribute.__init__(self=self, stat=EpicStat)
        CooldownAttribute.__init__(self=self, cooldown=epicCool,isresetable=False)
        DurationAttribute.__init__(
            self=self,
            duration=epicDuration,
            serverlack=True,
            isbuffmult=False
        )
    def UseSkill(self):
        return super().UseSkill()
    

class 오버로드_마나(PassiveSkill, BuffAttribute):
    def __init__(self, level=30):
        max = 30
        OverloadMP = CreateSpecVector([CoreStat.FINAL_DAMAGE_PERCENT], 5+math.floor(level/10))

        PassiveSkill.__init__(
            self=self,
            advanced=SkillAdvance.Fifth,
            level=level,
            max=max
        )
        BuffAttribute.__init__(
            self=self,
            stat=OverloadMP
        )

class 메이플_여신의_축복(OnPressSkill, BuffAttribute, DurationAttribute, ChargedCooldownAttribute, SkillDelayAttribute):
    def __init__(self, level=30):
        max = 30
        MapleGoddessBlessIcon = None
        MapleGoddessBlessBuffDuration = Cooldown(seconds=60)
        MapleGoddessBlessBuffCooldown = Cooldown(seconds=180)
        MapleGoddessBlessBuffCharage = 2
        MapleGoddessBlessCastingDelay = Cooldown(milliseconds=630)
        

        OnPressSkill.__init__(
            self=self,
            icon=MapleGoddessBlessIcon,
            advanced=SkillAdvance.Fifth,
            level=level,
            max=max
            )
        BuffAttribute.__init__(
            self=self,
            stat=SpecVector()
        )
        DurationAttribute.__init__(
            self=self,
            duration=MapleGoddessBlessBuffDuration,
            serverlack=True,
            isbuffmult=False
        )
        ChargedCooldownAttribute.__init__(
            self=self,
            cooldown=MapleGoddessBlessBuffCooldown,
            isresetable=False,
            maxcharge=MapleGoddessBlessBuffCharage,
            isCooldownable=True
        )
        SkillDelayAttribute.__init__(
            self=self,
            casting_delay=MapleGoddessBlessCastingDelay,
            applyAttackSpeed=True
        )

    def CalcStat(self):
        myStat = SpecVector()
        for buff in self.Owner._PassiveSkillList:
            if issubclass(buff, 메이플_용사):
                buff = buff()
                buff.Owner = self.Owner
                buff.ApplyCombat(isOriginal=False)
                
                myStat = buff.BuffStat
                break

        mainstat = self.Owner.MainStat[0]
        myStatValue = myStat[mainstat]
        myStat[mainstat] = 4 * myStatValue
        return myStat

    @property
    def BuffStat(self):

        return lambda a: self.CalcStat()
        
    
    def UseSkill(self):
        return super().UseSkill()

        
class 스파이더_인_미러(OnPressSkill, DamageAttribute, SkillDelayAttribute,CooldownAttribute,DurationAttribute):

    def __init__(self, level=30):
        spiderInMirrorIcon = None
        spiderInMirrorDamage = 450+18*level
        spiderInMirrorDamageLine = 15
        spiderInMirrorCastingDelay = Cooldown(milliseconds=960)
        spiderInMirrorCooldown = Cooldown(seconds=250)
        

        OnPressSkill.__init__(
            self=self,
            icon=spiderInMirrorIcon,
            advanced=SkillAdvance.Fifth,
            level=level,
            max=max
        )
        DamageAttribute.__init__(
            self=self,
            damage_point=spiderInMirrorDamage,
            line=spiderInMirrorDamageLine
        )
        SkillDelayAttribute.__init__(
            self=self,
            casting_delay=spiderInMirrorCastingDelay,
            applyAttackSpeed=True
        )
        CooldownAttribute.__init__(
            self=self,
            cooldown=spiderInMirrorCooldown,
            isresetable=False
        )

    def UseSkill(self):
        if not isinstance(self.Target, Dummy):
            raise TypeError("더미 입력값이 잘못되었음")
        

        spiderInMirrorLog = self.Target.TakeAttack(
            char = self.Owner,
            skill=self,
            add=SpecVector()
        )

        # 스인미 거울속의 거미 소환
        summon = 스파이더_인_미러_거울속의_거미(level=self.Level)
        summon.Owner = self.Owner
        summon.Target = self.Target

        self.Owner.SummonManager.Add(summon)


        return [spiderInMirrorLog]

class 스파이더_인_미러_거울속의_거미(OnPressSkill, DamageAttribute, NonlinearIntervalAttribute, SummonAttribute, SkillDelayAttribute):
    def __init__(self, level:int):
        max = 스파이더_인_미러().MaxLevel

        spiderInMirrorIcon = 스파이더_인_미러().Icon
        spiderInMirrorDamage = 175 + 7 * level
        spiderInMirrorDamageLine = 8
        spiderInMirrorCastingCount = 6
        spiderInMirrorNonlinearInterval = [Cooldown(milliseconds=e) for e in [900, 850, 750, 650, 5700]]
        spiderInMirrorNonlinearInterval = spiderInMirrorNonlinearInterval * spiderInMirrorCastingCount
        spiderInMirrorNonlinearInterval = spiderInMirrorNonlinearInterval[:-1]
        spiderInMirrorDuration = Cooldown(seconds=50)
        spiderInMirrorActivateDelay = Cooldown(milliseconds=1800) - 스파이더_인_미러().AttackDelay

        OnPressSkill.__init__(
            self=self,
            icon=spiderInMirrorIcon,
            advanced=SkillAdvance.Fifth,
            level=level,
            max=max
        )
        DamageAttribute.__init__(
            self=self,
            damage_point=spiderInMirrorDamage,
            line=spiderInMirrorDamageLine
        )
        NonlinearIntervalAttribute.__init__(
            self=self,
            intervals=spiderInMirrorNonlinearInterval,
            condition=lambda:True
        )
        SummonAttribute.__init__(
            self=self,
            duration=spiderInMirrorDuration,
            interval=None,
            mult=False
        )
        SkillDelayAttribute.__init__(
            self=self,
            casting_delay=spiderInMirrorActivateDelay,
            applyAttackSpeed=False
        )
        

    def UseSkill(self):
        if not isinstance(self.Target, Dummy):
            raise TypeError("더미 입력값이 잘못되었음")
        

        spiderInMirrorLog = self.Target.TakeAttack(
            char = self.Owner,
            skill=self,
            add=SpecVector()
        )

        

        return [spiderInMirrorLog]

class 크레스트_오브_더_솔라(OnPressSkill, DamageAttribute, CooldownAttribute,SkillDelayAttribute):
    def __init__(self, level=30):
        max = 30
        SunRiseIcon = None
        SunRiseDamage = 750 + 30*level
        SunRiseAttackLine = 12
        SunRiseAttackDelay = Cooldown(milliseconds=870)
        SunRiseCooldown = Cooldown(seconds=250)


        OnPressSkill.__init__(
            self=self,
            icon=SunRiseIcon,
            advanced=SkillAdvance.Fifth,
            level=level,
            max=max
        )
        DamageAttribute.__init__(
            self=self,
            damage_point=SunRiseDamage,
            line=SunRiseAttackLine
        )
        CooldownAttribute.__init__(
            self=self,
            cooldown=SunRiseCooldown,
            isresetable=False
        )
        SkillDelayAttribute.__init__(
            self=self,
            casting_delay=SunRiseAttackDelay,
            applyAttackSpeed=True
        )

    def UseSkill(self):
        
        if not isinstance(self.Target, Dummy):
            raise TypeError("더미 입력값이 잘못되었음")
        

        SunRiseLog = self.Target.TakeAttack(
            char = self.Owner,
            skill=self,
            add=SpecVector()
        )

        # 스인미 거울속의 거미 소환
        summon = 크레스트_오브_더_솔라_불꽃의_문양(level=self.Level)
        summon.Owner = self.Owner
        summon.Target = self.Target

        self.Owner.SummonManager.Add(summon)


        return [SunRiseLog]
    

class 크레스트_오브_더_솔라_불꽃의_문양(OnPressSkill, SummonAttribute, DamageAttribute, SkillDelayAttribute):
    def __init__(self, level = 30):
        
        SunRiseIcon = 크레스트_오브_더_솔라().Icon
        SunRiseDamage = 275 + 11 * level
        SunRiseDamageLine = 6
        SunRiseDuration = Cooldown(seconds=51)
        SunRiseInterval = Cooldown(milliseconds=2100)
        SunRiseActivateDelay =  Cooldown()

        OnPressSkill.__init__(
            self=self,
            icon=SunRiseIcon,
            advanced=SkillAdvance.Fifth,
            level=level,
            max=max
        )
        DamageAttribute.__init__(
            self=self,
            damage_point=SunRiseDamage,
            line=SunRiseDamageLine
        )
        SummonAttribute.__init__(
            self=self,
            duration=SunRiseDuration,
            interval= SunRiseInterval,
            mult=False
        )
        SkillDelayAttribute.__init__(
            self=self,
            casting_delay=SunRiseActivateDelay,
            applyAttackSpeed=True
        )
        

    def UseSkill(self):
        if not isinstance(self.Target, Dummy):
            raise TypeError("더미 입력값이 잘못되었음")
        

        SunRiseLog = self.Target.TakeAttack(
            char = self.Owner,
            skill=self,
            add=SpecVector()
        )

        

        return [SunRiseLog]
    

class 대기:
    def __init__(self) -> None:
        pass

    


    def UseSkill(self):
        return [DamageLog(self,0.0, 0, SpecVector(),SpecVector(), SpecVector(), None, line=0 )]
    
    def __str__(self):
        return '대기중'
        