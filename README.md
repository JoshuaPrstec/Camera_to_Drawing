# Camera_to_Drawing
1. Install Command Line Tools in Terminal:
   ```
   xcode-select --install
   ```
2. Download VSCode: https://code.visualstudio.com/docs/?dv=osx
3. Once the Command Line Tools have installed, install Homebrew in Terminal:
   ```bash
   /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
   ```
4. Add Homebrew to your path in Terminal:
   ```bash
   cd /opt/homebrew/bin/
   ls
   PATH=$PATH:/opt/homebrew/bin
   cd
   touch .zshrc
   echo 'export PATH=$PATH:/opt/homebrew/bin' >> .zshrc
   brew doctor
   ```
5. Test that Homebrew has been added successfully in Terminal:
   ```bash
   brew --version
   ```
6. Download the Camera_to_Drawing code: https://github.com/JoshuaPrstec/Camera_to_Drawing/archive/refs/heads/main.zip
7. Open VSCode and press `file`, `open folder`, and select the downloaded folder
8. In VSCode, press the extensions tab (three squares with a fourth in the top-right corner).
9. Type `python` and install the latest version of Python.
10. Go back to the explorer tab, open the terminal and type the following:
    ```bash
    brew install python
    ```
11. Change the interpreter to `Python [version] 64-bit /opt/homebrew/bin/python3`
12. Press the run button (this will open a new terminal tab).
13. Create a new virtual environment:
    ```bash
    python3 -m venv venv
    ```
    ```bash
    source venv/bin/activate
    ```
14. Change the interpreter to `Python [version] ('venv':venv)`
15. Press the bin icon, then press the run button again to relaunch the Python terminal in venv mode.
16. Install libraries:
    ```bash
    pip install --upgrade pip opencv-python pillow
    ```
17. Press the run button again to start the program (the first run may take a few seconds).
