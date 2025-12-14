import tkinter as tk
import time
import threading
from env import NetworkEnvironment
from agent import QLearningAgent, blue_dynamic_defense, update_blue_intel, reset_memory, EPISODES, EPSILON, MIN_EPSILON, EPSILON_DECAY
import agent

class CyberWarGUI:
    def __init__(self, master):
        self.master = master
        master.title("Cyber War: Advanced Simulation (MAS)")
        self.canvas = tk.Canvas(master, width=600, height=450, bg="#2c3e50")
        self.canvas.pack()
        
        # Visualization Coordinates
        self.node_pos = {0:(100,250), 1:(250,150), 2:(250,350), 3:(400,250), 4:(550,250)}
        self.node_objs = {}
        self.agent_obj = None
        self.fw_obj = [] 
        
        # UI Elements
        self.round_text = self.canvas.create_text(300, 50, text="WAITING...", font=("Impact", 20), fill="white")
        self.status_lbl = tk.Label(master, text="System Ready", font=("Consolas", 11), bg="#ecf0f1")
        self.status_lbl.pack(fill="x")
        
        self.env = NetworkEnvironment()
        self.agent = QLearningAgent(self.env)
        self.draw_network()
        self.btn = tk.Button(master, text="START SIMULATION", command=self.start_thread, bg="#e74c3c", fg="white", font=("Arial", 12, "bold"))
        self.btn.pack(pady=10)

    def draw_network(self):
        """Draws the network topology and link states."""
        self.canvas.delete("net_lines")
        
        base_lines = [(0,1), (0,2), (1,2), (1,3), (2,1), (2,3), (3,4)]
        for u, v in base_lines:
            x1, y1 = self.node_pos[u]
            x2, y2 = self.node_pos[v]
            self.canvas.create_line(x1, y1, x2, y2, fill="#95a5a6", width=2, tags="net_lines")

        # Draw Exploit 1 (2->4)
        x2, y2 = self.node_pos[2]
        x4, y4 = self.node_pos[4]
        if self.env.exploit_1_patched:
            self.canvas.create_line(x2, y2, x4, y4, fill="#e74c3c", width=4, dash=(4, 4), tags="net_lines")
            self.canvas.create_text((x2+x4)/2, (y2+y4)/2+20, text="PATCHED", fill="#e74c3c", font=("Arial", 9, "bold"), tags="net_lines")
        else:
            self.canvas.create_line(x2, y2, x4, y4, fill="#7f8c8d", width=1, tags="net_lines")

        # Draw Exploit 2 (1->4)
        x1, y1 = self.node_pos[1]
        if self.env.exploit_2_active:
            if self.env.exploit_2_patched:
                self.canvas.create_line(x1, y1, x4, y4, fill="#e74c3c", width=4, dash=(4, 4), tags="net_lines")
                self.canvas.create_text((x1+x4)/2, (y1+y4)/2-20, text="PATCHED", fill="#e74c3c", font=("Arial", 9, "bold"), tags="net_lines")
            else:
                self.canvas.create_line(x1, y1, x4, y4, fill="#f1c40f", width=3, tags="net_lines")
                self.canvas.create_text((x1+x4)/2, (y1+y4)/2-20, text="⚡ NEW EXPLOIT", fill="#f1c40f", font=("Arial", 9, "bold"), tags="net_lines")

        # Draw Nodes
        for n, (x, y) in self.node_pos.items():
            color = "#3498db" if n==0 else "#e74c3c" if n==4 else "#ecf0f1"
            self.canvas.create_oval(x-25, y-25, x+25, y+25, fill=color, outline="white", width=2, tags="nodes")
            self.canvas.create_text(x, y, text=str(n), font=("Arial", 14, "bold"), tags="nodes")
            self.node_objs[n] = (x, y)

    def update_agent(self, n):
        if self.agent_obj: self.canvas.delete(self.agent_obj)
        x, y = self.node_pos[n]
        self.agent_obj = self.canvas.create_oval(x-12, y-12, x+12, y+12, fill="#2ecc71", outline="black")

    def update_firewall(self, n):
        for item in self.fw_obj: self.canvas.delete(item)
        self.fw_obj = []
        if n != -1 and n is not None:
            x, y = self.node_objs[n]
            l1 = self.canvas.create_line(x-20, y-20, x+20, y+20, fill="#c0392b", width=5)
            l2 = self.canvas.create_line(x+20, y-20, x-20, y+20, fill="#c0392b", width=5)
            self.fw_obj.extend([l1, l2])

    def start_thread(self):
        threading.Thread(target=self.run, daemon=True).start()

    def run(self):
        """Main execution logic for the simulation."""
        self.btn.config(state="disabled")
        reset_memory() 
        self.canvas.itemconfigure(self.round_text, text="TRAINING AI MODELS...")
        
        # 1. Background Training Phase
        agent.EPSILON = 1.0
        for _ in range(200):
            state = self.env.reset()
            done = False
            while not done:
                blue_dynamic_defense(self.env, state)
                action = self.agent.choose_action(state)
                next_state, reward, done = self.env.step(action)
                self.agent.learn(state, action, reward, next_state)
                state = next_state
            if agent.EPSILON > MIN_EPSILON: agent.EPSILON *= EPSILON_DECAY

        # 2. Live Visualization Phase
        agent.EPSILON = 0.05 
        
        for r in range(1, 16):
            state = self.env.reset()
            current_loc = state[0]
            
            # --- Scenario Scripting ---
            
            # Step 1: Patch first exploit
            if r == 4: 
                agent.PATCH_1_DONE = True
                self.agent.forget_path(2, 4) 
                self.status_lbl.config(text="SYSTEM ALERT: Exploit at Node 2 Patched!", fg="red")

            # Step 2: Introduce new Zero-Day exploit
            if r == 7: 
                self.env.inject_exploit_2()
                self.canvas.itemconfigure(self.round_text, text="⚠️ VULNERABILITY INJECTED!", fill="orange")
                # Force the attacker to "discover" it immediately
                self.agent.force_insight(1, 4) 
            
            # Step 3: Patch second exploit
            if r == 11: 
                agent.PATCH_2_DONE = True
                self.agent.forget_path(1, 4)
                self.status_lbl.config(text="SYSTEM ALERT: Exploit at Node 1 Patched!", fg="red")

            # Update visuals
            self.draw_network() 
            self.update_agent(current_loc)
            self.update_firewall(-1)
            
            phase_text = f"ROUND {r}/15"
            self.canvas.itemconfigure(self.round_text, text=phase_text, fill="white")
            time.sleep(1)
            
            done = False
            steps = 0
            path = [state[0]]
            stuck_counter = 0 
            
            # Round Loop
            while not done:
                fw = blue_dynamic_defense(self.env, state)
                if fw != -1: self.update_firewall(fw)
                
                # Intelligent Retreat Logic
                if stuck_counter >= 2: 
                    if current_loc == 2: action = 1 
                    elif current_loc == 1: action = 0 
                    else: action = self.agent.choose_action(state)
                    self.status_lbl.config(text="Agent Retreating...", fg="orange")
                    stuck_counter = 0 
                else:
                    action = self.agent.choose_action(state)
                
                path.append(action)
                prev_loc = state[0]
                state, reward, done = self.env.step(action)
                current_loc = state[0]
                
                # Check for collisions/blocks
                if current_loc == prev_loc:
                    stuck_counter += 1
                    if reward == -10:
                        self.status_lbl.config(text=f"Blocked at Node {action}", fg="red")
                    elif reward == -5:
                        self.status_lbl.config(text=f"Path Dead / Patched", fg="orange")
                    time.sleep(0.5)
                else:
                    stuck_counter = 0 
                    self.update_agent(current_loc)
                
                time.sleep(0.4) 
                steps += 1
                if steps > 25: break
            
            if state[0] == 4:
                self.status_lbl.config(text="VICTORY! System Breached.", fg="green")
                update_blue_intel(path)
                if agent.PATCH_1_DONE or agent.PATCH_2_DONE: self.draw_network()
            else:
                self.status_lbl.config(text="DEFENSE SUCCESSFUL.", fg="blue")
            
            time.sleep(1)
        
        self.canvas.itemconfigure(self.round_text, text="SIMULATION COMPLETE", fill="#2ecc71")
        self.btn.config(state="normal")

if __name__ == "__main__":
    root = tk.Tk()
    gui = CyberWarGUI(root)
    root.mainloop()