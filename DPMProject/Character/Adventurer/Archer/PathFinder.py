from Character.ABCCharacter import ABCCharacter, AttackType
from Character.Mastery import Mastery
from Core.Job import JobType, JobGroup, JobTypeInfo, JobConstant, JobName, JobNameInfo
from Item.Weapons.WeaponConstant import WeaponConstant
from Skill.Attributes import JobName, JobType
from Skill.LinkSkill import *
from Character.Ability import CharacterAbilityEnum
from Character.FarmMonster import FarmMonster
from Character.Portion import PortionDoping, DopingListAlchemy
from Skill.CommonSkill import *
from Skill.Adventurer.Bowman.Archer import *
from Skill.Adventurer.Bowman.PathFinder import *
from Character.Union import Union8500_PathFinder

class PathFinder(ABCCharacter):
    def __init__(self, level):
        ABCCharacter.__init__(
            self=self,
            name= JobName.PathFinder,
            level=level,
            job = JobType.Bowman,
            constant=WeaponConstant.에인션트보우.value,
            mastery=Mastery.PathFinder.value,
            attacktype=AttackType.Physical
        )
        self.LinkSkillSlot = set([
            임피리컬_널리지,
            와일드_레이지,
            데몬스_퓨리,
            하이브리드_로직,
            판단,
            인텐시브_인설트,
            무아,
            소울_컨트랙트,
            시프_커닝,
            프라이어_프리퍼레이션,
            퍼미에이트,
            데들리_인스팅트,
            어드벤쳐러_큐리어스
        ])
        self.AbilitySlot = [CharacterAbilityEnum.BossDamage, CharacterAbilityEnum.CriticalProp, CharacterAbilityEnum.PanicDamage]
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

            FarmMonster.조류,
            FarmMonster.원숭이와곰,
            FarmMonster.마스터_렐릭,

            FarmMonster.로맨티스트_킹슬라임,
            FarmMonster.쁘띠_팬텀,
            FarmMonster.라즐리,

            FarmMonster.쁘띠_혼테일,
            FarmMonster.반반,
            FarmMonster.군단장_윌
        ]
        self.DopingBuff = DopingListAlchemy
        self.SetSkillList([
            # 공용
            연합의_의지,
            여제의_축복,
            리스트레인트링,
            웨폰퍼프_I링,
            스파이더_인_미러_패스파인더,
            크레스트_오브_더_솔라_패스파인더,
            # 쓸만한 스킬
            쓸만한_컴뱃오더스,
            # 아처
            크리티컬_샷,
            에인션트_보우_액셀레이션,
            카디널_디스차지,
            카디널_블래스트,
            카디널_트랜지션,
            # 스플릿 미스텔
            # 스필릿 미스텔 - 사출
            # 3차
            에인션트_보우_마스터리,
            에인션트_가이던스,
            # 카디널 트랜지션,
            레이븐,
            에디셔널_블래스트,
            에디셔널_디스차지,
            커스_인챈트_블래스트,
            커스_인챈트_디스차지,
            커스_인챈트_트랜지션,
            
            # 4차
            에센스_오브_아처,
            샤프_아이즈,
            에인션트_보우_엑스퍼트,
            일루전_스탭,
            어드밴스드_카디널_포스,
            에디셔널_트랜지션,
            에인션트_아처리,
            트리플_임팩트,
            엣지_오브_레조넌스,
            # 콤보 어설트 (디스차지 강화)
            # 콤보 어설트 활대(블래스트)
            # 콤보 어설트 (트랜지션)
            메이플_용사,
            에픽_어드벤처,
            # 하이퍼
            렐릭_에볼루션,
            카디널_포스_리인포스,
            카디널_포스_보너스_어택,
            카디널_포스_에디셔널_인핸스,
            에인션트_포스_보스킬러,
            에인션트_포스_이그노어_가드,
            
            # 에인션트 아스트라 생략함
            # 5차
            얼티밋_블래스트,
            이볼브,
            가이디드_에로우,
            #레이븐_템페스트,
            이볼브_템페스트,
            렐릭_언바운드,
            옵시디언_배리어,
            크리티컬_리인포스,
            메이플_여신의_축복,
            카디널_디스차지_강화_5th,
            카디널_블래스트_강화_5th,
            에디셔널_블래스트_강화_5th,
            에디셔널_디스차지_강화_5th,
            엣지_오브_레조넌스_강화_5th,
            레이븐_강화_5th,
            트리플_임팩트_강화_5th,
            # 6차 
            카디널_블래스트_6th,
            에디셔널_블래스트_6th,
            포세이큰_렐릭

       ])
        self.LegionList = Union8500_PathFinder