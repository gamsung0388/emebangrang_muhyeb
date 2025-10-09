# =========================================================
# 10_relationship.rpy
# ---------------------------------------------------------
# ▣ 인물 인덱스 생성/보장 + 관계 목록 화면
#   - MurimChar 클래스: 호감/적대/관계 타입
#   - 데이터셋(notable) → 캐릭 인덱스 빌드
#   - Screen: relationship_screen (리스트/상세)
# ---------------------------------------------------------
# ⚙️ 포인트
# - ensure_murim_index() 로드 보장
# - 화면 텍스트는 문자열 결합으로만!
# =========================================================

init python:
    import renpy.store as store

    # --------------------------
    # ▣ 캐릭터 클래스
    # --------------------------
    class MurimChar(object):
        def __init__(self, cid, name, faction_code, group_code, role="인물"):
            self.id = cid
            self.name = name
            self.faction = faction_code   # 세력 코드 (예: 'shaolin')
            self.group = group_code       # 그룹 코드 (예: 'orthodox')
            self.role = role

            # 수치(−100~100, 0~100)
            self.affinity = 0
            self.hostility = 0

            # 관계 딕셔너리 (키는 자유롭게 확장 가능)
            self.relations = {
                "사제": [], "원수": [], "라이벌": [], "연인": [],
                "자식": [], "스승": [], "동맹": [], "제자": []
            }

        def change_affinity(self, d):
            self.affinity = max(-100, min(100, self.affinity + d))

        def change_hostility(self, d):
            self.hostility = max(0, min(100, self.hostility + d))

    # --------------------------
    # ▣ 인덱스 컨테이너/플래그
    # --------------------------
    if not hasattr(store, "murim_chars"): store.murim_chars = {}
    if not hasattr(store, "murim_chars_by_id"): store.murim_chars_by_id = {}
    if not hasattr(store, "MURIM_INDEX_BUILT"): store.MURIM_INDEX_BUILT = False

    # ---------------------------------------------
    # ▣ 데이터셋 → 캐릭 인덱스 빌더
    # ---------------------------------------------
    def build_character_index_from_dataset():
        if not getattr(store, "MURIM_DATA_READY", False):
            return False

        store.murim_chars.clear()
        store.murim_chars_by_id.clear()

        # 모든 그룹/세력을 순회하면서 notable 인물 등록
        for gcode, factions in store.murim_factions.items():
            for fcode, data in factions.items():
                for p in data.get("notable", []):
                    cid = p["id"]
                    mc = MurimChar(cid, p["name"], fcode, gcode, p.get("role", "인물"))

                    # 관계 등록
                    for rtype, idlist in p.get("relation_ids", {}).items():
                        mc.relations.setdefault(rtype, [])
                        mc.relations[rtype].extend(idlist)

                    store.murim_chars[cid] = mc
                    store.murim_chars_by_id[cid] = mc

        store.MURIM_INDEX_BUILT = True
        return True

    # ---------------------------------------------
    # ▣ 인덱스 보장 함수 (화면 진입 시 호출)
    # ---------------------------------------------
    def ensure_murim_index():
        if getattr(store, "MURIM_DATA_READY", False) and not store.MURIM_INDEX_BUILT:
            build_character_index_from_dataset()

    # ---------------------------------------------
    # ▣ 유틸
    # ---------------------------------------------
    def mc_list_by_faction(fcode):
        return [c for c in store.murim_chars.values() if c.faction == fcode]

    def mc_change_affinity_by_id(cid, d):
        c = store.murim_chars_by_id.get(cid)
        if c:
            c.change_affinity(d)

    def mc_change_hostility_by_id(cid, d):
        c = store.murim_chars_by_id.get(cid)
        if c:
            c.change_hostility(d)

