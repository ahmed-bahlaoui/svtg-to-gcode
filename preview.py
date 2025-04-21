# preview.py
import customtkinter as ctk
from tkinter import filedialog, messagebox

def show_gcode_preview(gcode_text):
    preview_win = ctk.CTkToplevel()
    preview_win.title("G-code Preview")
    preview_win.geometry("600x400")
    preview_win.attributes("-topmost", True)

    # Create main frame
    main_frame = ctk.CTkFrame(preview_win)
    main_frame.pack(fill="both", expand=True, padx=10, pady=10)

    # Add text area
    textbox = ctk.CTkTextbox(main_frame, wrap="none")
    textbox.pack(fill="both", expand=True, padx=5, pady=(5, 10))
    textbox.insert("1.0", gcode_text)
    textbox.configure(state="disabled")

    # Add save button
    def save_gcode():
        file_path = filedialog.asksaveasfilename(
            defaultextension=".gcode",
            filetypes=[("G-code files", "*.gcode")]
        )
        if file_path:
            try:
                with open(file_path, "w") as f:
                    f.write(gcode_text)
                messagebox.showinfo("Success", "G-code file saved successfully!")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to save file: {str(e)}")

    save_button = ctk.CTkButton(
        main_frame, 
        text="Save G-code", 
        command=save_gcode
    )
    save_button.pack(pady=(0, 5))