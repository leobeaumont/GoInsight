import tkinter as tk
from typing import Tuple, Optional
import argparse
import json
from pathlib import Path
import os

import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure

from src.data.move import Move
from src.data.game import Game
from src.data.board import Board
from src.data.sgf import SgfTree
from src.features.analysis import Analizer
from src.API.API import API

# Minimal Mock for Constants
VALID_COLUMN_GTP = "ABCDEFGHJKLMNOPQRST"

# --- 3. THE TKINTER GUI CLASS ---

class GoBoardUI:
    def __init__(self, master, board_logic):
        self.master = master
        self.board_logic = board_logic 
        self.board_size = board_logic.size[0] 
        
        # Visual Configuration
        self.cell_size = 35
        self.margin = 35
        self.stone_rad = 14
        self.wood_color = '#E3C588'
        
        # Turn state (UI needs to know what color to create)
        self.current_turn = board_logic.game.next_color()

        # Calculate canvas size
        self.canvas_width = (self.cell_size * (self.board_size - 1)) + (2 * self.margin)
        self.canvas_height = (self.cell_size * (self.board_size - 1)) + (2 * self.margin)

        # Setup Canvas
        self.canvas = tk.Canvas(master, width=self.canvas_width, height=self.canvas_height, bg=self.wood_color)
        self.canvas.pack()

        # Bind Click
        self.canvas.bind("<Button-1>", self.handle_click)

        # Draw Static Elements
        self.draw_grid()
        self.draw_star_points()

        # Track where we are in history (Start at the end)
        self.view_index = len(self.board_logic.game.moves)

        # Allow the canvas to accept keyboard inputs
        self.canvas.focus_set()

        # Bind Arrow Keys
        self.master.bind("<Left>", self.go_back)
        self.master.bind("<Right>", self.go_forward)

        # Selection State Variables
        self.selection_mode = False  # Is the mode active?
        self.selection_clicks = []   # Stores the coordinates [(x1,y1), (x2,y2)]
        self.selected_area = []  # Stores the final selected area

        # Selection Button
        self.select_btn = tk.Button(self.master, text="Select Area", command=self.toggle_selection_mode)
        self.select_btn.place(x=200, y=20) # Adjust x/y as needed

        # Clear Selection Button
        self.clear_btn = tk.Button(self.master, text="Clear Selection", command=self.clear_selection)
        self.clear_btn.place(x=30, y=20) # Adjust position as needed

        # Invert Selection State 
        # False = Analyze INSIDE the zone
        # True  = Analyze OUTSIDE the zone
        self.invert_selection = False

        initial_text = "Analysis: Inside Zone" if not self.invert_selection else "Analysis: Outside Zone"
        self.invert_btn = tk.Button(self.master, text=initial_text, command=self.toggle_invert_mode)
        # Adjust x/y to sit next to your "Select Area" button
        self.invert_btn.place(x=30, y=60)

        # Analyze Button
        self.analyze_btn = tk.Button(self.master, text="Analyze Position", command=lambda: self.analyze_area(self.selected_area))
        self.analyze_btn.place(x=200, y=60) # Adjust x/y as needed

        # Analyze all game Button
        self.analyze_btn = tk.Button(self.master, text="Analyze Game", command=lambda: self.analyze_game())
        self.analyze_btn.place(x=30, y=100) # Adjust x/y as needed

        self.analysis_active = False
        self.full_game_analysis = {} # Stores the JSON from API
        self.graph_window = None

        # This will display "Move 15: MISTAKE" below the board
        self.classification_label = tk.Label(self.master, text="", font=("Arial", 12, "bold"), fg="#333")
        # Placing it dynamically below the canvas
        self.classification_label.place(x=50, y=140)

        # Restart Button 
        self.restart_btn = tk.Button(self.master, text="Restart Game", command=self.restart_game, fg="red")
        # Placing it a bit further down or to the side
        self.restart_btn.place(x=50, y=600)

        self.graph_frame = tk.Frame(self.master, width=self.canvas_width)
        self.graph_frame.pack(side=tk.TOP, fill=tk.NONE, expand=False, pady=(0, 20))
        self.init_embedded_graph()


    def get_temp_sgf_path(self, filename="temp_analysis.sgf"):
        """
        Generates a dynamic path to the 'games' folder at the project root.
        """
        # 1. Get the path of the current file (API.py or gui.py)
        current_file = Path(__file__).resolve()
        
        # 2. Go up to Project Root. 
        # If file is in src/features/API.py:
        # .parent = src/features
        # .parent.parent = src
        # .parent.parent.parent = Project_Root
        project_root = current_file.parent.parent.parent
        
        # 3. Define games folder path
        games_folder = project_root / "games"
        
        # 4. Create the folder if it doesn't exist (Safety check)
        games_folder.mkdir(parents=True, exist_ok=True)
        
        # 5. Return the full path including filename
        return str(games_folder / filename)


    def init_embedded_graph(self):
        """Creates an empty graph below the board with matching width."""
        # Matplotlib uses inches, Tkinter uses pixels. Default DPI is usually 100.
        dpi = 100
        width_inch = self.canvas_width / dpi
        height_inch = 2.0  # Keep it short so it fits in the window

        # Create Figure
        self.fig = Figure(figsize=(width_inch, height_inch), dpi=dpi)
        self.ax = self.fig.add_subplot(111)

        # Configure Empty Look
        self.ax.set_title("Score Lead", fontsize=9)
        self.ax.tick_params(axis='both', which='major', labelsize=8)
        self.ax.grid(True, linestyle=':', alpha=0.5)
        self.ax.set_ylim(-20, 20) # Placeholder limits

        # Create Canvas
        self.graph_canvas = FigureCanvasTkAgg(self.fig, master=self.graph_frame)
        self.graph_canvas.draw()
        self.graph_canvas.get_tk_widget().pack()

    def gtp_to_coords(self, gtp_vertex: str) -> Optional[Tuple[int, int]]:
        """
        Converts "C15" -> (2, 4) using VALID_COLUMN_GTP.
        """
        gtp_vertex = gtp_vertex.upper()
        if gtp_vertex == "PASS":
            return None

        col_char = gtp_vertex[0]
        try:
            col = VALID_COLUMN_GTP.index(col_char)
        except ValueError:
            print(f"Invalid column char: {col_char}")
            return None

        try:
            row_num = int(gtp_vertex[1:])
            row = self.board_size - row_num
        except ValueError:
            return None

        return (col, row)
    
    def go_back(self, event):
        """Show the previous move."""
        if self.view_index > 0:
            self.view_index -= 1
            self.update_board_to_current_index()

    def go_forward(self, event):
        """Show the next move."""
        # We can only go forward if there are actual moves in the history to show
        total_moves = len(self.board_logic.game.moves)
        if self.view_index < total_moves:
            self.view_index += 1
            self.update_board_to_current_index()

    def update_board_to_current_index(self):
        """
        Reconstructs the board state from move 0 up to self.view_index.
        """
        moves_to_replay = self.board_logic.game.moves[:self.view_index]

        self.clear_analysis_markers()
        
        try:
            self.board_logic.board_from_moves(moves_to_replay)
        except ValueError as e:
            print(f"History Error: {e}")

        # 3. Redraw the visual stones
        self.refresh_stones()

        if self.analysis_active:
            self.update_classification_label()
        
        # 4. Optional: Update Title to show move number
        self.master.title(f"Go - Move {self.view_index} / {len(self.board_logic.game.moves)}")

    def draw_grid(self):
        """Draws lines and labels."""
        for i in range(self.board_size):
            start = self.margin
            end = self.margin + (self.cell_size * (self.board_size - 1))
            pos = self.margin + (i * self.cell_size)

            # Lines
            self.canvas.create_line(pos, start, pos, end) # Vertical
            self.canvas.create_line(start, pos, end, pos) # Horizontal
            
            # Text Labels (1-19, A-T)
            self.canvas.create_text(pos, start - 20, text=VALID_COLUMN_GTP[i])
            self.canvas.create_text(start - 20, pos, text=str(self.board_size - i))

    def draw_star_points(self):
        """Draws hoshi points for 19x19."""
        if self.board_size != 19: return
        
        # Standard 19x19 star points
        points = [(3,3), (9,3), (15,3), (3,9), (9,9), (15,9), (3,15), (9,15), (15,15)]
        
        for col, row in points:
            cx = self.margin + (col * self.cell_size)
            cy = self.margin + (row * self.cell_size)
            self.canvas.create_oval(cx-3, cy-3, cx+3, cy+3, fill='black')

    def handle_click(self, event):
        """
        1. Convert Screen X/Y -> Board Grid X/Y
        2. Create a Move Object
        3. Pass to board_logic.add_move()
        4. Redraw based on board state
        """

        total_moves = len(self.board_logic.game.moves)
        if self.view_index != total_moves:
            print("Cannot play while viewing history! Press <Right> to go to current turn.")
            return

        # 1. Convert coords
        col = round((event.x - self.margin) / self.cell_size)
        row = round((event.y - self.margin) / self.cell_size)

        self.canvas.focus_set()

        if self.selection_mode:
            self.handle_selection_click(col, row)
            return # Skip normal move handling

        # 2. Basic Bounds Check (before calling logic)
        if 0 <= col < self.board_size and 0 <= row < self.board_size:
            self.clear_analysis_markers()
            print(f"Clicked on board position: ({col}, {row})")
            
            # Create the Move object your logic expects
            move = Move(game, color = self.current_turn, pos = (col, row))

            try:
                # 3. Attempt to add move to your logic
                # This validates the move AND calculates captures (update_board)
                self.board_logic.add_move(move)
                
                self.view_index += 1 # We just added a move, so increment index
                self.refresh_stones()

                # 4. Success? Toggle turn and Redraw
                self.current_turn = 'W' if self.current_turn == 'B' else 'B'
                self.master.title(f"Go - {self.current_turn}'s Turn")
                self.refresh_stones()
                
            except ValueError as e:
                print(e) # Logic rejected the move (occupied, etc)

    def refresh_stones(self):
        """
        Wipes all stones and redraws them based on self.board_logic.board.
        This ensures captures calculated in Python are reflected in GUI.
        """
        self.canvas.delete("stone") # Delete items tagged as "stone"

        # Iterate over your board logic's 2D array
        # self.board_logic.board is List[List[Optional[Move]]]
        for y in range(self.board_logic.size[1]):
            for x in range(self.board_logic.size[0]):
                move = self.board_logic.board[y][x]
                
                if move is not None:
                    self.draw_stone(x, y, move.color)

    def toggle_selection_mode(self):
        """Activates or cancels the area selection mode."""
        if not self.selection_mode:
            # Turn ON
            self.selection_mode = True
            self.selection_clicks = [] # Reset clicks
            self.canvas.config(cursor="crosshair") # Change cursor to indicate mode
            print("Selection Mode: ON. Click two corners.")
            self.select_btn.config(text="Cancel Selection", relief="sunken")
        else:
            # Turn OFF (Cancel)
            self.selection_mode = False
            self.selection_clicks = []
            self.canvas.delete("selection_marker") # Remove red dots
            self.canvas.config(cursor="") # Reset cursor
            print("Selection Mode: OFF")
            self.select_btn.config(text="Select Area", relief="raised")
    
    def handle_selection_click(self, col, row):
        # 1. Store the click
        self.selection_clicks.append((col, row))
        print(f"Selected corner: {col}, {row}")

        # 2. Visual Feedback (Draw a red dot for the corner)
        cx = self.margin + (col * self.cell_size)
        cy = self.margin + (row * self.cell_size)
        
        self.canvas.create_oval(
            cx-5, cy-5, cx+5, cy+5, 
            fill='red', outline='red', 
            tags="selection_visuals" # Tag allows us to delete dots + box together
        )

        # 3. Check if we have 2 corners (Selection Complete)
        if len(self.selection_clicks) == 2:
            c1 = self.selection_clicks[0]
            c2 = self.selection_clicks[1]

            # --- A. Calculate Logic (Your existing code) ---
            for i in self.board_logic.area_selection_positions(c1, c2):
                if i not in self.selected_area:
                    self.selected_area.append(i)
            print(f"Area defined. {len(self.selected_area)} positions selected.")
            print(f"Selected Area Positions: {self.selected_area}")
            
            # --- B. Draw the Red Dashed Rectangle ---
            self.draw_selection_box(c1, c2)

            # --- C. Turn off mode automatically ---
            self.toggle_selection_mode()

    def draw_selection_box(self, c1, c2):
        """Draws a dashed red rectangle around the selected grid points."""
        
        # Unpack grid coordinates
        col1, row1 = c1
        col2, row2 = c2
        
        # Determine Top-Left (min) and Bottom-Right (max) grid coords
        min_col, max_col = sorted([col1, col2])
        min_row, max_row = sorted([row1, row2])

        # Convert Grid -> Pixels
        # We add/subtract 'cell_size/2' to draw the box AROUND the intersections
        x_start = self.margin + (min_col * self.cell_size) - (self.cell_size / 2)
        y_start = self.margin + (min_row * self.cell_size) - (self.cell_size / 2)
        
        x_end = self.margin + (max_col * self.cell_size) + (self.cell_size / 2)
        y_end = self.margin + (max_row * self.cell_size) + (self.cell_size / 2)

        # Create the Rectangle
        self.canvas.create_rectangle(
            x_start, y_start, x_end, y_end,
            outline="red",
            width=2,
            dash=(5, 5),  # 5 pixels drawn, 5 pixels skip (Dashed Line)
            tags="selection_visuals" # Same tag as the dots!
        )
    
    def clear_selection(self):
        """Removes the selected area data and visual rectangle."""
        # 1. Clear Data
        self.selected_area = []
        self.selection_clicks = []
        
        # 2. Clear Visuals (Everything tagged "selection_visuals")
        self.canvas.delete("selection_visuals")
        
        print("Selection cleared.")
    
    def toggle_invert_mode(self):
        """Switches the analysis mode between Inside and Outside."""
        # 1. Flip the boolean
        self.invert_selection = not self.invert_selection
        
        # 2. Update the button text based on the new value
        if self.invert_selection:
            new_text = "Analysis: Outside Zone"
        else:
            new_text = "Analysis: Inside Zone"
            
        self.invert_btn.config(text=new_text)
        
        # Optional: Print for debugging
        print(f"Invert Mode changed to: {self.invert_selection}")
    
    def analyze_area(self, positions):
        """Integrate your analysis feature here."""

        # Prepare a Game object reflecting current state
        sgf_path = self.get_temp_sgf_path("area_analysis.sgf")
        current_rules = self.board_logic.game.ruleset

        if isinstance(current_rules, str):
            rules_arg = [current_rules]
        else:
            rules_arg = current_rules

        copy_game = Game(
            RU=rules_arg,  
            SZ=[str(self.board_logic.size[0])], 
            KM=[str(self.board_logic.game.komi)]
        )

        copy_game.moves = self.board_logic.game.moves[:self.view_index]
        print(f"Moves given: {len(copy_game.moves)}")

        sgf_game = copy_game.to_sgftree().to_sgf(sgf_path)
        api = API(file=sgf_path, player=self.current_turn)

        analysis_response = api.deep_turn_area_analysis(
            turn=self.view_index - 1,
            selection=self.selected_area,
            invert_selection=self.invert_selection
        )

        print("Raw API Response:", analysis_response)

        try:
            if isinstance(analysis_response, str):
                analysis_json = json.loads(analysis_response)
            else:
                analysis_json = analysis_response

            self.display_analysis_results(analysis_json)

        except json.JSONDecodeError as e:
            print(f"Error decoding analysis response: {e}")
    
    def display_analysis_results(self, analysis_data: list):
        """
        Draws semi-transparent blue stones on the best moves.
        """
        # 1. Clear old analysis first
        self.clear_analysis_markers()
        i=1

        for item in analysis_data:
            move_str = item.get("move")
            score = item.get("scoreLead")
            
            # Convert to X/Y
            coords = self.gtp_to_coords(move_str)
            if coords is None: 
                continue 
            
            col, row = coords

            # Calculate pixel positions
            cx = self.margin + (col * self.cell_size)
            cy = self.margin + (row * self.cell_size)

            # A. Draw Blue Circle
            # We use 'tags' to group them so we can delete them easily later
            if i==1:
                self.canvas.create_oval(
                cx - self.stone_rad, cy - self.stone_rad,
                cx + self.stone_rad, cy + self.stone_rad,
                fill="#28B463",   # Darker Blue
                outline="#1D8348",
                width=2,
                tags="analysis_marker" 
            )
            else:
                self.canvas.create_oval(
                    cx - self.stone_rad, cy - self.stone_rad,
                    cx + self.stone_rad, cy + self.stone_rad,
                    fill="#5DADE2",   # Light Blue
                    outline="blue",
                    width=2,
                    tags="analysis_marker" 
                )

            # B. Draw Score Text
            score_text = str(round(score, 1)) if score is not None else "?"
            self.canvas.create_text(
                cx, cy, 
                text=score_text, 
                fill="white", 
                font=("Arial", 8, "bold"),
                tags="analysis_marker"
            )
            i+=1
    
    def clear_analysis_markers(self):
        """Deletes all visuals tagged as 'analysis_marker'."""
        self.canvas.delete("analysis_marker")

    def draw_stone(self, col, row, color):
        cx = self.margin + (col * self.cell_size)
        cy = self.margin + (row * self.cell_size)
        fill_color = 'black' if (color == 'B' or color == 'b') else 'white'
        outline = 'white' if (color == 'B' or color == 'b') else 'black'

        self.canvas.create_oval(
            cx - self.stone_rad, cy - self.stone_rad,
            cx + self.stone_rad, cy + self.stone_rad,
            fill=fill_color, outline=outline,
            tags="stone" # Tag allows us to delete them easily later
        )

    def analyze_game(self):

        sgf_path = self.get_temp_sgf_path("full_game_analysis.sgf")
        # Prepare a Game object reflecting current state
        current_rules = self.board_logic.game.ruleset

        if isinstance(current_rules, str):
            rules_arg = [current_rules]
        else:
            rules_arg = current_rules

        copy_game = Game(
            RU=rules_arg,  
            SZ=[str(self.board_logic.size[0])], 
            KM=[str(self.board_logic.game.komi)]
        )

        copy_game.moves = self.board_logic.game.moves[:]
        print(f"Moves given: {len(copy_game.moves)}")

        sgf_game = copy_game.to_sgftree().to_sgf(sgf_path)
        api = API(file=sgf_path, player=self.current_turn)

        analysis_response = api.all_moves_analysis()
        print("Raw API Response:", analysis_response)

        try:
            if isinstance(analysis_response, str):
                self.full_game_analysis = json.loads(analysis_response)
            else:
                self.full_game_analysis = analysis_response

            self.analysis_active = True
            self.show_score_graph()          
            self.update_classification_label()
        
        except json.JSONDecodeError as e:
            print(f"Error decoding analysis response: {e}")

    def show_score_graph(self):
        """Updates the embedded graph with real data."""
        if not self.full_game_analysis or "scoreLeadList" not in self.full_game_analysis:
            return

        self.ax.clear()

        # Extract Data
        score_leads = self.full_game_analysis["scoreLeadList"]
        moves = range(1, len(score_leads) + 1)

        # Plot Data
        self.ax.plot(moves, score_leads, color='#8E44AD', linewidth=1.5, label='Score')
        
        # Formatting
        self.ax.set_title("Score Lead", fontsize=9)
        self.ax.axhline(y=0, color='black', linestyle='--', linewidth=1, alpha=0.5)
        self.ax.grid(True, linestyle=':', alpha=0.5)
        
        # Dynamic Limits with padding
        if score_leads:
            max_val = max(abs(min(score_leads)), abs(max(score_leads)))
            limit = max(10, max_val + 5)
            self.ax.set_ylim(-limit, limit)

        # Fill Colors
        self.ax.fill_between(moves, score_leads, 0, where=[s >= 0 for s in score_leads], 
                        facecolor='green', alpha=0.1, interpolate=True)
        self.ax.fill_between(moves, score_leads, 0, where=[s < 0 for s in score_leads], 
                        facecolor='gray', alpha=0.1, interpolate=True)

        self.graph_canvas.draw()

    def update_classification_label(self):
        """Updates the classification text based on the current view_index."""
        if not self.analysis_active or not self.full_game_analysis:
            self.classification_label.config(text="")
            return

        # Case: Start of game
        if self.view_index == 0:
             self.classification_label.config(text="Start of Game", fg="black")
             return

        # Case: Normal Move
        # The API keys are strings "0", "1", "2"... corresponding to (move number - 1)
        target_key = str(self.view_index - 1)
        turn_data = self.full_game_analysis.get("turnData", {})

        if target_key in turn_data:
            data = turn_data[target_key]
            
            # Extract info
            classification = data.get('classification', 'N/A').upper()
            score_lead = data.get('scoreLead', 0.0)
            
            # Set Colors
            if classification in ["BEST", "EXCELLENT", "GOOD"]:
                color = "#28B463" # Green
            elif classification in ["MISTAKE", "BLUNDER"]:
                color = "#CB4335" # Red
            elif classification == "INACCURACY":
                color = "#D4AC0D" # Orange/Yellow
            else:
                color = "#333" # Gray

            # Set Text
            text = f"Move {self.view_index}: {classification} (Lead: {round(score_lead, 1)})"
            self.classification_label.config(text=text, fg=color)
        else:
            self.classification_label.config(text="No analysis data")

    def restart_game(self):
        """Resets the game logic and the visual board to the initial state."""
        print("Restarting game...")

        # 1. Clear Game Logic
        # We empty the master move list in the Game object
        self.board_logic.game.moves = []
        
        # We tell the board to rebuild itself from this empty list (effectively wiping the grid)
        self.board_logic.board_from_moves([])

        # 2. Reset UI State Variables
        self.view_index = 0
        self.current_turn = 'B' # Reset to Black (or whatever your game starts with)
        self.selection_mode = False
        self.invert_selection = False
        
        # 3. Clear Visuals
        self.canvas.delete("stone")             # Remove all stones
        self.clear_analysis_markers()           # Remove blue/green analysis dots
        self.clear_selection()                  # Remove red selection box

        self.classification_label.config(text="")

        # Reset Graph
        self.ax.clear()
        self.ax.set_title("Score Lead (New Game)", fontsize=9)
        self.ax.grid(True, linestyle=':', alpha=0.5)
        self.graph_canvas.draw()
        
        # 4. Reset Button Texts (Optional but good polish)
        self.invert_btn.config(text="Analysis: Inside Zone")
        self.select_btn.config(text="Select Area", relief="raised")
        self.master.title("Go - New Game")

