import sublime
import sublime_plugin
import datetime
import time
import os


journaldir = "C:\\Users\\btd\\Documents\\Journal\\"
entryfmt = "%Y-%m-%d.org"


class OrgJournalOpenTodayCommand(sublime_plugin.WindowCommand):
    def run(self):
        filename = datetime.date.today().strftime(entryfmt)
        path = journaldir + filename
        if not os.path.exists(path):
            with open(path, 'wt') as file:
                file.write(datetime.date.today().strftime("* %A, %Y-%m-%d\n"))
        journal_entry = self.window.open_file(path)


def all_journal_entries():
    """Return a list of normalized filenames sorted by date"""

    # collect all journal file names and parse date:
    all_entries = []
    for name in os.listdir(journaldir):
        try:
            date = datetime.datetime.strptime(name, entryfmt)
            all_entries.append((os.path.abspath(journaldir + name), date))
        except ValueError:
            pass

    # return file names only, sorted by date:
    return [entry[0] for entry in sorted(all_entries, key=lambda entry: entry[1])]


class OrgJournalOpenPreviousCommand(sublime_plugin.WindowCommand):
    def run(self):
        try:
            all_entries = all_journal_entries()
            current_name = self.window.active_view().file_name()
            current_index = all_entries.index(os.path.abspath(current_name))
        except:
            sublime.status_message("OrgJournal: '{}' is not a journal entry".format(current_name))
            return

        if current_index > 0:
            self.window.open_file(all_entries[current_index-1])
        else:
            sublime.status_message("OrgJournal: no entry before '{}'".format(current_name))


class OrgJournalOpenNextCommand(sublime_plugin.WindowCommand):
    def run(self):
        try:
            all_entries = all_journal_entries()
            current_name = self.window.active_view().file_name()
            current_index = all_entries.index(os.path.abspath(current_name))
        except:
            sublime.status_message("OrgJournal: '{}' is not a journal entry".format(current_name))
            return

        if current_index < (len(all_entries) - 1):
            self.window.open_file(all_entries[current_index+1])
        else:
            sublime.status_message("OrgJournal: no entry after '{}'".format(current_name))


class OrgJournalSearchCommand(sublime_plugin.WindowCommand):
    def run(self):
        self.window.show_input_panel("Search for:", "", self.search, None, None)

    def search(self, search_string):
        sublime.run_command("new_window")
        new_window = sublime.active_window()
        for entry in all_journal_entries():
            with open(entry, 'rt', errors='replace') as file:
                if search_string.lower() in file.read().lower():
                    new_window.open_file(entry)
        new_window.run_command("show_panel", {"panel": "find_in_files",
                                              "pattern": search_string.lower(),
                                              "regex": False,
                                              "case_sensitive": False})