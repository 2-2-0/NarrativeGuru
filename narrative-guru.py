# narrative-guru.py, a vibe coded open source tool for writers and creators
#
# designed and vibe coded by 220 and Goggle's Gemini AI
# along with millions of coders around the world who provided for this code
#
# GPL v3.0 license - give credit for the idea and application where it's due
# version 1.0.0 - september 2025
#
# 2-2-0.online
# github.com/220nh


import tkinter as tk
from tkinter import messagebox, simpledialog, filedialog
import os
import json
import shutil
import platform
import subprocess

class NarrativeGuruApp:
    def __init__(self, root):
        """Initializes the main application window and its components."""
        self.root = root
        self.root.title("NarrativeGuru")
        
        # Determine the OS for platform-specific clipboard commands
        self.os_type = platform.system()
        
        # Set initial size, centered
        window_width = 800
        window_height = 828
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        x = (screen_width - window_width) // 2
        y = (screen_height - window_height) // 2
        self.root.geometry(f'{window_width}x{window_height}+{x}+{y}')

        # Define application state variables
        self.current_project = None
        self.project_path = "NarrativeGuru"
        self.resource_type = None

        # Create the main directory for projects if it doesn't exist
        os.makedirs(self.project_path, exist_ok=True)

        # Show the welcome screen first
        self.show_welcome_screen()

    def clear_frame(self):
        """Clears all widgets from the current frame."""
        for widget in self.root.winfo_children():
            widget.destroy()

    def show_welcome_screen(self):
        """Builds and displays the Welcome Screen."""
        self.clear_frame()

        # Welcome screen title
        welcome_frame = tk.Frame(self.root, padx=20, pady=20)
        welcome_frame.pack(expand=True, fill="both")

        tk.Label(welcome_frame, text="NarrativeGuru", font=("Helvetica", 24, "bold")).pack(pady=20)
        tk.Label(welcome_frame, text="by 220 (2-2-0.online)", font=("Helvetica", 12, "bold")).pack(pady=20)

        # Existing projects list
        tk.Label(welcome_frame, text="Existing Projects", font=("Helvetica", 14)).pack(pady=(10, 5))
        
        self.projects_listbox = tk.Listbox(welcome_frame, width=40, height=10, borderwidth=1, relief="sunken")
        self.projects_listbox.pack(pady=5)
        self.projects_listbox.bind("<<ListboxSelect>>", self.on_project_select)
        self.projects_listbox.bind("<Button-3>", self.show_project_context_menu)
        
        # Populate the listbox with existing projects
        self.populate_projects_list()
        
        # Add new project button
        add_project_button = tk.Button(welcome_frame, text="Add New Project", command=self.show_new_project_window)
        add_project_button.pack(pady=10)

    def populate_projects_list(self):
        """Fills the projects listbox with the names of project folders."""
        self.projects_listbox.delete(0, tk.END)
        try:
            projects = [d for d in os.listdir(self.project_path) if os.path.isdir(os.path.join(self.project_path, d))]
            for project in sorted(projects):
                self.projects_listbox.insert(tk.END, project)
        except OSError as e:
            messagebox.showerror("Error", f"Could not read project directory: {e}")

    def on_project_select(self, event):
        """Handles a project selection from the listbox."""
        if self.projects_listbox.curselection():
            index = self.projects_listbox.curselection()[0]
            self.current_project = self.projects_listbox.get(index)
            self.show_project_screen()

    def show_project_context_menu(self, event):
        """
        Displays a right-click context menu for deleting a project.
        This function is updated to ensure the item under the cursor is selected.
        """
        try:
            # Get the index of the item that was right-clicked
            index = self.projects_listbox.nearest(event.y)
            # Deselect any previously selected item
            self.projects_listbox.selection_clear(0, tk.END)
            # Select the item under the cursor
            self.projects_listbox.selection_set(index)
            # Ensure the selected item is visible
            self.projects_listbox.activate(index)
        except tk.TclError:
            # Handle cases where the click is not on an item in the listbox
            return
        
        context_menu = tk.Menu(self.root, tearoff=0)
        context_menu.add_command(label="Delete", command=lambda: self.delete_project(event))
        context_menu.post(event.x_root, event.y_root)

    def delete_project(self, event):
        """Deletes the selected project folder after confirmation."""
        if self.projects_listbox.curselection():
            index = self.projects_listbox.curselection()[0]
            project_to_delete = self.projects_listbox.get(index)
            
            if messagebox.askyesno("Confirm Delete", f"Are you sure you want to delete the project '{project_to_delete}'?"):
                project_dir = os.path.join(self.project_path, project_to_delete)
                try:
                    shutil.rmtree(project_dir)
                    messagebox.showinfo("Success", f"Project '{project_to_delete}' deleted.")
                    self.populate_projects_list()
                except OSError as e:
                    messagebox.showerror("Error", f"Failed to delete project: {e}")

    def show_new_project_window(self):
        """Displays the New Project Window popup."""
        self.new_project_window = tk.Toplevel(self.root)
        self.new_project_window.title("New Project")
        
        frame = tk.Frame(self.new_project_window, padx=20, pady=20)
        frame.pack()

        tk.Label(frame, text="Enter a name for the new project:").pack(pady=5)
        self.new_project_name_entry = tk.Entry(frame, width=30)
        self.new_project_name_entry.pack(pady=5)
        
        button_frame = tk.Frame(frame)
        button_frame.pack(pady=10)
        
        tk.Button(button_frame, text="Create", command=self.create_new_project).pack(side="left", padx=5)
        tk.Button(button_frame, text="Cancel", command=self.new_project_window.destroy).pack(side="left", padx=5)

    def create_new_project(self):
        """Creates a new project folder and its subdirectories."""
        project_name = self.new_project_name_entry.get().strip()
        if not project_name:
            messagebox.showerror("Error", "Project name cannot be empty.")
            return

        project_dir = os.path.join(self.project_path, project_name)
        if os.path.exists(project_dir):
            messagebox.showerror("Error", f"A project named '{project_name}' already exists.")
            return

        try:
            os.makedirs(os.path.join(project_dir, "characters"))
            os.makedirs(os.path.join(project_dir, "locations"))
            os.makedirs(os.path.join(project_dir, "props"))
            messagebox.showinfo("Success", f"Project '{project_name}' created.")
            self.new_project_window.destroy()
            self.current_project = project_name
            self.show_project_screen()
        except OSError as e:
            messagebox.showerror("Error", f"Failed to create project: {e}")

    def show_project_screen(self):
        """Builds and displays the main Project Screen workspace."""
        self.clear_frame()
        self.root.geometry("800x828")

        # Top area: Brand and project info
        top_frame = tk.Frame(self.root, padx=10, pady=10)
        top_frame.pack(fill="x")
        
        tk.Label(top_frame, text="NarrativeGuru", font=("Helvetica", 18, "bold")).pack(side="left", padx=(0, 20))
        
        tk.Label(top_frame, text=f"Project: {self.current_project}", font=("Helvetica", 14)).pack(side="left")
        tk.Button(top_frame, text="Back to Projects", command=self.show_welcome_screen).pack(side="right")

        # Bottom area: Left and right panes
        main_panes = tk.PanedWindow(self.root, orient=tk.HORIZONTAL, sashrelief=tk.SUNKEN)
        main_panes.pack(expand=True, fill="both", padx=10, pady=10)

        # Left pane: Resource Catalogs
        left_pane = tk.Frame(main_panes, padx=10, pady=10)
        main_panes.add(left_pane, width=300)

        self.char_listbox = self.create_resource_catalog(left_pane, "Characters", "characters")
        self.loc_listbox = self.create_resource_catalog(left_pane, "Locations", "locations")
        self.prop_listbox = self.create_resource_catalog(left_pane, "Props", "props")
        
        # Right pane: Preview and Remix
        right_pane = tk.Frame(main_panes, padx=10, pady=10)
        main_panes.add(right_pane)

        # Preview Window
        tk.Label(right_pane, text="Preview Window", font=("Helvetica", 12)).pack(anchor="w")
        self.preview_text = tk.Text(right_pane, wrap="word", height=15)
        self.preview_text.pack(fill="x", pady=5)
        preview_button_frame = tk.Frame(right_pane)
        preview_button_frame.pack(fill="x")
        tk.Button(preview_button_frame, text="Copy Context", command=lambda: self.copy_to_clipboard(self.preview_text)).pack(side="left")
        tk.Button(preview_button_frame, text="Update", command=self.update_resource_content).pack(side="right")
        
        # Remix Station
        tk.Label(right_pane, text="Remix Station", font=("Helvetica", 12)).pack(anchor="w", pady=(20, 0))
        self.remix_text = tk.Text(right_pane, wrap="word", height=15)
        self.remix_text.pack(fill="x", pady=5)
        remix_button_frame = tk.Frame(right_pane)
        remix_button_frame.pack(fill="x")
        tk.Button(remix_button_frame, text="Copy Context", command=lambda: self.copy_to_clipboard(self.remix_text)).pack(side="left")
        tk.Button(remix_button_frame, text="Clear Context", command=lambda: self.remix_text.delete("1.0", tk.END)).pack(side="left", padx=5)
        tk.Button(remix_button_frame, text="Export to File", command=self.export_remix_to_file).pack(side="right")

        # Refresh the resource lists on screen load
        self.populate_resource_lists()

    def create_resource_catalog(self, parent, label_text, type_name):
        """Creates a resource listbox and its associated 'Add' button."""
        frame = tk.Frame(parent, padx=5, pady=5)
        frame.pack(fill="x", pady=5)

        tk.Label(frame, text=label_text, font=("Helvetica", 12)).pack(anchor="w")
        
        listbox = tk.Listbox(frame, width=40, height=8, borderwidth=1, relief="sunken")
        listbox.pack(pady=5, fill="both", expand=True)
        
        # Bind events for the listbox
        listbox.bind("<<ListboxSelect>>", lambda event, type_name=type_name: self.on_resource_select(event, type_name))
        listbox.bind("<Double-Button-1>", lambda event, type_name=type_name: self.on_resource_double_click(event, type_name))
        listbox.bind("<Button-3>", lambda event, type_name=type_name: self.show_resource_context_menu(event, type_name))
        
        tk.Button(frame, text="Add", command=lambda: self.show_new_resource_window(type_name)).pack(pady=5)
        
        return listbox

    def populate_resource_lists(self):
        """Fills all three resource listboxes with available resources."""
        self.populate_listbox(self.char_listbox, "characters")
        self.populate_listbox(self.loc_listbox, "locations")
        self.populate_listbox(self.prop_listbox, "props")
    
    def populate_listbox(self, listbox, resource_type):
        """Helper function to populate a single listbox."""
        listbox.delete(0, tk.END)
        resource_dir = os.path.join(self.project_path, self.current_project, resource_type)
        if os.path.exists(resource_dir):
            resources = [f.split('.')[0] for f in os.listdir(resource_dir) if f.endswith('.json')]
            for res in sorted(resources):
                listbox.insert(tk.END, res)

    def on_resource_select(self, event, resource_type):
        """Loads and displays the content of a selected resource in the Preview Window."""
        listbox = event.widget
        if listbox.curselection():
            index = listbox.curselection()[0]
            resource_name = listbox.get(index)
            self.resource_type = resource_type # Store the current type for updates
            
            file_path = os.path.join(self.project_path, self.current_project, resource_type, f"{resource_name}.json")
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    content = data.get("content", "")
                self.preview_text.delete("1.0", tk.END)
                self.preview_text.insert("1.0", content)
                self.selected_resource_path = file_path # Store the path for updates
            except (IOError, json.JSONDecodeError) as e:
                messagebox.showerror("Error", f"Failed to load resource: {e}")

    def on_resource_double_click(self, event, resource_type):
        """Appends the content of a double-clicked resource to the Remix Station."""
        listbox = event.widget
        if listbox.curselection():
            index = listbox.curselection()[0]
            resource_name = listbox.get(index)
            file_path = os.path.join(self.project_path, self.current_project, resource_type, f"{resource_name}.json")
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    content = data.get("content", "")
                
                # Append a header and the content
                remix_content = f"--- {resource_name} ({resource_type.title()}) ---\n{content}\n\n"
                self.remix_text.insert(tk.END, remix_content)
            except (IOError, json.JSONDecodeError) as e:
                messagebox.showerror("Error", f"Failed to load resource for remix: {e}")

    def show_resource_context_menu(self, event, resource_type):
        """Displays a right-click context menu for deleting a resource."""
        listbox = event.widget
        if listbox.curselection():
            index = listbox.curselection()[0]
            resource_to_delete = listbox.get(index)
            
            context_menu = tk.Menu(self.root, tearoff=0)
            context_menu.add_command(label="Delete", command=lambda: self.delete_resource(resource_to_delete, resource_type))
            context_menu.post(event.x_root, event.y_root)
            
    def delete_resource(self, resource_name, resource_type):
        """Deletes a resource file after confirmation."""
        if messagebox.askyesno("Confirm Delete", f"Are you sure you want to delete the {resource_type.rstrip('s')} '{resource_name}'?"):
            file_path = os.path.join(self.project_path, self.current_project, resource_type, f"{resource_name}.json")
            try:
                os.remove(file_path)
                messagebox.showinfo("Success", f"{resource_type.rstrip('s').capitalize()} '{resource_name}' deleted.")
                self.populate_resource_lists()
            except OSError as e:
                messagebox.showerror("Error", f"Failed to delete resource: {e}")

    def update_resource_content(self):
        """Saves the content from the Preview Window back to the JSON file."""
        if not hasattr(self, 'selected_resource_path'):
            messagebox.showerror("Error", "No resource is selected to update.")
            return

        new_content = self.preview_text.get("1.0", tk.END).strip()
        try:
            with open(self.selected_resource_path, 'w', encoding='utf-8') as f:
                # The format is a simple JSON object with a 'content' key
                json.dump({"content": new_content}, f, indent=4)
            messagebox.showinfo("Success", "Resource content updated successfully.")
        except IOError as e:
            messagebox.showerror("Error", f"Failed to save changes: {e}")

    def export_remix_to_file(self):
        """Saves the content of the Remix Station to a new text file."""
        remix_content = self.remix_text.get("1.0", tk.END).strip()
        if not remix_content:
            messagebox.showinfo("Export", "Remix Station is empty. Nothing to export.")
            return

        file_path = filedialog.asksaveasfilename(defaultextension=".txt",
                                                filetypes=[("Text Files", "*.txt"), ("All Files", "*.*")],
                                                initialfile="remix.txt")
        if file_path:
            try:
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write(remix_content)
                messagebox.showinfo("Success", f"Content exported to '{os.path.basename(file_path)}' successfully.")
            except IOError as e:
                messagebox.showerror("Error", f"Failed to export file: {e}")

    def copy_to_clipboard(self, text_widget):
        """Copies the content of a text widget to the clipboard."""
        try:
            self.root.clipboard_clear()
            content = text_widget.get("1.0", tk.END)
            self.root.clipboard_append(content)
            messagebox.showinfo("Clipboard", "Content copied to clipboard!")
        except tk.TclError as e:
            messagebox.showerror("Clipboard Error", f"Failed to copy to clipboard: {e}")

    def show_new_resource_window(self, resource_type):
        """Displays a popup for creating a new resource (character, location, or prop)."""
        self.new_resource_window = tk.Toplevel(self.root)
        self.new_resource_window.title(f"New {resource_type.capitalize().rstrip('s')}")
        self.new_resource_window.grab_set()

        frame = tk.Frame(self.new_resource_window, padx=20, pady=20)
        frame.pack()

        tk.Label(frame, text=f"New {resource_type.capitalize().rstrip('s')} Name:").pack(pady=5)
        self.new_resource_name_entry = tk.Entry(frame, width=30)
        self.new_resource_name_entry.pack(pady=5)
        
        tk.Label(frame, text="Content:").pack(pady=5)
        self.new_resource_content_text = tk.Text(frame, wrap="word", height=10, width=50)
        self.new_resource_content_text.pack(pady=5)
        
        button_frame = tk.Frame(frame)
        button_frame.pack(pady=10)
        
        tk.Button(button_frame, text="Create", 
                  command=lambda: self.create_new_resource(resource_type)).pack(side="left", padx=5)
        tk.Button(button_frame, text="Cancel", command=self.new_resource_window.destroy).pack(side="left", padx=5)
        
    def create_new_resource(self, resource_type):
        """Saves a new resource as a JSON file."""
        resource_name = self.new_resource_name_entry.get().strip()
        resource_content = self.new_resource_content_text.get("1.0", tk.END).strip()
        
        if not resource_name:
            messagebox.showerror("Error", "Resource name cannot be empty.")
            return

        file_path = os.path.join(self.project_path, self.current_project, resource_type, f"{resource_name}.json")
        if os.path.exists(file_path):
            messagebox.showerror("Error", f"A {resource_type.rstrip('s')} with that name already exists.")
            return

        try:
            with open(file_path, 'w', encoding='utf-8') as f:
                json.dump({"content": resource_content}, f, indent=4)
            messagebox.showinfo("Success", f"{resource_type.capitalize().rstrip('s')} created successfully.")
            self.new_resource_window.destroy()
            self.populate_resource_lists()
        except IOError as e:
            messagebox.showerror("Error", f"Failed to create resource: {e}")

# Entry point of the application
if __name__ == "__main__":
    root = tk.Tk()
    app = NarrativeGuruApp(root)
    root.mainloop()
