# =========================================================
# 01_world_murim.rpy
# ---------------------------------------------------------
# ▣ 무림 세계의 기본 데이터 정의 파일
#   - 그룹(정파/세가/사파/마교)
#   - 각 세력의 메타정보(근거지/특징/무공/보물/이벤트/대표인물)
#   - 지역(월드맵)와 세력 연결
#   - 월드 이벤트 목록
# ---------------------------------------------------------
# ⚙️ 주의
# - 화면(Text) 내 대괄호 보간을 막기 위해 문자열 결합만 사용.
# - 이 파일이 먼저 로드되어야 하므로 init 우선순위 낮춤(-10).
# =========================================================

init -10 python:

    # --------------------------
    # ▣ 그룹 코드 → 표기명
    # --------------------------
    store.murim_groups = {
        "Jung": "정파",
        "clans": "세가",
        "Safa": "사파",
        "demon": "마교",
    }

    # ---------------------------------------------------
    # ▣ 세력 트리 (group → faction → meta)
    #   meta keys:
    #   - display, location, traits[], skills[], treasure[], event, notable[]
    #   - notable[] item:
    #       { id, name, role, relation_ids{rtype: [target_id,…]} }
    # ---------------------------------------------------
    store.murim_factions = {
        # ========== 정파 ==========
        "Jung": {
            "solim": {
                "display": "소림사",
                "location": "하남성 등봉산",
                "traits": ["무림 수장", "자비와 절제", "불살"],
                "skills": ["금강불괴신공", "나한권", "십팔동인수"],
                "treasure": ["금강염주", "대장경심법"],
                "event": "정사대전, 비무대회",
                "notable": [
                    {"id": "hyegong", "name": "혜공 대사", "role": "장문",
                        "relation_ids": {"사제": ["hyemyeong"], "원수": ["cheonma"]}},
                    {"id": "hyemyeong", "name": "혜명", "role": "수좌",
                        "relation_ids": {"사제": ["hyegong"], "연인": ["unran"]}}
                ]
            },
            "mudang": {
                "display": "무당파",
                "location": "호북성 무당산",
                "traits": ["선검", "조화", "유연한 내공"],
                "skills": ["태극검법", "건곤대나이"],
                "treasure": ["태극검", "무당비서"],
                "event": "맹주전, 절세비급출현",
                "notable": [
                    {"id": "zhang_san_feng", "name": "장삼봉", "role": "창시자",
                        "relation_ids": {"사제": ["cheongun"], "원수": ["blood_king"]}},
                    {"id": "cheongun", "name": "청운진인", "role": "장문대사",
                        "relation_ids": {"사제": ["zhang_san_feng"], "라이벌": ["gokun"]}}
                ]
            },
            "hawshan": {
                "display": "화산파",
                "location": "섬서성 화산",
                "traits": ["검법 중심", "협의와 의협심"],
                "skills": ["이십사수매화검법", "풍화류운검"],
                "treasure": ["매화비검"],
                "event": "비무대회, 절세비급출현",
                "notable": [
                    {"id": "yoo_cheongun", "name": "유청운", "role": "장문",
                        "relation_ids": {"라이벌": ["namgung_taeha"]}},
                    {"id": "namgung_pung", "name": "남궁풍", "role": "검수",
                        "relation_ids": {"연인": ["unran"], "원수": ["muryong_hwan"]}}
                ]
            },
            "kongdong": {
                "display": "공동파",
                "location": "감숙성 평량 공동산",
                "traits": ["광성자 전통", "심법 중심"],
                "skills": ["광성심법", "혼원기공"],
                "treasure": ["공명구슬"],
                "event": "맹주전",
                "notable": [
                    {"id": "gongmyeong", "name": "공명도인", "role": "장문",
                        "relation_ids": {"라이벌": ["ma_hon"]}}
                ]
            }
        },

        # ========== 세가 ==========
        "clans": {
            "namgung": {
                "display": "남궁세가",
                "location": "안휘성",
                "traits": ["검가 최고", "명예중시"],
                "skills": ["제왕검형", "패천검류"],
                "treasure": ["남궁검보", "패왕보검"],
                "event": "가주교체전, 세가혼인",
                "notable": [
                    {"id": "namgung_taeha", "name": "남궁태하", "role": "가주",
                        "relation_ids": {"자식": ["namgung_yeon"], "라이벌": ["yoo_cheongun"]}},
                    {"id": "namgung_yeon", "name": "남궁연", "role": "소공자",
                        "relation_ids": {"연인": ["jegal_seol"], "원수": ["muryong_yeon"]}}
                ]
            },
            "sachun": {
                "display": "사천당가",
                "location": "사천성",
                "traits": ["독공과 암기", "폐쇄적"],
                "skills": ["만천화우", "무형지독"],
                "treasure": ["만독단경"],
                "event": "정사대전, 독공유출",
                "notable": [
                    {"id": "dang_mulim", "name": "당무림", "role": "가주",
                        "relation_ids": {"제자": ["dang_okjin"], "원수": ["blood_king"]}},
                    {"id": "dang_okjin", "name": "당옥진", "role": "여독사",
                        "relation_ids": {"연인": ["namgung_yeon"], "스승": ["dang_mulim"]}}
                ]
            },
            "jegal": {
                "display": "제갈세가",
                "location": "섬서성",
                "traits": ["지략과 병법", "기관술"],
                "skills": ["제갈진법", "연환기술"],
                "treasure": ["천기진도", "기계도식"],
                "event": "맹주전, 절세비급출현",
                "notable": [
                    {"id": "jegal_mun", "name": "제갈문", "role": "가주",
                        "relation_ids": {"자식": ["jegal_seol"], "동맹": ["namgung"]}},
                    {"id": "jegal_seol", "name": "제갈설", "role": "기관술사",
                        "relation_ids": {"연인": ["namgung_yeon"], "라이벌": ["muryong_yeon"]}}
                ]
            },
            "muryong": {
                "display": "모용세가",
                "location": "요녕성",
                "traits": ["환영술", "검술/기재"],
                "skills": ["환영검", "분신검류"],
                "treasure": ["거울의 눈"],
                "event": "절세비급출현",
                "notable": [
                    {"id": "muryong_hwan", "name": "모용환", "role": "가주",
                        "relation_ids": {"자식": ["muryong_yeon"], "원수": ["namgung"]}},
                    {"id": "muryong_yeon", "name": "모용연", "role": "검가의 딸",
                        "relation_ids": {"연적": ["jegal_seol"], "원수": ["namgung_yeon"]}}
                ]
            }
        },

        # ========== 사파 ==========
        "Safa": {
            "haomen": {
                "display": "하오문",
                "location": "중원 암부",
                "traits": ["첩보·도둑·암시장"],
                "skills": ["잠행술", "흑풍지음"],
                "treasure": ["하오검", "어둠의비서"],
                "event": "암살극",
                "notable": [
                    {"id": "myoseon", "name": "묘선", "role": "문주",
                        "relation_ids": {"원수": ["cheongun"], "연인": ["blood_blade"]}}
                ]
            },
            "green_forest": {
                "display": "녹림맹",
                "location": "중원 산간",
                "traits": ["의적/도적 혼재"],
                "skills": ["녹림팔문참", "풍림도법"],
                "treasure": ["산군의령패"],
                "event": "사도련결성",
                "notable": [
                    {"id": "red_eye_tiger", "name": "적안호", "role": "맹주",
                        "relation_ids": {"원수": ["namgung"]}}
                ]
            }
        },

        # ========== 마교 ==========
        "demon": {
            "cheonma_sect": {
                "display": "천마신교",
                "location": "십만대산",
                "traits": ["천마 숭배", "절대강자주의"],
                "skills": ["천마신공", "파천마공", "마령진"],
                "treasure": ["마혼옥", "천마비결"],
                "event": "천마출세, 혈겁",
                "notable": [
                    {"id": "cheonma", "name": "천마", "role": "교주",
                        "relation_ids": {"원수": ["hyegong"], "라이벌": ["namgung_taeha"]}},
                    {"id": "ma_hon", "name": "마혼", "role": "좌사",
                        "relation_ids": {"스승": ["cheonma"], "원수": ["gongmyeong"]}},
                    {"id": "ma_wolryeong", "name": "마월령", "role": "마녀",
                        "relation_ids": {"라이벌": ["dang_okjin"], "연인": ["namgung_yeon"]}}
                ]
            },
            "blood_cult": {
                "display": "혈교",
                "location": "서남혈계",
                "traits": ["피의 의식", "인신공양"],
                "skills": ["혈수공", "혈신대법"],
                "treasure": ["혈영주"],
                "event": "혈겁, 정토대전",
                "notable": [
                    {"id": "blood_king", "name": "혈왕", "role": "교주",
                        "relation_ids": {"원수": ["zhang_san_feng", "dang_mulim"]}}
                ]
            }
        }
    }

    # ---------------------------------------------
    # ▣ 지역(월드맵) 코드 → 표기/소속 세력
    # ---------------------------------------------
    store.murim_worldmap = {
        "hebei":   {"display": "하북", "factions": ["namgung", "green_forest"]},
        "henan":   {"display": "하남", "factions": ["solim"]},
        "hubei":   {"display": "호북", "factions": ["mudang"]},
        "sichuan": {"display": "사천", "factions": ["sachun"]},
        "shanxi":  {"display": "섬서", "factions": ["hawshan", "kongdong", "jegal"]},
        "liaoning":{"display": "요녕", "factions": ["muryong"]},
        "ten_thousand_mountains": {"display": "십만대산", "factions": ["cheonma_sect"]},
        "southwest_blood": {"display": "서남혈계", "factions": ["blood_cult"]}
    }

    # ---------------------------------------------
    # ▣ 월드 이벤트 정의(코드/표기)
    # ---------------------------------------------
    store.murim_events = [
        {"code": "war_righteous_evil", "display": "정사대전"},
        {"code": "alliance_leader_duel", "display": "맹주전"},
        {"code": "clan_marriage", "display": "세가혼인"},
        {"code": "clan_succession", "display": "가주교체전"},
        {"code": "blood_ritual", "display": "혈겁"},
        {"code": "cheonma_return", "display": "천마출세"},
        {"code": "legend_book", "display": "절세비급출현"},
        {"code": "biwu", "display": "비무대회"},
        {"code": "assassination", "display": "암살극"},
        {"code": "foreign_invasion", "display": "외적침입"},
    ]

    # 데이터 준비 플래그
    store.MURIM_DATA_READY = True
