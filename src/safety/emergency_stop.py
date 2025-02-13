"""
Emergency Stop System for Web UI
"""

import os
import sys
import json
import signal
import keyboard
import threading
import tkinter as tk
from typing import Callable, List
from pathlib import Path


class EmergencyStop:
    _instance = None
    _lock = threading.Lock()

    def __new__(cls):
        with cls._lock:
            if cls._instance is None:
                cls._instance = super().__new__(cls)
            return cls._instance

    def __init__(self):
        if not hasattr(self, "initialized"):
            self.initialized = True
            self.stop_handlers: List[Callable] = []
            self.is_stopped = False
            self.overlay_window = None
            self.hotkey = "ctrl+shift+x"  # Default emergency stop hotkey

            # Set up the keyboard hook
            keyboard.add_hotkey(self.hotkey, self.trigger_stop)

            # Create overlay window
            self.create_overlay()

    def create_overlay(self):
        """Create an always-on-top overlay window with emergency stop button"""
        self.overlay_window = tk.Tk()
        self.overlay_window.title("Emergency Stop")
        self.overlay_window.attributes("-topmost", True)
        self.overlay_window.geometry("200x100")

        # Make window semi-transparent
        self.overlay_window.attributes("-alpha", 0.8)

        # Style the stop button
        stop_button = tk.Button(
            self.overlay_window,
            text="EMERGENCY STOP",
            command=self.trigger_stop,
            bg="red",
            fg="white",
            font=("Arial", 12, "bold"),
            height=2,
        )
        stop_button.pack(expand=True, fill="both", padx=10, pady=10)

        # Add hotkey label
        hotkey_label = tk.Label(
            self.overlay_window, text=f"Hotkey: {self.hotkey}", font=("Arial", 8)
        )
        hotkey_label.pack(pady=5)

        # Allow window to be dragged
        self.overlay_window.bind("<Button-1>", self.start_move)
        self.overlay_window.bind("<B1-Motion>", self.do_move)

        # Start window minimized
        self.overlay_window.iconify()

    def start_move(self, event):
        self.x = event.x
        self.y = event.y

    def do_move(self, event):
        deltax = event.x - self.x
        deltay = event.y - self.y
        x = self.overlay_window.winfo_x() + deltax
        y = self.overlay_window.winfo_y() + deltay
        self.overlay_window.geometry(f"+{x}+{y}")

    def register_stop_handler(self, handler: Callable):
        """Register a function to be called when emergency stop is triggered"""
        self.stop_handlers.append(handler)

    def trigger_stop(self):
        """Trigger the emergency stop"""
        if not self.is_stopped:
            self.is_stopped = True
            print("\n🛑 EMERGENCY STOP TRIGGERED 🛑")

            # Execute all stop handlers
            for handler in self.stop_handlers:
                try:
                    handler()
                except Exception as e:
                    print(f"Error in stop handler: {e}")

            # Change overlay appearance
            if self.overlay_window:
                for widget in self.overlay_window.winfo_children():
                    if isinstance(widget, tk.Button):
                        widget.configure(text="STOPPED", bg="darkred", state="disabled")

            # Kill the process
            os.kill(os.getpid(), signal.SIGTERM)

    def update_hotkey(self, new_hotkey: str):
        """Update the emergency stop hotkey"""
        try:
            keyboard.remove_hotkey(self.hotkey)
            keyboard.add_hotkey(new_hotkey, self.trigger_stop)
            self.hotkey = new_hotkey

            # Update overlay label
            if self.overlay_window:
                for widget in self.overlay_window.winfo_children():
                    if isinstance(widget, tk.Label):
                        widget.configure(text=f"Hotkey: {self.hotkey}")

            return True
        except Exception as e:
            print(f"Error updating hotkey: {e}")
            return False

    def start(self):
        """Start the overlay window main loop"""
        if self.overlay_window:
            self.overlay_window.deiconify()  # Show window
            self.overlay_window.mainloop()


# Global instance
emergency_stop = EmergencyStop()
