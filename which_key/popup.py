import subprocess
import tkinter as tk
from pathlib import Path
from tkinter import ttk
from typing import Any, Union

import toml

from which_key.config import Config


class WhichKeyDialog:
    def __init__(self, config_path: Union[str, Path]) -> None:
        with open(config_path) as f:
            self.config = Config(**toml.load(f))

            self.current_config = self.config.leader
            self.root = tk.Tk()
            self.root.attributes("-type", "dialog")
            self.root.title("Which Key")

            ws = self.root.winfo_screenwidth()
            hs = self.root.winfo_screenheight()
            x = int((self.config.which_key.x * ws) - (self.config.which_key.width / 2))
            y = int((self.config.which_key.y * hs) - (self.config.which_key.height / 2))
            self.root.geometry(
                f"{self.config.which_key.width}x{self.config.which_key.height}+{x}+{y}"
            )
            self.root.bind("<Key>", self.handle_keypress)

    def handle_keypress(self, event: Any) -> None:
        char = getattr(event, "char", None)
        assert isinstance(char, str)

        if char == "\x1b":  # Escape
            self.root.quit()
            return

        if char in self.current_config.__fields_set__:
            self.current_config = self.current_config.__dict__[char]

            if self.current_config.action:
                command = self.config.which_key.action_templates[
                    self.current_config.template
                    or self.config.which_key.default_template
                ].format(
                    action=self.current_config.action,
                    **self.config.which_key.template_variables,
                )
                print("doing:", command)
                subprocess.Popen(command, start_new_session=True, shell=True)
                self.root.quit()
            else:
                self.update_view()

    def run(self) -> None:
        self.update_view()
        self.root.mainloop()

    def update_view(self) -> None:
        for element in self.root.winfo_children():
            element.destroy()

        lf = ttk.LabelFrame(self.root, text=self.current_config.label or "")
        lf.grid(column=0, row=0, padx=20, pady=20)

        for i, key in enumerate(sorted(self.current_config.__fields_set__)):
            if len(key) == 1:
                opts = self.current_config.__dict__[key]
                label = opts.label or opts.action
                if label:
                    tk_label = ttk.Label(lf, text=f"{key}: {label}")
                    tk_label.grid(column=i, row=0, ipadx=10, ipady=10)


if __name__ == "__main__":

    dialog = WhichKeyDialog(Path(__file__).parent.parent / "config.toml")
    dialog.run()
