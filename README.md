# 🐟 Aqua Eater

Aqua Eater is a 2D arcade-style game developed in Python using the Pygame library.  
The player controls a fish that must survive in the ocean by eating smaller fish and avoiding larger ones.

As the player grows, they can eventually dominate the sea and win the game.

---

## Gameplay Video

👉 Watch the gameplay here: https://www.youtube.com/watch?v=QGZUfuFPFiE

---

## Gameplay

- Control a fish and move freely through the ocean  
- Eat smaller fish to grow  
- Avoid bigger fish to survive  
- Progress until you become the largest fish  

Special **booster fish** occasionally appear, providing temporary abilities.

---

## Booster System

There are 4 types of special fish:

- 🛡️ **Armor Fish** – makes the player immune (cannot be eaten)  
- 🔥 **Frenzy Fish** – allows the player to eat any fish regardless of size  
- ⚡ **Speed Fish** – increases movement speed  
- ☠️ **Poison Fish** – decreases speed and score  

> Only one booster can be active at a time.  
> Booster effects last **5 seconds**.

---

## Features

- Fish selection system (unlockable skins based on high score)  
- Dynamic enemy fish with different sizes and speeds  
- Booster mechanics with unique effects  
- Win and Game Over screens  
- Sound effects for gameplay events  
- High score saving system  

---

## Tech Stack

- **Language:** Python  
- **Library:** Pygame  

---

## Project Structure
```
AquaEater/
├── main.py
├── assets/ # images and sounds
└── data/
└── high_score.txt
```


---

## Sound Effects

- `eat.wav` – played when eating a fish  
- `victory.wav` – played on win  
- `game_over.wav` – played on defeat  

---

## High Score System

The game stores the highest score in:
-data/high_score.txt

## Run the game:
```bash
python main.py
```

