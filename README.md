# Camera_to_Drawing
## Mac
1. Install Command Line Tools in Terminal:
   ```
   xcode-select --install
   ```
2. Once the Command Line Tools have installed, install Homebrew in Terminal:
   ```bash
   /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
   cd /opt/homebrew/bin/
   ls
   PATH=$PATH:/opt/homebrew/bin
   cd
   touch .zshrc
   echo 'export PATH=$PATH:/opt/homebrew/bin' >> .zshrc
   brew doctor
   brew --version
   ```
3. If the Homebrew version appears in the terminal, it has installed successfully. You can now install VSCode:
   ```bash
   brew install --cask visual-studio-code
   brew install python python-tk
   ```
4. Download the Camera_to_Drawing code: https://github.com/JoshuaPrstec/Camera_to_Drawing/archive/refs/heads/main.zip
5. Open VSCode and press `file`, `open folder`, and select the downloaded folder
6. In VSCode, press the extensions tab (three squares with a fourth in the top-right corner).
7. Type `python` and install the latest version of the Python extension.
8. Create a virtual environment in the VSCode terminal:
    ```bash
    python3.x -m venv venv
    source venv/bin/activate
    ```
    Replace 3.x with the downloaded python version (e.g. 3.13)
9. Press the Python version (e.g. `3.9.6 64-bit`), then select the Python venv option (e.g. `Python 3.13.0 ('venv': venv) ./venv/bin/python`.
10. Press the bin icon, then press the run button again to relaunch the Python terminal in venv mode.
11. Install libraries:
    ```bash
    pip install --upgrade pip opencv-python pillow
    ```
12. Press the run button again to start the program (the first run may take a few seconds).


## Windows
1. Install Python for Windows: https://www.python.org/downloads/release/python-3130/
2. While installing, make sure to tick `Add Python 3.x to PATH`:
   
   ![image](https://github.com/user-attachments/assets/99ab601e-5a20-4195-96a6-af93962e09f4)
4. Install VSCode for Windows: https://code.visualstudio.com/Download
5. Download the Camera_to_Drawing code: https://github.com/JoshuaPrstec/Camera_to_Drawing/archive/refs/heads/main.zip
6. Open VSCode and press `file`, `open folder`, and select the downloaded folder
7. In VSCode, press the extensions tab (three squares with a fourth in the top-right corner).
8. Type `python` and install the latest version of the Python extension.
9. Create a virtual environment in the VSCode terminal:
   ```bash
   python3.x -m venv venv
   venv\Scripts\activate.bat
   ```
   Replace 3.x with the downloaded python version (e.g. 3.13)
10. Press the Python version (e.g. `3.9.6 64-bit`), then select the Python venv option (e.g. `Python 3.13.0 ('venv': venv) ./venv/bin/python`.
11. Press the bin icon, then press the run button again to relaunch the Python terminal in venv mode.
12. Install libraries:
    ```bash
    pip install --upgrade pip opencv-python pillow tk
    ```
13. Press the run button again to start the program (the first run may take a few seconds).
