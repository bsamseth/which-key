# Which-Key

Like [Emacs which-key](https://github.com/justbur/emacs-which-key) but for anything.

Which-Key is a customizable command launcher. It lets you define any command,
be it starting an application, running a script, or _anything_ else, and bind
it to a memorable sequence of keys. Just bind `which-key` to some keyboard
shortcut, and then trigger your commands.

**Note**: This is in early development, so the UI doesn't look amazing, and there will be bugs.

## Installation

Install with [`pipx`](https://pypa.github.io/pipx/):

```
pipx install which-key
```

If you don't care enough you can of course also install with `pip`.

## Configuration

Every aspect of Which-Key is customizable, and everything is controlled by a single configuration file. By default, the file should be called `~/.config/which-key/which-key.toml`.

TODO: List out everything that can be configured.

## Example

Take this example configuration:

```toml
# Saved as ~/.config/which-key/which-key.toml

[which_key]
default_template = "command"
width = 500
height = 100
x = 0.5
y = 0.8

[which_key.template_variables]
terminal = "alacritty"
editor = "lvim"

[which_key.action_templates]
command = "{action}"
terminal = "{terminal} -e {action}"
edit = "gtk-launch {editor} {action}"

[leader.c]
label = "Edit configs"

[leader.c.l]
label = "lvim"
template = "edit"
action = "~/.config/lvim/config.lua"

[leader.c.w]
label = "which-key"
template = "edit"
action = "~/.config/which-key/which-key.toml"

[leader.a]
label = "Applications"

[leader.a.h]
template = "terminal"
action = "htop"

[leader.a.i]
template = "terminal"
action = "ipython"
```

Here we first define some general settings for Which-Key, some template variables and some command templates (TODO: Add docs for each of these and add links).

Now run `which-key`. A pop-up appears with the various options. Typing the `c` for `Edit configs` updates the view and shows the sub-menu of all the files we can edit. Typing `w` will run the command `gtk-launch lvim ~/.config/lvim/config.lua`, which on my machine opens up the file in [LunarVim](https://www.lunarvim.org/).
