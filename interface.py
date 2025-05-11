import tkinter as tk
from tkinter import scrolledtext, ttk
import asyncio
from voice_assistant import VoiceAssistant

# === Colores y Estilo ===
FONT_FAMILY = "Arial"
FONT_SIZE = 12
FONT_BOLD = (FONT_FAMILY, FONT_SIZE, "bold")
FONT_ITALIC = (FONT_FAMILY, FONT_SIZE, "italic")
FONT_REGULAR = (FONT_FAMILY, FONT_SIZE)

class VoiceAssistantApp:
    THEMES = {
        "Oscuro": {
            "primary": "#1E1E2E", "secondary": "#282A36", "text": "#F8F8F2",
            "accent": "#6272A4", "success": "#50FA7B", "error": "#FF5555", "button": "#44475A",
            "textbox": "#282A36"
        },
        "Claro": {
            "primary": "#FFFFFF", "secondary": "#F0F0F0", "text": "#000000",
            "accent": "#4A90E2", "success": "#28A745", "error": "#DC3545", "button": "#E0E0E0",
            "textbox": "#D3D3D3"
        }
    }

    def __init__(self, root):
        self.root = root
        self.root.title("Asistente de Voz IA")
        self.root.geometry("1200x800")
        self.current_theme = "Oscuro"
        self.assistant = VoiceAssistant()
        self.setup_ui()
        self.apply_theme(self.current_theme)

    def setup_ui(self):
        """Configura la interfaz gráfica."""
        self.menubar = tk.Menu(self.root)
        theme_menu = tk.Menu(self.menubar, tearoff=0)
        for theme_name in self.THEMES:
            theme_menu.add_command(label=theme_name, command=lambda t=theme_name: self.apply_theme(t))
    
        self.root.config(menu=self.menubar)

        self.main_frame = tk.Frame(self.root)
        self.main_frame.pack(expand=True, fill=tk.BOTH, padx=20, pady=20)

        self.input_frame = tk.Frame(self.main_frame)
        self.input_frame.pack(fill=tk.X, pady=(0, 10))

        self.entrada_texto = tk.Text(
            self.input_frame, height=4, font=FONT_REGULAR, wrap=tk.WORD,
            bd=0, padx=10, pady=10
        )
        self.entrada_texto.pack(side=tk.LEFT, expand=True, fill=tk.X, padx=(0, 10))
        self.entrada_texto.bind("<Return>", lambda event: self.enviar_mensaje())

        self.boton_enviar = tk.Button(
            self.input_frame, text="Enviar", font=FONT_BOLD,
            bd=0, padx=15, pady=5, command=self.enviar_mensaje
        )
        self.boton_enviar.pack(side=tk.RIGHT)

        self.voice_frame = tk.Frame(self.main_frame)
        self.voice_frame.pack(pady=(0, 10))

        self.boton_grabar = tk.Button(
            self.voice_frame, text="🎤 Hablar", font=FONT_BOLD,
            bd=0, padx=20, pady=10, command=self.iniciar_conversacion_por_voz
        )
        self.boton_grabar.pack(side=tk.LEFT, padx=10)

        self.boton_detener = tk.Button(
            self.voice_frame, text="⏹️ Detener", font=FONT_BOLD,
            bd=0, padx=20, pady=10, command=self.assistant.voice_processor.stop_speaking
        )
        self.boton_detener.pack(side=tk.LEFT, padx=10)

        self.progress_bar = ttk.Progressbar(
            self.main_frame, mode="indeterminate", maximum=100
        )
        self.progress_bar.pack(pady=(5, 0))
        self.progress_bar.pack_forget()

        self.status_label = tk.Label(
            self.main_frame, text="", font=FONT_ITALIC
        )
        self.status_label.pack()

        self.output_frame = tk.Frame(self.main_frame)
        self.output_frame.pack(expand=True, fill=tk.BOTH, pady=(10, 0))

        self.output_text = scrolledtext.ScrolledText(
            self.output_frame, wrap=tk.WORD, font=FONT_REGULAR,
            bd=0, padx=10, pady=10, state="normal"
        )
        self.output_text.pack(expand=True, fill=tk.BOTH)

        self.bottom_frame = tk.Frame(self.main_frame)
        self.bottom_frame.pack(pady=(10, 0))

        self.boton_cambiar_tema = tk.Button(
            self.bottom_frame, text="Cambiar Tema", font=FONT_BOLD,
            bd=0, padx=20, pady=10, command=self.toggle_theme
        )
        self.boton_cambiar_tema.pack(side=tk.LEFT, padx=10)

        self.boton_salir = tk.Button(
            self.bottom_frame, text="Salir", font=FONT_BOLD,
            bd=0, padx=20, pady=10, command=self.root.destroy
        )
        self.boton_salir.pack(side=tk.LEFT)


    def apply_theme(self, theme_name):
        """Aplica un tema visual a la interfaz."""
        theme = self.THEMES[theme_name]
        self.root.configure(bg=theme["primary"])
        self.main_frame.configure(bg=theme["primary"])
        self.input_frame.configure(bg=theme["secondary"])
        self.voice_frame.configure(bg=theme["secondary"])
        self.output_frame.configure(bg=theme["secondary"])
        self.bottom_frame.configure(bg=theme["primary"])
        self.entrada_texto.configure(bg=theme["textbox"], fg=theme["text"], insertbackground=theme["text"])
        self.output_text.configure(bg=theme["textbox"], fg=theme["text"])
        self.status_label.configure(bg=theme["primary"], fg=theme["success"])
        self.boton_enviar.configure(bg=theme["success"], fg=theme["primary"], activebackground=theme["success"])
        self.boton_grabar.configure(bg=theme["accent"], fg=theme["text"], activebackground=theme["accent"])
        self.boton_detener.configure(bg=theme["error"], fg=theme["text"], activebackground=theme["error"])
        self.boton_cambiar_tema.configure(bg=theme["button"], fg=theme["text"], activebackground=theme["button"])
        self.boton_salir.configure(bg=theme["button"], fg=theme["text"], activebackground=theme["button"])
        self.current_theme = theme_name

    def toggle_theme(self):
        """Alterna entre los temas Oscuro y Claro."""
        new_theme = "Claro" if self.current_theme == "Oscuro" else "Oscuro"
        self.apply_theme(new_theme)

    def actualizar_salida(self, text):
        """Actualiza el área de salida de texto."""
        self.output_text.insert(tk.END, text)
        self.output_text.see(tk.END)

    def actualizar_estado(self, text):
        """Actualiza la etiqueta de estado."""
        self.status_label.config(text=text)
        self.root.update_idletasks()

    async def iniciar_conversacion_por_voz_async(self):
        """Inicia una conversación por voz de forma asíncrona."""
        if not self.assistant.voice_processor.is_speaking and not self.assistant.api_client.is_thinking:
            self.boton_grabar.config(state="disabled")
            self.boton_enviar.config(state="disabled")
            self.progress_bar.pack(pady=(5, 0))
            self.progress_bar.start()
            await self.assistant.ejecutar_conversacion(self.actualizar_salida, self.actualizar_estado)
            self.progress_bar.stop()
            self.progress_bar.pack_forget()
            self.boton_grabar.config(state="normal")
            self.boton_enviar.config(state="normal")

    def iniciar_conversacion_por_voz(self):
        """Ejecuta la función asíncrona para conversación por voz."""
        asyncio.run(self.iniciar_conversacion_por_voz_async())

    async def enviar_mensaje_async(self):
        """Envía un mensaje desde el área de texto de forma asíncrona."""
        if not self.assistant.voice_processor.is_speaking and not self.assistant.api_client.is_thinking:
            self.boton_grabar.config(state="disabled")
            self.boton_enviar.config(state="disabled")
            self.progress_bar.pack(pady=(5, 0))
            self.progress_bar.start()
            texto_usuario = self.entrada_texto.get("1.0", tk.END).strip()
            self.entrada_texto.delete("1.0", tk.END)
            if texto_usuario:
                await self.assistant.ejecutar_conversacion(self.actualizar_salida, self.actualizar_estado, texto_usuario)
            self.progress_bar.stop()
            self.progress_bar.pack_forget()
            self.boton_grabar.config(state="normal")
            self.boton_enviar.config(state="normal")

    def enviar_mensaje(self):
        """Ejecuta la función asíncrona para enviar mensaje."""
        asyncio.run(self.enviar_mensaje_async())

    def run(self):
        """Inicia la aplicación."""
        self.root.mainloop()