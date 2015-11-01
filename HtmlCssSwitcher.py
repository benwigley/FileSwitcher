import sublime
import sublime_plugin
import re, os

class HtmlCssSwitcherCommand(sublime_plugin.WindowCommand):


    def run(self):
        if not self.window.active_view(): return

        current_file_path = self.window.active_view().file_name()
        if current_file_path is None: return

        print("------ File Switcher ------")
        print("Current filepath: " + current_file_path)

        # Get the file name (without the path)
        current_file_name = re.search(r"[\w-]+\.", current_file_path).group(0)[:-1]
        print("Current filename: " + current_file_name)

        # Run this twice to remove up to three file extensions from the file name.
        current_file_name = os.path.splitext(current_file_name)[0]
        current_file_name = os.path.splitext(current_file_name)[0]
        current_file_name = os.path.splitext(current_file_name)[0]

        is_css_file = False
        for ext in [".css", ".scss", ".sass", ".styl", ".less"]:
            if ext in current_file_path:
                is_css_file = True

        is_html_file = False
        for ext in [".html", ".hbs", ".jsx"]:
            if ext in current_file_path:
                is_html_file = True

        if is_css_file:
            print("Looking for a matching html file")
            source_matcher = re.compile(r"[/\\]" + current_file_name + "\.(html|haml|hbs|jsx)(\.haml|\.erb|)$")
            self.open_project_file(source_matcher, current_file_path)
        elif is_html_file:
            print("Looking for a matching css file")
            source_matcher = re.compile(r"[/\\]" + current_file_name + "\.(css|sass|scss|styl|less)(\.sass|\.scss|)(\.erb|)$")
            self.open_project_file(source_matcher, current_file_path)
        else:
            print("Error: current file is not a css or html file")


    def open_project_file(self, file_matcher, file_path):

        # Walk the project directory looking for files
        for path, dirs, filenames in self.walk_project_folder(file_path):

            # Loop over each file in the directory. Filter by files with the correct extensions.
            for filename in filter(lambda f: re.search(r"\.(html|hbs|jsx|css|scss|sass|styl|less)(\.haml|\.erb|\.scss|\.sass|)(\.erb|\.erb|)$", f), filenames):
                current_file = os.path.join(path, filename)
                if file_matcher.search(current_file):
                    return self.switch_to(os.path.join(path, filename))

        print("File Switcher: No matching files found")


    def walk_project_folder(self, file_path):
        for folder in self.window.folders():
            if not file_path.startswith(folder):
                continue
            yield from os.walk(folder)


    def switch_to(self, file_path):
        file_view = self.window.open_file(file_path)
        print("Opened: " + file_path)
        return True
