# 전투 시작
label battle_start:
    # 적 생성(샘플)
    $ enemy = Actor("홍가룡", hp=80, qi=50, atk=14, df=6, eva=8, faction="evil")

    # 플레이어 공격력에 숙련 반영
    $ me.atk = base_atk + (sword_mastery*2)

    # 전투 UI 호출
    call screen battle_ui

    if me.alive():
        "승리! 명성 +3"
        $ fame += 3
    else:
        "패배… 며칠 요양이 필요하다."
        $ injured_days = 3
    return

# 전투 UI
screen battle_ui():
    default turn = "player"
    default log = ["전투 시작!"]

    frame:
        xalign 0.5
        has vbox

        # 상태창
        text "적: [enemy.name]  HP [enemy.hp]  Qi [enemy.qi]"
        text "나: [me.name]     HP [me.hp]     Qi [me.qi]"

        # 로그
        viewport:
            draggable True
            vbox:
                for line in log:
                    text line

        # 행동 영역
        if turn == "player":
            hbox:
                for s in me.skills:
                    $ usable = (s.cd_left==0 and me.qi >= s.cost_qi)
                    textbutton s.name action Function(_use_skill, s, log) sensitive usable
        else:
            text "적의 차례..."
            timer 1.0 action Function(_enemy_act, log)

init python:
    # 데미지 계산
    def _calc_damage(attacker, defender, skill):
        base = attacker.atk + skill.power - defender.df
        base = max(1, base)
        import random
        # 회피 판정
        if random.random() < defender.eva*0.01:
            return 0, True
        return base, False

    # 플레이어 스킬 사용
    def _use_skill(skill, log):
        if skill.cd_left>0 or store.me.qi < skill.cost_qi or not store.enemy.alive():
            return
        dmg, evaded = _calc_damage(store.me, store.enemy, skill)
        store.me.qi -= skill.cost_qi
        skill.cd_left = skill.cooldown

        if evaded:
            log.append("상대가 경공으로 회피했다!")
        else:
            store.enemy.hp -= dmg
            log.append("「%s」 명중! %d 피해"%(skill.name, dmg))

        # 쿨타임 틱
        for s in store.me.skills:
            if s.cd_left>0: s.cd_left -= 1

        # 적 생존 여부에 따라 턴 전환/전투 종료
        if store.enemy.alive():
            store.turn = "enemy"
        else:
            renpy.end_interaction()

    # 적 AI
    def _enemy_act(log):
        if not store.me.alive() or not store.enemy.alive():
            renpy.end_interaction(); return
        basic = Skill("atk","난격","fist", power=10)
        dmg, evaded = _calc_damage(store.enemy, store.me, basic)
        if evaded:
            log.append("네가 경공으로 회피했다!")
        else:
            store.me.hp -= dmg
            log.append("적의 공격! %d 피해"%dmg)
        store.turn = "player"
