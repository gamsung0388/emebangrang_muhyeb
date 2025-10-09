# =========================================================
# world_map.rpy
# ---------------------------------------------------------
# ▣ 지역 → 세력 선택 UI
#   - 좌측: 지역 목록
#   - 우측: 세력 목록 + 세력 상세 + 이동 버튼
# ---------------------------------------------------------
# ⚙️ 이미지
# - gui/worldmap_placeholder.png 있으면 배경으로 사용
# =========================================================

init python:

    # 화면 상태 저장용 (간단한 state dict)
    if not hasattr(store, "wm_state"):
        store.wm_state = {"region": None, "faction": None}

    # 지역 리스트 [(코드, 표기)]
    def wm_regions():
        return [(code, data["display"]) for code, data in store.murim_worldmap.items()]

    # 해당 지역의 세력 코드 배열
    def wm_factions_in(region_code):
        return store.murim_worldmap.get(region_code, {}).get("factions", [])

    # 세력 코드 → 메타 + 편의 필드
    def wm_find_faction_meta(fcode):
        for gcode, factions in store.murim_factions.items():
            if fcode in factions:
                meta = factions[fcode].copy()
                meta["_group"] = gcode
                meta["_group_display"] = store.murim_groups.get(gcode, gcode)
                meta["_code"] = fcode
                meta["_display"] = meta.get("display", fcode)
                return meta
        return None

    # 상태 변경 헬퍼
    def wm_select_region(code):
        store.wm_state["region"] = code
        store.wm_state["faction"] = None

    def wm_select_faction(code):
        store.wm_state["faction"] = code

# ---------------------------------------------------------
# ▣ 월드맵 화면
# ---------------------------------------------------------
screen world_map():
    $ ensure_murim_index()
    style_prefix "murim"
    tag menu

    if renpy.loadable("gui/worldmap_placeholder.png"):
        add "gui/worldmap_placeholder.png" at truecenter

    frame:
        background Solid("#0008")
        xalign 0.02 yalign 0.05
        xmaximum 500 ymaximum 0.9
        vbox:
            spacing 10
            text "지역 선택" size 30 color "#fff" substitute False
            viewport:
                draggable True mousewheel True
                xmaximum 480 ymaximum 600
                vbox:
                    spacing 6
                    for rcode, rdisp in wm_regions():
                        # 지역 버튼
                        textbutton Text(rdisp, substitute=False) action Function(wm_select_region, rcode) xfill True

    frame:
        background Solid("#000B")
        xalign 0.98 yalign 0.05
        xmaximum 700 ymaximum 0.9
        vbox:
            spacing 10
            text "세력 정보" size 30 color "#fff" substitute False

            if wm_state["region"] is None:
                text "왼쪽에서 지역을 먼저 선택하세요." size 22 color "#ddd" substitute False
            else:
                $ region_code = wm_state["region"]
                $ region_disp = store.murim_worldmap[region_code]["display"]
                text ("지역: " + region_disp) size 24 color "#eee" substitute False

                viewport:
                    draggable True mousewheel True
                    xmaximum 680 ymaximum 180
                    grid 2 100:
                        transpose True xfill True
                        for fcode in wm_factions_in(region_code):
                            $ meta_tmp = wm_find_faction_meta(fcode)
                            $ fdisp = meta_tmp["_display"] if meta_tmp else fcode
                            # 지역 내 세력 버튼
                            textbutton Text(fdisp, substitute=False) action Function(wm_select_faction, fcode) xfill True

                if wm_state["faction"]:
                    $ meta = wm_find_faction_meta(wm_state["faction"])
                    if meta:
                        null height 10
                        frame:
                            background Solid("#111c")
                            xfill True
                            vbox:
                                spacing 8
                                text (meta["_group_display"] + "  ·  " + meta["_display"]) size 26 color "#fff" substitute False
                                if "location" in meta:
                                    text ("근거지: " + meta["location"]) color "#ddd" substitute False
                                if "traits" in meta:
                                    text "특징:" color "#ccc" substitute False
                                    for t in meta["traits"]:
                                        text ("• " + t) color "#ddd" substitute False
                                if "skills" in meta:
                                    text "대표 무공:" color "#ccc" substitute False
                                    text ", ".join(meta["skills"]) color "#ddd" substitute False
                                if "treasure" in meta:
                                    text "보물/비급:" color "#ccc" substitute False
                                    text ", ".join(meta["treasure"]) color "#ddd" substitute False
                                if "event" in meta:
                                    text ("연관 이벤트: " + str(meta["event"])) color "#ddd" substitute False
                                if "notable" in meta and meta["notable"]:
                                    text "대표 인물:" color "#ccc" substitute False
                                    for p in meta["notable"]:
                                        $ role = p.get("role", "인물")
                                        text ("• " + p["name"] + "  (" + role + ")") color "#ddd" substitute False
                                hbox:
                                    spacing 10
                                    # 지역 버튼
                                    textbutton Text(rdisp, substitute=False) action Function(wm_select_region, rcode) xfill True

                                    # 지역 내 세력 버튼
                                    textbutton Text(fdisp, substitute=False) action Function(wm_select_faction, fcode) xfill True

                                    # 세부패널 이동 버튼들
                                    textbutton Text("인물 관계 보기", substitute=False) action Show("relationship_screen", preselect_faction=meta["_code"])
                                    textbutton Text("관계도 보기", substitute=False) action Show("relationship_graph_screen", preselect_faction=meta["_code"])
                                    textbutton Text("닫기", substitute=False) action SetDict(wm_state, "faction", None)

    # 화면 닫기
    textbutton Text("닫기", substitute=False) action Return() xalign 0.98 yalign 0.02

