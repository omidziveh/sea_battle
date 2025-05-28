# Sea Battle V2 🚢💣

## What's This All About?

Sea Battle V2 is a cool take on the classic battleship game, cooked up in Python with the Pygame library. You get to set up your ships and then trade shots with an opponent to see who rules the waves! This version lets you battle it out against a bot. 🤖

## Awesome Features ✨

* **Looks Good!** A visual game, all thanks to Pygame.
* **Place Your Ships:** You're the admiral! Decide where your ships go.
    * Drag 'em and drop 'em.
    * Spin 'em around (horizontal or vertical) with the rotate button.
* **You vs. The Machine:** Take on an AI opponent.
* **Take Turns Blasting:** You and the bot go back and forth, firing at each other's grids.
* **Hit or Miss?** See right away if your shot was a hit (🔴) or a miss (🔵).
* **Bonus Shot!** Land a hit? You get to fire again! 🎉
* **Battle Stations:** See your ships on your board and keep track of your attacks on the bot's board.
* **Saves Your Progress (Sort Of):** Ship positions and stuff get saved in CSV files in the `db` folder.

## How to Play (Our Best Guess!) 🚤

1.  **Get Your Ships Ready (Main Screen):**
    * The game starts with your ships chilling on the right, off the main board.
    * Drag your ships onto your grid (that's the one on the left).
    * Want to rotate a ship? Click it, then hit the 'rotate' button. 🔄
    * Make sure they fit on the board and don't crash into each other!
    * All set with your 20 ship pieces? Smash that 'done' button to start the battle!
2.  **Attack Time! 💥**
    * Now you'll see your board (with your ships) and the bot's board (ships are hiding!).
    * Green arrow (🟢) means it's your turn. Red arrow (🔴) means the bot's up.
    * Click a square on the bot's grid (the right one) to shoot.
    * Red marker = HIT! 🔥 Blue marker = MISS. 💧
    * Hit a ship? You get another go!
    * If you miss, it's the bot's turn to fire at your ships.
    * The bot picks random spots to attack on your board.
    * Keep going until someone's entire fleet is at the bottom of the sea!

##What's Where? (File Map) 🗺️

* `main.py`: The big boss. Starts the game, handles clicks and stuff.
* `attack_page.py`: Runs the show during the attack phase.
* `board.py`: Makes the game board look pretty and knows where ships are.
* `ship.py`: All about the ships – how they look, move, and if they get hit.
* `bot.py`: The brains of your AI opponent. 🧠
* `button.py`: Makes those clickable buttons.
* `click_manager.py`: Figures out what to do when you click (like rotating ships).
* `drag_manager.py`: Lets you drag your ships around.
* `drop_manager.py`: Handles dropping ships and making sure they're in a good spot.
* `motion_manager.py`: Shows where your mouse is on the board.
* `loading_page.py`: That "please wait" screen.
* `photo.py`: Shows other pictures in the game.
* `color.py`: All the pretty colors used.
* `efects.py`: Supposed to be for sounds (mostly just music for now 🎶).
* `db/`: Where all the nitty-gritty data for ships is kept (in CSV files).
* `assets/images/`: Pictures for ships, buttons, and other game bits.

## Stuff You Need 💻

* **Pygame:** The main ingredient! (Make sure you have it: `pip install pygame`)

## Still Tinkering / Cool Ideas for Later 🛠️

* **Who Won?!** Actually show a victory or defeat screen. 🏆
* **More Sounds!** Add booms, splashes, and "You sunk my battleship!" (Right now, `efects.py` is a bit quiet).
* **Smarter Bot:** Make the bot less random and more sneaky. 🕵️
* **Prettier UI:**
    * Show how many ships are left for everyone.
    * Jazz up the visuals.
* **Fewer Oopsies:** Make sure the game doesn't crash if something weird happens.
* **Code Clean-Up:**
    * The `check_formation` in `bot.py` might need a little fix for how it checks other ships.
    * In `ship.py`, when a ship can't rotate, it draws a red box like crazy – maybe something nicer for the user?
    * Could tidy up some of the global variables.
* **Better Instructions:** Add more comments in the code and make this README even clearer.
