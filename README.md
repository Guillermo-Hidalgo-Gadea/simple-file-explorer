# Simple File Explorer

Simple File Explorer is a graphical user interface (GUI) application built using Python and the `tkinter` library. It allows users to navigate through directories, view and edit README files, and open files with their system default applications on right-click.

## Background

Modern note-taking apps like Notion are championing a text-first approach to project management. However, I find myself drawn to a structured, file-based workflow, where project files and their documentation are tightly connected.

### The Idea

Automatically render README.md files for each directory, seamlessly integrating documentation with the file structure. Instead of toggling between a separate editor and file explorer, this approach allows navigation and editing in context—much like GitHub's repository view.

### Benefits

Encourages better documentation practices: Simplifies the creation and maintenance of directory-specific README.md files with automatic generation and inline editing.
Creates structured project wikis: Supports a text-based approach to project organization, blending documentation with the file system naturally.

## Usage

1. **Open Folder**: Click the "Open Folder" button to select a directory to explore.
2. **Navigate**: Use the tree view on the left panel to navigate through directories.
3. **View README**: The middle panel displays the content of the nearest `README.md` file in the selected directory.
4. **Edit README**: You can edit the content of the `README.md` file directly in the middle panel. Changes are auto-saved every 4 seconds.
5. **View Metadata**: The right panel displays metadata about the selected directory, including the number of files, subdirectories, and total size.
6. **Open Files**: Right-click on a file in the tree view and select "Open with ..." to open the file with its default application.

## Roadmap

- Add contextual documentation for files, not only directories
- Add settings option to save contextual documentation
  - something different than README.md to avoid conflicts
  - consider hidden metadata file
- Add support for viewing pdf, png, jpeg preview in metadata panel
- Add support for linking readme.md files, e.g. copy relative path on right click
- Add search functionality on file tree
- Make interface faster and more responsive
- Add readme.md templates with open science best practices

## Contributing

Contributions are welcome! Please fork the repository and submit a pull request with your changes.

## License

TBD

## Acknowledgements

- [Pillow](https://python-pillow.org/) for image processing.
- [tkinter](https://docs.python.org/3/library/tkinter.html) for the GUI framework.
