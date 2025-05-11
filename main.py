import tkinter as tk
from interface import VoiceAssistantApp

def main():
    window = tk.Tk()
    app = VoiceAssistantApp(window)
    app.run()

if __name__ == "__main__":
    main()