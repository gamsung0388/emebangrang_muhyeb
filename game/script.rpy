# 이 파일에 게임 스크립트를 입력합니다.

# image 문을 사용해 이미지를 정의합니다.
# image eileen happy = "eileen_happy.png"

# 게임에서 사용할 캐릭터를 정의합니다.
# define e = Character('아이린', color="#c8ffc8")

label start:
    $ ensure_murim_index()
    
    menu:
        "무림 월드맵/관계 데모를 시작합니다.":
            call screen world_map
        "관계목록을 확인해봅시다.":
            call screen relationship_screen
        "관계도를 확인해봅시다.":
            call screen relationship_graph_screen
label worldmap:



# 여기에서부터 게임이 시작합니다.
# label start:
# 
#     scene black
#     "강호의 아침이 밝았다."
#     jump prologue
# 
# label prologue:
#     "운명의 갈림길에 서 있다."
#     menu:
#         "정파의 길을 따른다":
#             $ fame += 5
#             $ faction = "orthodox"
#         "사파의 손을 잡는다":
#             $ fame -= 3
#             $ faction = "evil"
#         "강호를 자유롭게 떠난다 (중립)":
#             $ faction = "neutral"
#     jump worldmap
