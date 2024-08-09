import flet as ft
from collections import deque, defaultdict
import json

class AhoCorasick:
    def __init__(self):
        self.trie = {}
        self.output = defaultdict(list)
        self.fail = {}

    def build_trie(self, patterns):
        for pattern in patterns:
            current_dict = self.trie
            for char in pattern:
                current_dict = current_dict.setdefault(char, {})
            current_dict['output'] = pattern

    def build_automaton(self):
        queue = deque()
        self.fail[id(self.trie)] = self.trie

        for key in self.trie:
            self.fail[id(self.trie[key])] = self.trie
            queue.append(self.trie[key])

        while queue:
            current_dict = queue.popleft()

            for key in current_dict:
                if key == 'output':
                    continue

                child_dict = current_dict[key]
                queue.append(child_dict)

                failure = self.fail[id(current_dict)]
                while key not in failure and failure is not self.trie:
                    failure = self.fail[id(failure)]

                self.fail[id(child_dict)] = failure.get(key, self.trie)
                self.output[id(child_dict)] += self.output[id(self.fail[id(child_dict)])]

    def search(self, text):
        current_dict = self.trie
        results = defaultdict(int)
        indices = defaultdict(list)

        for index, char in enumerate(text):
            while char not in current_dict and current_dict is not self.trie:
                current_dict = self.fail[id(current_dict)]

            if char in current_dict:
                current_dict = current_dict[char]
            else:
                current_dict = self.trie

            if 'output' in current_dict:
                pattern = current_dict['output']
                results[pattern] += 1
                indices[pattern].append((index - len(pattern) + 1, index))

        return results, indices

def main(page: ft.Page):
    padding = 20

    def display_manual_input(e):
        page.controls.clear()
        page.add(main_column)
        page.update()

    def display_json_input(e):
        page.clean()
        page.add(main_column_json)
        page.update()

    def on_search_click(e):
        text = text_input.value.lower()
        patterns = [p.strip().lower() for p in pattern_input.value.split(",")]
        ac = AhoCorasick()
        ac.build_trie(patterns)
        ac.build_automaton()
        results, _ = ac.search(text)

        result_display.controls.clear()
        for pattern, count in results.items():
            result_display.controls.append(ft.Text(f'Pola "{pattern}" ditemukan {count}x.'))
        page.update()

    def on_file_selected(e: ft.FilePickerResultEvent):
        if e.files:
            with open(e.files[0].path, 'r') as f:
                data = json.load(f)
            text = data["text"].lower()
            patterns = [p.lower() for p in data["patterns"]]
            ac = AhoCorasick()
            ac.build_trie(patterns)
            ac.build_automaton()
            results, _ = ac.search(text)

            result_display.controls.clear()
            for pattern, count in results.items():
                result_display.controls.append(ft.Text(f'Pola "{pattern}" ditemukan {count}x.'))
            page.update()

    # Initialize components
    file_picker = ft.FilePicker()
    text_input = ft.TextField(label="Masukkan teks", multiline=True, width=400)
    pattern_input = ft.TextField(label="Masukkan pola (pisahkan dengan koma)", width=400)
    result_display = ft.Column()
    # Define GUI Components
# Define GUI Components for JSON handling
    json_button = ft.ElevatedButton(text="Pilih File JSON", on_click=lambda _: file_picker.pick_files())
    main_column_json = ft.Column([
          ft.Row(
                [
                    ft.ElevatedButton(text="Manual Input", on_click=lambda _: toggle_view(True)),
                    ft.ElevatedButton(text="Upload JSON", on_click=lambda _: toggle_view(False)),
                ],
                alignment=ft.MainAxisAlignment.CENTER,
            ),
        ft.Row([json_button, result_display], alignment=ft.MainAxisAlignment.CENTER)
    ], 
    spacing=20, visible=False)

    # Main manual input column
    main_column = ft.Column(
        [
            ft.Row(
                [
                    ft.ElevatedButton(text="Manual Input", on_click=lambda _: toggle_view(True)),
                    ft.ElevatedButton(text="Upload JSON", on_click=lambda _: toggle_view(False)),
                ]
            ),
            text_input,
            pattern_input,
            ft.ElevatedButton(text="Cari"),
            result_display,
        ],
        alignment=ft.MainAxisAlignment.CENTER,
        spacing=20,
        visible=True  # Initially visible
    )

    # Toggle view function to switch between manual and JSON input views
    def toggle_view(is_manual: bool):
        main_column.visible = is_manual
        main_column_json.visible = not is_manual
        page.update()

    # Add components to page initially
    page.add(main_column, main_column_json, file_picker)

    # Initial page update to reflect all components
    page.update()

if __name__ == "__main__":
    ft.app(target=main)