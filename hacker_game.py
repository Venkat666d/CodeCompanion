# hacker_game.py
import pygame
import random
import sys
import contextlib
import io
import math
import time
import json
import requests
from enum import Enum
from typing import List, Dict, Tuple, Optional

# --- Initialization ---
pygame.init()
pygame.mixer.init()

# --- Game Constants ---
WIDTH, HEIGHT = 1200, 800
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("🔥 CYBER APEX: Global Domination Protocol")
clock = pygame.time.Clock()

# Colors
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
DARK_GREEN = (0, 100, 0)
RED = (255, 0, 0)
WHITE = (255, 255, 255)
YELLOW = (255, 255, 0)
BLUE = (0, 120, 255)
PURPLE = (128, 0, 128)
ORANGE = (255, 165, 0)
CYAN = (0, 255, 255)
MAGENTA = (255, 0, 255)

# Fonts
FONT_SIZE = 16
FONT = pygame.font.SysFont('Consolas', FONT_SIZE)
TITLE_FONT = pygame.font.SysFont('Consolas', 36, bold=True)
HEADER_FONT = pygame.font.SysFont('Consolas', 24, bold=True)
SMALL_FONT = pygame.font.SysFont('Consolas', 14)

# Language Support
class ProgrammingLanguage(Enum):
    PYTHON = "Python"
    JAVASCRIPT = "JavaScript"
    JAVA = "Java"
    CPP = "C++"
    CSHARP = "C#"

# AI Assistant Class
class AIAssistant:
    def __init__(self):
        self.api_key = "AIzaSyBJtlYGk_oHUq5zmRhc9UnMhmyhmo1I2QA"
        
    def get_hint(self, challenge: str, user_code: str, language: ProgrammingLanguage) -> str:
        """Get a hint for the current challenge"""
        hints = [
            "Think about the basic syntax for this operation...",
            "Check your variable names and data types...",
            "Remember the proper structure for this programming construct...",
            "Look at the expected output format carefully...",
            "Consider edge cases and boundary conditions..."
        ]
        return random.choice(hints)

    def fix_code(self, challenge: str, user_code: str, error: str, language: ProgrammingLanguage) -> str:
        """Automatically fix user code"""
        if "variable" in challenge.lower():
            return "access_code = 'BANK2024'\nprint(access_code)"
        elif "loop" in challenge.lower():
            return "for i in range(1, 6):\n    print(i)"
        elif "function" in challenge.lower() and "multiply" in challenge.lower():
            return "def multiply(a, b):\n    return a * b\n\nresult = multiply(6, 7)\nprint(result)"
        elif "list" in challenge.lower():
            return "targets = ['server1', 'server2', 'server3']\nprint(targets[1])"
        elif "class" in challenge.lower():
            return "class Hacker:\n    def breach(self):\n        return 'ACCESS_GRANTED'\n\nh = Hacker()\nprint(h.breach())"
        elif "file" in challenge.lower():
            return "with open('passwords.txt', 'r') as file:\n    content = file.readline().strip()\n    print(content)"
        elif "recursion" in challenge.lower() or "factorial" in challenge.lower():
            return "def factorial(n):\n    if n <= 1:\n        return 1\n    return n * factorial(n-1)\n\nresult = factorial(5)\nprint(result)"
        else:
            return user_code + "\n# AI fix applied"

# Advanced Particle System
class ParticleSystem:
    def __init__(self):
        self.particles = []
        
    class Particle:
        def __init__(self, x, y, particle_type="spark"):
            self.x = x
            self.y = y
            self.particle_type = particle_type
            
            if particle_type == "spark":
                self.color = random.choice([GREEN, BLUE, CYAN, YELLOW])
                self.size = random.randint(2, 5)
                self.speed_x = random.uniform(-3, 3)
                self.speed_y = random.uniform(-3, 3)
                self.lifetime = random.randint(30, 60)
            elif particle_type == "explosion":
                self.color = random.choice([RED, ORANGE, YELLOW])
                self.size = random.randint(3, 8)
                angle = random.uniform(0, 2 * math.pi)
                speed = random.uniform(2, 8)
                self.speed_x = math.cos(angle) * speed
                self.speed_y = math.sin(angle) * speed
                self.lifetime = random.randint(40, 80)
            elif particle_type == "trail":
                self.color = (100, 255, 100, 150)
                self.size = random.randint(1, 3)
                self.speed_x = random.uniform(-1, 1)
                self.speed_y = random.uniform(-1, 1)
                self.lifetime = random.randint(20, 40)
                
        def update(self):
            self.x += self.speed_x
            self.y += self.speed_y
            self.lifetime -= 1
            self.size = max(0, self.size - 0.1)
            return self.lifetime > 0
            
        def draw(self, surface):
            if self.particle_type == "trail":
                surf = pygame.Surface((self.size * 2, self.size * 2), pygame.SRCALPHA)
                pygame.draw.circle(surf, self.color, (self.size, self.size), self.size)
                surface.blit(surf, (int(self.x - self.size), int(self.y - self.size)))
            else:
                pygame.draw.circle(surface, self.color, (int(self.x), int(self.y)), int(self.size))
    
    def add_particles(self, x, y, count=10, particle_type="spark"):
        for _ in range(count):
            self.particles.append(self.Particle(x, y, particle_type))
            
    def update(self):
        self.particles = [p for p in self.particles if p.update()]
        
    def draw(self, surface):
        for particle in self.particles:
            particle.draw(surface)

