default fame = 0
default faction = "neutral"
default day_time = 0
default stamina = 5

# self.name=name   # 이름
# self.hp=hp       # 체력
# self.qi=qi       # 내공
# self.atk=atk     # 공격력
# self.df=df       # 방어력
# self.eva=eva     # 회피율
# self.faction=faction  # 소속 세력 (정파/사파/중립 등)
# self.factionDet=faction  # 소속 세력 ()
# self.skills=[]   # 보유 무공 리스트
# self.buffs=[]    # 현재 적용된 버프/디버프

# 플레이어 샘플
default me = Actor("주인공", hp=100, qi=50, atk=50, df=50, eva=50, faction="neutral")
# 별하랑 - 사천당가 
default byuel = Actor("별하랑", hp=100, qi=60, atk=12, df=5, eva=10, faction="neutral")
# 바또랑 - 하북팽가
default baddo = Actor("바또랑", hp=100, qi=60, atk=12, df=5, eva=10, faction="neutral")
# 홍호돋 - 남궁 막내 - 제왕검법
default hong = Actor("홍호돋", hp=100, qi=60, atk=12, df=5, eva=10, faction="neutral")
# 문이유 - 무당파 - 나비검법
default moon = Actor("문이유", hp=100, qi=60, atk=12, df=5, eva=10, faction="neutral")
# 밤새나 - 금전을 준다 안준다 이벤트로 주면 하오문/ 안주면 개방으로 세력이동
default bam = Actor("밤새나", hp=100, qi=60, atk=12, df=5, eva=10, faction="neutral")


# 간단한 숙련/능력치 파생
default base_atk = 10
default sword_mastery = 0
default money = 20
default injured_days = 0

init -10 python:

    import renpy.store as store
    
    store.me = Actor("주인공", hp=100, qi=60, atk=12, df=5, eva=10, faction="neutral")

    # 지역별 이벤트 풀
    EVENT_POOLS = {
        "무림맹": ["summon_meeting","spar_training","merchant"],
        "취화루": ["thugs_trouble","spy_contact","rest"]
    }

    # 시작 무공 예시(원하면 data/skills.json 로 대체 가능)
    starter_skills = [
        Skill("s_slash","일섬","sword", power=8, cost_qi=5, cooldown=1),
        Skill("s_thrust","찌르기","sword", power=10, cost_qi=6, cooldown=2),
        Skill("i_breath","운기조식","inner", power=0, cost_qi=0, cooldown=2, tags=["recover"]),
        Skill("l_step","경공보","lightness", power=0, cost_qi=4, cooldown=3, tags=["evasion"])
    ]
    
    store.me.skills = starter_skills[:]
