from tkintermapview import TkinterMapView
from tkinter import Event
from config import API_KEY, TOLERANCE_RADIUS_PX, BLOCKED_BINDING_SEQUENCES, CITY_MARKER_COLOR_INSIDE, CITY_MARKER_COLOR_OUTSIDE, GUESS_MARKER_CIRCLE_COLOR, GUESS_MARKER_COLOR, MARKER_TEXT_COLOR, FONT, RESULT_PATH_COLOR, RESULT_PATH_WIDTH
from math import sqrt
from models import Difficulty, Guess, Coordinates, BoundingBox

class MapController(TkinterMapView):
    def __init__(self, master, enable_guess_button, disable_guess_button):
        super().__init__(master)

        self.pressed_pos: Event | None = None
        self.guess_coordinates : Coordinates | None = None
        self.guess_marker = None
        self.city_marker = None
        self.input_blocked: bool = False

        self.set_tile_server(f"https://a.basemaps.cartocdn.com/rastertiles/voyager_nolabels/{{z}}/{{x}}/{{y}}.png?key={API_KEY}")
        self._bind_button_clicks()
        self._install_input_blocker()

        self._disable_guess_button = disable_guess_button
        self._enable_guess_button = enable_guess_button


    def _bind_button_clicks(self):
        # bind the left click to the canvas
        # add="+" runs these bindings alongside tkintermapviews bindings and doesn't replace or break anything
        self.canvas.bind("<ButtonPress-1>", self._on_press, add="+")
        self.canvas.bind("<ButtonRelease-1>", self._on_release, add="+")

        #disable default right click command of showing the coordinates
        self.canvas.bind("<Button-3>", lambda _: "break")
        
    def _on_press(self, event: Event):
        self.pressed_pos = event

    def _on_release(self, event: Event):
        if self.pressed_pos == None:
            return

        distance_x = abs(self.pressed_pos.x - event.x)
        distance_y = abs(self.pressed_pos.y - event.y)
        # use pythagorean theorem to calculate diagonal distance 
        # allows to compare it against a radius of tolerance instead of a box
        distance = sqrt(distance_x ** 2 + distance_y ** 2)

        if distance > TOLERANCE_RADIUS_PX:
            self.pressed_pos = None
            return

        self._cleanup_guess_marker()

        coords_x, coords_y = self.convert_canvas_coords_to_decimal_coords(
            canvas_x=self.pressed_pos.x, 
            canvas_y=self.pressed_pos.y
        )

        self.guess_marker = self.set_marker(
            deg_x=coords_x, 
            deg_y=coords_y,
            text="YOUR GUESS",
            marker_color_outside=GUESS_MARKER_COLOR,
            marker_color_circle=GUESS_MARKER_CIRCLE_COLOR,
            text_color=MARKER_TEXT_COLOR,
            font=(FONT, 8, "bold"),
        )

        self.guess_coordinates = Coordinates(lat=coords_x, lon=coords_y)
        self._enable_guess_button()

    def _install_input_blocker(self):
        # creates a unique blocking tag bind for each map so if multiple ones are created they don't interfere
        block_tag = f"map_block_{id(self)}"

        # change bind tags so that the custom one is at the start
        # this way it runs before any other bindings are completed and can interrupt any unwanted bindings to go through
        self.canvas.bindtags((block_tag, ) + self.canvas.bindtags())

        # bind all disallowed buttons to the blocking bind tag
        for sequence in BLOCKED_BINDING_SEQUENCES:
            self.canvas.bind_class(block_tag, sequence, self._swallow_event)

    def _swallow_event(self, _event: Event):
        if self.input_blocked:
            return "break"  # ends the bind tag chain = every binding does not run
        return None         # bindings follow through like normal

    def _set_input_blocked(self, blocked: bool):
        self.input_blocked = blocked
        if blocked:
            self._disable_guess_button()
        else:
            self._enable_guess_button()
        self.pressed_pos = None # set position to None: if a user pressed a button exactly when the movement gets locked it could cause problems

    def _cleanup_guess_marker(self):
        if self.guess_marker:
            self.guess_marker.delete()
            self.guess_marker = None

    def _cleanup_city_marker(self):
        if self.city_marker:
            self.city_marker.delete()
            self.city_marker = None
    
    def reset(self, difficulty: Difficulty):
        #change the position and zoom of the map according to the mode to a default position
        self.set_position(
            deg_x=difficulty.reset_coordinates.lat, 
            deg_y=difficulty.reset_coordinates.lon
        )
        self.set_zoom(difficulty.reset_zoom)

        self.guess_coordinates = None
        
        self._cleanup_guess_marker()
        self._cleanup_city_marker()
        # cleanup paths
        self.delete_all_path()

        # allow interaction for the next round
        self._set_input_blocked(False)

    def show_guess_result(self, guess: Guess):
        self._set_input_blocked(True)

        #prevents a city marker being placed extra when the function is called twice in a round
        self._cleanup_city_marker()

        self.city_marker = self.set_marker(
            deg_x=guess.city.coords.lat, 
            deg_y=guess.city.coords.lon, 
            text=guess.city.name,
            marker_color_circle=CITY_MARKER_COLOR_INSIDE,
            marker_color_outside=CITY_MARKER_COLOR_OUTSIDE,
            text_color=MARKER_TEXT_COLOR,
            font=(FONT, 8, "bold")
        )

        bounding_box = BoundingBox.from_points(points=[guess.coords, guess.city.coords])

        #automatically zooms to the specified points so you can see your guesses better
        self.fit_bounding_box(
            position_top_left=(bounding_box.nw_corner.lat, bounding_box.nw_corner.lon), 
            position_bottom_right=(bounding_box.se_corner.lat, bounding_box.se_corner.lon))

        self.set_path(
            [(guess.coords.lat, guess.coords.lon),
             (guess.city.coords.lat, guess.city.coords.lon)],
            color= RESULT_PATH_COLOR,
            width= RESULT_PATH_WIDTH
        )

    def show_grid(self, row: int, column: int):
        self.grid(row=row, column=column, sticky="nswe")