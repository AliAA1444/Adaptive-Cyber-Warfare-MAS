import time

class NetworkEnvironment:
    """
    Simulates a computer network environment for Multi-Agent Systems.
    تحاكي بيئة شبكة حاسوبية لأنظمة الوكلاء المتعددة.
    """
    def __init__(self):
        # Define network topology: Node -> List of connected neighbors
        # تعريف هيكلية الشبكة: العقدة -> قائمة الجيران المتصلين بها
        self.default_graph = {
            0: [1, 2],       # Start Node / نقطة البداية
            1: [0, 2, 3],    # Server A
            2: [0, 1, 3, 4], # Server B (Contains Zero-Day Exploit path to 4)
            3: [1, 2, 4],    # File Server
            4: [3]           # Target Database / قاعدة البيانات الهدف
        }
        
        # Create a mutable copy of the graph
        # إنشاء نسخة قابلة للتعديل من الشبكة
        self.network_graph = {k: v[:] for k, v in self.default_graph.items()}
        
        self.red_agent_location = 0
        self.target_node = 4
        self.max_steps = 25 
        self.current_step = 0
        self.blocked_node = None 
        
        # Exploit States / حالات الثغرات الأمنية
        self.exploit_1_patched = False
        self.exploit_2_active = False 
        self.exploit_2_patched = False

    def reset(self):
        """Resets the agent position and steps for a new episode."""
        self.red_agent_location = 0
        self.current_step = 0
        self.blocked_node = None
        return (self.red_agent_location, self.blocked_node)

    def patch_exploit_1(self):
        """Removes the connection between Node 2 and 4 (Patching)."""
        if 4 in self.network_graph[2]:
            self.network_graph[2].remove(4)
            self.exploit_1_patched = True

    def inject_exploit_2(self):
        """Injects a new vulnerability from Node 1 to 4."""
        if 4 not in self.network_graph[1]:
            self.network_graph[1].append(4)
            self.exploit_2_active = True

    def patch_exploit_2(self):
        """Removes the connection between Node 1 and 4."""
        if 4 in self.network_graph[1]:
            self.network_graph[1].remove(4)
            self.exploit_2_patched = True

    def set_firewall(self, node):
        """Blue agent sets a firewall on a specific node."""
        self.blocked_node = node

    def get_possible_actions(self, node):
        return self.network_graph.get(node, [])

    def step(self, action_node):
        """
        Executes a move in the environment.
        تنفيذ خطوة في البيئة.
        Returns: (New State, Reward, Done)
        """
        self.current_step += 1
        possible_moves = self.get_possible_actions(self.red_agent_location)
        
        reward = 0
        done = False
        
        if action_node in possible_moves:
            # Check for firewall collision / التحقق من الاصطدام بالجدار الناري
            if action_node == self.blocked_node:
                reward = -10 
            else:
                self.red_agent_location = action_node
        else:
            reward = -5 # Penalty for invalid move / عقوبة حركة غير صالحة

        # Check Win/Loss conditions
        if self.red_agent_location == self.target_node:
            reward = 100
            done = True
        elif self.current_step >= self.max_steps:
            reward = -10
            done = True
        else:
            if reward == 0: reward = -1 # Time penalty / تكلفة الوقت
        
        return (self.red_agent_location, self.blocked_node), reward, done