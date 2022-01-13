# Python Interfaces to Use cases  

This folder contains a set of Open-AI-gym Python Environments for interfacing with 
emulations and studying various use cases.
The Python environments expose MDP/POMDP interfaces to emulated infrastructures 
that can be used to optimize control policies. 

- **Network intrusion** ([network_intrusion](./network_intrusion)):
     - *Capture the flag* ([ctf](./network_intrusion/ctf)): A general interface to the CTF minigame is implemented which supports: System identification, policy optimization (PPO, Reinforce, DQN, DDPG, Q-Learning, A2C), generalization, parallel training, domain randomization.
     
## Ideas for future minigames: 

- **DoS**: 
     - *BotNet* minigame
- **Malware**: 
     - *Self replicating malware* minigame
- **Network intrusion**:
     - *Man-in-the-Middle* minigame
     - *Network protocol attack* minigame
     - *Network sniffing* minigame
     - *Spoofing* minigame                    
- **Server exploit**
     - *Advanced persistent threats* minigame
     - *Binary exploit* minigame          
- **Web Hacking**     
     - *SQL Injection* minigame     
     
 
## Author & Maintainer

Kim Hammar <kimham@kth.se>

## Copyright and license

[LICENSE](../../LICENSE.md)

Creative Commons

(C) 2021, Kim Hammar