screen relationship_screen(preselect_faction=None):
    tag menu
    style_prefix "murim"   # ⬅️ 추가: 이 화면 전역에서 substitute=False 적용
    $ ensure_murim_index()
    
    default _selected_faction = preselect_faction
    default _selected_char = None

    frame:
        background Solid("#000b")
        xalign 0.02 yalign 0.05
        xmaximum 520 ymaximum 0.9

        vbox:
            spacing 10
            text "인물 관계/호감도" size 30 color "#fff" substitute False
            text "세력 선택" color "#ccc" substitute False

            viewport:
                draggable True mousewheel True
                xmaximum 500 ymaximum 240
                vbox:
                    spacing 6
                    for gcode, factions in store.murim_factions.items():
                        text (store.murim_groups[gcode]) color "#8ad" substitute False
                        for fcode in sorted(factions.keys()):
                            $ fdisp = factions[fcode]["display"]
                            textbutton Text(fdisp, substitute=False) action SetScreenVariable("_selected_faction", fcode)

            if _selected_faction:
                null height 10
                $ fdisp = None
                for gc, fs in store.murim_factions.items():
                    if _selected_faction in fs:
                        $ fdisp = fs[_selected_faction]["display"]
                        break
                text ("세력: " + (fdisp or _selected_faction)) size 22 color "#eee" substitute False

                viewport:
                    draggable True mousewheel True
                    xmaximum 500 ymaximum 300
                    vbox:
                        spacing 4
                        $ lst = mc_list_by_faction(_selected_faction)
                        if not lst:
                            text "등록된 인물이 없습니다." color "#ddd" substitute False
                        else:
                            for ch in lst:
                                textbutton Text("• " + ch.name + "  (" + ch.role + ")", substitute=False) \
                                    action SetScreenVariable("_selected_char", ch.id)

    frame:
        background Solid("#111c")
        xalign 0.98 yalign 0.05
        xmaximum 720 ymaximum 0.9

        vbox:
            spacing 10
            text "상세 정보" size 30 color "#fff" substitute False

            if _selected_char is None:
                text "왼쪽에서 인물을 선택하세요." color "#ddd" substitute False
            else:
                $ c = store.murim_chars_by_id[_selected_char]
                text (c.name + "  —  " + c.role) size 24 color "#fff" substitute False

                $ gname = store.murim_groups.get(c.group, c.group)
                $ fname = store.murim_factions[c.group][c.faction]["display"]
                text ("소속: " + gname + " / " + fname) color "#ccc" substitute False

                frame:
                    background Solid("#0006")
                    xfill True
                    vbox:
                        spacing 8
                        text "호감도 / 적대도" color "#ddd" substitute False
                        bar value AnimatedValue(c.affinity + 100, 200, 0.4) xmaximum 600
                        text ("호감도: " + str(c.affinity)) color "#8f8" substitute False
                        bar value AnimatedValue(c.hostility, 100, 0.4) xmaximum 600
                        text ("적대도: " + str(c.hostility)) color "#f88" substitute False

                        hbox:
                            spacing 8
                            # 조작 버튼들
                            textbutton Text("호감 +5", substitute=False) action Function(mc_change_affinity_by_id, c.id, +5)
                            textbutton Text("호감 -5", substitute=False) action Function(mc_change_affinity_by_id, c.id, -5)
                            textbutton Text("적대 +5", substitute=False) action Function(mc_change_hostility_by_id, c.id, +5)
                            textbutton Text("적대 -5", substitute=False) action Function(mc_change_hostility_by_id, c.id, -5)
                null height 10
                text "관계" color "#ddd" substitute False

                viewport:
                    draggable True mousewheel True
                    xmaximum 680 ymaximum 260
                    vbox:
                        for rtype, ids in c.relations.items():
                            if ids:
                                text rtype color "#9cf" substitute False
                                for tid in ids:
                                    $ t = store.murim_chars_by_id.get(tid)
                                    if t:
                                        text ("  ↳ " + t.name + "  (" + t.role + ")") color "#ddd" substitute False

    # 닫기 버튼
    textbutton Text("닫기", substitute=False) action Return() xalign 0.98 yalign 0.02
