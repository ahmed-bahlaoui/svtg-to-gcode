# ui.py
import customtkinter as ctk
from tkinter import filedialog, messagebox
from logic import convert_svg_to_gcode
from preview import show_gcode_preview
import os


class GCodeApp:
    def __init__(self, master):
        self.master = master
        master.title("SVG to G-code Converter")
        master.geometry("600x300")
        master.minsize(500, 300)

        self.svg_path_var = ctk.StringVar()
        self.current_gcode = None  # Store the generated gcode

        # Main container frame
        self.frame = ctk.CTkFrame(master)
        self.frame.pack(fill="both", expand=True, padx=20, pady=20)

        self.frame.grid_columnconfigure(1, weight=1)  # Allow entry fields to stretch

        # --- SVG File Row ---
        ctk.CTkLabel(self.frame, text="SVG File:").grid(
            row=0, column=0, sticky="e", padx=10, pady=10
        )

        self.svg_entry = ctk.CTkEntry(self.frame, textvariable=self.svg_path_var)
        self.svg_entry.grid(row=0, column=1, sticky="ew", padx=(0, 10))

        ctk.CTkButton(self.frame, text="Browse", command=self.browse_file).grid(
            row=0, column=2, padx=10
        )

        # --- Parameters ---
        self._add_param("Movement Speed:", 1, "3000")
        self._add_param("Cutting Speed:", 2, "3000")
        self._add_param("Pass Depth:", 3, "0")

        # --- Buttons Frame ---
        button_frame = ctk.CTkFrame(self.frame)
        button_frame.grid(row=4, column=1, pady=20)

        # Convert and Save Button
        self.convert_btn = ctk.CTkButton(
            button_frame, text="Convert and Save", command=self.generate_and_save_gcode
        )
        self.convert_btn.pack(side="left", padx=5)

        # Preview Button
        self.preview_btn = ctk.CTkButton(
            button_frame,
            text="Preview",
            command=self.preview_gcode,
            state="normal",
        )
        self.preview_btn.pack(side="left", padx=5)

        # --- Resize behavior ---
        master.bind("<Configure>", self.on_resize)

    def _add_param(self, label, row, default_value):
        ctk.CTkLabel(self.frame, text=label).grid(
            row=row, column=0, sticky="e", padx=10, pady=5
        )
        entry = ctk.CTkEntry(self.frame)
        entry.insert(0, default_value)
        entry.grid(row=row, column=1, sticky="ew", padx=(0, 10))
        setattr(self, f"param_{row}", entry)

    def browse_file(self):
        file_path = filedialog.askopenfilename(filetypes=[("SVG files", "*.svg")])
        if file_path:
            self.svg_path_var.set(file_path)

    def generate_gcode(self):
        try:
            svg_path = self.svg_path_var.get()
            movement_speed = int(self.param_1.get())
            cutting_speed = int(self.param_2.get())
            pass_depth = float(self.param_3.get())

            self.current_gcode = convert_svg_to_gcode(
                svg_path, movement_speed, cutting_speed, pass_depth
            )
            return True
        except Exception as e:
            messagebox.showerror("Error", str(e))
            return False

    def generate_and_save_gcode(self):
        if self.generate_gcode():
            self.save_gcode()
            self.preview_btn.configure(state="normal")  # Enable preview button

    def save_gcode(self):
        file_path = filedialog.asksaveasfilename(
            defaultextension=".gcode",
            filetypes=[("G-code files", "*.gcode")],
            initialfile=os.path.splitext(os.path.basename(self.svg_path_var.get()))[0]
            + ".gcode",
        )
        if file_path and self.current_gcode:
            with open(file_path, "w") as f:
                f.write(self.current_gcode)
            messagebox.showinfo("Success", "G-code file saved successfully!")

    def preview_gcode(self):
        try:
            # Get the SVG path
            svg_path = self.svg_path_var.get()
            if not svg_path:
                messagebox.showerror("Error", "Please select an SVG file first")
                return

            # Get parameters
            movement_speed = self.param_1.get()
            cutting_speed = self.param_2.get()
            pass_depth = self.param_3.get()

            # Generate G-code without saving
            try:
                gcode = convert_svg_to_gcode(
                    svg_path,
                    movement_speed=float(movement_speed),
                    cutting_speed=float(cutting_speed),
                    pass_depth=float(pass_depth),
                )
                # Store the generated gcode
                self.current_gcode = gcode
                # Show preview
                show_gcode_preview(gcode)
            except ValueError as e:
                messagebox.showerror(
                    "Error", "Please enter valid numbers for speeds and depth"
                )
            except Exception as e:
                messagebox.showerror("Error", f"Failed to generate preview: {str(e)}")

        except Exception as e:
            messagebox.showerror("Error", f"Preview failed: {str(e)}")

    def on_resize(self, event):
        """Handle window resize events"""
        # Minimum width to prevent UI elements from overlapping
        min_width = 500
        # If window gets too small, enforce minimum size
        if event.widget == self.master:  # Only respond to main window resizes
            if event.width < min_width:
                self.master.geometry(f"{min_width}x{event.height}")
