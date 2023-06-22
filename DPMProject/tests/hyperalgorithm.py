from Core.Damage import BattlePower
from Core.SpecElements import SpecVector
from Core.Job import JobType
import math


from sympy import symbols, lambdify
def deff():
    # 심볼 생성
    
    atk, mainstat, mainstat_per, mainstat_fixed, substat, substat_fixed, damage_total, ignore_now, ignore_add = symbols('a b c d e f g h i')
    # 식 정의
    y = atk*(4*(mainstat*(1+0.01*mainstat_per) +mainstat_fixed)+substat*(1+0.01*substat_fixed))*(1+0.01*damage_total)*(100-3*(100-ignore_now)*(100-ignore_add)/10000)/100

    # 각 변수에 대한 편미분
    diff_atk = y.diff(atk)
    diff_mainstat = y.diff(mainstat)
    diff_mainstat_fixed = y.diff(mainstat_fixed)
    diff_damage = y.diff(damage_total)
    diff_ignore = y.diff(ignore_add)

    # 각 편미분 결과를 함수로 변환
    f_atk = lambdify((atk, mainstat, mainstat_per, mainstat_fixed, substat, substat_fixed, damage_total, ignore_now, ignore_add), diff_atk, "numpy")
    f_mainstat = lambdify((atk, mainstat, mainstat_per, mainstat_fixed, substat, substat_fixed, damage_total, ignore_now, ignore_add), diff_mainstat, "numpy")
    f_mainstat_fixed = lambdify((atk, mainstat, mainstat_per, mainstat_fixed, substat, substat_fixed, damage_total, ignore_now, ignore_add), diff_mainstat_fixed, "numpy")
    f_g = lambdify((atk, mainstat, mainstat_per, mainstat_fixed, substat, substat_fixed, damage_total, ignore_now, ignore_add), diff_damage, "numpy")
    f_i = lambdify((atk, mainstat, mainstat_per, mainstat_fixed, substat, substat_fixed, damage_total, ignore_now, ignore_add), diff_ignore, "numpy")

    # 예시: a = 1, b = 2, c = 3, d = 4, e = 5, f = 6, g = 7, h = 8, i = 9를 대입한 경우
    print(f"하이퍼 공격력:{f_atk(2328, 4651, 324, 18760, 1958, 75, 67, 95.61, 1)*3}")  # a에 대한 편미분 결과 출력
    print(f"주스텟:{f_mainstat(2328, 4651, 324, 18760, 1958, 75, 67, 95.61, 1)}")  # a에 대한 편미분 결과 출력
    print(f"하이퍼 주스텟:{f_mainstat_fixed(2328, 4651, 324, 18760, 1958, 75, 67, 95.61, 1)*30}")
    print(f"하이퍼 데미지:{f_g(2328, 4651, 324, 18760, 1958, 75, 67, 95.61, 1)*3}")  # a에 대한 편미분 결과 출력
    print(f"하이퍼 방무:{f_i(2328, 4651, 324, 18760, 1958, 75, 67, 95.61, 1)*3}") # a에 대한 편미분 결과 출력

    

    

from scipy.special import comb

def weapon_algo1():
    count = 0
    
    for i in [0,3,4,6,7,8]:
        for j in [0,3,4,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21]:
            if 30 -i -j in [0,3,4,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21]:
                print(i, j, 30-i-j)
                count += 1
                print(f"count = {count}")


def weapon_algo2():
    count = 0

    
    atklist = []
    for j in range(0, 4):
        atklist += [e*9 + 3*j for e in range(j, 10-1*j)]
    atklist = list(set(atklist))
    
    for atk in atklist:
        left = 10*(90 - atk)/3
        for ignore in [0,3,4,6,7,8]:
            ignore *= 10
            boss = left - ignore
            boss = int(boss)

            if boss >= 0 and ignore >= 0 and not 0 < boss < 30 and not 0 < ignore < 30:
                print(f"{atk}, {ignore}, {boss}")







STAT_STR:                      1006
STAT_DEX:                      1011
STAT_INT:                      4672
STAT_LUK:                      2191
STAT_ALL:                      0
STAT_STR_FIXED:                40
STAT_DEX_FIXED:                40
STAT_INT_FIXED:                18860
STAT_LUK_FIXED:                440
STAT_ALL_FIXED:                0
STAT_STR_PERCENTAGE:           75
STAT_DEX_PERCENTAGE:           75
STAT_INT_PERCENTAGE:           392
STAT_LUK_PERCENTAGE:           75
STAT_ALL_PERCENTAGE:           0
STAT_STR_9LEVEL:               0
STAT_DEX_9LEVEL:               0
STAT_INT_9LEVEL:               0
STAT_LUK_9LEVEL:               0
ATTACK_PHYSICAL:               1012
ATTACK_SPELL:                  2240
ATTACK_PHYSICAL_FIXED:         13
ATTACK_SPELL_FIXED:            13
ATTACK_PHYSICAL_PERCENTAGE:    4
ATTACK_SPELL_PERCENTAGE:       97
DAMAGE_PERCENTAGE:             131.2
DAMAGE_PERCENTAGE_BOSS:        289
CRITICAL_PERCENTAGE:           100
CRITICAL_DAMAGE:               70
IGNORE_GUARD_PERCENTAGE:       88.64483115809576
IGNORE_ELEMENTAL_RESISTANCE:   20
FINAL_DAMAGE_PERCENT:          40.0
STAT_HP:                       21735
STAT_HP_PERCENTAGE:            35
STAT_HP_FIXED:                 0
STAT_MP:                       9175
STAT_MP_PERCENTAGE:            50