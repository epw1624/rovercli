# `rovercli`
A multi-purpose CLI for UBC Rover operations. Add commands as needed

# Installation
`rovercli` has no dependencies outside the Python standard library. To use it:
1. Clone this repo
2. From the root of the repo, run `python main.py [COMMAND] [ARGS]`
3. **[OPTIONAL BUT RECOMMENDED]** To install the CLI on the system root and run commands from anywhere using `rovercli [COMMAND] [ARGS]`:
   1. Ensure you are in the root of the repo
   2. `chmod +x main.py`
   3. `ln -s "$(pwd)/main.py" ~/.local/bin/rovercli`
   4. Verify that the symlink worked by running `rovercli`

# Commands
## `sync`
Sync files between devices on the UBC Rover network, without unecessary copying of files that haven't changed.

### Usage

```
python main.py sync [SOURCE ROOT] [DEST ROOT] [DEST ADDRESS]
```
For example:
```
python main.py sync ~/RoverFlake2 ~/RoverFlake2 rv@192.168.1.4
```