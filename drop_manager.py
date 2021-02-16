from ship import get_moving_ship

def drop_ship(ships, board):
    moving_ship = get_moving_ship()
    for ship in ships:
        if ship.ID == moving_ship:
            ship.set_moving_status(False)
            ship_hitbox = ship.get_hitbox()
            if ship_hitbox[0] < board.left or ship_hitbox[1] > board.right or \
                    ship_hitbox[2] < board.up or ship_hitbox[3] > board.down or \
                    not ship.check_ships_in_safe_area(ships):
                ship.set_new_location(ship.x_first, ship.y_first)
                return True