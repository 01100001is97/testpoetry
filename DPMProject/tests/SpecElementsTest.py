from Core.SpecElements import CoreStat, SpecVector


# 인스턴스 할당
TestSpecVector1 = SpecVector()
TestSpecVector2 = SpecVector()

# 초기화 테스트
#print(TestSpecVector1)

# 스텟 변경
TestSpecVector1[CoreStat.ATTACK_PHYSICAL] = 10
TestSpecVector1[CoreStat.STAT_DEX] = 15

# 연산자 오버로딩 테스트
TestSpecVector1[CoreStat.IGNORE_GUARD_PERCENTAGE] = 10
TestSpecVector1[CoreStat.FINAL_DAMAGE_PERCENT] = 10

TestSpecVector2[CoreStat.IGNORE_GUARD_PERCENTAGE] = 20
TestSpecVector2[CoreStat.FINAL_DAMAGE_PERCENT] = 10.0

TestSpecVector3 = TestSpecVector1 + TestSpecVector2
#print(TestSpecVector3[CoreStat.IGNORE_GUARD_PERCENTAGE])
#print(TestSpecVector3)
#TestSpecVector3.Show()

# Stat 유효성 검사
#print(TestSpecVector1.IsValidStat(CoreStat.IGNORE_GUARD_PERCENTAGE, 1000))
#print(TestSpecVector1.IsValidStat(CoreStat.IGNORE_GUARD_PERCENTAGE, 10))
#print(TestSpecVector1.IsValidStat(CoreStat.ATTACK_PHYSICAL, 1000))

# 인자 범위 테스트
TestSpecVector4 = SpecVector()
#TestSpecVector4["anything"] = 15
#TestSpecVector4[CoreStat.ATTACK_PHYSICAL_FIXED] = -1
#TestSpecVector4[CoreStat.IGNORE_ELEMENTAL_RESISTANCE] = 110
#TestSpecVector4[CoreStat.IGNORE_GUARD_PERCENTAGE] =  110