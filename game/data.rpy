default fame = 0
default faction = "neutral"
default day_time = 0
default stamina = 5

# 플레이어 샘플
default me = Actor("주인공", hp=100, qi=60, atk=12, df=5, eva=10, faction="neutral")
# 별하랑
default byuel = Actor("별하랑", hp=100, qi=60, atk=12, df=5, eva=10, faction="neutral")
# 바또랑
default baddo = Actor("바또랑", hp=100, qi=60, atk=12, df=5, eva=10, faction="neutral")
# 홍호돋
default hong = Actor("홍호돋", hp=100, qi=60, atk=12, df=5, eva=10, faction="neutral")

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
