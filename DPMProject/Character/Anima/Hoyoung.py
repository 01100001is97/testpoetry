from Character.ABCCharacter import ABCCharacter, AttackType
from Character.Mastery import Mastery
from Core.Job import JobType, JobGroup, JobTypeInfo, JobConstant, JobName, JobNameInfo
from Item.Weapons.WeaponConstant import WeaponConstant
from Character.Ability import CharacterAbilityEnum
from Character.FarmMonster import FarmMonster
from Character.Portion import PortionDoping, DopingListAlchemy
from Skill.Attributes import JobName, JobType
from Skill.LinkSkill import *
from Skill.CommonSkill import *
from Skill.Anima.Hoyoung import *
from Character.Union import Union8500_Hoyoung
from Simulator.Anima.HoyoungDealingCycle import *

class Hoyoung(ABCCharacter):
    def __init__(self, level: int):
        ABCCharacter.__init__(
            self=self,
            name=JobName.Hoyoung,
            level=level,
            job=JobType.Thief,
            constant= WeaponConstant.부채.value,
            mastery= Mastery.Hoyeong.value,
            attacktype=AttackType.Physical
        )
        부적.Owner = self
        두루마리.Owner = self
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
        # TODO:패시브 레벨 1 적용되는 로직 확인
        self.AbilitySlot = [CharacterAbilityEnum.PassiveLevel, CharacterAbilityEnum.BossDamage, CharacterAbilityEnum.PanicDamage]
        self.FarmList = [
            FarmMonster.검은_바이킹,
            FarmMonster.쁘띠_시그너스,
            FarmMonster.허수아비,

            FarmMonster.쁘띠_반_레온,
            FarmMonster.쁘띠_랑,
            FarmMonster.쁘띠_루미너스,

            FarmMonster.쁘띠_루미너스_어둠,
            FarmMonster.쁘띠_루미너스_이퀄리브리엄,
            FarmMonster.쁘띠_은월,

            FarmMonster.쁘띠_힐라,
            FarmMonster.라즐리,
            FarmMonster.고양이,

            FarmMonster.검은_마법사의_그림자,
            FarmMonster.미르,
            FarmMonster.쁘띠_팬텀,

            FarmMonster.양철_나무꾼,
            FarmMonster.쁘띠_매그너스,
            FarmMonster.라피스
        ]
        self.DopingBuff = DopingListAlchemy
        self.SetSkillList([
            연합의_의지,
            여제의_축복,
            리스트레인트링,
            웨폰퍼프_L링,
            스파이더_인_미러,
            크레스트_오브_더_솔라,
            쓸만한_컴뱃오더스,
            쓸만한_샤프아이즈,
            레디_투_다이_패시브,
            레디_투_다이_1단계,
            레디_투_다이_2단계,
            # 패시브
            정령친화,
            괴이봉인,
            # 2차
            부채_숙련,
            심안,
            신체_단련,
            # 3차
            득의,
            수라,
            # 4차
            고급_부채_숙련,
            득도,
            점정,
            메이플_용사,
            # 하이퍼
            천지인_리인포스,
            천지인_보스킬러,
            환영분신부_이그노어가드,
            추적귀화부_헤이스트,
            권술_흡성와류_헤이스트,
            #액티브
            여의선_인,
            마봉_호로부,
            토파류_지,
            토파류_허실,
            환영_분신부,
            파초풍_천,
            파초풍_허실,
            지진쇄_지,
            지진쇄_허실,
            추적_귀화부,
            권술_미생강변,
            멸화염_천,
            멸화염_허실,
            금고봉_인,
            #둔갑_천근석,
            권술_흡성와류,
            권술_호접지몽,
            선기_영약_태을선단,
            #선기_몽유도원,
            #선기_분신_둔갑_태을선인,
            선기_극대_분신난무,
            권술_산령소환,
            선기_강림_괴력난신,
            선기_강림_괴력난신_신들의_강림,
            선기_천지인_환영_버프,
            그란디스_여신의_축복,
            여의선_인_강화_5th,
            토파류_강화_5th,
            지진쇄_강화_5th,
            파초풍_강화_5th,
            멸화염_강화_5th,
            금고봉_강화_5th,
            마봉_호로부_강화_5th,
            환영_분신부_강화_5th,
            추적_귀화부_강화_5th,
            권술_흡성와류_강화_5th,
            권술_미생강변_강화_5th,
            권술_호접지몽_강화_5th,
            # 6차
            금고봉_강화_6th,
            지진쇄_강화_6th,
            멸화염_강화_6th,
            천지만물,
            선기_극대_분신난무_강화_6th,
            권술_산령소환_강화_6th,
            선기_천지인_환영_강화_6th,
            선기_강림_괴력난신_강화_6th,
            선기_파천황
            

        ])
        self.LegionList = Union8500_Hoyoung

    
    def GetFlexibleScheduler(self, mode:HoyoungDealingMode):
        schedule = HoyoungSkillSchedule()
        schedule.Owner = self
        schedule.ExtremeAttackMode = mode

        return schedule
