"""
Watches for new functions and runs tests automatically
"""
import os
import time
import subprocess
import logging
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

logger = logging.getLogger(__name__)

class FunctionTestHandler(FileSystemEventHandler):
    def __init__(self, test_command):
        self.test_command = test_command
        self.last_run = 0
        self.cooldown = 2  # Seconds between test runs

    def on_modified(self, event):
        if event.src_path.endswith('.py') and 'custom_functions' in event.src_path:
            current_time = time.time()
            if current_time - self.last_run > self.cooldown:
                self.last_run = current_time
                self.run_tests()

    def run_tests(self):
        logger.info("Running function tests...")
        try:
            result = subprocess.run(
                self.test_command,
                capture_output=True,
                text=True
            )
            if result.returncode == 0:
                logger.info("✅ All tests passed!")
            else:
                logger.error("❌ Tests failed!")
                logger.error(result.stderr)
        except Exception as e:
            logger.error(f"Error running tests: {str(e)}")

def start_watcher():
    """Start watching the custom_functions directory"""
    custom_functions_dir = os.path.dirname(__file__)
    test_command = ["pytest", "tests/test_custom_functions.py", "-v"]
    
    event_handler = FunctionTestHandler(test_command)
    observer = Observer()
    observer.schedule(event_handler, custom_functions_dir, recursive=False)
    observer.start()
    
    logger.info(f"Watching {custom_functions_dir} for changes...")
    
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()

if __name__ == "__main__":
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    start_watcher()
