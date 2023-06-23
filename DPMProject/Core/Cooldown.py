from datetime import timedelta

class Cooldown:
    """
    쿨다운 시간을 관리하는 클래스입니다.

    쿨다운 시간은 timedelta 객체를 사용하여 관리되며, 
    객체 생성 시 쿨다운 시간, 초, 분, 밀리초 중 하나를 전달하여 설정할 수 있습니다.

    Attributes:
        cooldown: 쿨다운 시간을 나타내는 timedelta 객체.
    """
    cooldown: timedelta

    def __init__(self, **kwargs):
        """
        Cooldown 클래스의 인스턴스를 초기화합니다.

        Args:
            kwargs: 가변 키워드 인자.
                'cooldown': timedelta 객체.
                'seconds': 초를 나타내는 정수.
                'minutes': 분을 나타내는 정수.
                'milliseconds': 밀리초를 나타내는 정수.
        """
        if "cooldown" in kwargs:
            cooldown = kwargs["cooldown"]
            if not isinstance(cooldown, timedelta):
                raise TypeError("cooldown must be a timedelta instance")
            self.cooldown = cooldown
        elif "seconds" in kwargs:
            seconds = kwargs["seconds"]
            self.cooldown = timedelta(seconds=seconds)
        elif "minutes" in kwargs:
            min = kwargs["minutes"]
            self.cooldown = timedelta(minutes=min)
        elif "milliseconds" in kwargs:
            milliseconds = kwargs["milliseconds"]
            self.cooldown = timedelta(milliseconds=milliseconds) 
        else:
            raise ValueError("either 'cooldown' or 'seconds' argument must be provided")
    
    def __sub__(self, other):
        """
        두 쿨다운 시간의 차이를 반환합니다.

        Args:
            other: Cooldown 객체 또는 timedelta 객체.

        Returns:
            쿨다운 시간의 차이를 나타내는 timedelta 객체.

        Raises:
            TypeError: other가 Cooldown 객체나 timedelta 객체가 아닐 경우.
        """
        if isinstance(other, timedelta):
            return self.cooldown - other
        elif isinstance(other, Cooldown):
            return self.cooldown - other.cooldown
        else:
            raise TypeError("unsupported operand type(s) for -: 'SkillCooldown' and '{}'".format(type(other)))
    
    def __isub__(self, other):
        """
        현재 객체의 쿨다운 시간에서 다른 쿨다운 시간을 뺍니다.

        Args:
            other: Cooldown 객체 또는 timedelta 객체.

        Returns:
            쿨다운이 업데이트된 자신의 객체.

        Raises:
            TypeError: other가 Cooldown 객체나 timedelta 객체가 아닐 경우.
        """
        if isinstance(other, timedelta):
            self.cooldown -= other
        elif isinstance(other, Cooldown):
            self.cooldown -= other.cooldown
        else:
            raise TypeError("unsupported operand type(s) for -=: 'SkillCooldown' and '{}'".format(type(other)))
        return self
    
    def __add__(self, other):
        if isinstance(other, timedelta):
            return Cooldown(cooldown=self.cooldown + other)
        elif isinstance(other, Cooldown):
            return Cooldown(cooldown=self.cooldown + other.cooldown)
        else:
            raise TypeError(f"unsupported operand type(s) for +: 'Cooldown' and '{type(other)}'")

    def __iadd__(self, other):
        if isinstance(other, timedelta):
            self.cooldown += other
        elif isinstance(other, Cooldown):
            self.cooldown += other.cooldown
        else:
            raise TypeError(f"unsupported operand type(s) for +=: 'Cooldown' and '{type(other)}'")
        return self

    def update(self):
        """
        현재 쿨다운 시간에서 10마이크로초를 뺍니다.
        """
        self.cooldown -= timedelta(milliseconds=10)
    
    def __repr__(self):
        """
        현재 쿨다운 시간을 문자열 형태로 반환합니다.

        Returns:
            쿨다운 시간을 나타내는 문자열.
        """
        return "SkillCooldown({})".format(self.cooldown)

  
    def __lt__(self, other):
        """
        현재 객체의 쿨다운 시간이 other의 쿨다운 시간보다 작은지 확인합니다.

        Args:
            other: Cooldown 객체.

        Returns:
            쿨다운 시간이 작으면 True, 그렇지 않으면 False.
        """
        if isinstance(other, Cooldown):
            return self.cooldown < other.cooldown
        elif isinstance(other, timedelta):
            return self.cooldown < other
        else:
            raise TypeError("unsupported operand type(s) for <: 'Cooldown' and '{}'".format(type(other)))

    def __le__(self, other):
        """
        현재 객체의 쿨다운 시간이 other의 쿨다운 시간보다 작거나 같은지 확인합니다.

        Args:
            other: Cooldown 객체.

        Returns:
            쿨다운 시간이 작거나 같으면 True, 그렇지 않으면 False.
        """
        if isinstance(other, Cooldown):
            return self.cooldown <= other.cooldown
        elif isinstance(other, timedelta):
            return self.cooldown <= other
        else:
            raise TypeError("unsupported operand type(s) for <=: 'Cooldown' and '{}'".format(type(other)))

    def __gt__(self, other):
        """
        현재 객체의 쿨다운 시간이 other의 쿨다운 시간보다 큰지 확인합니다.

        Args:
            other: Cooldown 객체.

        Returns:
            쿨다운 시간이 크면 True, 그렇지 않으면 False.
        """
        if isinstance(other, Cooldown):
            return self.cooldown > other.cooldown
        elif isinstance(other, timedelta):
            return self.cooldown > other
        else:
            raise TypeError("unsupported operand type(s) for >: 'Cooldown' and '{}'".format(type(other)))

    def __ge__(self, other):
        """
        현재 객체의 쿨다운 시간이 other의 쿨다운 시간보다 크거나 같은지 확인합니다.

        Args:
            other: Cooldown 객체.

        Returns:
            쿨다운 시간이 크거나 같으면 True, 그렇지 않으면 False.
        """
        if isinstance(other, Cooldown):
            return self.cooldown >= other.cooldown
        elif isinstance(other, timedelta):
            return self.cooldown >> other
        else:
            raise TypeError("unsupported operand type(s) for >=: 'Cooldown' and '{}'".format(type(other)))

    def __eq__(self, other):
        if isinstance(other, timedelta):
            return self.cooldown == other
        elif isinstance(other, Cooldown):
            return self.cooldown == other.cooldown
        else:
            raise TypeError(f"unsupported operand type(s) for ==: 'Cooldown' and '{type(other)}'")
