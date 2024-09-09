import tkinter as tk
from tkinter import scrolledtext, filedialog, ttk
import threading
import subprocess
import ttkbootstrap as tb

class LoggerApp:
    def __init__(self, root):
        self.root = root
        self.frame = tk.Frame(root)
        self.frame.pack()
        self.root.resizable(False, False)  # Disable resizing the window
        self.root.title("Logger GUI")
        self.root.geometry("800x480")  # Set window size to match 7-inch Raspberry Pi display resolution
        self.logger_frame = tk.Frame(root)
        self.logger_frame.pack(side=tk.LEFT)

        # style = ttk.Style()
        # style.theme_use("clam")  # Choose a modern theme like "clam", "alt", or "default"
        # Create frame for buttons
        self.button_frame = tk.Frame(root)
        self.button_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)
        #set border
        self.button_frame.config(bd=2, relief=tk.RAISED, background="green")


        self.log_output = scrolledtext.ScrolledText(self.logger_frame, width=65, height=27, font=("Consolas", 10), bg="#f7f7f7", fg="#333")
        self.log_output.pack(side=tk.LEFT, expand=True, fill=tk.BOTH)

        # start button
        self.start_button = ttk.Button(self.button_frame, text="Start Logging", command=self.start_logging, style="TButton")
        self.start_button.pack(side=tk.TOP, fill=tk.BOTH, expand=True)

        # stop button
        self.stop_button = ttk.Button(self.button_frame, text="Stop Logging", command=self.stop_logging, style="TButton")
        self.stop_button.pack(side=tk.TOP, fill=tk.BOTH, expand=True)

        # switch view button
        self.view_button = ttk.Button(self.button_frame, text="Switch View", command=self.switch_view, style="TButton")

        self.view_button.pack(side=tk.TOP, fill=tk.BOTH, expand=True)

        # save button
        self.save_log = ttk.Button(self.button_frame, text="Save Output", command=self.save_data, style="TButton")
        self.save_log.pack(side=tk.TOP, fill=tk.BOTH, expand=True)

        # quit button
        self.quit_button = ttk.Button(self.button_frame, text="Quit", command=self.quit, style="TButton")
        self.quit_button.pack(side=tk.TOP, fill=tk.BOTH, expand=True)

        self.logging = False
        self.process = None
        self.log_thread = None


    def start_logging(self):
        if not self.logging:
            self.log_output.delete(1.0, tk.END)  # Clear the log output
            self.logging = True

            # Start the external Python script using subprocess with unbuffered output
            self.process = subprocess.Popen(
                ['python3', '-u', 'sensor_script.py'],  # Replace with the actual script path
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
                bufsize=1  # Line-buffered
            )

            # Start the thread to capture and display the output from the script
            self.log_thread = threading.Thread(target=self.capture_output)
            self.log_thread.start()

    def stop_logging(self):
        if self.logging:
            self.logging = False
            if self.process:
                self.process.terminate()  # Terminate the external process
                self.process = None
        

    def quit(self):
        self.root.quit()
    
    def save_data(self):
        # Prompt user to save log file
        file_path = filedialog.asksaveasfilename(defaultextension=".txt",
                                                 filetypes=[("Text files", "*.txt"), ("All files", "*.*")])
        if file_path:
            with open(file_path, 'w') as file:
                file.write(self.log_output.get(1.0, tk.END))  # Save the log content to a file

    def switch_view(self):
        print("Switch View")


    def capture_output(self):
        """Capture the output from the external script and display it in the log."""
        while self.logging and self.process and self.process.poll() is None:
            output = self.process.stdout.readline()
            if output:
                self.log_output.insert(tk.END, output)
                self.log_output.see(tk.END)  # Scroll to the end

        # If the process is done, capture any remaining output
        if self.process:
            remaining_output = self.process.stdout.read()
            if remaining_output:
                self.log_output.insert(tk.END, remaining_output)
                self.log_output.see(tk.END)

if __name__ == "__main__":
    root = tb.Window(themename="superhero")
    app = LoggerApp(root)
    root.mainloop()
