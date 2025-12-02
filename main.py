import tkinter as tk
from tkinter import filedialog, messagebox, ttk
from PIL import Image, ImageTk
import os
import shutil

class GradientFrameGenerator:
    def __init__(self, root):
        self.root = root
        self.root.title("Gradient Frame Generator")
        self.root.geometry("1200x800")

        self.save_folder = "save"
        os.makedirs(self.save_folder, exist_ok=True)

        self.image1_path = None
        self.image2_path = None
        self.color_pairs = []
        self.color_entries = []
        self.current_frame = 0

        self.setup_ui()
        
    def setup_ui(self):
        main_container = tk.Frame(self.root)
        main_container.pack(fill=tk.BOTH, expand=True)

        self.canvas = tk.Canvas(main_container)
        scrollbar = ttk.Scrollbar(main_container, orient="vertical", command=self.canvas.yview)

        self.canvas_frame = tk.Frame(self.canvas)

        self.canvas_frame.bind("<Configure>", lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all")))

        self.canvas_window = self.canvas.create_window((0, 0), window=self.canvas_frame, anchor="n")

        self.canvas.configure(yscrollcommand=scrollbar.set)

        self.canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        self.canvas.bind_all("<MouseWheel>", self._on_mousewheel)

        self.canvas.bind("<Configure>", self._center_content)

        center_frame = tk.Frame(self.canvas_frame)
        center_frame.pack(expand=True, fill=tk.X)

        title_label = tk.Label(center_frame, text="Gradient Frame Generator", font=("Arial", 16, "bold"))
        title_label.pack(pady=(0, 10))

        images_container = tk.Frame(center_frame)
        images_container.pack(fill=tk.BOTH, expand=True, padx=20)

        self.left_frame = tk.LabelFrame(images_container, text="Starting Image", padx=10, pady=10)
        self.left_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 10))
    
        self.left_image_label = tk.Label(self.left_frame, text="No image loaded", bg="gray90", width=40, height=20)
        self.left_image_label.pack(padx=10, pady=10)
    
        left_btn_frame = tk.Frame(self.left_frame)
        left_btn_frame.pack()
    
        tk.Button(left_btn_frame, text="Load Image 1", command=self.load_image1).pack(side=tk.LEFT, padx=5)

        self.right_frame = tk.LabelFrame(images_container, text="Ending Image", padx=10, pady=10)
        self.right_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=(10, 0))
    
        self.right_image_label = tk.Label(self.right_frame, text="No image loaded", bg="gray90", width=40, height=20)
        self.right_image_label.pack(padx=10, pady=10)
    
        right_btn_frame = tk.Frame(self.right_frame)
        right_btn_frame.pack()
    
        tk.Button(right_btn_frame, text="Load Image 2", command=self.load_image2).pack(side=tk.LEFT, padx=5)

        color_container = tk.Frame(center_frame)
        color_container.pack(fill=tk.X, expand=True, padx=20, pady=(10, 0))
    
        color_frame = tk.LabelFrame(color_container, text="Color Mapping", padx=10, pady=10)
        color_frame.pack(fill=tk.X, expand=True)

        header_frame = tk.Frame(color_frame)
        header_frame.pack(fill=tk.X, pady=(0, 10))

        start_header_frame = tk.Frame(header_frame, width=135, height=25)
        start_header_frame.grid(row=0, column=0, padx=(0, 15), sticky="w")
        start_header_frame.grid_propagate(False)
    
        end_header_frame = tk.Frame(header_frame, width=135, height=25)
        end_header_frame.grid(row=0, column=1, padx=(0, 15), sticky="w")
        end_header_frame.grid_propagate(False)
    
        preview_header_frame = tk.Frame(header_frame, width=40, height=25)
        preview_header_frame.grid(row=0, column=2, padx=(0, 15), sticky="w")
        preview_header_frame.grid_propagate(False)

        remove_header_frame = tk.Frame(header_frame, width=40, height=25)
        remove_header_frame.grid(row=0, column=3, sticky="w")
        remove_header_frame.grid_propagate(False)

        tk.Label(start_header_frame, text="Starting Color", font=("Arial", 10, "bold"), anchor="w").pack(fill=tk.BOTH, expand=True, anchor="w")
        tk.Label(end_header_frame, text="Ending Color", font=("Arial", 10, "bold"), anchor="w").pack(fill=tk.BOTH, expand=True, anchor="w")
        tk.Label(preview_header_frame, text="Preview", font=("Arial", 10, "bold"), anchor="w").pack(fill=tk.BOTH, expand=True, anchor="w")
        tk.Label(remove_header_frame, text="", font=("Arial", 10, "bold")).pack(fill=tk.BOTH, expand=True)

        header_frame.grid_columnconfigure(0, weight=1, minsize=120)
        header_frame.grid_columnconfigure(1, weight=1, minsize=120)
        header_frame.grid_columnconfigure(2, weight=0, minsize=40)
        header_frame.grid_columnconfigure(3, weight=0, minsize=40)

        self.color_container = tk.Frame(color_frame)
        self.color_container.pack(fill=tk.X)

        self.add_color_pair()

        btn_frame = tk.Frame(color_frame)
        btn_frame.pack(fill=tk.X, pady=5)
    
        tk.Button(btn_frame, text="+ Add Color", command=self.add_color_pair, bg="lightblue").pack(side=tk.LEFT)

        controls_container = tk.Frame(center_frame)
        controls_container.pack(fill=tk.X, expand=True, padx=20, pady=(10, 0))
    
        controls_frame = tk.LabelFrame(controls_container, text="Generation Controls", padx=10, pady=10)
        controls_frame.pack(fill=tk.X, expand=True)

        slider_frame = tk.Frame(controls_frame)
        slider_frame.pack(fill=tk.X, pady=(0, 10))
    
        tk.Label(slider_frame, text="Number of Frames:").pack(side=tk.LEFT, padx=(0, 10))
    
        self.frame_count_var = tk.IntVar(value=10)
        self.frame_slider = tk.Scale(slider_frame, from_=2, to=500, variable=self.frame_count_var, orient=tk.HORIZONTAL, length=300)
        self.frame_slider.pack(side=tk.LEFT)
    
        tk.Label(slider_frame, textvariable=self.frame_count_var, width=4).pack(side=tk.LEFT, padx=(5, 0))

        start_button_frame = tk.Frame(controls_frame)
        start_button_frame.pack(fill=tk.X, pady=10)
    
        self.start_button = tk.Button(start_button_frame, text="START GENERATION", command=self.start_generation, bg="lightgreen", font=("Arial", 12, "bold"), padx=20, pady=10)
        self.start_button.pack()

        self.status_label = tk.Label(center_frame, text="Ready", fg="blue")
        self.status_label.pack(pady=(10, 20))

    def _center_content(self, event):
        canvas_width = event.width

        self.canvas_frame.update_idletasks()
        frame_width = self.canvas_frame.winfo_reqwidth()

        if frame_width < canvas_width:
            new_x = (canvas_width - frame_width) // 2
        else:
            new_x = 0

        self.canvas.coords(self.canvas_window, new_x, 0)

        self.canvas.itemconfig(self.canvas_window, width=max(frame_width, canvas_width))

    def _on_mousewheel(self, event):
        if hasattr(event, 'delta'):
            self.canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")
        elif event.num == 5:
            self.canvas.yview_scroll(1, "units")
        elif event.num == 4:
            self.canvas.yview_scroll(-1, "units")
        
    def load_image1(self):
        path = filedialog.askopenfilename(
            filetypes=[("Image files", "*.png *.jpg *.jpeg *.bmp *.gif")]
        )
        if path:
            self.image1_path = path
            self.display_image(path, self.left_image_label)
            
    def load_image2(self):
        path = filedialog.askopenfilename(
            filetypes=[("Image files", "*.png *.jpg *.jpeg *.bmp *.gif")]
        )
        if path:
            self.image2_path = path
            self.display_image(path, self.right_image_label)
            
    def display_image(self, path, label):
        try:
            img = Image.open(path)
            img.thumbnail((400, 400))
            photo = ImageTk.PhotoImage(img)
            label.configure(image=photo, text="")
            label.image = photo
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load image: {str(e)}")
    
    def add_color_pair(self):
        color_frame = tk.Frame(self.color_container)
        color_frame.pack(fill=tk.X, pady=5)

        color_frame.widget_id = len(self.color_entries)

        start_color_entry = tk.Entry(color_frame, width=10, font=("Arial", 10))
        start_color_entry.insert(0, "#000000")
        start_color_entry.grid(row=0, column=0, padx=(0, 15), sticky="ew")

        end_color_entry = tk.Entry(color_frame, width=10, font=("Arial", 10))
        end_color_entry.insert(0, "#000000")
        end_color_entry.grid(row=0, column=1, padx=(0, 15), sticky="ew")

        preview_frame = tk.Frame(color_frame, width=40, height=40, bg="gray", relief="solid", bd=1)
        preview_frame.grid(row=0, column=2, padx=(0, 15), sticky="w")
        preview_frame.grid_propagate(False)

        preview_label = tk.Label(preview_frame, text="→", font=("Arial", 20, "bold"), bg="gray", fg="black")
        preview_label.place(relx=0.5, rely=0.5, anchor="center")
        remove_button = tk.Button(color_frame, text="−", width=3, font=("Arial", 10, "bold"), bg="salmon", fg="white", command=lambda: self.remove_color_pair(color_frame))

        if len(self.color_entries) == 0:
            remove_button.grid_remove()
        else:
            remove_button.grid(row=0, column=3, sticky="w")

        color_frame.grid_columnconfigure(0, weight=1, minsize=120)
        color_frame.grid_columnconfigure(1, weight=1, minsize=120)
        color_frame.grid_columnconfigure(2, weight=0, minsize=40)
        color_frame.grid_columnconfigure(3, weight=0, minsize=40)

        color_widgets = {
            'frame': color_frame,
            'start_entry': start_color_entry,
            'end_entry': end_color_entry,
            'preview_label': preview_label,
            'preview_frame': preview_frame,
            'remove_button': remove_button
        }
        self.color_entries.append(color_widgets)

        start_color_entry.bind('<KeyRelease>', lambda e, w=color_widgets: self.update_preview(w))
        end_color_entry.bind('<KeyRelease>', lambda e, w=color_widgets: self.update_preview(w))

        self.update_preview(color_widgets)

        self.update_remove_buttons()

    def update_preview(self, widgets):
        try:
            start_color = widgets['start_entry'].get()
            end_color = widgets['end_entry'].get()

            if (start_color.startswith('#') and len(start_color) == 7 and
                end_color.startswith('#') and len(end_color) == 7):

                widgets['preview_label'].configure(bg=start_color, fg=end_color)

                widgets['preview_frame'].configure(bg=start_color)
            
            else:
                widgets['preview_label'].configure(bg="gray", fg="black")
                widgets['preview_frame'].configure(bg="gray")
            
        except Exception as e:
            widgets['preview_label'].configure(bg="gray", fg="black")
            widgets['preview_frame'].configure(bg="gray")

    def remove_color_pair(self, color_frame):
        for i, widgets in enumerate(self.color_entries):
            if widgets['frame'] == color_frame:
                self.color_entries.pop(i)

                color_frame.destroy()

                self.update_remove_buttons()
                break

    def update_remove_buttons(self):
        for i, widgets in enumerate(self.color_entries):
            if i == 0:
                if 'remove_button' in widgets:
                    widgets['remove_button'].grid_remove()
            else:
                if 'remove_button' in widgets:
                    widgets['remove_button'].grid(row=0, column=3, sticky="w")

    def get_brightness(self, hex_color):
        """Calculate brightness of a hex color"""
        hex_color = hex_color.lstrip('#')
        r, g, b = int(hex_color[0:2], 16), int(hex_color[2:4], 16), int(hex_color[4:6], 16)
        return (r * 299 + g * 587 + b * 114) / 1000
    
    def hex_to_rgb(self, hex_color):
        """Convert hex color to RGB tuple"""
        hex_color = hex_color.lstrip('#')
        return tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))
    
    def rgb_to_hex(self, rgb):
        """Convert RGB tuple to hex color"""
        return '#{:02x}{:02x}{:02x}'.format(*rgb)
    
    def start_generation(self):
        if not self.image1_path or not self.image2_path:
            messagebox.showwarning("Warning", "Please load both images!")
            return

        self.color_pairs = []
        for widgets in self.color_entries:
            start_color = widgets['start_entry'].get().strip().upper()
            end_color = widgets['end_entry'].get().strip().upper()

            if (len(start_color) == 7 and start_color.startswith('#') and
                len(end_color) == 7 and end_color.startswith('#')):
                self.color_pairs.append((start_color, end_color))
            else:
                messagebox.showwarning("Warning", 
                    f"Invalid color format: {start_color} or {end_color}\nUse #RRGGBB format")
                return
        
        if not self.color_pairs:
            messagebox.showwarning("Warning", "Please add at least one color pair!")
            return

        frame_count = self.frame_count_var.get()

        self.status_label.config(text="Generating frames...", fg="orange")
        self.root.update()
        
        try:
            img1 = Image.open(self.image1_path).convert('RGBA')
            img2 = Image.open(self.image2_path).convert('RGBA')

            if img1.size != img2.size:
                img2 = img2.resize(img1.size)

            pixels1 = img1.load()
            pixels2 = img2.load()

            color_positions = {}
            for start_color, _ in self.color_pairs:
                rgb_target = self.hex_to_rgb(start_color)
                positions = []

                for x in range(img1.width):
                    for y in range(img1.height):
                        if pixels1[x, y][:3] == rgb_target:
                            positions.append((x, y))
                
                if positions:
                    color_positions[start_color] = positions
                else:
                    print(f"Warning: Color {start_color} not found in starting image")

            output_dir = os.path.join(self.save_folder, f"gradient_frames_{len(os.listdir(self.save_folder))}")
            os.makedirs(output_dir, exist_ok=True)

            for frame in range(frame_count):
                result = Image.new('RGBA', img1.size)
                result_pixels = result.load()

                factor = frame / (frame_count - 1) if frame_count > 1 else 0

                for x in range(img1.width):
                    for y in range(img1.height):
                        result_pixels[x, y] = pixels1[x, y]

                for start_color, end_color in self.color_pairs:
                    if start_color in color_positions:
                        rgb_start = self.hex_to_rgb(start_color)
                        rgb_end = self.hex_to_rgb(end_color)
                        
                        for x, y in color_positions[start_color]:
                            r1, g1, b1, a1 = pixels1[x, y]
                            r2, g2, b2, a2 = pixels2[x, y]

                            r = int(r1 + (r2 - r1) * factor)
                            g = int(g1 + (g2 - g1) * factor)
                            b = int(b1 + (b2 - b1) * factor)
                            a = int(a1 + (a2 - a1) * factor)
                            
                            result_pixels[x, y] = (r, g, b, a)

                result.save(os.path.join(output_dir, f"frame_{frame:04d}.png"))

                if frame % 10 == 0:
                    self.status_label.config(text=f"Generating... {frame+1}/{frame_count}")
                    self.root.update()

            self.status_label.config(text=f"{frame_count} frames saved to {output_dir}", fg="green")
            messagebox.showinfo("Success", 
                f"Generated {frame_count} frames!\nSaved to: {output_dir}")
            
        except Exception as e:
            self.status_label.config(text="Error!", fg="red")
            messagebox.showerror("Error", f"Generation failed: {str(e)}")

def main():
    root = tk.Tk()
    app = GradientFrameGenerator(root)
    root.mainloop()

if __name__ == "__main__":
    main()