# Advanced Matrix Rain
class CyberMatrix:
    def __init__(self, width, height, font_size):
        self.width, self.height = width, height
        self.font_size = font_size
        self.columns = width // font_size
        self.drops = [random.randint(-50, height // font_size) for _ in range(self.columns)]
        self.speeds = [random.uniform(0.3, 2.5) for _ in range(self.columns)]
        self.brightness = [random.uniform(0.3, 1.0) for _ in range(self.columns)]
        self.symbols = "01アイウエオカキクケコサシスセソタチツテトナニヌネノハヒフヘホマミムメモヤユヨラリルレロワヲン"
        
    def draw(self, surface):
        # Multi-layer fade effect
        for alpha in [5, 10, 20]:
            fade_surface = pygame.Surface((self.width, self.height), pygame.SRCALPHA)
            fade_surface.fill((0, 0, 0, alpha))
            surface.blit(fade_surface, (0, 0))

        for i in range(len(self.drops)):
            # Draw main character with glow
            char = random.choice(self.symbols)
            brightness = self.brightness[i]
            
            # Main character
            color = (0, int(255 * brightness), 0)
            char_surf = FONT.render(char, True, color)
            surface.blit(char_surf, (i * self.font_size, self.drops[i] * self.font_size))
            
            # Glow trail
            trail_length = int(15 * brightness)
            for j in range(1, trail_length):
                if self.drops[i] - j >= 0:
                    trail_alpha = int(255 * (1 - j/trail_length) * brightness)
                    trail_color = (0, trail_alpha, 0)
                    trail_surf = FONT.render(char, True, trail_color)
                    surface.blit(trail_surf, (i * self.font_size, (self.drops[i] - j) * self.font_size))

            # Move drops
            self.drops[i] += self.speeds[i]
            
            # Reset with random conditions
            if self.drops[i] * self.font_size > self.height and random.random() > 0.97:
                self.drops[i] = random.randint(-50, 0)
                self.speeds[i] = random.uniform(0.3, 2.5)
                self.brightness[i] = random.uniform(0.3, 1.0)

# Animated UI Components
class CyberButton:
    def __init__(self, x, y, width, height, text, color=GREEN, icon=""):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.color = color
        self.hover_color = self._adjust_color(color, 30)
        self.current_color = color
        self.is_hovered = False
        self.is_clicked = False
        self.icon = icon
        self.pulse_timer = 0
        self.glow_intensity = 0
        
    def _adjust_color(self, color, amount):
        return tuple(max(0, min(255, c + amount)) for c in color)
        
    def update(self, mouse_pos, mouse_click):
        self.is_hovered = self.rect.collidepoint(mouse_pos)
        self.current_color = self.hover_color if self.is_hovered else self.color
        
        if self.is_hovered:
            self.glow_intensity = min(100, self.glow_intensity + 10)
        else:
            self.glow_intensity = max(0, self.glow_intensity - 5)
            
        self.pulse_timer = (self.pulse_timer + 1) % 60
        
        if mouse_click and self.is_hovered:
            self.is_clicked = True
            return True
        return False
        
    def draw(self, surface):
        # Glow effect
        if self.glow_intensity > 0:
            glow_surf = pygame.Surface((self.rect.width + 20, self.rect.height + 20), pygame.SRCALPHA)
            pygame.draw.rect(glow_surf, (*self.current_color, self.glow_intensity), 
                           (10, 10, self.rect.width, self.rect.height), border_radius=8)
            surface.blit(glow_surf, (self.rect.x - 10, self.rect.y - 10))
        
        # Main button
        pygame.draw.rect(surface, self.current_color, self.rect, border_radius=5)
        pygame.draw.rect(surface, WHITE, self.rect, 2, border_radius=5)
        
        # Pulsing border
        if self.pulse_timer < 30:
            pulse_alpha = int(128 * (self.pulse_timer / 30))
            pulse_surf = pygame.Surface((self.rect.width + 4, self.rect.height + 4), pygame.SRCALPHA)
            pygame.draw.rect(pulse_surf, (*self.current_color, pulse_alpha), 
                           (0, 0, self.rect.width + 4, self.rect.height + 4), 2, border_radius=7)
            surface.blit(pulse_surf, (self.rect.x - 2, self.rect.y - 2))
        
        # Text
        text_surf = FONT.render(self.text, True, WHITE)
        text_rect = text_surf.get_rect(center=self.rect.center)
        surface.blit(text_surf, text_rect)

class AnimatedAlert:
    def __init__(self):
        self.alerts = []
        self.duration = 180  # frames
        
    def add_alert(self, message, alert_type="warning"):
        self.alerts.append({
            "message": message,
            "type": alert_type,
            "timer": self.duration,
            "y_offset": len(self.alerts) * 40
        })
        
    def update(self):
        for alert in self.alerts[:]:
            alert["timer"] -= 1
            if alert["timer"] <= 0:
                self.alerts.remove(alert)
                
    def draw(self, surface):
        for i, alert in enumerate(self.alerts):
            alpha = min(255, alert["timer"] * 2)
            y_pos = 50 + i * 40
            
            # Background
            if alert["type"] == "warning":
                color = (255, 100, 0, alpha)
            elif alert["type"] == "success":
                color = (0, 200, 0, alpha)
            else:
                color = (200, 0, 0, alpha)
                
            alert_surf = pygame.Surface((400, 30), pygame.SRCALPHA)
            pygame.draw.rect(alert_surf, color, (0, 0, 400, 30), border_radius=5)
            pygame.draw.rect(alert_surf, WHITE, (0, 0, 400, 30), 1, border_radius=5)
            
            # Text
            text_surf = SMALL_FONT.render(alert["message"], True, WHITE)
            text_surf.set_alpha(alpha)
            alert_surf.blit(text_surf, (10, 8))
            
            surface.blit(alert_surf, (WIDTH - 420, y_pos))

# Game State Manager
class GameState(Enum):
    MAIN_MENU = "main_menu"
    LANGUAGE_SELECT = "language_select"
    PLAYING = "playing"
    LEVEL_COMPLETE = "level_complete"
    GAME_OVER = "game_over"
    GAME_WON = "game_won"
    UPGRADES = "upgrades"

# Main Game Class
class CyberApexGame:
    def __init__(self):
        self.state = GameState.MAIN_MENU
        self.language = ProgrammingLanguage.PYTHON
        self.ai_assistant = AIAssistant()
        self.particle_system = ParticleSystem()
        self.alert_system = AnimatedAlert()
        self.matrix_rain = CyberMatrix(WIDTH, HEIGHT, FONT_SIZE)
        
        # Player progression
        self.player_level = 1
        self.player_xp = 0
        self.player_credits = 100
        self.skills = {
            "coding": 1,
            "security": 1,
            "stealth": 1,
            "ai_usage": 1
        }
        
        # Game balance
        self.trace_meter = 0
        self.max_trace = 100
        self.current_level_index = 0
        self.user_code_lines = [""]
        self.input_active = True
        self.captured_output = ""
        self.feedback = ""
        
        # Animation timers
        self.cursor_blink_timer = 0
        self.cursor_visible = True
        self.success_timer = 0
        self.global_timer = 0
        self.level_start_time = pygame.time.get_ticks()
        
        # Create UI elements
        self.create_ui_elements()
        
        # Load extensive level system
        self.levels = self.load_levels()
        
    def load_levels(self) -> List[Dict]:
        """Load extensive level system with multiple difficulty tiers"""
        return [
            # TIER 1: Beginner Challenges
            {
                "name": "Gateway Initiation",
                "target": "🌐 Global Bank Login Portal",
                "challenge": "Create a variable 'access_code' with value 'BANK2024' and print it",
                "expected_output": "BANK2024",
                "validation_func": self.validate_variable_creation,
                "time_limit": 45,
                "difficulty": "🟢 NOVICE",
                "xp_reward": 50,
                "credit_reward": 25,
                "trace_penalty": 20,
                "language_syntax": {
                    ProgrammingLanguage.PYTHON: "# Python syntax example\nvariable_name = 'value'",
                    ProgrammingLanguage.JAVASCRIPT: "// JavaScript syntax example\nlet variableName = 'value';",
                    ProgrammingLanguage.JAVA: "// Java syntax example\nString variableName = \"value\";",
                    ProgrammingLanguage.CPP: "// C++ syntax example\nstd::string variableName = \"value\";",
                    ProgrammingLanguage.CSHARP: "// C# syntax example\nstring variableName = \"value\";"
                }
            },
            {
                "name": "Firewall Penetration I",
                "target": "🔥 Cyber Corp Firewall v1.0",
                "challenge": "Write a loop that prints numbers 1 through 5 on separate lines",
                "expected_output": "1\n2\n3\n4\n5",
                "validation_func": self.validate_loop_output,
                "time_limit": 60,
                "difficulty": "🟢 APPRENTICE", 
                "xp_reward": 75,
                "credit_reward": 35,
                "trace_penalty": 25,
                "language_syntax": {
                    ProgrammingLanguage.PYTHON: "for i in range(1, 6):\n    print(i)",
                    ProgrammingLanguage.JAVASCRIPT: "for (let i = 1; i <= 5; i++) {\n    console.log(i);\n}",
                    ProgrammingLanguage.JAVA: "for (int i = 1; i <= 5; i++) {\n    System.out.println(i);\n}",
                    ProgrammingLanguage.CPP: "for (int i = 1; i <= 5; i++) {\n    std::cout << i << std::endl;\n}",
                    ProgrammingLanguage.CSHARP: "for (int i = 1; i <= 5; i++) {\n    Console.WriteLine(i);\n}"
                }
            },
            # TIER 2: Intermediate Challenges  
            {
                "name": "Data Extraction Protocol",
                "target": "💾 NSA Data Vault Alpha",
                "challenge": "Create function 'multiply(a,b)' that returns product, then call multiply(6,7) and print result",
                "expected_output": "42",
                "validation_func": self.validate_function,
                "time_limit": 75,
                "difficulty": "🟡 OPERATIVE",
                "xp_reward": 120,
                "credit_reward": 50,
                "trace_penalty": 35,
                "language_syntax": {
                    ProgrammingLanguage.PYTHON: "def function_name(param1, param2):\n    return param1 + param2",
                    ProgrammingLanguage.JAVASCRIPT: "function functionName(param1, param2) {\n    return param1 + param2;\n}",
                    ProgrammingLanguage.JAVA: "public int functionName(int param1, int param2) {\n    return param1 + param2;\n}",
                    ProgrammingLanguage.CPP: "int functionName(int param1, int param2) {\n    return param1 + param2;\n}",
                    ProgrammingLanguage.CSHARP: "public int FunctionName(int param1, int param2) {\n    return param1 + param2;\n}"
                }
            },
            {
                "name": "Encryption Bypass", 
                "target": "🔒 CIA Crypto Matrix",
                "challenge": "Create list 'targets' with 3 items: 'server1', 'server2', 'server3', then print second element",
                "expected_output": "server2",
                "validation_func": self.validate_list_access,
                "time_limit": 80,
                "difficulty": "🟡 SPECIALIST",
                "xp_reward": 150,
                "credit_reward": 65,
                "trace_penalty": 40,
                "language_syntax": {
                    ProgrammingLanguage.PYTHON: "my_list = ['item1', 'item2', 'item3']\nprint(my_list[1])  # Index 1 is second item",
                    ProgrammingLanguage.JAVASCRIPT: "let myArray = ['item1', 'item2', 'item3'];\nconsole.log(myArray[1]);",
                    ProgrammingLanguage.JAVA: "String[] myArray = {\"item1\", \"item2\", \"item3\"};\nSystem.out.println(myArray[1]);",
                    ProgrammingLanguage.CPP: "std::vector<std::string> myVector = {\"item1\", \"item2\", \"item3\"};\nstd::cout << myVector[1] << std::endl;",
                    ProgrammingLanguage.CSHARP: "string[] myArray = {\"item1\", \"item2\", \"item3\"};\nConsole.WriteLine(myArray[1]);"
                }
            }
        ]
    
    def create_ui_elements(self):
        """Create all UI buttons and elements"""
        # Main menu buttons
        self.menu_buttons = [
            CyberButton(WIDTH//2 - 100, 300, 200, 50, "🚀 START MISSION", GREEN),
            CyberButton(WIDTH//2 - 100, 370, 200, 50, "🌐 SELECT LANGUAGE", BLUE),
            CyberButton(WIDTH//2 - 100, 440, 200, 50, "📊 STATS & UPGRADES", PURPLE),
            CyberButton(WIDTH//2 - 100, 510, 200, 50, "❌ EXIT", RED)
        ]
        
        # Language selection buttons
        self.language_buttons = [
            CyberButton(WIDTH//2 - 250, 200, 200, 50, "🐍 Python", GREEN),
            CyberButton(WIDTH//2 - 250, 270, 200, 50, "🟨 JavaScript", YELLOW),
            CyberButton(WIDTH//2 - 250, 340, 200, 50, "☕ Java", ORANGE),
            CyberButton(WIDTH//2 - 250, 410, 200, 50, "⚡ C++", BLUE),
            CyberButton(WIDTH//2 - 250, 480, 200, 50, "🔷 C#", MAGENTA),
            CyberButton(WIDTH//2 - 250, 550, 200, 50, "🔙 Back", RED)
        ]
        
        # Gameplay buttons
        self.game_buttons = [
            CyberButton(WIDTH - 220, HEIGHT - 180, 200, 40, "🚀 SUBMIT CODE", GREEN),
            CyberButton(WIDTH - 220, HEIGHT - 130, 200, 40, "🤖 HACKER EYE (5¢)", BLUE),
            CyberButton(WIDTH - 220, HEIGHT - 80, 200, 40, "🔧 AUTO FIX (10¢)", ORANGE),
            CyberButton(20, HEIGHT - 80, 200, 40, "🏃 ESCAPE", RED)
        ]
    
    # Validation functions for different challenge types
    def validate_variable_creation(self, local_scope, captured_output):
        return ('access_code' in local_scope and 
                local_scope['access_code'] == 'BANK2024' and 
                captured_output.strip() == 'BANK2024')

    def validate_loop_output(self, local_scope, captured_output):
        return captured_output.strip() == "1\n2\n3\n4\n5"

    def validate_function(self, local_scope, captured_output):
        return ('multiply' in local_scope and 
                callable(local_scope['multiply']) and 
                local_scope['multiply'](6, 7) == 42 and 
                captured_output.strip() == '42')

    def validate_list_access(self, local_scope, captured_output):
        return ('targets' in local_scope and 
                len(local_scope['targets']) == 3 and 
                captured_output.strip() == 'server2')

    def handle_input(self, event):
        """Handle keyboard input for code editing"""
        if self.state != GameState.PLAYING or not self.input_active:
            return

        if event.key == pygame.K_RETURN:
            self.user_code_lines.append("")
        elif event.key == pygame.K_BACKSPACE:
            if self.user_code_lines and self.user_code_lines[-1]:
                self.user_code_lines[-1] = self.user_code_lines[-1][:-1]
            elif len(self.user_code_lines) > 1:
                self.user_code_lines.pop()
        elif event.key == pygame.K_TAB:
            self.user_code_lines[-1] += "    "
        else:
            self.user_code_lines[-1] += event.unicode
            
        self.cursor_blink_timer = 0

    def submit_code(self):
        """Execute and validate user code"""
        full_code = "\n".join(self.user_code_lines)
        level = self.levels[self.current_level_index]
        
        local_scope = {}
        self.captured_output = ""

        try:
            with self.capture_stdout() as stdout:
                # Enhanced security for code execution
                safe_builtins = {
                    'print': print,
                    'len': len,
                    'str': str,
                    'int': int,
                    'range': range
                }
                exec(full_code, {"__builtins__": safe_builtins}, local_scope)
            self.captured_output = stdout.getvalue().strip()
            
            validation_func = level["validation_func"]
            if validation_func(local_scope, self.captured_output):
                self.handle_success()
            else:
                self.handle_failure("Logic error in implementation")
                
        except SyntaxError as e:
            self.handle_failure(f"Syntax error: {e}")
        except Exception as e:
            self.handle_failure(f"Runtime error: {e}")

    def handle_success(self):
        """Handle successful level completion"""
        level = self.levels[self.current_level_index]
        
        # Rewards
        self.player_xp += level["xp_reward"]
        self.player_credits += level["credit_reward"]
        
        # Visual effects
        self.particle_system.add_particles(WIDTH//2, HEIGHT//2, 50, "explosion")
        self.alert_system.add_alert(f"ACCESS GRANTED! +{level['xp_reward']} XP", "success")
        
        self.feedback = f"🎉 SYSTEM BREACHED! +{level['xp_reward']} XP"
        self.success_timer = 180
        self.input_active = False
        
        # Check for level up
        if self.player_xp >= self.player_level * 100:
            self.player_level += 1
            self.alert_system.add_alert(f"LEVEL UP! Now level {self.player_level}", "success")

    def handle_failure(self, error_msg):
        """Handle code execution failure"""
        level = self.levels[self.current_level_index]
        
        self.trace_meter += level["trace_penalty"]
        self.feedback = f"❌ {error_msg}. Trace +{level['trace_penalty']}%"
        self.alert_system.add_alert(f"SECURITY ALERT! Trace level increased", "warning")
        
        if self.trace_meter >= self.max_trace:
            self.state = GameState.GAME_OVER

    def use_hacker_eye(self):
        """Use AI assistant for a hint"""
        if self.player_credits >= 5:
            self.player_credits -= 5
            level = self.levels[self.current_level_index]
            hint = self.ai_assistant.get_hint(
                level["challenge"], 
                "\n".join(self.user_code_lines), 
                self.language
            )
            self.alert_system.add_alert(f"🤖 HINT: {hint}", "success")
            self.particle_system.add_particles(WIDTH - 100, HEIGHT - 150, 20, "spark")
        else:
            self.alert_system.add_alert("Insufficient credits for Hacker Eye!", "warning")

    def use_auto_fix(self):
        """Use AI to automatically fix code"""
        if self.player_credits >= 10:
            self.player_credits -= 10
            level = self.levels[self.current_level_index]
            fixed_code = self.ai_assistant.fix_code(
                level["challenge"],
                "\n".join(self.user_code_lines),
                self.feedback,
                self.language
            )
            self.user_code_lines = fixed_code.split('\n')
            self.alert_system.add_alert("AI fix applied! Code has been corrected.", "success")
            self.particle_system.add_particles(WIDTH - 100, HEIGHT - 100, 30, "spark")
        else:
            self.alert_system.add_alert("Insufficient credits for Auto Fix!", "warning")

    @contextlib.contextmanager
    def capture_stdout(self):
        """Capture standard output for code execution"""
        old_stdout = sys.stdout
        new_stdout = io.StringIO()
        sys.stdout = new_stdout
        try:
            yield new_stdout
        finally:
            sys.stdout = old_stdout

    def update(self):
        """Update game state"""
        self.global_timer += 1
        self.particle_system.update()
        self.alert_system.update()
        
        # Update cursor blink
        self.cursor_blink_timer += 1
        if self.cursor_blink_timer >= 30:
            self.cursor_visible = not self.cursor_visible
            self.cursor_blink_timer = 0
            
        # Handle success animation
        if self.success_timer > 0:
            self.success_timer -= 1
            if self.success_timer == 0:
                self.current_level_index += 1
                if self.current_level_index >= len(self.levels):
                    self.state = GameState.GAME_WON
                else:
                    self.reset_level()
                    
        # Update buttons based on state
        mouse_pos = pygame.mouse.get_pos()
        mouse_click = pygame.mouse.get_pressed()[0]
        
        if self.state == GameState.MAIN_MENU:
            for button in self.menu_buttons:
                if button.update(mouse_pos, mouse_click):
                    self.handle_menu_click(button.text)
                    
        elif self.state == GameState.LANGUAGE_SELECT:
            for button in self.language_buttons:
                if button.update(mouse_pos, mouse_click):
                    self.handle_language_click(button.text)
                    
        elif self.state == GameState.PLAYING:
            for button in self.game_buttons:
                if button.update(mouse_pos, mouse_click):
                    self.handle_game_click(button.text)

    def handle_menu_click(self, button_text):
        """Handle main menu button clicks"""
        if "START" in button_text:
            self.state = GameState.PLAYING
            self.reset_level()
        elif "LANGUAGE" in button_text:
            self.state = GameState.LANGUAGE_SELECT
        elif "STATS" in button_text:
            self.state = GameState.UPGRADES
        elif "EXIT" in button_text:
            pygame.quit()
            sys.exit()

    def handle_language_click(self, button_text):
        """Handle language selection"""
        language_map = {
            "🐍 Python": ProgrammingLanguage.PYTHON,
            "🟨 JavaScript": ProgrammingLanguage.JAVASCRIPT, 
            "☕ Java": ProgrammingLanguage.JAVA,
            "⚡ C++": ProgrammingLanguage.CPP,
            "🔷 C#": ProgrammingLanguage.CSHARP
        }
        
        if button_text in language_map:
            self.language = language_map[button_text]
            self.alert_system.add_alert(f"Language set to {self.language.value}", "success")
        elif "Back" in button_text:
            self.state = GameState.MAIN_MENU

    def handle_game_click(self, button_text):
        """Handle gameplay button clicks"""
        if "SUBMIT" in button_text:
            self.submit_code()
        elif "HACKER EYE" in button_text:
            self.use_hacker_eye()
        elif "AUTO FIX" in button_text:
            self.use_auto_fix()
        elif "ESCAPE" in button_text:
            self.state = GameState.MAIN_MENU

    def reset_level(self):
        """Reset current level state"""
        self.user_code_lines = [""]
        self.feedback = ""
        self.captured_output = ""
        self.input_active = True
        self.level_start_time = pygame.time.get_ticks()

    def draw(self, surface):
        """Draw complete game state"""
        surface.fill(BLACK)
        self.matrix_rain.draw(surface)
        self.particle_system.draw(surface)
        self.alert_system.draw(surface)
        
        if self.state == GameState.MAIN_MENU:
            self.draw_main_menu(surface)
        elif self.state == GameState.LANGUAGE_SELECT:
            self.draw_language_select(surface)
        elif self.state == GameState.PLAYING:
            self.draw_gameplay(surface)
        elif self.state == GameState.GAME_OVER:
            self.draw_game_over(surface)
        elif self.state == GameState.GAME_WON:
            self.draw_game_won(surface)
        elif self.state == GameState.UPGRADES:
            self.draw_upgrades(surface)

    def draw_main_menu(self, surface):
        """Draw main menu screen"""
        # Title
        title = TITLE_FONT.render("🔥 CYBER APEX", True, GREEN)
        subtitle = HEADER_FONT.render("Global Domination Protocol", True, CYAN)
        surface.blit(title, (WIDTH//2 - title.get_width()//2, 150))
        surface.blit(subtitle, (WIDTH//2 - subtitle.get_width()//2, 200))
        
        # Player info
        info_text = FONT.render(f"Level {self.player_level} | XP: {self.player_xp} | Credits: {self.player_credits}¢", True, WHITE)
        surface.blit(info_text, (WIDTH//2 - info_text.get_width()//2, 250))
        
        # Draw buttons
        for button in self.menu_buttons:
            button.draw(surface)

    def draw_language_select(self, surface):
        """Draw language selection screen"""
        title = TITLE_FONT.render("Select Programming Language", True, GREEN)
        surface.blit(title, (WIDTH//2 - title.get_width()//2, 100))
        
        current_lang = HEADER_FONT.render(f"Current: {self.language.value}", True, YELLOW)
        surface.blit(current_lang, (WIDTH//2 - current_lang.get_width()//2, 150))
        
        for button in self.language_buttons:
            button.draw(surface)

    def draw_gameplay(self, surface):
        """Draw main gameplay screen"""
        level = self.levels[self.current_level_index]
        
        # Header section
        self.draw_game_header(surface, level)
        
        # Code editor section
        self.draw_code_editor(surface)
        
        # Output and feedback section
        self.draw_output_section(surface)
        
        # Game buttons
        for button in self.game_buttons:
            button.draw(surface)
            
        # Syntax helper
        self.draw_syntax_helper(surface, level)

    def draw_game_header(self, surface, level):
        """Draw game header with level info"""
        # Mission info
        target_text = HEADER_FONT.render(f"🎯 TARGET: {level['target']}", True, GREEN)
        difficulty_text = FONT.render(f"DIFFICULTY: {level['difficulty']}", True, YELLOW)
        challenge_text = FONT.render(f"OBJECTIVE: {level['challenge']}", True, CYAN)
        
        surface.blit(target_text, (20, 20))
        surface.blit(difficulty_text, (WIDTH - 250, 25))
        surface.blit(challenge_text, (20, 60))
        
        # Progress and stats
        progress_text = FONT.render(f"MISSION: {self.current_level_index + 1}/{len(self.levels)}", True, WHITE)
        trace_text = FONT.render(f"TRACE: {self.trace_meter}%", True, RED if self.trace_meter > 70 else YELLOW)
        language_text = FONT.render(f"LANG: {self.language.value}", True, BLUE)
        
        surface.blit(progress_text, (WIDTH - 250, 60))
        surface.blit(trace_text, (WIDTH - 250, 85))
        surface.blit(language_text, (WIDTH - 250, 110))
        
        # Trace meter
        pygame.draw.rect(surface, DARK_GREEN, (WIDTH - 250, 140, 230, 20), border_radius=3)
        trace_width = (self.trace_meter / self.max_trace) * 230
        pygame.draw.rect(surface, RED, (WIDTH - 250, 140, trace_width, 20), border_radius=3)
        
        # Time display
        if self.input_active:
            time_left = max(0, level['time_limit'] - (pygame.time.get_ticks() - self.level_start_time) / 1000)
            time_color = RED if time_left < 10 else YELLOW if time_left < 30 else GREEN
            time_text = FONT.render(f"TIME: {int(time_left)}s", True, time_color)
            surface.blit(time_text, (WIDTH - 250, 170))

    def draw_code_editor(self, surface):
        """Draw code editor with syntax highlighting"""
        # Editor background
        editor_rect = pygame.Rect(20, 120, WIDTH - 40, HEIGHT - 350)
        pygame.draw.rect(surface, (10, 20, 10), editor_rect, border_radius=8)
        pygame.draw.rect(surface, GREEN, editor_rect, 2, border_radius=8)
        
        # Line numbers and code
        for i, line in enumerate(self.user_code_lines):
            # Line number
            line_color = (100, 150, 100) if i % 5 == 0 else (80, 120, 80)
            line_num = FONT.render(f"{i+1:3d}", True, line_color)
            surface.blit(line_num, (30, 130 + i * FONT_SIZE))
            
            # Code line with basic syntax highlighting
            words = line.split(' ')
            x_offset = 80
            for word in words:
                if word in ['def', 'class', 'for', 'while', 'if', 'else']:
                    color = MAGENTA
                elif word in ['print', 'return']:
                    color = YELLOW
                elif word.startswith("'") or word.startswith('"'):
                    color = GREEN
                elif word.isdigit():
                    color = CYAN
                else:
                    color = WHITE
                    
                word_surf = FONT.render(word + ' ', True, color)
                surface.blit(word_surf, (x_offset, 130 + i * FONT_SIZE))
                x_offset += word_surf.get_width()
        
        # Cursor
        if self.input_active and self.cursor_visible:
            cursor_x = 80 + FONT.size(self.user_code_lines[-1])[0]
            cursor_y = 130 + (len(self.user_code_lines) - 1) * FONT_SIZE
            pygame.draw.line(surface, GREEN, (cursor_x, cursor_y), (cursor_x, cursor_y + FONT_SIZE), 2)

    def draw_output_section(self, surface):
        """Draw output and feedback section"""
        # Output box
        output_rect = pygame.Rect(20, HEIGHT - 220, WIDTH - 40, 80)
        pygame.draw.rect(surface, (20, 20, 30), output_rect, border_radius=8)
        pygame.draw.rect(surface, BLUE, output_rect, 2, border_radius=8)
        
        output_title = FONT.render("💻 PROGRAM OUTPUT:", True, BLUE)
        surface.blit(output_title, (30, HEIGHT - 210))
        
        output_lines = self.captured_output.split('\n') if self.captured_output else ["No output yet..."]
        for i, line in enumerate(output_lines[:3]):
            output_text = FONT.render(line, True, WHITE)
            surface.blit(output_text, (30, HEIGHT - 180 + i * 20))
        
        # Feedback box
        feedback_rect = pygame.Rect(20, HEIGHT - 120, WIDTH - 40, 40)
        feedback_color = GREEN if "GRANTED" in self.feedback else RED if "ERROR" in self.feedback else YELLOW
        pygame.draw.rect(surface, (30, 20, 20), feedback_rect, border_radius=8)
        pygame.draw.rect(surface, feedback_color, feedback_rect, 2, border_radius=8)
        
        feedback_text = FONT.render(self.feedback, True, feedback_color)
        surface.blit(feedback_text, (30, HEIGHT - 110))

    def draw_syntax_helper(self, surface, level):
        """Draw syntax helper for current language"""
        helper_rect = pygame.Rect(WIDTH - 320, 200, 300, 300)
        pygame.draw.rect(surface, (20, 30, 40), helper_rect, border_radius=8)
        pygame.draw.rect(surface, PURPLE, helper_rect, 2, border_radius=8)
        
        helper_title = FONT.render(f"📚 {self.language.value} SYNTAX HELP:", True, PURPLE)
        surface.blit(helper_title, (WIDTH - 310, 210))
        
        syntax_example = level["language_syntax"][self.language]
        syntax_lines = syntax_example.split('\n')
        
        for i, line in enumerate(syntax_lines[:8]):
            syntax_text = SMALL_FONT.render(line, True, (200, 200, 255))
            surface.blit(syntax_text, (WIDTH - 310, 240 + i * 18))

    def draw_game_over(self, surface):
        """Draw game over screen"""
        overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 200))
        surface.blit(overlay, (0, 0))
        
        title = TITLE_FONT.render("💀 MISSION FAILED", True, RED)
        reason = HEADER_FONT.render("Trace level reached 100% - You've been detected!", True, YELLOW)
        stats = FONT.render(f"Progress: {self.current_level_index}/{len(self.levels)} levels | Total XP: {self.player_xp}", True, WHITE)
        
        surface.blit(title, (WIDTH//2 - title.get_width()//2, HEIGHT//2 - 100))
        surface.blit(reason, (WIDTH//2 - reason.get_width()//2, HEIGHT//2 - 40))
        surface.blit(stats, (WIDTH//2 - stats.get_width()//2, HEIGHT//2))
        
        # Restart button
        restart_btn = CyberButton(WIDTH//2 - 100, HEIGHT//2 + 80, 200, 50, "🔄 RESTART MISSION", GREEN)
        menu_btn = CyberButton(WIDTH//2 - 100, HEIGHT//2 + 150, 200, 50, "📋 MAIN MENU", BLUE)
        
        mouse_pos = pygame.mouse.get_pos()
        mouse_click = pygame.mouse.get_pressed()[0]
        
        if restart_btn.update(mouse_pos, mouse_click):
            self.__init__()  # Complete reset
        if menu_btn.update(mouse_pos, mouse_click):
            self.state = GameState.MAIN_MENU
            
        restart_btn.draw(surface)
        menu_btn.draw(surface)

    def draw_game_won(self, surface):
        """Draw game completion screen"""
        overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
        overlay.fill((0, 20, 0, 200))
        surface.blit(overlay, (0, 0))
        
        title = TITLE_FONT.render("🏆 GLOBAL DOMINATION ACHIEVED!", True, GREEN)
        subtitle = HEADER_FONT.render("All systems breached. You are the ultimate hacker!", True, YELLOW)
        stats = FONT.render(f"Final Score: {self.player_xp} XP | Level {self.player_level} | Credits: {self.player_credits}¢", True, CYAN)
        
        surface.blit(title, (WIDTH//2 - title.get_width()//2, HEIGHT//2 - 120))
        surface.blit(subtitle, (WIDTH//2 - subtitle.get_width()//2, HEIGHT//2 - 60))
        surface.blit(stats, (WIDTH//2 - stats.get_width()//2, HEIGHT//2 - 20))
        
        # Celebration particles
        if random.random() < 0.3:
            self.particle_system.add_particles(random.randint(0, WIDTH), random.randint(0, HEIGHT), 10, "explosion")

    def draw_upgrades(self, surface):
        """Draw stats and upgrades screen"""
        title = TITLE_FONT.render("📊 HACKER PROFILE & UPGRADES", True, GREEN)
        surface.blit(title, (WIDTH//2 - title.get_width()//2, 50))
        
        # Player stats
        stats_y = 120
        stats = [
            f"🔰 Level: {self.player_level}",
            f"⭐ XP: {self.player_xp}",
            f"💰 Credits: {self.player_credits}¢",
            f"🎯 Missions Completed: {self.current_level_index}/{len(self.levels)}",
            f"🛡️ Trace Level: {self.trace_meter}%"
        ]
        
        for stat in stats:
            stat_text = HEADER_FONT.render(stat, True, WHITE)
            surface.blit(stat_text, (100, stats_y))
            stats_y += 50
            
        # Back button
        back_btn = CyberButton(WIDTH//2 - 100, HEIGHT - 100, 200, 50, "🔙 BACK", BLUE)
        mouse_pos = pygame.mouse.get_pos()
        mouse_click = pygame.mouse.get_pressed()[0]
        
        if back_btn.update(mouse_pos, mouse_click):
            self.state = GameState.MAIN_MENU
        back_btn.draw(surface)

# Main game loop
def main():
    game = CyberApexGame()
    running = True
    
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if game.state == GameState.PLAYING:
                    game.handle_input(event)
        
        game.update()
        game.draw(screen)
        
        pygame.display.flip()
        clock.tick(60)
    
    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()