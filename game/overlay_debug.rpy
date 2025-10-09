# =========================================================
# overlay_debug.rpy (선택)
# ---------------------------------------------------------
# ▣ 화면 우상단에 빠른 전환 버튼 추가
#   - 필요 없으면 파일을 만들지 않으면 됨
# =========================================================

screen quick_panel_additions():
    frame:
        background Solid("#0006")
        xalign 0.98 yalign 0.02
        hbox:
            spacing 8
            textbutton "월드맵" action Show("world_map")
            textbutton "관계목록" action Show("relationship_screen")
            textbutton "관계도" action Show("relationship_graph_screen")

init python:
    config.overlay_screens.append("quick_panel_additions")
