from Core.SpecElements import SpecVector, CoreStat, CreateSpecVector
from enum import Enum

class FarmMonsterEnum(Enum):
    # 힘덱인럭
    소 = CreateSpecVector([CoreStat.STAT_STR], 14)
    솔져 = CreateSpecVector([CoreStat.STAT_STR, CoreStat.STAT_INT], 7)
    개 = CreateSpecVector([CoreStat.STAT_STR, CoreStat.STAT_LUK], 7)

    조류 = CreateSpecVector([CoreStat.STAT_DEX], 14)
    원숭이와곰 = CreateSpecVector([CoreStat.STAT_DEX], 14)
    마스터_렐릭 = CreateSpecVector([CoreStat.STAT_DEX], 15)
    파충류 = CreateSpecVector([CoreStat.STAT_DEX, CoreStat.STAT_INT], 7)
    악마 = CreateSpecVector([CoreStat.STAT_DEX, CoreStat.STAT_LUK], 7)

    아인종 = CreateSpecVector([CoreStat.STAT_INT], 14)
    정령 = CreateSpecVector([CoreStat.STAT_INT, CoreStat.STAT_LUK], 7)
    마스터_마르가나 = CreateSpecVector([CoreStat.STAT_INT], 15)

    마스터_히삽 = CreateSpecVector([CoreStat.STAT_LUK], 15)

    고양이 = CreateSpecVector([CoreStat.STAT_LUK], 14)

    # 올스텟 증가
    오베론 = CreateSpecVector([CoreStat.STAT_ALL], 5)
    파풀라투스의_시계 = CreateSpecVector([CoreStat.STAT_ALL], 5)
    각성한_락_스피릿 = CreateSpecVector([CoreStat.STAT_ALL], 5)
    마스터_잭슨 = CreateSpecVector([CoreStat.STAT_ALL], 5)
    강화형_베릴 = CreateSpecVector([CoreStat.STAT_ALL], 6)
    마스터_레드너그 = CreateSpecVector([CoreStat.STAT_STR], 15)
    성장한_미르 = CreateSpecVector([CoreStat.STAT_ALL], 20)
    쁘띠_라니아 = CreateSpecVector([CoreStat.STAT_ALL], 20) # Assumes all required prerequisites are met.

    # HP 옵션
    돼지 = CreateSpecVector([CoreStat.STAT_HP], 350)
    내면의_분노 = CreateSpecVector([CoreStat.STAT_HP], 500)  # 최대 HP 500 증가
    자이언트_다크소울 = CreateSpecVector([CoreStat.STAT_HP], 500)  # 최대 HP 500 증가
    킹_캐슬_골렘 = CreateSpecVector([CoreStat.STAT_HP], 750)  # 방어력 150, 최대 HP 750 증가 (방어력은 무시)
    작은_운영자_벌룬 = CreateSpecVector([CoreStat.STAT_HP_PERCENTAGE], 2)  # 최대 HP 2% 증가


    # MP 옵션
    요정 = CreateSpecVector([CoreStat.STAT_MP], 350)

    # 데미지류
    검은_바이킹 = CreateSpecVector([CoreStat.STAT_DEX], 5, [CoreStat.DAMAGE_PERCENTAGE], 2) 
    쁘띠_시그너스 = CreateSpecVector([CoreStat.DAMAGE_PERCENTAGE], 3)
    허수아비 = CreateSpecVector([CoreStat.DAMAGE_PERCENTAGE], 4)
    쁘띠_반_레온 = CreateSpecVector([CoreStat.DAMAGE_PERCENTAGE_BOSS], 5)
    쁘띠_매그너스 = CreateSpecVector([CoreStat.IGNORE_GUARD_PERCENTAGE], 5)
    쁘띠_랑 = CreateSpecVector([CoreStat.DAMAGE_PERCENTAGE_BOSS], 8)  # Assuming 쁘띠 은월 condition is handled elsewhere

    # 공마
    티폰 = CreateSpecVector([CoreStat.ATTACK_PHYSICAL, CoreStat.ATTACK_SPELL], 1)
    무공의_분신 = CreateSpecVector([CoreStat.ATTACK_PHYSICAL], 3)
    에피네아 = CreateSpecVector([CoreStat.ATTACK_SPELL], 3)
    미르 = CreateSpecVector([CoreStat.ATTACK_PHYSICAL, CoreStat.ATTACK_SPELL], 5)
    쁘띠_루미너스_어둠 = CreateSpecVector([CoreStat.ATTACK_PHYSICAL, CoreStat.ATTACK_SPELL], 5)
    검은_마법사의_그림자 = CreateSpecVector([CoreStat.ATTACK_PHYSICAL, CoreStat.ATTACK_SPELL], 6)
    쁘띠_루미너스_이퀄리브리엄 = 1 # 20레벨당 공/마1(공마% 받지 않음)

    
    # 크리티컬 확률
    로맨티스트_킹슬라임 = CreateSpecVector([CoreStat.CRITICAL_PERCENTAGE], 3)
    쁘띠_혼테일 = CreateSpecVector([CoreStat.CRITICAL_PERCENTAGE], 3)
    쁘띠_팬텀 = CreateSpecVector([CoreStat.CRITICAL_PERCENTAGE], 4)
    라즐리 = CreateSpecVector([CoreStat.CRITICAL_PERCENTAGE], 5)

    # 크리티컬 데미지
    쁘띠_힐라 = CreateSpecVector([CoreStat.CRITICAL_DAMAGE], 2)

    # 방어율 무시   
    라피스 = CreateSpecVector([CoreStat.IGNORE_GUARD_PERCENTAGE], 5)
    양철_나무꾼 = CreateSpecVector([CoreStat.IGNORE_GUARD_PERCENTAGE], 6)

    # 소환수 지속시간
    사랑에_빠진_커플예티 = 7  # 소환수 지속시간 7% 증가
    빅_펌킨 = 6  # 소환수 지속시간 6% 증가

    # 버프 지속시간
    쁘띠_아카이럼 = 5  # 버프 지속시간 5% 증가
    반반 = 5  # 버프 지속시간 5% 증가
    군단장_윌 = 6  # 버프 지속시간 6% 증가

    # 재사용 대기시간
    큰_운영자의_벌룬 = 2  # 2% 확률로 스킬 재사용 대기시간 미적용
    쁘띠_은월 = 4  # 4% 확률로 스킬 재사용 대기시간 미적용

    # 파이널어택류 데미지 증가
    피에르 = 15  # 파이널 어택류의 데미지 15% 증가

