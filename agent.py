import time
import random
from env import NetworkEnvironment

# --- Configuration & Hyperparameters ---
LEARNING_RATE = 0.7   
DISCOUNT_FACTOR = 0.9 
EPSILON = 1.0         
EPSILON_DECAY = 0.95  
MIN_EPSILON = 0.05    
EPISODES = 400 

# --- Global Defender Memory / ذاكرة المدافع ---
ATTACK_HISTORY = {1: 1, 2: 1, 3: 1}
DETECT_COUNT_1 = 0 
DETECT_COUNT_2 = 0 
PATCH_1_DONE = False
PATCH_2_DONE = False

def reset_memory():
    """Resets defender's knowledge for a fresh simulation run."""
    global ATTACK_HISTORY, DETECT_COUNT_1, DETECT_COUNT_2, PATCH_1_DONE, PATCH_2_DONE
    ATTACK_HISTORY = {1: 1, 2: 1, 3: 1}
    DETECT_COUNT_1 = 0
    DETECT_COUNT_2 = 0
    PATCH_1_DONE = False
    PATCH_2_DONE = False

class QLearningAgent:
    """
    Represents the Red Agent (Attacker) using Q-Learning.
    يمثل العميل المهاجم باستخدام خوارزمية التعلم المعزز.
    """
    def __init__(self, env):
        self.env = env
        self.q_table = {}

    def get_q_value(self, state, action):
        return self.q_table.get((state, action), 0.0)

    def force_insight(self, node_from, node_to):
        """
        Simulates vulnerability scanning tool results.
        Updates Q-Table to prioritize a newly discovered path across all firewall states.
        يحاكي نتائج أدوات فحص الشبكة لتوجيه المهاجم نحو ثغرة جديدة.
        """
        for fw in [None, 1, 2, 3, 4]:
            state = (node_from, fw)
            self.q_table[(state, node_to)] = 1000.0

    def forget_path(self, node_from, node_to):
        """
        Forces the agent to unlearn a path (used when patched).
        يجبر العميل على نسيان مسار تم إغلاقه.
        """
        for fw in [None, 1, 2, 3, 4]:
            state = (node_from, fw)
            self.q_table[(state, node_to)] = -1000.0

    def choose_action(self, state):
        current_node = state[0] if isinstance(state, tuple) else state
        possible_actions = self.env.get_possible_actions(current_node)
        if not possible_actions: return current_node

        # Exploration vs Exploitation
        if random.random() < EPSILON:
            return random.choice(possible_actions)
        
        random.shuffle(possible_actions)
        best_action = possible_actions[0]
        best_val = -float('inf')
        
        for action in possible_actions:
            q_val = self.get_q_value(state, action)
            if q_val > best_val:
                best_val = q_val
                best_action = action
        return best_action

    def learn(self, state, action, reward, next_state):
        next_node = next_state[0] if isinstance(next_state, tuple) else next_state
        next_possible = self.env.get_possible_actions(next_node)
        max_future = max([self.get_q_value(next_state, a) for a in next_possible]) if next_possible else 0.0
        current = self.get_q_value(state, action)
        
        # Bellman Equation Update
        new_q = current + LEARNING_RATE * (reward + DISCOUNT_FACTOR * max_future - current)
        self.q_table[(state, action)] = new_q

# --- Blue Agent Logic (Defender) ---
def blue_dynamic_defense(env, state):
    """
    Implements a Reactive & Strategic Defense logic.
    يطبق منطق دفاعي تفاعلي واستراتيجي.
    """
    global PATCH_1_DONE, PATCH_2_DONE
    
    red_location = state[0] if isinstance(state, tuple) else state
    
    # Apply patches if vulnerabilities are detected
    if PATCH_1_DONE: env.patch_exploit_1()
    if PATCH_2_DONE: env.patch_exploit_2()
    
    blocked = None
    
    # Strategic decisions based on attacker's location
    if red_location == 0:
        blocked = random.choices([1, 2], weights=[0.5, 0.5], k=1)[0]
    elif red_location == 1:
        if env.exploit_2_active and not PATCH_2_DONE:
             blocked = 3 # Defender unaware of Node 4 exploit via Node 1
        else:
             blocked = 3
    elif red_location == 2:
        blocked = 3 
    elif red_location == 3:
        blocked = 4 # Protect the target

    if blocked is not None:
        env.set_firewall(blocked)
    return blocked

def update_blue_intel(path):
    """
    Updates defender's knowledge base after an attack.
    تحديث قاعدة معرفة المدافع بعد الهجوم.
    """
    global DETECT_COUNT_1, DETECT_COUNT_2, PATCH_1_DONE, PATCH_2_DONE
    
    if len(path) >= 2:
        node_before_target = path[-2]
        
        # Logic to detect Exploit 1 (Node 2)
        if node_before_target == 2:
            DETECT_COUNT_1 += 1
            if DETECT_COUNT_1 >= 3: 
                PATCH_1_DONE = True
                print("BLUE SYSTEM: Exploit at Node 2 identified and patched.")

        # Logic to detect Exploit 2 (Node 1)
        elif node_before_target == 1:
            DETECT_COUNT_2 += 1
            if DETECT_COUNT_2 >= 3: 
                PATCH_2_DONE = True
                print("BLUE SYSTEM: New Exploit at Node 1 identified and patched.")

if __name__ == "__main__":
    pass