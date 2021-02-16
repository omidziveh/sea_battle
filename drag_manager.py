from ship import get_moving_ship, get_clicked

def drag_ship(ships, x, y):
    if not get_moving_ship():
        for ship in ships:
            if ship.check_hit(x, y):
                for i in ships:
                    if i.ID == get_clicked():
                        i.set_clicked_status(False)
                ship.set_clicked_status(True)
                ship.set_moving_status(True)
                ship.move(x, y)

    else:
        for ship in ships:
            if ship.ID == get_moving_ship():
                ship.move(x, y)

