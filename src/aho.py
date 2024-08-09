import flet as ft
from collections import deque, defaultdict
import json
import graphviz

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
    
    def generate_graph(self):
        dot = graphviz.Digraph(comment='Aho-Corasick Automaton', format='png')
        seen = set()

        def visualize(current_dict, parent_id=None):
            current_id = id(current_dict)
            if current_id in seen:
                return
            seen.add(current_id)

            for char, node in current_dict.items():
                if char == 'output':
                    dot.node(str(current_id), label=node, shape='doublecircle')
                else:
                    node_id = id(node)
                    dot.node(str(node_id), label="")
                    if parent_id is not None:
                        dot.edge(str(parent_id), str(node_id), label=char)
                    visualize(node, node_id)

        visualize(self.trie)
        return dot


def main(page: ft.Page):
    page.bgcolor = "#0A162C"
    page.title = "Aho-Corasick Algorithm"
    page.window_width = 800
    page.window_height = 600
    page.window_resizable = False
    
    def on_search_click(e):
        text = text_input.value.lower()
        patterns = [p.strip().lower() for p in pattern_input.value.split(",") if p.strip()]
        ac = AhoCorasick()
        ac.build_trie(patterns)
        ac.build_automaton()
        results, indices = ac.search(text)

        dot = ac.generate_graph()
        dot.render('./img/automaton_visual', format='png', cleanup=True)
        automaton_visual = ft.Container(content=ft.Image(src='./img/automaton_visual.png'), padding= ft.padding.only(bottom = 100))

        result_display_manual.controls.clear()
        for pattern, count in results.items():
            index_list = ', '.join([f"[{start},{end}]" for start, end in indices[pattern]])
            result_display_manual.controls.append(ft.Text(f'Pola "{pattern}" ditemukan {count}x, ditemukan pada indeks ({index_list}).', color="white"))   
        result_display_manual.controls.append(automaton_visual)
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
            results, indices = ac.search(text)

            dot = ac.generate_graph()
            dot.render('./img/automaton_visual_json', format='png', cleanup=True)
            automaton_visual = ft.Container(content=ft.Image(src='./img/automaton_visual_json.png'), padding= ft.padding.only(bottom = 100))

            result_display_json.controls.clear()
            for pattern, count in results.items():
                index_list = ', '.join([f"[{start},{end}]" for start, end in indices[pattern]])
                result_display_json.controls.append(ft.Text(f'Pola "{pattern}" ditemukan {count}x, ditemukan pada indeks ({index_list}).', color="white"))
            result_display_json.controls.append(automaton_visual)
            page.update()

    # Initialize components
    file_picker = ft.FilePicker(on_result=on_file_selected)
    text_input = ft.TextField(label="Masukkan teks", multiline=True, width=400)
    pattern_input = ft.TextField(label="Masukkan pola (pisahkan dengan koma)", width=400)
    result_display_manual = ft.Column()
    result_display_json = ft.Column()

    
    # Define GUI Components for JSON handling
    json_button = ft.ElevatedButton(text="Pilih File JSON", color="#000000", bgcolor="#CBA133", on_click=lambda _: file_picker.pick_files())
    main_column_json = ft.Column([
        ft.Row([ft.Text("Aho-Corasick Text Finder", style=ft.TextStyle(size=24, weight= "bold", color="#FFFFFF"))], alignment=ft.MainAxisAlignment.CENTER),
        ft.Row([ft.Image(src="./assets/textfinder-removebg-preview.png", width=200, height=200)], alignment=ft.MainAxisAlignment.CENTER),
        ft.Row(
            [
                ft.ElevatedButton(text="Manual Input", color="#000000", bgcolor="#CBA133", on_click=lambda _: toggle_view(True)),
                ft.ElevatedButton(text="Upload JSON", color="#000000", bgcolor="#CBA133", on_click=lambda _: toggle_view(False)),
            ],
            alignment=ft.MainAxisAlignment.CENTER,
        ),
        ft.Row([json_button], alignment=ft.MainAxisAlignment.CENTER),
        ft.Row([result_display_json], alignment=ft.MainAxisAlignment.CENTER),
    ], 
    spacing=20, visible=False,
    width= page.window_width,
    height= page.window_height,
    alignment=ft.MainAxisAlignment.CENTER,
    scroll = ft.ScrollMode.ALWAYS,
    )

    # Main manual input column
    main_column = ft.Column(

        [
            ft.Row([ft.Text("Aho-Corasick Text Finder", style=ft.TextStyle(size=24, weight= "bold", color="#FFFFFF"))], alignment=ft.MainAxisAlignment.CENTER),
            ft.Row([ft.Image(src="./assets/textfinder-removebg-preview.png", width=200, height=200)], alignment=ft.MainAxisAlignment.CENTER),
            ft.Row(
                [
                    ft.ElevatedButton(text="Manual Input", color="#000000", bgcolor="#CBA133", on_click=lambda _: toggle_view(True)),
                    ft.ElevatedButton(text="Upload JSON", color="#000000", bgcolor="#CBA133", on_click=lambda _: toggle_view(False)),
                ],
                alignment=ft.MainAxisAlignment.CENTER,
            ),
            ft.Row([text_input], alignment=ft.MainAxisAlignment.CENTER),
            ft.Row([pattern_input], alignment=ft.MainAxisAlignment.CENTER),
            ft.Row([ft.ElevatedButton(text="Cari", color="#000000", bgcolor="#CBA133", on_click= on_search_click)], alignment=ft.MainAxisAlignment.CENTER),
            ft.Row([result_display_manual], alignment=ft.MainAxisAlignment.CENTER),
        ],
        width= page.window_width,
        height= page.window_height,
        alignment=ft.MainAxisAlignment.CENTER,
        spacing=20,
        visible=True,  # Initially visible
        scroll = ft.ScrollMode.ALWAYS,
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
    ft.app(
        target=main
    )
