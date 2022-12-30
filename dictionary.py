import mouse_mover


olg_bag_layout = [(562, 238, 602, 278), (607, 238, 651, 278), (651, 238, 692, 278), (692, 238, 728, 278),
                  (562, 278, 602, 315), (607, 278, 651, 315), (651, 278, 692, 315), (692, 278, 728, 315),
                  (562, 315, 602, 352), (607, 315, 651, 352), (651, 315, 692, 352), (692, 315, 728, 352),
                  (562, 352, 602, 387), (607, 352, 651, 387), (651, 352, 692, 387), (692, 352, 728, 387),
                  (562, 387, 602, 423), (607, 387, 651, 423), (651, 387, 692, 423), (692, 387, 728, 423),
                  (562, 423, 602, 459), (607, 423, 651, 459), (651, 423, 692, 459), (692, 423, 728, 459),
                  (562, 459, 602, 495), (607, 459, 651, 495), (651, 459, 692, 495), (692, 459, 728, 495)]
templates = {}
fishing_spot_lower = [103, 50, 20]
fishing_spot_upper = [106, 255, 255]
game_screen = [12, 33, 515, 335]
full_inv_screen = [190, 470, 155, 20]
full_inv_wc = [19, 475, 142, 15]
bag_screen = [560, 240, 180, 255]
hp_orb = [530, 87, 21, 13]
prayer_orb = [530, 122, 21, 13]
cow_text = [65, 39, 28, 13]
health_bar = [237, 163, 50, 40]
bot_type = {"Mining": "roboflow", "Woodcutting": "roboflow", "Fishing": "color", "Combat": "local"}
scripts = []
action_list = {}
full_inv_lower = (106, 50, 20)
full_inv_upper = (138, 255, 255)


# DEPRECATED
def get_gathering_bag():
    weights_x = []
    weights_y = []
    for i in olg_bag_layout:
        weights_x.append(mouse_mover.weight_generator([i[0], i[2]]))
        weights_y.append(mouse_mover.weight_generator([i[1], i[3]]))
    test = list(zip(olg_bag_layout, weights_x, weights_y))
    return test



