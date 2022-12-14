# Packwiz Toml to Excel 2 way sync
load existing [packwiz](https://github.com/packwiz/packwiz) mods toml into excel containing name, filename, url and side for easy `server`, `client`, and `both` tag editing. Exisitng config from toml will be loaded into excel and new excel side will be saved back into toml. url to allow quick access of the mod page for checking if the mods is for client only. (If you do not have excel just upload it to google doc and export it back down after editing)

**Always backup before using it, as this script is altering packwiz toml files.**
**Always save and close excel before running the script, otherwise excel will self destruct**

## Installation & Usage
### Option 1
Use `pwss.exe` directly with bash or any other terminal, an excel will be generated in current working directory. Add to environment path if needed.
```sh
cd "YOUR_PACK"
./pwss
```

### Option 2
Running from source, whichs uses `Python 3.10.5`(not a must) and packages.  
Clone this repo and open terminal in repo folder. Bash commands as follow:
```sh
python -m venv pwss/venv
pip install -r pwss/requirements.txt
```
Activate virtual environment and use it
```sh
cd "pwss/venv/Scripts"
./activate
cd "YOUR_PACK"
python -u "PATH_TO_pwss.py"
deactivate
```
Additionally if you want to build it just do this, and do it when your virtual environment is activated.
```
pip install pyinstaller
pyinstaller --onefile .\pwss\pwss.py
```