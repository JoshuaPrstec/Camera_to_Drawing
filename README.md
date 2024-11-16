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
   ```bash
   brew install --cask visual-studio-code
   brew install python
   ```
5. Download the Camera_to_Drawing code: https://github.com/JoshuaPrstec/Camera_to_Drawing/archive/refs/heads/main.zip
6. Open VSCode and press `file`, `open folder`, and select the downloaded folder
7. In VSCode, press the extensions tab (three squares with a fourth in the top-right corner).
8. Type `python` and install the latest version of the Python extension.
9. Change the interpreter to `Python [version] 64-bit /opt/homebrew/bin/python3`
10. Press the run button (this will open a new terminal tab).
11. Create a new virtual environment:
    ```bash
    python3 -m venv venv
    source venv/bin/activate
    ```
12. Change the interpreter to `Python [version] ('venv':venv)`
13. Press the bin icon, then press the run button again to relaunch the Python terminal in venv mode.
14. Install libraries:
    ```bash
    pip install --upgrade pip opencv-python pillow
    ```
15. Press the run button again to start the program (the first run may take a few seconds).
