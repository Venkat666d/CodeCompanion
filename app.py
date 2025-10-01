# app.py
import customtkinter as ctk
from main import AIEngine
import threading
import subprocess
import sys
import time
from typing import List, Tuple

class AnimatedButton(ctk.CTkButton):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.original_color = self.cget("fg_color")
        self.hover_color = self.cget("hover_color")
        self.is_animating = False
        
    def pulse_animation(self):
        if self.is_animating:
            return
            
        self.is_animating = True
        def animate_step(step=0):
            if step < 10 and self.is_animating:
                if step % 2 == 0:
                    self.configure(fg_color=self.hover_color)
                else:
                    self.configure(fg_color=self.original_color)
                self.after(100, lambda: animate_step(step + 1))
            else:
                self.configure(fg_color=self.original_color)
                self.is_animating = False
                
        animate_step()
        
    def stop_animation(self):
        self.is_animating = False
        self.configure(fg_color=self.original_color)

class CodeCompanionApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("CodeCompanion - The Ultimate AI Tutor")
        self.geometry("1200x900")
        ctk.set_appearance_mode("Dark")
        ctk.set_default_color_theme("blue")

        self.ai_engine = AIEngine()
        self.is_generating = False
        self.stop_requested = False
        self.typing_job = None
        self.current_concept = None
        self.animated_buttons = []
        self.last_user_message = ""  # Store the last user message for progress tracking

        # Configure grid
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)

        # Main container with gradient background
        self.main_container = ctk.CTkFrame(self, corner_radius=20)
        self.main_container.grid(row=0, column=0, padx=20, pady=20, sticky="nsew")
        self.main_container.grid_columnconfigure(0, weight=1)
        self.main_container.grid_rowconfigure(3, weight=1)
        self.main_container.grid_rowconfigure(5, weight=1)

        # Header with animated title
        self.header_frame = ctk.CTkFrame(self.main_container, fg_color="transparent")
        self.header_frame.grid(row=0, column=0, padx=20, pady=(20, 10), sticky="ew")
        
        self.title_label = ctk.CTkLabel(
            self.header_frame, 
            text="🚀 CodeCompanion AI Tutor", 
            font=("Arial", 24, "bold"),
            text_color="#4FC3F7"
        )
        self.title_label.grid(row=0, column=0, sticky="w")
        
        self.subtitle_label = ctk.CTkLabel(
            self.header_frame,
            text="Your Personal Programming Mentor",
            font=("Arial", 14),
            text_color="#B3E5FC"
        )
        self.subtitle_label.grid(row=1, column=0, sticky="w", pady=(0, 10))

        # Concept Selection with modern design
        self.concept_frame = ctk.CTkFrame(self.main_container, corner_radius=15)
        self.concept_frame.grid(row=1, column=0, padx=20, pady=10, sticky="ew")
        self.concept_frame.grid_columnconfigure(1, weight=1)
        
        ctk.CTkLabel(
            self.concept_frame, 
            text="🎯 Select Learning Topic:", 
            font=("Arial", 16, "bold")
        ).grid(row=0, column=0, padx=15, pady=15, sticky="w")
        
        self.concept_var = ctk.StringVar(value="Select a concept")
        concepts = self.ai_engine.get_concept_list()
        self.concept_optionmenu = ctk.CTkOptionMenu(
            self.concept_frame, 
            values=concepts, 
            variable=self.concept_var,
            command=self.on_concept_selected,
            dropdown_font=("Arial", 14),
            corner_radius=10,
            fg_color="#2B2B2B",
            button_color="#4FC3F7",
            button_hover_color="#29B6F6"
        )
        self.concept_optionmenu.grid(row=0, column=1, padx=15, pady=15, sticky="ew")

        # Button Grid with modern layout
        self.button_frame = ctk.CTkFrame(self.main_container, fg_color="transparent")
        self.button_frame.grid(row=2, column=0, padx=20, pady=10, sticky="ew")
        self.button_frame.grid_columnconfigure((0,1,2,3), weight=1)

        # Explanation buttons with icons and animations
        button_configs = [
            ("😂 Funny Example", "Funny Real-World Example", "#FF9800"),
            ("🔧 Technical Definition", "Technical Definition", "#2196F3"),
            ("📝 Pseudocode", "Pseudocode Example", "#4CAF50"),
            ("📚 Comprehensive", "Comprehensive Explanation", "#9C27B0"),
            ("🌐 Wikipedia", "Wikipedia Search", "#00BCD4"),
            ("📖 Documentation", "Documentation", "#607D8B"),
            ("⚡ Syntax", "Syntax", "#FF5722")
        ]

        self.explanation_buttons = []
        for i, (text, command, color) in enumerate(button_configs):
            row, col = i // 4, i % 4
            btn = AnimatedButton(
                self.button_frame,
                text=text,
                command=lambda cmd=command: self.trigger_explanation(cmd),
                state="disabled",
                fg_color=color,
                hover_color=self.adjust_brightness(color, -20),
                font=("Arial", 12, "bold"),
                corner_radius=10,
                height=40
            )
            btn.grid(row=row, column=col, padx=5, pady=5, sticky="ew")
            self.explanation_buttons.append(btn)
            self.animated_buttons.append(btn)

        # Game Launch Button
        self.btn_hacker_game = AnimatedButton(
            self.button_frame,
            text="🎮 Launch Hacker Challenge",
            command=lambda: self.launch_game("hacker_game.py"),
            fg_color="#6C3483",
            hover_color="#5B2C6F",
            font=("Arial", 12, "bold"),
            corner_radius=10,
            height=40
        )
        self.btn_hacker_game.grid(row=1, column=3, padx=5, pady=5, sticky="ew")
        self.animated_buttons.append(self.btn_hacker_game)

        # Stop button (hidden initially)
        self.stop_button = ctk.CTkButton(
            self.button_frame,
            text="⏹️ Stop Generating",
            command=self.stop_generation,
            fg_color="#C0392B",
            hover_color="#A93226",
            font=("Arial", 12, "bold"),
            corner_radius=10,
            height=40
        )

        # Tabview for Explanation and Chat
        self.tabview = ctk.CTkTabview(self.main_container, corner_radius=15)
        self.tabview.grid(row=3, column=0, padx=20, pady=10, sticky="nsew")
        self.tabview.add("💡 Explanation")
        self.tabview.add("💬 Chat Session")
        self.tabview.add("🎯 Learning Progress")

        # Explanation Display with enhanced styling
        self.explanation_display = ctk.CTkTextbox(
            self.tabview.tab("💡 Explanation"), 
            state="disabled", 
            font=("Consolas", 14),
            wrap="word",
            corner_radius=10,
            fg_color="#1E1E1E",
            scrollbar_button_color="#4FC3F7"
        )
        self.explanation_display.pack(fill="both", expand=True, padx=10, pady=10)

        # Chat Log Display
        self.chat_log_display = ctk.CTkTextbox(
            self.tabview.tab("💬 Chat Session"),
            state="disabled",
            font=("Arial", 14),
            wrap="word",
            corner_radius=10,
            fg_color="#1E1E1E",
            scrollbar_button_color="#4FC3F7"
        )
        self.chat_log_display.pack(fill="both", expand=True, padx=10, pady=10)

        # Progress Tracking
        self.progress_frame = ctk.CTkFrame(self.tabview.tab("🎯 Learning Progress"), fg_color="transparent")
        self.progress_frame.pack(fill="both", expand=True, padx=10, pady=10)
        
        self.progress_label = ctk.CTkLabel(
            self.progress_frame,
            text="Your Learning Journey",
            font=("Arial", 16, "bold")
        )
        self.progress_label.pack(pady=10)
        
        self.progress_text = ctk.CTkTextbox(
            self.progress_frame,
            state="disabled",
            font=("Arial", 12),
            height=100
        )
        self.progress_text.pack(fill="both", expand=True)

        # Chat Input with modern design
        self.chat_input_frame = ctk.CTkFrame(self.main_container, corner_radius=15)
        self.chat_input_frame.grid(row=4, column=0, padx=20, pady=10, sticky="ew")
        self.chat_input_frame.grid_columnconfigure(0, weight=1)
        
        self.chat_user_input = ctk.CTkEntry(
            self.chat_input_frame,
            placeholder_text="💭 Ask a follow-up question...",
            font=("Arial", 14),
            state="disabled",
            corner_radius=10,
            height=40
        )
        self.chat_user_input.grid(row=0, column=0, padx=10, pady=10, sticky="ew")
        self.chat_user_input.bind("<Return>", self.send_chat_message)
        
        self.chat_send_button = ctk.CTkButton(
            self.chat_input_frame,
            text="Send 🚀",
            command=self.send_chat_message,
            state="disabled",
            fg_color="#4FC3F7",
            hover_color="#29B6F6",
            font=("Arial", 14, "bold"),
            corner_radius=10,
            height=40
        )
        self.chat_send_button.grid(row=0, column=1, padx=10, pady=10)

        # Status bar
        self.status_bar = ctk.CTkLabel(
            self.main_container,
            text="Ready to learn! Select a concept to begin your programming journey.",
            font=("Arial", 12),
            text_color="#81D4FA"
        )
        self.status_bar.grid(row=5, column=0, padx=20, pady=10, sticky="ew")

        # Initial message with typing animation
        self.after(1000, lambda: self.animate_welcome_message())
        
    def adjust_brightness(self, hex_color, factor):
        """Adjust color brightness"""
        hex_color = hex_color.lstrip('#')
        rgb = tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))
        new_rgb = tuple(max(0, min(255, c + factor)) for c in rgb)
        return f"#{new_rgb[0]:02x}{new_rgb[1]:02x}{new_rgb[2]:02x}"

    def animate_welcome_message(self):
        welcome_text = "🚀 Welcome to CodeCompanion! Select a learning topic to begin your programming adventure."
        self.stream_response(self.explanation_display, welcome_text, append=False)

    def launch_game(self, game_script_name):
        python_executable = sys.executable
        try:
            if game_script_name == "game_app.py":
                self.display_message(self.explanation_display, "🎮 The Boss Battle game is coming soon! For now, please enjoy the Hacker Challenge.")
                return
            
            # Animate game launch
            self.btn_hacker_game.pulse_animation()
            self.after(500, lambda: subprocess.Popen([python_executable, game_script_name]))
            
        except FileNotFoundError:
            self.display_message(self.explanation_display, f"❌ Error: {game_script_name} not found. Make sure it's in the same folder.")

    def on_concept_selected(self, choice):
        if choice == "Select a concept":
            return
            
        self.current_concept = choice
        self.enable_all_buttons()
        self.ai_engine.reset_chat_context(choice)
        
        # Update progress
        self.update_progress(f"Started learning: {choice}")
        
        # Animate concept selection
        for btn in self.animated_buttons:
            btn.pulse_animation()
            
        self.display_message(self.explanation_display, f"🎯 You selected '{choice}'. Choose an explanation style or ask follow-up questions!")
        self.clear_chat_log()
        self.status_bar.configure(text=f"Learning: {choice} - Ready for explanations!")

    def trigger_explanation(self, explanation_type):
        concept = self.concept_var.get()
        if concept == "Select a concept": 
            return
            
        # Animate the clicked button
        for btn in self.explanation_buttons:
            if explanation_type in btn.cget("text"):
                btn.pulse_animation()
                break
                
        self.start_thinking()
        threading.Thread(target=self._call_ai_and_stream, args=(concept, explanation_type), daemon=True).start()

    def send_chat_message(self, event=None):
        user_text = self.chat_user_input.get().strip()
        if not user_text or self.is_generating: 
            return
        
        # Store the user message for progress tracking
        self.last_user_message = user_text
            
        self.display_message(self.chat_log_display, f"👤 You: {user_text}", append=True)
        self.chat_user_input.delete(0, "end")
        self.start_thinking()
        threading.Thread(target=self._call_ai_chat_and_stream, args=(user_text,), daemon=True).start()

    def _call_ai_and_stream(self, concept, explanation_type):
        try:
            response = self.ai_engine.get_explanation(concept, explanation_type)
            self.after(0, lambda: self._display_explanation(response))
        except Exception as e:
            self.after(0, lambda: self._display_explanation(f"❌ Error: {str(e)}"))

    def _display_explanation(self, response):
        """Display explanation in main thread"""
        self.stream_response(self.explanation_display, f"🤖 {response}")
        self.update_progress(f"Viewed explanation for {self.concept_var.get()}")

    def _call_ai_chat_and_stream(self, user_text):
        try:
            response = self.ai_engine.chat_with_ai(user_text)
            self.after(0, lambda: self._display_chat_response(response, user_text))
        except Exception as e:
            self.after(0, lambda: self._display_chat_response(f"❌ Error: {str(e)}", user_text))

    def _display_chat_response(self, response, user_text=""):
        """Display chat response in main thread"""
        self.stream_response(self.chat_log_display, f"🤖 {response}", append=True)
        if user_text:
            self.update_progress(f"Chatted about: {user_text[:50]}...")
        else:
            self.update_progress("Chatted with AI assistant")

    def start_thinking(self):
        self.is_generating = True
        self.stop_requested = False
        self.disable_all_buttons()
        
        # Show thinking animation
        self.status_bar.configure(text="🤔 AI is thinking...")
        
        # Hide game button, show stop button
        self.btn_hacker_game.grid_forget()
        self.stop_button.grid(row=1, column=3, padx=5, pady=5, sticky="ew")

    def stop_generation(self):
        self.stop_requested = True
        if self.typing_job:
            self.after_cancel(self.typing_job)
        self.finish_generation()
        self.status_bar.configure(text="⏹️ Generation stopped")

    def stream_response(self, textbox, full_text, append=False):
        if self.stop_requested:
            textbox.configure(state="disabled")
            return
            
        textbox.configure(state="normal")
        
        if not append:
            textbox.delete("1.0", "end")
        
        def type_text(index=0):
            if index < len(full_text) and not self.stop_requested:
                textbox.insert("end", full_text[index])
                textbox.see("end")
                self.typing_job = self.after(10, lambda: type_text(index + 1))
            else:
                if append:
                    textbox.insert("end", "\n\n")
                textbox.see("end")
                textbox.configure(state="disabled")
                self.typing_job = None
                self.finish_generation()
        
        type_text()

    def finish_generation(self):
        self.is_generating = False
        self.stop_requested = False
        self.enable_all_buttons()
        
        # Hide stop button, show game button
        self.stop_button.grid_forget()
        self.btn_hacker_game.grid(row=1, column=3, padx=5, pady=5, sticky="ew")
        
        self.status_bar.configure(text="✅ Ready for your next question!")

    def display_message(self, textbox, message, append=False):
        textbox.configure(state="normal")
        if not append:
            textbox.delete("1.0", "end")
        textbox.insert("end", message + "\n\n")
        textbox.configure(state="disabled")
        textbox.see("end")
    
    def clear_chat_log(self):
        self.chat_log_display.configure(state="normal")
        self.chat_log_display.delete("1.0", "end")
        self.chat_log_display.configure(state="disabled")
    
    def update_progress(self, activity):
        self.progress_text.configure(state="normal")
        timestamp = time.strftime("%H:%M:%S")
        self.progress_text.insert("end", f"[{timestamp}] {activity}\n")
        self.progress_text.see("end")
        self.progress_text.configure(state="disabled")
    
    def enable_all_buttons(self):
        if self.concept_var.get() != "Select a concept":
            for btn in self.explanation_buttons:
                btn.configure(state="normal")
            self.chat_user_input.configure(state="normal")
            self.chat_send_button.configure(state="normal")
        else:
            for btn in self.explanation_buttons:
                btn.configure(state="disabled")
            self.chat_user_input.configure(state="disabled")
            self.chat_send_button.configure(state="disabled")
        
        self.btn_hacker_game.configure(state="normal")

    def disable_all_buttons(self):
        for btn in self.explanation_buttons:
            btn.configure(state="disabled")
        self.chat_user_input.configure(state="disabled")
        self.chat_send_button.configure(state="disabled")
        self.btn_hacker_game.configure(state="disabled")


if __name__ == "__main__":
    app = CodeCompanionApp()
    app.mainloop()