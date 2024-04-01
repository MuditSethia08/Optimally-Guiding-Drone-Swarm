# Optimally Guiding Drone Swarm
 Project form ME 312 IIT Bombay
How to run the project:
1. Create the state-action-state' transitions .txt file by this command `python3 new_encoder.py > SASRP.txt`
2. Use Mdp to solve it `python3 planner.py --mdp SASRP.txt > strategy.txt`
3. Plot it `plot_aa_strategy.py --file_path strategy.txt`
