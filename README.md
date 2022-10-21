# Artificial Intelligence for Reversi 

## 1. Description of the Project

[//]: # "What was the purpose of the project?" 
The purpose of the project is to build an Artificial Intelligence which plays the board game called Reversi. An heuristics approach was used in conjuction with the minimax algorithm with alpha-beta pruning. The objective of the project was to create a player for Reversi using these heuristics that could beat as many other players as possible. A tournament was created where the different implemented heuristics were playing against each other in a tournament to decide which one was the best. 

[//]: # "What your application does?" 
During the first phase of the project, the alpha-beta pruning algorithm was implemented. It was tested with some simple heuristics. When the algorithm was working, the next step wa to build the heuristics. Different approaches were developed to solve the problem of finding the best heuristics. The key observation was that developing several common sense simple heuristics and combining them would be easier and probably better than a very complex heuristic. After several simple heuristics were developed, attention was shifted finding a way to create the most efficient combination of these simple heuristics for our final player. 

Insight for these type of observations was obtained by reading several academic papers which had already done an in depth analysis about how to use Game Theory, Machine Learning and Heuristics analysis. The detailed list of these papers can be found on the report.

[//]: # "What problem does it solve" 


[//]: # "What was your motivation?" 
The main motivation for this project was that a tournament would be carried out, were heuristics would be submitted by different people and the different players/heuristics will be made to play against each other. Each win against another player would give points that were reflected in a leaderboard every time a tournament was run.

[//]: # "Why did you build this project?" 


[//]: # "Building Procedure" 


### Project Strucuture
The project includes a report called `report.pdf` at the root directory. This reports includes:
- An in depth discussion of the implementation of the alpha-beta algorithm, including tests used, design and implementation discussion, and efficiency analysis with some measurements and conclusions on the measurements.
- A discussion on the design of the heuristics. These includes a review on the academic papers used, a detailed description of the dessign process and the description of the final heuristics.

Inside the root directory we can finde the subdirectory `code`, which contains all the python code used for implementing the games and the heuristics. This directory contains:
- A subdirectory `game_infrastracture` which contains all the infrastructure provided to us to run the Reversi game in Python and execute tournaments. It also contains some files to see how the Reversi game works, such as `demo_reversy.py`.
- `strategy.py`: Contains several strategies to play the Reversi game. One of them allows to play manually and the main one we had to implement was the `MinimaxAlphaBetaStrategy` Strategy which implements the minimax algorithm with alpha-beta pruning.
- `heuristic.py`: Contains the definition of the class `Heuristic` which will be implemented by each of the different heuristics in the `tournament.py` file. But it also contains the different evaluation functions which will be later tried to minimize by the different heuristics. 
- `tournament.py`: This file is divide into three parts:
  - The first part contains the different heuristics which make use of the functions defined in `heuristic.py`.
  - The second part contains the variable which will be used to setup the tournament which will be played. Adjusting this different values will run different types of tournaments accordingly. See more information in the `How to Install and Run` section.
  - The last part runs the different types tournament and prints the results. Some of the tournaments will help us decide which of our heuristic is best. 


## 2. Technologies Used

[//]: # "What technologies were used?" 
The main technology used was Python.  

[//]: # "Why you used the technologies you used?" 


[//]: # "Some of the challenges you faced and features you hope to implement in the future." 





## 3. Learning outcomes

[//]: # "What did you learn?" 
The main learning outcomes were:
- Strengthen my knowledge of Python.
- Learn how to implement complex algorithms such as the minimax algorithm with alpha-beta pruning.
- In depth understanding of the minimax algorithm.
- How to build useful heuristics to solve hard problems using Artificial Intelligence. 
- Using Heuristic approaches in order to easily construct Artifial Intelligences players which would probably beat any human player.
- Heuristic selection and optimization


## 4. How to Install and Run
In order to run the program, Python 3.7 or higher is needed. In order to run a tournament, different parameters can be adjusted in the `tournament.py` file inside the `code` directory. In its default setting, if the program is run using 
```
python3 tournament.py
```
in a terminal inside the `code` directory, a simple tournament will be executed were the heuristic `HeuristicPonderationMax` will be playing two Reversi games against the heuristic `HeuristicParityMobilityCorners1`. The execution of the program will print a table with the results of this simple tournament. 

However, this is the most simple execution of the tournament. Most of the parameters can be modified in the `Tournament Configuration` section inside `tournament.py`. The main parameters to adjust are:
- `initial_state`: A list containing different strings representing the initial board in which the game will be played. The size of the board can be modified with just by creating a bigger list and strings. The initial pieces in the board are represented with a `W` and `B` for white and black pieces respectively.
- `repetitions`: How many times the tournament will be played.
- `depth`: Search depth used by the search algorithms. For example, in the default configuration, the minimax algorithm will only go to depth 2 which means that only the next 2 moves will be taken into account for the decission of the heuristic. 
- `max_sec_per_move`: If this value is exceeded by a player in any of its turns, it will loose the game because of timeout.
- `test`: This variable allows to select which type of tournament will be carried our. It possible values are:
  - 0, which means a normal tournament will be run.
  - 1, which means only one heuristic (tested_against_heuristics) tested against others.
  - 2, optimize one heuristic's ponderations. This allows to optimize the weights of Heuristics which are made by a ponderation of other simpler heuristics. This mode helped me to optimize my final Heuristics.
- `strats`: Contains the list of heuristics which will be tested against each other in the normal tournament. 
- `tested_heuristic` and `tested_against_heuristics`: These varibles are used in one_heuristic_against_others.

After adjusting the parameters as desired each tournament can be run with the same command as before, but you should be careful so that the tournament ends in a reasonable time, being careful eith the depth allowd for the strategies and the number of heuristics tested in each tournament.


[//]: # "## 5. Extra Information"


