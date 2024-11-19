import os
import tkinter as tk
from tkinter import filedialog, ttk
from PIL import Image, ImageTk

class FileExplorer:
    def __init__(self, root):
        self.root = root
        self.root.title("Simple File Explorer")
        self.root.geometry("1200x600")

        # Center the window on the screen
        self.center_window()
        
        # Set window background color
        self.root.configure(bg='#1a1b26')
        
        # Initialize current paths
        self.current_folder_path = ""
        self.current_readme_path = ""

        # Create main frame
        self.main_frame = ttk.Frame(root, padding="8")
        self.main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        # Create and configure modern dark theme styling
        self.setup_styles()

        # Load icons
        self.load_icons()

        # Create three panels
        self.create_panels()

        # Set up auto-save
        self.auto_save_interval = 4000
        self.auto_save()

    def center_window(self):
        """
        Centers the application window on the screen.

        This method updates the window's idle tasks to ensure the geometry
        information is up-to-date, then calculates the appropriate x and y
        coordinates to position the window in the center of the screen. Finally,
        it sets the window's geometry to the calculated position.

        Returns:
            None
        """
        self.root.update_idletasks()
        width = self.root.winfo_width()
        height = self.root.winfo_height()
        x = (self.root.winfo_screenwidth() // 2) - (width // 2)
        y = (self.root.winfo_screenheight() // 2) - (height // 2)
        self.root.geometry('{}x{}+{}+{}'.format(width, height, x, y))

    def setup_styles(self):
        """
        Set up the styles for the application's widgets using the ttk.Style class.
        This method configures the visual appearance of various ttk widgets such as 
        frames, labelframes, buttons, treeviews, and scrollbars. It uses a custom 
        color palette to define background colors, text colors, and other style 
        attributes to create a cohesive theme.
        Returns:
            dict: A dictionary containing the color palette used for styling.
        """
        self.style = ttk.Style()
        self.style.theme_use('clam')

        # Color palette
        colors = {
            'bg_dark': '#1a1b26',
            'bg_medium': '#24283b',
            'bg_light': '#2f334d',
            'accent': '#7aa2f7',
            'text': '#ffffff',  # Increased contrast to white
            'text_dim': '#565f89',
            'border': '#414868'
        }

        # Configure frame styles
        self.style.configure('TFrame', background=colors['bg_dark'])
        
        # Configure labelframe styles
        self.style.configure('TLabelframe', 
            background=colors['bg_dark'],
            bordercolor=colors['border'],
            darkcolor=colors['border'],
            lightcolor=colors['border'])
        self.style.configure('TLabelframe.Label', 
            background=colors['bg_dark'],
            foreground=colors['text'],
            font=('Helvetica', 11, 'bold'),
            padding=(10, 5))

        # Configure button styles
        self.style.configure('TButton',
            background=colors['bg_light'],
            foreground=colors['text'],
            font=('Helvetica', 10),
            borderwidth=0,
            padding=(10, 5))
        self.style.map('TButton',
            background=[('active', colors['accent'])],
            foreground=[('active', colors['bg_dark'])])

        # Configure treeview styles
        self.style.configure('Treeview',
            background=colors['bg_medium'],
            foreground=colors['text'],
            fieldbackground=colors['bg_medium'],
            font=('Helvetica', 10),
            borderwidth=0)
        self.style.map('Treeview',
            background=[('selected', colors['accent'])],
            foreground=[('selected', colors['bg_dark'])])
        
        # Remove borders
        self.style.layout('Treeview', [('Treeview.treearea', {'sticky': 'nswe'})])

        # Configure scrollbar style
        self.style.configure('Vertical.TScrollbar',
            background=colors['bg_light'],
            bordercolor=colors['bg_light'],
            arrowcolor=colors['text'],
            troughcolor=colors['bg_medium'])

        return colors

    def load_icons(self):
        """
        Load and process icons for the file explorer.

        This method performs the following steps:
        1. Determines the directory of the current script.
        2. Loads PNG icons for folders and files from the script directory.
        3. Resizes the icons to 16x16 pixels using the LANCZOS filter.
        4. Converts the icons to white using the `convert_to_white` method.

        Attributes:
            folder_icon (PIL.Image.Image): The processed folder icon.
            file_icon (PIL.Image.Image): The processed file icon.
        """
        # Get the directory of the current script
        script_dir = os.path.dirname(os.path.abspath(__file__))

        # Load PNG icons
        folder_icon_path = os.path.join(script_dir, "folder-icon.png")
        file_icon_path = os.path.join(script_dir, "file-icon.png")
        folder_icon = Image.open(folder_icon_path).resize((16, 16), Image.LANCZOS)
        file_icon = Image.open(file_icon_path).resize((16, 16), Image.LANCZOS)

        # Convert icons to white
        self.folder_icon = self.convert_to_white(folder_icon)
        self.file_icon = self.convert_to_white(file_icon)

    def convert_to_white(self, icon):
        """
        Converts all non-transparent pixels of an image to white.

        Args:
            icon (PIL.Image): The image to be converted.

        Returns:
            ImageTk.PhotoImage: The converted image with all non-transparent pixels changed to white.
        """
        icon = icon.convert("RGBA")
        data = icon.getdata()
        new_data = []
        for item in data:
            # Change all non-transparent pixels to white
            if item[3] > 0:  # Check if pixel is not transparent
                new_data.append((255, 255, 255, item[3]))  # Change to white
            else:
                new_data.append(item)
        icon.putdata(new_data)
        return ImageTk.PhotoImage(icon)

    def create_panels(self):
        """
        Creates the main panels of the file explorer application.
        This method sets up three main panels:
        1. Left Panel: File Explorer - Contains a treeview for file navigation and a button to open folders.
        2. Middle Panel: Documentation - Displays README or other content in a text widget with custom styles.
        3. Right Panel: Metadata - Shows metadata information in a text widget with custom styles.
        Each panel includes a scrollbar for vertical scrolling. The file explorer panel also includes a right-click context menu for additional file operations.
        Returns:
            None
        """
        colors = self.setup_styles()

        # Left Panel: File Explorer
        self.explorer_frame = ttk.LabelFrame(self.main_frame, text="Explorer", padding=(5, 5, 5, 5), width=400)
        self.explorer_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=5)

        self.open_button = ttk.Button(self.explorer_frame, text="Open Folder", command=self.open_folder)
        self.open_button.pack(pady=(5, 10))

        # Create a frame for the treeview and scrollbar
        tree_frame = ttk.Frame(self.explorer_frame)
        tree_frame.pack(fill=tk.BOTH, expand=True)

        self.tree = ttk.Treeview(tree_frame, show='tree')
        self.tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        # Add scrollbar to treeview
        scrollbar = ttk.Scrollbar(tree_frame, orient="vertical", command=self.tree.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.tree.configure(yscrollcommand=scrollbar.set)
        
        self.tree.bind('<<TreeviewSelect>>', self.on_file_select)

        # Add right-click context menu
        self.tree.bind("<Button-2>", self.show_context_menu)
        self.context_menu = tk.Menu(self.tree, tearoff=0)
        self.context_menu.add_command(label="Open with ...", command=self.open_file)

        # Middle Panel: README/Content View
        self.readme_frame = ttk.LabelFrame(self.main_frame, text="Documentation", padding=(5, 5, 5, 5), width=500)
        self.readme_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=5)

        # Create text widget with custom colors and scrollbar
        self.readme_text = tk.Text(self.readme_frame, 
            wrap=tk.WORD,
            bg=colors['bg_medium'],
            fg=colors['text'],
            insertbackground=colors['text'],  # Cursor color
            selectbackground=colors['accent'],
            selectforeground=colors['bg_dark'],
            font=('Courier', 13),  # Change to monospace font
            padx=10,
            pady=10,
            spacing1=5,  # Spacing before a line
            spacing2=5,  # Spacing between lines
            spacing3=5,  # Spacing after a line
            borderwidth=0)
        self.readme_text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        readme_scrollbar = ttk.Scrollbar(self.readme_frame, orient="vertical", command=self.readme_text.yview)
        readme_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.readme_text.configure(yscrollcommand=readme_scrollbar.set)

        # Right Panel: Metadata
        self.metadata_frame = ttk.LabelFrame(self.main_frame, text="Metadata", padding=(5, 5, 5, 5), width=300)
        self.metadata_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=5)

        self.metadata_text = tk.Text(self.metadata_frame, 
            wrap=tk.WORD,
            bg=colors['bg_medium'],
            fg=colors['text'],
            insertbackground=colors['text'],  # Cursor color
            selectbackground=colors['accent'],
            selectforeground=colors['bg_dark'],
            font=('Helvetica', 12),
            padx=10,
            pady=10,
            borderwidth=0)
        self.metadata_text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        metadata_scrollbar = ttk.Scrollbar(self.metadata_frame, orient="vertical", command=self.metadata_text.yview)
        metadata_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.metadata_text.configure(yscrollcommand=metadata_scrollbar.set)

    def open_folder(self):
        """
        Opens a folder selection dialog for the user to choose a directory.
        
        If a folder is selected, updates the current root path and current folder path,
        populates the tree view with the contents of the selected folder, updates the
        metadata, and displays the README file if present.
        
        Uses:
            - filedialog.askdirectory(): To open the folder selection dialog.
            - os.path.dirname(): To get the directory name of the selected folder.
            - os.path.relpath(): To get the relative path of the selected folder.
            - self.populate_tree(folder_path): To populate the tree view with folder contents.
            - self.update_metadata(folder_path): To update the metadata of the selected folder.
            - self.display_readme(folder_path): To display the README file if it exists.
        """
        folder_path = filedialog.askdirectory()
        if folder_path:
            self.current_root_path = os.path.dirname(folder_path)
            self.current_folder_path = os.path.relpath(folder_path, self.current_root_path)
            self.populate_tree(folder_path)
            self.update_metadata(folder_path)
            self.display_readme(folder_path)

    def populate_tree(self, folder_path):
        """
        Populates the tree view with the directory structure starting from the given folder path.

        Args:
            folder_path (str): The path of the folder to populate the tree view with.

        Returns:
            None
        """
        self.tree.delete(*self.tree.get_children())
        root_node = self.tree.insert('', 'end', text='   ' + os.path.basename(folder_path), open=True, image=self.folder_icon)
        self.insert_items(root_node, folder_path)

    def insert_items(self, parent, path):
        """
        Recursively inserts items from the given directory path into the tree view widget.

        Args:
            parent (str): The parent node in the tree view where items will be inserted.
            path (str): The directory path from which items will be listed and inserted.

        Returns:
            None
        """
        for item in os.listdir(path):
            if item == '.DS_Store':
                continue
            item_path = os.path.join(path, item)
            if os.path.isdir(item_path):
                node = self.tree.insert(parent, 'end', text='   ' + item, open=False, image=self.folder_icon)
                self.insert_items(node, item_path)
            else:
                self.tree.insert(parent, 'end', text='   ' + item, open=False, image=self.file_icon)

    def on_file_select(self, event):
        """
        Handles the event when a file or directory is selected in the file explorer tree.

        Args:
            event: The event object containing information about the selection event.

        Retrieves the selected item's text and its parent's path, constructs the full path
        of the selected item, and updates the current folder path relative to the root path.
        If the selected item is a directory, it updates the metadata and displays the README file.

        """
        selected_item = self.tree.selection()[0]
        item_text = self.tree.item(selected_item, 'text').strip()
        parent_iid = self.tree.parent(selected_item)
        parent_path = self.get_full_path(parent_iid)
        selected_path = os.path.join(self.current_root_path, parent_path, item_text)
        self.current_folder_path = os.path.relpath(selected_path, self.current_root_path)

        if os.path.isdir(selected_path):
            self.update_metadata(selected_path)
            self.display_readme(selected_path)

    def get_full_path(self, item):
        """
        Constructs the full path of a given item in the tree.

        Args:
            item (str): The identifier of the item in the tree.

        Returns:
            str: The full path of the item, constructed by joining the text of each 
                 item from the root to the given item. Returns an empty string if 
                 the path is empty.
        """
        path = []
        while item:
            path.insert(0, self.tree.item(item, 'text').strip())
            item = self.tree.parent(item)
        return os.path.join(*path) if path else ''

    def update_metadata(self, folder_path):
        """
        Update the metadata information for the given folder path.

        This method calculates the number of files, number of directories, and the total size
        of all files (excluding '.DS_Store') within the specified folder. It then updates the
        metadata display with this information.

        Args:
            folder_path (str): The path to the folder for which metadata is to be updated.

        Updates:
            self.metadata_text (tk.Text): The text widget displaying the metadata information.
        """
        num_files = 0
        num_dirs = 0
        total_size = 0
        for root, dirs, files in os.walk(folder_path):
            num_files += len([f for f in files if f != '.DS_Store'])
            num_dirs += len(dirs)
            break
        for root, dirs, files in os.walk(folder_path):
            total_size += sum(os.path.getsize(os.path.join(root, name)) for name in files if name != '.DS_Store')

        metadata_info = f"Path: {self.current_folder_path}\n"
        metadata_info += f"Files: {num_files}\n"
        metadata_info += f"Directories: {num_dirs}\n"
        metadata_info += f"Size: {total_size / (1024 * 1024):.2f} MB\n"

        self.metadata_text.delete(1.0, tk.END)
        self.metadata_text.insert(tk.END, metadata_info)

    def display_readme(self, path):
        """
        Displays the content of a README.md file located in the specified directory.

        Args:
            path (str): The path to the directory where the README.md file is located.

        Behavior:
            - If the specified path is a directory, it searches for a README.md file within that directory.
            - If a README.md file is found, its content is read and displayed in the readme_text widget.
            - If no README.md file is found, a message "No README.md found." is displayed in the readme_text widget.
            - If the specified path is not a directory, a message "Selected item is not a directory." is displayed in the readme_text widget.
        """
        if os.path.isdir(path):
            readme_path = self.find_readme(path)
            if readme_path:
                self.current_readme_path = readme_path
                with open(readme_path, 'r', encoding='utf-8') as file:
                    content = file.read()
                self.readme_text.delete(1.0, tk.END)
                self.readme_text.insert(tk.END, content)
            else:
                self.current_readme_path = ""
                self.readme_text.delete(1.0, tk.END)
                self.readme_text.insert(tk.END, "No README.md found.")
        else:
            self.current_readme_path = ""
            self.readme_text.delete(1.0, tk.END)
            self.readme_text.insert(tk.END, "Selected item is not a directory.")

    def find_readme(self, path):
        """
        Finds or creates a README.md file in the specified directory.

        Args:
            path (str): The directory path where to look for or create the README.md file.

        Returns:
            str: The path to the README.md file.

        If the README.md file does not exist in the specified directory, it will be created
        with a default template.
        """
        readme_path = os.path.join(path, 'README.md')
        if os.path.exists(readme_path):
            return readme_path
        else:
            with open(readme_path, "w") as readme:
                readme.write("# This is a new README file.")
                # add template for perfect README.md
        return readme_path

    def auto_save(self):
        """
        Automatically saves the content of the README text widget to the current README file path at regular intervals.

        This method retrieves the content from the `readme_text` widget and writes it to the file specified by 
        `current_readme_path`. It then schedules itself to run again after a specified interval.

        Attributes:
            current_readme_path (str): The file path where the README content should be saved.
            readme_text (tk.Text): The Tkinter Text widget containing the README content.
            auto_save_interval (int): The interval in milliseconds at which the auto-save should occur.
            root (tk.Tk): The root Tkinter window, used to schedule the next auto-save.
        """
        if self.current_readme_path:
            content = self.readme_text.get(1.0, tk.END)
            with open(self.current_readme_path, 'w', encoding='utf-8') as file:
                file.write(content)
        self.root.after(self.auto_save_interval, self.auto_save)
    
    def show_context_menu(self, event):
        """
        Display the context menu at the location of the event.

        This method is triggered by an event (typically a right-click) and displays
        the context menu at the coordinates where the event occurred.

        Args:
            event: The event object containing information about the event, including
                   the x and y coordinates where the event occurred.
        """
        try:
            self.context_menu.tk_popup(event.x_root, event.y_root)
        finally:
            self.context_menu.grab_release()

    def open_file(self):
        """
        Opens the selected file in the file explorer.

        This method retrieves the selected item from the tree view, constructs the full path
        to the selected file, and opens it using the appropriate system command based on the
        operating system.

        - On Windows, it uses `os.startfile()`.
        - On macOS and Linux, it uses the `open` command.

        Raises:
            IndexError: If no item is selected in the tree view.
            KeyError: If the selected item does not have a parent in the tree view.
        """
        selected_item = self.tree.selection()[0]
        item_text = self.tree.item(selected_item, 'text').strip()
        parent_iid = self.tree.parent(selected_item)
        parent_path = self.get_full_path(parent_iid)
        selected_path = os.path.join(self.current_root_path, parent_path, item_text)

        if os.path.isfile(selected_path):
            if os.name == 'nt':  # Windows
                os.startfile(selected_path)
            elif os.name == 'posix':  # macOS and Linux
                os.system(f'open "{selected_path}"')

if __name__ == "__main__":
    root = tk.Tk()
    app = FileExplorer(root)
    root.mainloop()