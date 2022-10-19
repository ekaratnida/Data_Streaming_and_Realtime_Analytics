## Week 10 Video games data analytics 2</br></br>
### Outline </br>

### 10.1 What we've learned so far </br>

### 10.2 Case study: Game Analytics
+ Slide [paper: A game analytics model to identify player profiles in singleplayer games https://www.sbgames.org/sbgames2019/files/papers/ComputacaoFull/198360.pdf] </br>
+ Get and run the python game from https://github.com/DanPetersson/SpaceWars.git
+ pip install pygame (If you don't have it.)
    - If you don't want to play the game in a fullscreen mode, you can comment line 419 of space_wars.py out and then uncomment line 418 of the same file.

**Week 12 Game Analytics Implementation** </br></br>
***Get your hand dirty*** </br>

- Modify the game from this link ( https://github.com/DanPetersson/SpaceWars ) to collect your game data.
  - Show your name on the screen while playing
  - Show top 3 scores while playing
  - Add collectable coins (graphics and marks)
  - Collect the following data every 1 second
    - A0) Position in X axis
    - A1) Position in Y axis
    - A2) Number of coins collected
    - A3) Number of destroyed enemies
    - A4) Number of shots
    - A5) Number of shots without enemies
- Apply K-Means clustering, K = 4
- Apply Decision Trees to classify users into 4 groups (Hardcore achiever, Hardcore killer, Casual achiever, Hardcore achiever)

### Case study
+ Deep Reinforcement Learning in Production at Zynga https://www.youtube.com/watch?v=q4b-HHG5dG4
