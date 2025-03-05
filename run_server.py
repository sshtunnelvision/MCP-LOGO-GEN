#!/usr/bin/env python
"""
Server runner script with clean shutdown handling and auto-reload.
This script runs the server in a subprocess, handles Ctrl+C properly,
and automatically restarts the server when files change.
"""

import os
import signal
import subprocess
import sys
import time
import threading
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

# Flag to indicate if we should restart the server
restart_server = False
# Flag to indicate if we're shutting down
shutting_down = False

class FileChangeHandler(FileSystemEventHandler):
    def on_any_event(self, event):
        global restart_server
        # Skip temporary files and __pycache__ directories
        if (event.src_path.endswith('.pyc') or 
            '__pycache__' in event.src_path or 
            '.git' in event.src_path or
            event.is_directory):
            return
        
        # Only restart for Python files
        if event.src_path.endswith('.py'):
            print(f"\n[RELOAD] Detected change in {event.src_path}")
            restart_server = True

def start_file_watcher(directory):
    """Start watching for file changes in the specified directory."""
    event_handler = FileChangeHandler()
    observer = Observer()
    observer.schedule(event_handler, directory, recursive=True)
    observer.start()
    return observer

def run_server():
    """Run the server process and handle its lifecycle."""
    global restart_server, shutting_down
    
    # Start the server as a subprocess
    server_process = subprocess.Popen(
        [sys.executable, "server.py"],
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        universal_newlines=True,
        bufsize=1  # Line buffered
    )
    
    # Print server output in real-time
    def print_output():
        for line in server_process.stdout:
            if not shutting_down:  # Only print if we're not shutting down
                print(line, end='')
    
    # Start a thread to print output
    output_thread = threading.Thread(target=print_output)
    output_thread.daemon = True
    output_thread.start()
    
    # Monitor the server process
    while server_process.poll() is None:
        if restart_server:
            print("\n[RELOAD] Restarting server due to file changes...")
            server_process.terminate()
            try:
                server_process.wait(timeout=2)
            except subprocess.TimeoutExpired:
                server_process.kill()
                server_process.wait()
            restart_server = False
            return True  # Signal to restart
        time.sleep(0.1)
    
    # If we get here, the server exited on its own
    return_code = server_process.poll()
    print(f"\nServer exited with code {return_code}")
    return False  # Signal not to restart

def main():
    global restart_server, shutting_down
    
    print("Starting MCP Tool Server with clean shutdown handling and auto-reload...")
    
    # Start file watcher
    observer = start_file_watcher("mcp_tool_server")
    
    # Function to handle Ctrl+C
    def signal_handler(sig, frame):
        global shutting_down
        print("\nReceived shutdown signal. Terminating server...")
        shutting_down = True
        observer.stop()
        sys.exit(0)
    
    # Register signal handlers
    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)
    
    # Run the server, restarting as needed
    try:
        while True:
            should_restart = run_server()
            if not should_restart:
                break
            time.sleep(0.5)  # Small delay before restart
    except KeyboardInterrupt:
        signal_handler(signal.SIGINT, None)
    finally:
        observer.stop()
        observer.join()
    
    return 0

if __name__ == "__main__":
    sys.exit(main()) 