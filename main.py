import tkinter as tk
from tkinter import filedialog, messagebox, ttk
from PIL import Image, ImageTk
import os
import math

class GradientFrameGenerator:
    def __init__(self, root):
        self.notebook = None
        self.root = root
        self.root.title("Gradient Frame Generator")
        self.root.geometry("1200x800")

        self.save_folder = "save"
        os.makedirs(self.save_folder, exist_ok=True)

        self.auto_mode = tk.BooleanVar(value=True)

        self.frame_extractor_mode = tk.BooleanVar(value=False)

        self.image1_path = None
        self.image2_path = None
        self.color_pairs = []
        self.color_entries = []
        self.current_frame = 0

        self.setup_ui()

        self.create_menu_bar()
        self.name_pattern = tk.StringVar(value="frame_{number:04d}")
        self.custom_name_enabled = tk.BooleanVar(value=False)

    def create_menu_bar(self):
        menubar = tk.Menu(self.root)
        self.root.config(menu=menubar)

        file_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="File", menu=file_menu)
        file_menu.add_command(label="Change output naming", command=self.open_naming_settings)
        file_menu.add_command(label="Reset to Default", command=self.reset_naming_settings)
        file_menu.add_separator()
        file_menu.add_command(label="Exit", command=self.root.quit)

        about_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="About", menu=about_menu)
        about_menu.add_command(label="Bug reports/Feature Requests", command=lambda: self.open_url("https://github.com/WMZS-Modding/gradient-frame-generator/issues"))
        about_menu.add_command(label="Pull Requests", command=lambda: self.open_url("https://github.com/WMZS-Modding/gradient-frame-generator/pulls"))
        about_menu.add_command(label="Discord", command=lambda: self.open_url("https://discord.gg/5BWTwGf8Rt"))
        about_menu.add_command(label="YouTube", command=lambda: self.open_url("https://youtube.com/@SuperHero20102"))
        about_menu.add_separator()
        about_menu.add_command(label="Check for update", command=lambda: self.open_url("https://github.com/WMZS-Modding/gradient-frame-generator/releases"))
        about_menu.add_command(label="About", command=self.show_about)

    def open_url(self, url):
        import webbrowser
        try:
            webbrowser.open(url)
        except Exception as e:
            messagebox.showerror("Error", f"Could not open URL: {e}")

    def setup_ui(self):
        main_container = tk.Frame(self.root)
        main_container.pack(fill=tk.BOTH, expand=True)

        self.canvas = tk.Canvas(main_container, highlightthickness=0)
        scrollbar = ttk.Scrollbar(main_container, orient="vertical", command=self.canvas.yview)

        self.canvas_frame = tk.Frame(self.canvas)

        self.canvas_window = self.canvas.create_window((0, 0), window=self.canvas_frame, anchor="n")

        self.canvas.configure(yscrollcommand=scrollbar.set)

        self.canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        self.canvas.bind_all("<MouseWheel>", self._on_mousewheel)

        self.canvas.bind("<Configure>", self._center_content)
        self.canvas_frame.bind("<Configure>", self._update_scrollregion)

        self.canvas.bind_all("<MouseWheel>", self._on_mousewheel)
        self.canvas.bind_all("<Button-4>", self._on_mousewheel)
        self.canvas.bind_all("<Button-5>", self._on_mousewheel)

        center_frame = tk.Frame(self.canvas_frame)
        center_frame.pack(expand=True, fill=tk.X, padx=20)

        title_label = tk.Label(center_frame, text="Gradient Frame Generator", font=("Arial", 16, "bold"))
        title_label.pack(pady=(0, 10))

        self.notebook = ttk.Notebook(self.canvas_frame)
        self.notebook.pack(fill=tk.BOTH, expand=True, padx=20, pady=(0, 10))

        self.gradient_tab = tk.Frame(self.notebook)
        self.notebook.add(self.gradient_tab, text="Gradient Frame Generator")
        self._setup_gradient_tab()

        self.extractor_tab = tk.Frame(self.notebook)
        self.notebook.add(self.extractor_tab, text="Frame Extractor")
        self._setup_extractor_tab()

        self.notebook.bind("<<NotebookTabChanged>>", self.on_tab_changed)

    def _setup_gradient_tab(self):
        images_container = tk.Frame(self.gradient_tab)
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

        color_container = tk.Frame(self.gradient_tab)
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

        controls_container = tk.Frame(self.gradient_tab)
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

        mode_frame = tk.Frame(controls_frame)
        mode_frame.pack(fill=tk.X, pady=(0, 10))

        tk.Label(mode_frame, text="Mode:").pack(side=tk.LEFT, padx=(0, 10))

        self.mode_toggle = tk.Checkbutton(mode_frame, text="Auto Mode", variable=self.auto_mode, command=self.toggle_mode, font=("Arial", 10))
        self.mode_toggle.pack(side=tk.LEFT)

        self.mode_desc = tk.Label(mode_frame, text="", fg="gray", font=("Arial", 9))
        self.mode_desc.pack(side=tk.LEFT, padx=(10, 0))

        controls_container = tk.Frame(self.gradient_tab)
        controls_container.pack(fill=tk.X, expand=True, padx=20, pady=(10, 0))

        controls_frame = tk.LabelFrame(controls_container, text="Generation Controls", padx=10, pady=10)
        controls_frame.pack(fill=tk.X, expand=True)

        self.start_button = tk.Button(self.gradient_tab, text="START GENERATION", command=self.start_generation, bg="lightgreen", font=("Arial", 12, "bold"), padx=20, pady=10)
        self.start_button.pack()

        self.status_label = tk.Label(self.gradient_tab, text="Ready", fg="blue")
        self.status_label.pack(pady=(10, 20))

    def _setup_extractor_tab(self):
        extractor_title = tk.Label(self.extractor_tab, text="Frame Extractor", font=("Arial", 14, "bold"))
        extractor_title.pack(pady=(0, 10))

        desc = tk.Label(self.extractor_tab, text="Extract individual frames from sprite sheets or image sequences", fg="gray", font=("Arial", 10))
        desc.pack(pady=(0, 20))

        notebook_container = tk.Frame(self.extractor_tab, height=500)
        notebook_container.pack(fill=tk.X, pady=(0, 10))
        notebook_container.pack_propagate(False)

        self.extractor_notebook = ttk.Notebook(notebook_container)
        self.extractor_notebook.pack(fill=tk.BOTH, expand=True)

        self.single_tab = tk.Frame(self.extractor_notebook)
        self.extractor_notebook.add(self.single_tab, text="Single Image")
        self._setup_single_extractor()

        self.folder_tab = tk.Frame(self.extractor_notebook)
        self.extractor_notebook.add(self.folder_tab, text="Folder Batch")
        self._setup_folder_extractor()

        tk.Button(self.extractor_tab, text="EXTRACT FRAMES", command=self.extract_frames, bg="lightblue", font=("Arial", 12, "bold"), padx=20, pady=10).pack(pady=20)

        self.extractor_status = tk.Label(self.extractor_tab, text="Ready", fg="blue")
        self.extractor_status.pack()

    def _setup_single_extractor(self):
        input_frame = tk.LabelFrame(self.single_tab, text="Input Image", padx=10, pady=10)
        input_frame.pack(fill=tk.X, pady=(0, 10))

        self.extractor_image_label = tk.Label(input_frame, text="No image loaded", bg="gray90", width=50, height=15)
        self.extractor_image_label.pack(padx=10, pady=10)

        tk.Button(input_frame, text="Load Sprite Sheet", command=self.load_extractor_image).pack()

        size_frame = tk.LabelFrame(self.single_tab, text="Frame Settings", padx=10, pady=10)
        size_frame.pack(fill=tk.X, pady=(0, 10))

        width_frame = tk.Frame(size_frame)
        width_frame.pack(fill=tk.X, pady=(0, 10))

        tk.Label(width_frame, text="Frame Width:", width=15, anchor="w").pack(side=tk.LEFT)
        self.frame_width_var = tk.IntVar(value=32)
        self.frame_width_entry = tk.Entry(width_frame, textvariable=self.frame_width_var, width=10)
        self.frame_width_entry.pack(side=tk.LEFT, padx=(10, 0))
        tk.Label(width_frame, text="px").pack(side=tk.LEFT, padx=(5, 0))

        height_frame = tk.Frame(size_frame)
        height_frame.pack(fill=tk.X, pady=(0, 10))

        tk.Label(height_frame, text="Frame Height:", width=15, anchor="w").pack(side=tk.LEFT)
        self.frame_height_var = tk.IntVar(value=32)
        self.frame_height_entry = tk.Entry(height_frame, textvariable=self.frame_height_var, width=10)
        self.frame_height_entry.pack(side=tk.LEFT, padx=(10, 0))
        tk.Label(height_frame, text="px").pack(side=tk.LEFT, padx=(5, 0))

    def _setup_folder_extractor(self):
        folder_frame = tk.LabelFrame(self.folder_tab, text="Input Folder (Sprite Sheets)", padx=10, pady=10)
        folder_frame.pack(fill=tk.X, pady=(0, 10))

        self.folder_path_var = tk.StringVar(value="No folder selected")
        folder_label = tk.Label(folder_frame, textvariable=self.folder_path_var, bg="white", relief="sunken", anchor="w", padx=5, pady=5)
        folder_label.pack(fill=tk.X, padx=10, pady=(10, 5))

        tk.Button(folder_frame, text="Browse Folder", command=self.select_extractor_folder).pack(pady=(5, 10))

    def open_naming_settings(self):
        dialog = tk.Toplevel(self.root)
        dialog.title("Output Naming Settings")
        dialog.geometry("400x250")
        dialog.transient(self.root)
        dialog.grab_set()

        dialog.update_idletasks()
        x = self.root.winfo_x() + (self.root.winfo_width() // 2) - (400 // 2)
        y = self.root.winfo_y() + (self.root.winfo_height() // 2) - (250 // 2)
        dialog.geometry(f"+{x}+{y}")

        tk.Label(dialog, text="Custom Output Naming", font=("Arial", 12, "bold")).pack(pady=(10, 5))

        enable_frame = tk.Frame(dialog)
        enable_frame.pack(fill=tk.X, padx=20, pady=(5, 10))

        tk.Checkbutton(enable_frame, text="Enable custom naming", variable=self.custom_name_enabled, command=lambda: self.update_naming_widgets(dialog)).pack(anchor="w")

        pattern_frame = tk.Frame(dialog)
        pattern_frame.pack(fill=tk.X, padx=20, pady=(5, 10))

        tk.Label(pattern_frame, text="Naming Pattern:", anchor="w").pack(fill=tk.X, pady=(0, 5))

        self.pattern_entry = tk.Entry(pattern_frame, width=40)
        self.pattern_entry.insert(0, self.name_pattern.get())
        self.pattern_entry.pack(fill=tk.X)

        warning_frame = tk.Frame(dialog)
        warning_frame.pack(fill=tk.X, padx=20, pady=(5, 5))

        self.warning_label = tk.Label(warning_frame, text="Must include {number} placeholder", fg="red", font=("Arial", 9))
        self.warning_label.pack()
        self.warning_label.pack_forget()

        button_frame = tk.Frame(dialog)
        button_frame.pack(fill=tk.X, padx=20, pady=(10, 10))

        tk.Button(button_frame, text="Cancel", command=dialog.destroy, width=10).pack(side=tk.LEFT, padx=(0, 10))

        tk.Button(button_frame, text="Save", command=lambda: self.save_naming_settings(dialog), bg="lightgreen", width=10).pack(side=tk.LEFT)

        self.update_naming_widgets(dialog)

    def update_naming_widgets(self, dialog):
        if hasattr(self, 'pattern_entry'):
            state = 'normal' if self.custom_name_enabled.get() else 'disabled'
            self.pattern_entry.config(state=state)

            if state == 'normal':
                self.check_pattern_validity()
            else:
                self.warning_label.pack_forget()

    def check_pattern_validity(self):
        pattern = self.pattern_entry.get()
        if '{number' in pattern:
            self.warning_label.pack_forget()
            return True
        else:
            self.warning_label.pack()
            return False

    def save_naming_settings(self, dialog):
        if self.custom_name_enabled.get():
            pattern = self.pattern_entry.get()

            if '{number' not in pattern:
                messagebox.showerror("Invalid Pattern", "Pattern must include {number} placeholder!")
                return

            try:
                test_pattern = pattern.replace('{number', '{0')
                test_pattern.format(0)
                self.name_pattern.set(pattern)
            except Exception as e:
                messagebox.showerror("Invalid Format", 
                    f"Pattern format error: {str(e)}\n\n"
                    "Valid formats:\n"
                    "- {number:04d} - 4-digit zero padding\n"
                    "- {number:03d} - 3-digit zero padding\n"
                    "- {number:d} - no padding\n"
                    "- {number:02d} - 2-digit zero padding")
                return
        else:
            self.name_pattern.set("frame_{number:04d}")

        dialog.destroy()
        messagebox.showinfo("Settings Saved", f"Naming pattern updated to:\n{self.name_pattern.get()}")

    def reset_naming_settings(self):
        self.custom_name_enabled.set(False)
        self.name_pattern.set("frame_{number:04d}")
        messagebox.showinfo("Settings Reset", "Naming pattern reset to default: frame_{number:04d}")

    def _center_content(self, event):
        self._update_scrollregion()

        canvas_width = self.canvas.winfo_width()

        self.canvas_frame.update_idletasks()
        frame_width = self.canvas_frame.winfo_reqwidth()

        if frame_width < canvas_width:
            new_x = (canvas_width - frame_width) // 2
        else:
            new_x = 0

        self.canvas.coords(self.canvas_window, new_x, 0)

        self.canvas.itemconfig(self.canvas_window, width=canvas_width)

    def _on_mousewheel(self, event):
        if hasattr(event, 'delta'):
            delta = event.delta
            if delta:
                self.canvas.yview_scroll(int(-1 * (delta / 120)), "units")

        elif event.num in (4, 5):
            delta = -1 if event.num == 4 else 1
            self.canvas.yview_scroll(delta, "units")

        return "break"

    def _update_scrollregion(self, event=None):
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))

    def load_image1(self):
        path = filedialog.askopenfilename(filetypes=[("Image files", "*.png *.jpg *.jpeg *.bmp *.gif")])
        if path:
            self.image1_path = path
            self.display_image(path, self.left_image_label)

    def load_image2(self):
        path = filedialog.askopenfilename(filetypes=[("Image files", "*.png *.jpg *.jpeg *.bmp *.gif")])
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

    def toggle_mode(self):
        if self.auto_mode.get():
            self.mode_desc.config(text="(Automatically detects color differences)")

            color_frame = self.color_container.master
            color_frame.pack_forget()

        else:
            self.mode_desc.config(text="(Manually specify color mappings)")

            color_frame = self.color_container.master
            color_frame.pack(fill=tk.X, pady=(10, 0))

        self.root.update_idletasks()
        self._update_scrollregion()

    def get_brightness(self, hex_color):
        hex_color = hex_color.lstrip('#')
        r, g, b = int(hex_color[0:2], 16), int(hex_color[2:4], 16), int(hex_color[4:6], 16)
        return (r * 299 + g * 587 + b * 114) / 1000

    def hex_to_rgb(self, hex_color):
        hex_color = hex_color.lstrip('#')
        return tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))

    def rgb_to_hex(self, rgb):
        return '#{:02x}{:02x}{:02x}'.format(*rgb)

    def start_generation(self):
        if not self.image1_path or not self.image2_path:
            messagebox.showwarning("Warning", "Please load both images!")
            return

        if self.auto_mode.get():
            self.start_auto_generation()
        else:
            self.start_manual_generation()

    def start_auto_generation(self):
        if not self.image1_path or not self.image2_path:
            messagebox.showwarning("Warning", "Please load both images!")
            return

        frame_count = self.frame_count_var.get()

        self.status_label.config(text="Analyzing images...", fg="orange")
        self.root.update()

        try:
            img1 = Image.open(self.image1_path).convert('RGBA')
            img2 = Image.open(self.image2_path).convert('RGBA')

            if img1.size != img2.size:
                img2 = img2.resize(img1.size)

            pixels1 = img1.load()
            pixels2 = img2.load()

            color_positions = {}
            for x in range(img1.width):
                for y in range(img1.height):
                    color1 = pixels1[x, y][:3]
                    color2 = pixels2[x, y][:3]

                    if color1 != color2:
                        hex_color = self.rgb_to_hex(color1)
                        if hex_color not in color_positions:
                            color_positions[hex_color] = []
                        color_positions[hex_color].append((x, y))

            if not color_positions:
                messagebox.showinfo("Info", "No color differences found between images!")
                return

            print(f"Found {len(color_positions)} unique colors to animate")

            output_dir = os.path.join(self.save_folder, f"gradient_frames_{len(os.listdir(self.save_folder))}")
            os.makedirs(output_dir, exist_ok=True)

            self.status_label.config(text="Generating frames...", fg="orange")
            self.root.update()

            for frame in range(frame_count):
                result = Image.new('RGBA', img1.size)
                result_pixels = result.load()

                factor = frame / (frame_count - 1) if frame_count > 1 else 0

                for x in range(img1.width):
                    for y in range(img1.height):
                        result_pixels[x, y] = pixels1[x, y]

                for hex_color, positions in color_positions.items():
                    for x, y in positions:
                        r1, g1, b1, a1 = pixels1[x, y]
                        r2, g2, b2, a2 = pixels2[x, y]

                        r = int(r1 + (r2 - r1) * factor)
                        g = int(g1 + (g2 - g1) * factor)
                        b = int(b1 + (b2 - b1) * factor)
                        a = int(a1 + (a2 - a1) * factor)

                        result_pixels[x, y] = (r, g, b, a)

                if self.custom_name_enabled.get():
                    filename = self.name_pattern.get().replace('{number', '{0').format(frame)
                else:
                    filename = f"frame_{frame:04d}.png"

                if not filename.lower().endswith('.png'):
                    filename += '.png'

                result.save(os.path.join(output_dir, filename))

                if frame % 10 == 0 or frame == frame_count - 1:
                    self.status_label.config(text=f"Generating... {frame+1}/{frame_count}")
                    self.root.update()

            self.status_label.config(text=f"{frame_count} frames saved to {output_dir}", fg="green")
            messagebox.showinfo("Success", 
                f"Generated {frame_count} frames!\n"
                f"Animated {len(color_positions)} unique colors\n"
                f"Saved to: {output_dir}")

        except Exception as e:
            self.status_label.config(text="Error!", fg="red")
            messagebox.showerror("Error", f"Generation failed: {str(e)}")

    def start_manual_generation(self):
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

                        for x, y in color_positions[start_color]:
                            r1, g1, b1, a1 = pixels1[x, y]
                            r2, g2, b2, a2 = pixels2[x, y]

                            r = int(r1 + (r2 - r1) * factor)
                            g = int(g1 + (g2 - g1) * factor)
                            b = int(b1 + (b2 - b1) * factor)
                            a = int(a1 + (a2 - a1) * factor)

                            result_pixels[x, y] = (r, g, b, a)

                if self.custom_name_enabled.get():
                    filename = self.name_pattern.get().replace('{number', '{0').format(frame)
                else:
                    filename = f"frame_{frame:04d}.png"

                if not filename.lower().endswith('.png'):
                    filename += '.png'

                result.save(os.path.join(output_dir, filename))

                if frame % 10 == 0:
                    self.status_label.config(text=f"Generating... {frame+1}/{frame_count}")
                    self.root.update()

            self.status_label.config(text=f"{frame_count} frames saved to {output_dir}", fg="green")
            messagebox.showinfo("Success", 
                f"Generated {frame_count} frames!\nSaved to: {output_dir}")

        except Exception as e:
            self.status_label.config(text="Error!", fg="red")
            messagebox.showerror("Error", f"Generation failed: {str(e)}")

    def load_extractor_image(self):
        path = filedialog.askopenfilename(filetypes=[("Image files", "*.png *.jpg *.jpeg *.bmp *.gif")])
        if path:
            self.extractor_image_path = path
            self.display_extractor_image(path)

    def display_extractor_image(self, path):
        try:
            img = Image.open(path)
            img.thumbnail((400, 400))
            photo = ImageTk.PhotoImage(img)
            self.extractor_image_label.configure(image=photo, text="")
            self.extractor_image_label.image = photo
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load image: {str(e)}")

    def select_extractor_folder(self):
        folder_path = filedialog.askdirectory(title="Select folder with images")
        if folder_path:
            self.extractor_folder_path = folder_path
            self.folder_path_var.set(folder_path)

            image_count = self._count_images_in_folder(folder_path)
            self.extractor_status.config(text=f"Found {image_count} images in folder", fg="blue")

    def _count_images_in_folder(self, folder_path):
        valid_extensions = {'.png', '.jpg', '.jpeg', '.bmp', '.gif'}
        count = 0
        for filename in os.listdir(folder_path):
            if os.path.splitext(filename)[1].lower() in valid_extensions:
                count += 1
        return count

    def extract_frames(self):
        selected_tab = self.extractor_notebook.index(self.extractor_notebook.select())

        if selected_tab == 0:
            self._extract_single_frames()
        else:
            self._extract_folder_frames()

    def _extract_single_frames(self):
        if not hasattr(self, 'extractor_image_path') or not self.extractor_image_path:
            messagebox.showwarning("Warning", "Please load an image first!")
            return

        try:
            width = self.frame_width_var.get()
            height = self.frame_height_var.get()

            if width <= 0 or height <= 0:
                messagebox.showwarning("Warning", "Frame dimensions must be positive!")
                return

            img = Image.open(self.extractor_image_path)

            cols = img.width // width
            rows = img.height // height

            if cols == 0 or rows == 0:
                messagebox.showwarning("Warning", f"Frame size ({width}x{height}) is larger than image ({img.width}x{img.height})!")
                return

            total_frames = cols * rows

            output_dir = os.path.join(self.save_folder, f"frames_{len(os.listdir(self.save_folder))}")
            os.makedirs(output_dir, exist_ok=True)

            self.extractor_status.config(text=f"Extracting {total_frames} frames...", fg="orange")
            self.root.update()

            frame_count = 0
            for row in range(rows):
                for col in range(cols):
                    left = col * width
                    upper = row * height
                    right = left + width
                    lower = upper + height

                    if self.custom_name_enabled.get():
                        filename = self.name_pattern.get().replace('{number', '{0').format(frame_count)
                    else:
                        filename = f"frame_{frame_count:04d}.png"

                    if not filename.lower().endswith('.png'):
                        filename += '.png'

                    frame = img.crop((left, upper, right, lower))
                    frame.save(os.path.join(output_dir, filename))
                    frame_count += 1

            self.extractor_status.config(text=f"{total_frames} frames saved to {output_dir}", fg="green")
            messagebox.showinfo("Success", 
                f"Extracted {total_frames} frames!\n"
                f"Saved to: {output_dir}")

        except Exception as e:
            self.extractor_status.config(text="Error!", fg="red")
            messagebox.showerror("Error", f"Extraction failed: {str(e)}")

    def _extract_folder_frames(self):
        if not hasattr(self, 'extractor_folder_path') or not self.extractor_folder_path:
            messagebox.showwarning("Warning", "Please select a folder first!")
            return

        try:
            valid_extensions = {'.png', '.jpg', '.jpeg', '.bmp', '.gif'}
            image_files = []

            for filename in os.listdir(self.extractor_folder_path):
                ext = os.path.splitext(filename)[1].lower()
                if ext in valid_extensions:
                    image_files.append(filename)

            if not image_files:
                messagebox.showwarning("Warning", "No image files found in selected folder!")
                return

            output_dir = os.path.join(self.save_folder, f"frames_{len(os.listdir(self.save_folder))}")
            os.makedirs(output_dir, exist_ok=True)

            self.extractor_status.config(text=f"Processing {len(image_files)} sprite sheets...", fg="orange")
            self.root.update()

            total_frames = 0
            processed_sheets = 0

            for i, filename in enumerate(sorted(image_files)):
                try:
                    if i % 2 == 0 or i == len(image_files) - 1:
                        self.extractor_status.config(text=f"Processing sheet {i+1}/{len(image_files)}...")
                        self.root.update()

                    img_path = os.path.join(self.extractor_folder_path, filename)
                    img = Image.open(img_path)

                    width, height = img.size

                    max_possible = min(width, height)
                    frame_size = 32

                    for size in range(max_possible, 1, -1):
                        if width % size == 0 and height % size == 0:
                            frame_size = size
                            break

                    if frame_size == 32:
                        frame_size = math.gcd(width, height)
                        if frame_size < 2:
                            frame_size = min(32, max_possible)

                    cols = width // frame_size
                    rows = height // frame_size

                    if cols == 0 or rows == 0:
                        print(f"Warning: {filename} too small for detected frame size {frame_size}px")
                        continue

                    frames_from_this_sheet = 0
                    for row in range(rows):
                        for col in range(cols):
                            left = col * frame_size
                            upper = row * frame_size
                            right = left + frame_size
                            lower = upper + frame_size

                            if self.custom_name_enabled.get():
                                save_name = self.name_pattern.get().replace('{number', '{0').format(total_frames)
                            else:
                                save_name = f"frame_{total_frames:04d}.png"

                            if not save_name.lower().endswith('.png'):
                                save_name += '.png'

                            frame = img.crop((left, upper, right, lower))
                            frame.save(os.path.join(output_dir, save_name))
                            total_frames += 1
                            frames_from_this_sheet += 1

                    processed_sheets += 1
                    print(f"Extracted {frames_from_this_sheet} frames from {filename} "
                          f"({width}x{height}) using {frame_size}x{frame_size} frames")

                except Exception as e:
                    print(f"Warning: Failed to process {filename}: {str(e)}")
                    continue

            if total_frames == 0:
                self.extractor_status.config(text="Error: No frames extracted!", fg="red")
                messagebox.showwarning("Warning", 
                    f"No frames extracted from {len(image_files)} sprite sheets!")
            else:
                self.extractor_status.config(text=f"{total_frames} frames saved to {output_dir}", fg="green")

                message = (f"Processed {processed_sheets}/{len(image_files)} sprite sheets\n"
                           f"Extracted {total_frames} total frames\n"
                           f"Saved to: {output_dir}")

                messagebox.showinfo("Success", message)

        except Exception as e:
            self.extractor_status.config(text="Error!", fg="red")
            messagebox.showerror("Error", f"Batch extraction failed: {str(e)}")

    def on_tab_changed(self, event):
        selected = self.notebook.index(self.notebook.select())
        self.frame_extractor_mode.set(selected == 1)

    def show_bug_reports(self):
        messagebox.showinfo("Bug Reports/Feature Requests", "Please report bugs and feature requests on our GitHub repository.")

    def show_pull_requests(self):
        messagebox.showinfo("Pull Requests", "We welcome pull requests! Please contribute to our GitHub repository.")

    def show_discord(self):
        messagebox.showinfo("Discord", "Join our Discord community for discussions and support.")

    def show_youtube(self):
        messagebox.showinfo("YouTube", "Check our YouTube channel for tutorials and demonstrations.")

    def show_about(self):
        messagebox.showinfo("About", "Gradient Frame Generator v0.3.2\n\nA tool designed to create frames of your gradient.\n\nCredits:\nSuperHero2010: Owner and Author of Gradient Frame Generator")

def main():
    root = tk.Tk()
    app = GradientFrameGenerator(root)
    root.mainloop()

if __name__ == "__main__":
    main()