# 취화루 이벤트: 깡패 소동
label ev_thugs_trouble:
    "취화루 골목에서 깡패들이 행패를 부린다."
    menu:
        "싸운다 (전투 진입)":
            jump battle_start
        "은전으로 무마한다 (명성 -2, 은화 -5)":
            $ fame -= 2
            $ money -= 5
            return

# 예: 수련 이벤트
label ev_spar_training:
    "도장에서 검법을 연마한다."
    $ day_time += 1
    $ sword_mastery += 1
    "검법 숙련이 올랐다."
    return

# 예: 휴식/회복
label ev_rest:
    "취화루에서 며칠 묵었다."
    $ stamina = min(stamina+2, 5)
    $ me.qi = min(me.qi+8, 60)
    "기력을 되찾는다."
    return
