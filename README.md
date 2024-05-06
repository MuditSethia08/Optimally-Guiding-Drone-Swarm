# Optimally Guiding Drone Swarm
Project form ME 312 IIT Bombay <br>
How to run the project:
1. Create the state-action-state transitions .txt file by this command `python3 encoder.py > SASRP.txt`
2. Use Mdp to solve it `python3 planner.py --mdp SASRP.txt > strategy.txt`
3. Go to `main.py` and replace the strategy file with `strategy.txt` and the corresponding inputs, such as the number of drones, number of defenses, grid size, etc.
