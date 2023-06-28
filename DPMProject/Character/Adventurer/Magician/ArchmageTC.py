from Character.ABCCharacter import ABCCharacter, AttackType
from Character.Mastery import Mastery
from Core.Job import JobType, JobGroup, JobTypeInfo, JobConstant, JobName, JobNameInfo
from Item.Weapons.WeaponConstant import WeaponConstant
from Skill.LinkSkill import *
from Character.Union import Union8500_archmageTC
from Character.Ability import CharacterAbilityEnum
from Character.FarmMonster import FarmMonster
from Character.Portion import PortionDoping
from Skill.Adventurer.Magician.Archmage import *
from Skill.Adventurer.Magician.Magician import *
from Skill.Adventurer.Magician.ThunderCold import *
from Skill.CommonSkill import *

class ArchmageTC(ABCCharacter):
    def __init__(self,level: int):
        
        

        ABCCharacter.__init__(
            self,
            name = JobName.ArchmageTC,
            level = level,
            job = JobType.Magician,
            constant = WeaponConstant.스태프.value * JobConstant.ArchmageTC.value,
            mastery = Mastery.ArchMageTC.value,
            attacktype=AttackType.Spell,
        )
        
        self.LinkSkillSlot = set([
            와일드_레이지,
            데몬스_퓨리,
            퍼미에이트,
            무아,
            판단,
            소울_컨트랙트,
            시프_커닝,
            임피리컬_널리지,
            인텐시브_인설트,
            데들리_인스팅트,
            하이브리드_로직,
            전투의_흐름,
            자신감,
        ])
        self.AbilitySlot = [CharacterAbilityEnum.BuffDuration, CharacterAbilityEnum.CriticalProp, CharacterAbilityEnum.BossDamage]
        self.FarmList = [
                FarmMonster.반반,
                FarmMonster.검은_바이킹,
                FarmMonster.쁘띠_시그너스,

                FarmMonster.허수아비,
                FarmMonster.쁘띠_힐라,
                FarmMonster.쁘띠_반_레온,

                FarmMonster.쁘띠_은월,
                FarmMonster.쁘띠_랑,
                FarmMonster.쁘띠_라니아,

                FarmMonster.쁘띠_루미너스_어둠,
                FarmMonster.쁘띠_루미너스,
                FarmMonster.쁘띠_팬텀,

                FarmMonster.양철_나무꾼,
                FarmMonster.라피스,
                FarmMonster.쁘띠_아카이럼,

                FarmMonster.군단장_윌,
                FarmMonster.미르,
                FarmMonster.성장한_미르
            ]
        self.DopingBuff = [
            PortionDoping.반빨별,
            PortionDoping.고관비,
            PortionDoping.주스텟물약,
            PortionDoping.익스레드,
            PortionDoping.익스블루,
            PortionDoping.우뿌,
            PortionDoping.길축,
            PortionDoping.MVP슈파,
            PortionDoping.유힘,
            PortionDoping.붕뿌_생축_러파,
            PortionDoping.만렙버프275,
            PortionDoping.영메,
            PortionDoping.길드크뎀,
            PortionDoping.길드뎀지,
            PortionDoping.길드보공
        ]
        self.SetupPersonalTrait()
        self.SetSkillList([
            # 공용
            연합의_의지,
            여제의_축복,
            리스트레인트링,
            웨폰퍼프_I링,
            스파이더_인_미러_썬콜,
            크레스트_오브_더_솔라_썬콜,
            # 쓸만한 스킬
            쓸만한_샤프아이즈,
            쓸만한_컴뱃오더스,
            # 매지션
            MP증가,
            # 아크메이지
            매직_엑셀레이션,
            메디테이션,
            스펠_마스터리,
            하이_위즈덤,
            엘리멘탈_리셋,
            매직_크리티컬,
            엘리먼트_앰플리피케이션,
            # 썬콜
            썬더_스피어,
            체인_라이트닝,
            프리징_브레스,
            블리자드,
            블리자드_파이널어택,
            프로즌_오브,
            엘퀴네스,
            마스터_매직,
            메이플_용사,
            인피니티,
            # 하이퍼
            라이트닝_스피어,
            에픽_어드벤처,
            아이스_오라,
            아이스_오라_사용,
            체인_라이트닝_리인포스,
            체인_라이트닝_보너스어택,
            # 5차 스킬
            썬더_브레이크,
            스피릿_오브_스노우,
            아이스_에이지,
            주피터_썬더,
            오버로드_마나,
            메이플_여신의_축복,
            썬더_스피어_강화_5th,
            체인_라이트닝_강화_5th,
            프로즌_오브_강화_5th,
            블리자드_강화_5th,
            엘퀴네스_강화_5th,
            라이트닝_스피어_강화_5th,
            # 6차 스킬
            체인_라이트닝_강화_6th,
            체인_라이트닝_전류지대,
            프로즌_라이트닝


        ])
        self.LegionList = Union8500_archmageTC
        
        
