from ship import get_clicked
import bot
from attack_page import Attack
import loading_page


def action(x, y, ships, buttons, board):
    attack = Attack(1000, 560, ships)
    global ship
    for ship in ships:
        if ship.check_hit(x, y):
            ship.set_clicked_status(True)
    for button in buttons:
        if button.check_hit(x, y):
            if button.name == 'rotate':
                for ship in ships:
                    if ship.ID == get_clicked():
                        if ship.orientation == 'H':
                            ship.rotate(ships, 'V')
                        else:
                            ship.rotate(ships, 'H')
            if button.name == 'done':
                print("done")
                bot.init_ships(board, board.block_size)
                bot.deploy(board, board.block_size)
                if board.read_board('user') == 20:
                    loading_page.deploy_page()
                    board.read_board('bot')
                    board.read_board('user')
                    print('checked')
                    attack.deploy_page(ships)