# --- 4. MAIN EXECUTION ---
if __name__ == "__main__":

    parser = argparse.ArgumentParser(description="Run the Go Board GUI.")
    parser.add_argument(
        "--path", 
        type=str, 
        help="Path to an SGF file to load.",
        default=None # If not provided, it stays None
    )

    args = parser.parse_args()

    base_path = Path(__file__).resolve().parent.parent.parent
    games_dir = base_path / "games"

    if args.path:
        path_to_game = games_dir / args.path
        tree_imported = SgfTree.from_sgf(str(path_to_game))
        game = Game.from_sgftree(tree_imported)
        board_logic = Board(game, size=(game.size[0], game.size[1]), moves=game.moves)
        print(board_logic.game.next_color())

    else:
        print("No SGF path provided, starting a new game.")
        # 1. Setup Logic
        game = Game(RU=["Japanese"], SZ=["19"], KM=["6.5"])
        board_logic = Board(game)

    # 2. Setup GUI
    root = tk.Tk()

    root.title(f"Go Game - {'Replay' if args.path else 'New Game'}")
    gui = GoBoardUI(root, board_logic)

    if args.path:
        # Update view index to the end
        gui.view_index = len(game.moves)
        # Manually trigger the board update to show stones
        gui.update_board_to_current_index()
        print("Starting analysis for loaded game...")
        gui.master.after(1000, gui.analyze_game)  # Delay to ensure GUI is ready

    root.mainloop()