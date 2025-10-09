# =========================================================
# 11_relationship_graph.rpy
# ---------------------------------------------------------
# ▣ 관계도의 네트워크 시각화
#   - 원형 자동 배치
#   - 호감/적대에 따른 선 색상
#   - 노드 클릭 → 하단 요약창
# ---------------------------------------------------------
# ⚙️ 구현 노트
# - add Transform(Solid(..., rotate=각도)) 로 선을 안전하게 그림
# - 스크린 내부에서는 $ 로 대입, if/elif 줄바꿈 엄수
# =========================================================

init python:
    import math
    import renpy.store as store

    # 노드 위치 캐시 (필요시 확장해 고정 위치 저장 가능)
    if not hasattr(store, "rel_graph_pos"):
        store.rel_graph_pos = {}

    # ---------------------------------------------
    # ▣ 세력별 인물 좌표 계산 (원형 배치)
    # ---------------------------------------------
    def build_relationship_positions(faction_code=None):
        ensure_murim_index()

        pos = {}
        members = [c for c in store.murim_chars.values()
            if (not faction_code or c.faction == faction_code)]

        n = len(members)
        if n == 0:
            return {}

        cx, cy, r = 640, 360, 260  # 중심/반지름
        for i, c in enumerate(members):
            angle = 2.0 * math.pi * i / max(1, n)
            x = cx + r * math.cos(angle)
            y = cy + r * math.sin(angle)
            pos[c.id] = (x, y)
        return pos

    # ---------------------------------------------
    # ▣ 선(엣지) 표시용 Displayable
    #   - (x1,y1)→(x2,y2) 방향으로 회전된 얇은 사각형
    # ---------------------------------------------
    def edge_displayable(x1, y1, x2, y2, color="#888", width=2):
        dx = x2 - x1
        dy = y2 - y1
        length = max(1.0, (dx*dx + dy*dy) ** 0.5)
        angle = math.degrees(math.atan2(dy, dx))
        d = Solid(color, xsize=int(length), ysize=width)
        return Transform(d, rotate=angle, anchor=(0.0, 0.5), xpos=x1, ypos=y1)

# ---------------------------------------------------------
# ▣ 관계도 화면
# ---------------------------------------------------------
screen relationship_graph_screen(preselect_faction=None):
    tag menu
    style_prefix "murim"
    $ ensure_murim_index()

    default _selected_faction = preselect_faction
    default _pos = build_relationship_positions(_selected_faction)
    default _focus_char = None

    frame:
        background Solid("#000c")
        xalign 0.5 yalign 0.5
        xmaximum 1280 ymaximum 720

        vbox:
            spacing 6
            text "무림 관계도" size 32 color "#fff" xalign 0.5 substitute False
            if _selected_faction:
                $ fdisp = None
                for g, fset in store.murim_factions.items():
                    if _selected_faction in fset:
                        $ fdisp = fset[_selected_faction]["display"]
                        break
                text ("세력: " + (fdisp or _selected_faction)) color "#aaa" xalign 0.5 substitute False

    fixed:
        xfill True
        yfill True
        # (엣지 루프 그대로)

    fixed:
        xfill True
        yfill True

        for cid, c in store.murim_chars.items():
            if _selected_faction and c.faction != _selected_faction:
                continue
            $ (x, y) = _pos.get(cid, (0, 0))
            frame:
                background Solid("#0008")
                xpos x ypos y
                xanchor 0.5 yanchor 0.5
                xsize 130 ysize 66
                vbox:
                    spacing 2
                    text c.name color "#fff" xalign 0.5 substitute False
                    text c.role color "#ccc" size 18 xalign 0.5 substitute False
                    # 각 노드 카드의 '보기' 버튼
                    textbutton Text("보기", substitute=False) action SetScreenVariable("_focus_char", cid) xalign 0.5

    if _focus_char:
        $ c = store.murim_chars_by_id[_focus_char]
        frame:
            background Solid("#111c")
            xalign 0.5 yalign 0.92
            xsize 640 ysize 220
            vbox:
                spacing 6
                text (c.name + " (" + c.role + ")") size 24 color "#fff" substitute False
                text ("호감: " + str(c.affinity) + "  /  적대: " + str(c.hostility)) color "#ccc" substitute False
                if c.relations:
                    for rtype, ids in c.relations.items():
                        if ids:
                            text rtype color "#9cf" substitute False
                            hbox:
                                spacing 6
                                for tid in ids:
                                    $ t = store.murim_chars_by_id.get(tid)
                                    if t:
                                        text t.name color "#ddd" substitute False

    hbox:
        xalign 0.5 yalign 0.98 spacing 10

        textbutton Text("닫기", substitute=False) action Return()
        if _selected_faction:
            textbutton Text("목록 보기", substitute=False) action Show("relationship_screen", preselect_faction=_selected_faction)
