import tkinter as tk
import sys

print("Starting test window")

try:
    # Create the main window
    root = tk.Tk()
    print("Window created successfully")
    root.title("Test Window")
    root.geometry("800x600")
    
    # Set window background color
    root.configure(bg='lightblue')
    print("Background color set")
    
    # Create a large red rectangle
    red_rect = tk.Frame(root, bg='red', width=200, height=200)
    red_rect.pack(pady=200)
    print("Red rectangle created")
    
    # Start the main event loop
    print("Starting main loop")
    root.mainloop()
    
except Exception as e:
    print(f"Error: {str(e)}", file=sys.stderr)
    print("Exiting due to error")
    sys.exit(1)
