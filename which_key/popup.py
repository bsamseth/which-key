import os
import subprocess
import tkinter as tk
from pathlib import Path
from typing import Any, Optional, Union

import toml
from pydantic import BaseModel, Extra


class WhichKeyConfig(BaseModel):
    terminal: str = "alacritty"
    editor: str = os.getenv("EDITOR", "nano")
    action_templates: dict[str, str]
    default_template: str


class BindingsConfig(BaseModel):
    label: Optional[str]
    action: Optional[str]
    template: Optional[str]

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        new_kwargs = {
            k: (BindingsConfig(**v) if len(k) == 1 and isinstance(v, dict) else v)
            for k, v in kwargs.items()
        }
        super().__init__(*args, **new_kwargs)

    class Config:
        extra = Extra.allow


class Config(BaseModel):
    which_key: WhichKeyConfig
    leader: BindingsConfig


class WhichKeyDialog:
    def __init__(self, config_path: Union[str, Path]) -> None:
        with open(config_path) as f:
            self.config = Config(**toml.load(f))

            self.current_config = self.config.leader
            self.root = tk.Tk()
            self.root.attributes("-type", "dialog")
            self.root.title("Which Key")
            self.root.geometry("500x100")
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
                    terminal=self.config.which_key.terminal,
                    editor=self.config.which_key.editor,
                    action=self.current_config.action,
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
        for key in sorted(self.current_config.__fields_set__):
            if len(key) == 1:
                opts = self.current_config.__dict__[key]
                label = opts.label or opts.action
                if label:
                    tk.Label(self.root, text=f"{key}: {label}").pack()


if __name__ == "__main__":

    dialog = WhichKeyDialog(Path(__file__).parent.parent / "config.toml")
    dialog.run()
