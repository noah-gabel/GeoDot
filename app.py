import customtkinter as ctk
from tkintermapview import TkinterMapView

class App(ctk.CTk):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.title("GeoDot")
        self.geometry(str(self.winfo_screenwidth()) + "x" + str(self.winfo_screenheight()))
        self.configure(fg_color="#1e1e2e")

        self.current_city = ctk.StringVar(value="München")
        self.round = ctk.StringVar(value="1/10")
        self.current_score = ctk.IntVar(value=1000)

        self.grid_rowconfigure(0, weight=0)
        self.grid_rowconfigure(1, weight=1)
        self.grid_rowconfigure(2, weight=0)

        self.grid_columnconfigure(0, weight=1)

        self.setup_ui()

    def setup_ui(self):
        self._setup_map_widget()
        self._setup_top_hud()
        self._setup_bottom_hud()

    def _setup_map_widget(self):
        self.map = TkinterMapView(self, corner_radius=0)
        self.map.grid(row=1, column=0, sticky="nswe")

        self.map.set_tile_server("https://a.basemaps.cartocdn.com/rastertiles/voyager_nolabels/{z}/{x}/{y}.png")

    def _setup_top_hud(self):
        #background frame
        top_bar = ctk.CTkFrame(self, fg_color="#1e1e2e", height=75)
        top_bar.grid(row=0, column=0, sticky="ew", padx=100)

        top_bar.grid_propagate(False)

        top_bar.grid_rowconfigure(0, weight=1)

        top_bar.grid_columnconfigure(0, weight=1)
        top_bar.grid_columnconfigure(1, weight=1)
        top_bar.grid_columnconfigure(2, weight=1)
        top_bar.grid_columnconfigure(3, weight=1)
        top_bar.grid_columnconfigure(4, weight=1)
        top_bar.grid_columnconfigure(5, weight=1)
        top_bar.grid_columnconfigure(6, weight=1)

        #display current round
        round_frame = ctk.CTkFrame(top_bar, fg_color="transparent")
        round_frame.grid(row=0, column=1)
        ctk.CTkLabel(round_frame, text="ROUND", text_color="#5AB1FC", font=("Segoe UI", 10, "bold")).pack()
        ctk.CTkLabel(round_frame, textvariable=self.round, font=("Segoe UI", 20, "bold")).pack()

        city_frame = ctk.CTkFrame(top_bar, fg_color="transparent")
        city_frame.grid(row=0, column=3)
        ctk.CTkLabel(city_frame, text="FIND CITY", font=("Segoe UI", 10, "bold"), text_color="#5AB1FC").pack()
        ctk.CTkLabel(city_frame, textvariable=self.current_city, font=("Segoe UI", 20, "bold")).pack()

        score_frame = ctk.CTkFrame(top_bar, fg_color="transparent")
        score_frame.grid(row=0, column=5)
        ctk.CTkLabel(score_frame, text="SCORE", font=("Segoe UI", 10, "bold"), text_color="#5AB1FC").pack()
        ctk.CTkLabel(score_frame, textvariable=self.current_score, font=("Segoe UI", 20, "bold")).pack()

    def _setup_bottom_hud(self):
        #background frame
        bottom_bar = ctk.CTkFrame(self, fg_color="#1e1e2e", height=75)
        bottom_bar.grid(row=2, column=0, sticky="ew")
        bottom_bar.pack_propagate(False)

        self.guess_button = ctk.CTkButton(
            bottom_bar,
            corner_radius=25,
            text="Guess",
            font=("Segoe UI", 20, "bold"),
            fg_color="#dd2476",
            hover_color="#ff4e9d",
            height=50,
            command=self.guess)

        self.guess_button.pack(expand=True)

    def _disable_guess_button(self):
        self.guess_button.configure(state="disabled", fg_color="#737273")

    def _enable_guess_button(self):
        self.guess_button.configure(state="normal", fg_color="#dd2476")

    def guess(self):
        print("clicked")

    def start(self):
        self.mainloop()
