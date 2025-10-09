init -20 python:
    # 무공(Skill) 클래스
    class Skill(object):
        def __init__(self, key, name, kind, req_qi=0, power=0, cost_qi=0, cooldown=0, tags=None):
            self.key = key            # 무공 고유 ID
            self.name = name          # 무공 이름
            self.kind = kind          # 무공 종류 (검법, 권법, 내공, 경공 등)
            self.req_qi = req_qi      # 요구 내공치
            self.power = power        # 공격력/효과 수치
            self.cost_qi = cost_qi    # 사용 시 내공 소모
            self.cooldown = cooldown  # 재사용 대기 턴
            self.tags = set(tags or [])  # 태그 (출혈, 기절 같은 특수효과)
            self.cd_left = 0          # 현재 남은 쿨타임 턴

    # 배우(플레이어/적 공용)
    class Actor(object):
        def __init__(self, name, hp, qi, atk, df, eva, faction="neutral"):
            self.name=name   # 이름
            self.hp=hp       # 체력
            self.qi=qi       # 내공
            self.atk=atk     # 공격력
            self.df=df       # 방어력
            self.eva=eva     # 회피율(%)
            self.faction=faction  # 소속 세력 (정파/사파/중립 등)
            self.skills=[]   # 보유 무공 리스트
            self.buffs=[]    # 현재 적용된 버프/디버프
            
        def alive(self): 
            return self.hp>0  # 살아있는지 체크
