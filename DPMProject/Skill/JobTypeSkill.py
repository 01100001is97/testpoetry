from Core.ABCSkill import Skill, SkillAdvance
from Attributes import JobTypeAttribute
from Core.Job import JobType

class WorriorSkill(Skill, JobTypeAttribute):
    """
    전사 직업 유형의 스킬을 나타내는 클래스입니다.

    Args:
        icon: 스킬 아이콘을 나타내는 객체.
        advanced: 스킬의 향상 단계를 나타내는 SkillAdvance 객체.
    """
    def __init__(self, icon: any, advanced: SkillAdvance):
        Skill.__init__(self, icon=icon, advanced=advanced)
        JobTypeAttribute.__init__(self, job_type=JobType.Worrior)

class BowmanSkill(Skill, JobTypeAttribute):
    """
    궁수 직업 유형의 스킬을 나타내는 클래스입니다.

    Args:
        icon: 스킬 아이콘을 나타내는 객체.
        advanced: 스킬의 향상 단계를 나타내는 SkillAdvance 객체.
    """
    def __init__(self, icon: any, advanced: SkillAdvance):
        Skill.__init__(self, icon=icon, advanced=advanced)
        JobTypeAttribute.__init__(self, job_type=JobType.Bowman)

class MagicianSkill(Skill, JobTypeAttribute):
    """
    마법사 직업 유형의 스킬을 나타내는 클래스입니다.

    Args:
        icon: 스킬 아이콘을 나타내는 객체.
        advanced: 스킬의 향상 단계를 나타내는 SkillAdvance 객체.
    """
    
    def __init__(self, icon: any, advanced: SkillAdvance):
        Skill.__init__(self, icon=icon, advanced=advanced)
        JobTypeAttribute.__init__(self, job_type=JobType.Magician)

class TheifSkill(Skill, JobTypeAttribute):
    """
    도적 직업 유형의 스킬을 나타내는 클래스입니다.

    Args:
        icon: 스킬 아이콘을 나타내는 객체.
        advanced: 스킬의 향상 단계를 나타내는 SkillAdvance 객체.
    """
    def __init__(self, icon: any, advanced: SkillAdvance):
        Skill.__init__(self, icon=icon, advanced=advanced)
        JobTypeAttribute.__init__(self, job_type=JobType.Theif)

class PirateSkill(Skill, JobTypeAttribute):
    """
    해적 직업 유형의 스킬을 나타내는 클래스입니다.

    Args:
        icon: 스킬 아이콘을 나타내는 객체.
        advanced: 스킬의 향상 단계를 나타내는 SkillAdvance 객체.
    """
    def __init__(self, icon: any, advanced: SkillAdvance):
        Skill.__init__(self, icon=icon, advanced=advanced)
        JobTypeAttribute.__init__(self, job_type=JobType.Pirate)



