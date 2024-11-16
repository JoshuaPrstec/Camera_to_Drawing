# Camera_to_Drawing
1. Install Command Line Tools in Terminal:
   ```
   xcode-select --install
   ```
2. Once the Command Line Tools have installed, install Homebrew in Terminal:
   ```bash
   /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
   ```
3. Add Homebrew to your path in Terminal:
   ```bash
   cd /opt/homebrew/bin/
   ls
   PATH=$PATH:/opt/homebrew/bin
   cd
   touch .zshrc
   echo 'export PATH=$PATH:/opt/homebrew/bin' >> .zshrc
   brew doctor
   brew --version
   ```
4. If the Homebrew version appears in the terminal, it has installed successfully. You can now install VSCode:
   ```
   brew install --cask visual-studio-code
   ```
5. Download the Camera_to_Drawing code: https://github.com/JoshuaPrstec/Camera_to_Drawing/archive/refs/heads/main.zip
6. Open VSCode and press `file`, `open folder`, and select the downloaded folder
7. In VSCode, press the extensions tab (three squares with a fourth in the top-right corner).
8. Type `python` and install the latest version of Python.
9. Go back to the explorer tab, open the terminal and type the following:
    ```bash
    brew install python
    ```
10. Change the interpreter to `Python [version] 64-bit /opt/homebrew/bin/python3`
11. Press the run button (this will open a new terminal tab).
12. Create a new virtual environment:
    ```bash
    python3 -m venv venv
    source venv/bin/activate
    ```
13. Change the interpreter to `Python [version] ('venv':venv)`
14. Press the bin icon, then press the run button again to relaunch the Python terminal in venv mode.
15. Install libraries:
    ```bash
    pip install --upgrade pip opencv-python pillow
    ```
16. Press the run button again to start the program (the first run may take a few seconds).
