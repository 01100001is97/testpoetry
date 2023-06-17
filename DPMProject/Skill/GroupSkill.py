from Core.ABCSkill import Skill, SkillAdvance
from Skill.Attributes import JobGroupAttribute
from Core.Job import JobGroup

# 모험가 직업군
class AdventurerSkill(Skill, JobGroupAttribute):
    """
    모험가 직업군의 스킬을 나타내는 클래스입니다.

    Args:
        icon: 스킬 아이콘을 나타내는 객체.
        advanced: 스킬의 향상 단계를 나타내는 SkillAdvance 객체.
    """
    def __init__(self, icon: any, advanced: SkillAdvance):
        Skill.__init__(self, advanced=advanced)
        JobGroupAttribute.__init__(self, job_group=JobGroup.Adventurer)

# 시그너스 기사단 직업군
class CygnusKnightsSkill(Skill, JobGroupAttribute):
    """
    시그너스 기사단 직업군의 스킬을 나타내는 클래스입니다.

    Args:
        icon: 스킬 아이콘을 나타내는 객체.
        advanced: 스킬의 향상 단계를 나타내는 SkillAdvance 객체.
    """
    def __init__(self, icon: any, advanced: SkillAdvance):
        Skill.__init__(self, advanced=advanced)
        JobGroupAttribute.__init__(self, job_group=JobGroup.CygnusKnights)

# 레지스탕스 직업군
class ResistanceSkill(Skill, JobGroupAttribute):
    """
    레지스탕스 직업군의 스킬을 나타내는 클래스입니다.

    Args:
        icon: 스킬 아이콘을 나타내는 객체.
        advanced: 스킬의 향상 단계를 나타내는 SkillAdvance 객체.
    """
    def __init__(self, icon: any, advanced: SkillAdvance):
        Skill.__init__(self, advanced=advanced)
        JobGroupAttribute.__init__(self, job_group=JobGroup.Resistance)

# 데몬 직업군
class DemonSkill(Skill, JobGroupAttribute):
    """
    데몬 직업군의 스킬을 나타내는 클래스입니다.

    Args:
        icon: 스킬 아이콘을 나타내는 객체.
        advanced: 스킬의 향상 단계를 나타내는 SkillAdvance 객체.
    """
    def __init__(self, icon: any, advanced: SkillAdvance):
        Skill.__init__(self, advanced=advanced)
        JobGroupAttribute.__init__(self, job_group=JobGroup.Demon)

# 영웅 직업군
class HerosSkill(Skill, JobGroupAttribute):
    """
    영웅 직업군의 스킬을 나타내는 클래스입니다.

    Args:
        icon: 스킬 아이콘을 나타내는 객체.
        advanced: 스킬의 향상 단계를 나타내는 SkillAdvance 객체.
    """
    def __init__(self, icon: any, advanced: SkillAdvance):
        Skill.__init__(self, advanced=advanced)
        JobGroupAttribute.__init__(self, job_group=JobGroup.Heros)

# 노바 직업군
class NovaSkill(Skill, JobGroupAttribute):
    """
    노바 직업군의 스킬을 나타내는 클래스입니다.

    Args:
        icon: 스킬 아이콘을 나타내는 객체.
        advanced: 스킬의 향상 단계를 나타내는 SkillAdvance 객체.
    """
    def __init__(self, icon: any, advanced: SkillAdvance):
        Skill.__init__(self, advanced=advanced)
        JobGroupAttribute.__init__(self, job_group=JobGroup.Nova)

# 레프 직업군
class FloraSkill(Skill, JobGroupAttribute):
    """
    레프 직업군의 스킬을 나타내는 클래스입니다.

    Args:
        icon: 스킬 아이콘을 나타내는 객체.
        advanced: 스킬의 향상 단계를 나타내는 SkillAdvance 객체.
    """
    def __init__(self, icon: any, advanced: SkillAdvance):
        Skill.__init__(self, advanced=advanced)
        JobGroupAttribute.__init__(self, job_group=JobGroup.Flora)

# 아니마 직업군
class AnimaSkill(Skill, JobGroupAttribute):
    """
    아니마 직업군의 스킬을 나타내는 클래스입니다.

    Args:
        icon: 스킬 아이콘을 나타내는 객체.
        advanced: 스킬의 향상 단계를 나타내는 SkillAdvance 객체.
    """
    def __init__(self, icon: any, advanced: SkillAdvance):
        Skill.__init__(self, advanced=advanced)
        JobGroupAttribute.__init__(self, job_group=JobGroup.Anima)

# 초월자 직업군
class OverlordSkill(Skill, JobGroupAttribute):
    """
    초월자 직업군의 스킬을 나타내는 클래스입니다.

    Args:
        icon: 스킬 아이콘을 나타내는 객체.
        advanced: 스킬의 향상 단계를 나타내는 SkillAdvance 객체.
    """
    def __init__(self, icon: any, advanced: SkillAdvance):
        Skill.__init__(self, advanced=advanced)
        JobGroupAttribute.__init__(self, job_group=JobGroup.Overlord)

# 프렌즈 직업군
class FriendsSkill(Skill, JobGroupAttribute):
    """
    프렌즈 직업군의 스킬을 나타내는 클래스입니다.

    Args:
        icon: 스킬 아이콘을 나타내는 객체.
        advanced: 스킬의 향상 단계를 나타내는 SkillAdvance 객체.
    """
    def __init__(self, icon: any, advanced: SkillAdvance):
        Skill.__init__(self, advanced=advanced)
        JobGroupAttribute.__init__(self, job_group=JobGroup.Friends)
