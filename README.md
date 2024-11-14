# Camera_to_Drawing
1. Install Command Line Tools in Terminal:
   ```
   xcode-select --install
   ```
2. Download VSCode: https://code.visualstudio.com/download
3. Once the Command Line Tools have installed, install Homebrew in Terminal:
   ```bash
   /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
   ```
4. Add Homebrew to your path in Terminal (type each command one at a time):
   ```
   cd /opt/homebrew/bin/
   ```
   ```
   ls
   ```
   ```
   PATH=$PATH:/opt/homebrew/bin
   ```
   ```
   cd
   ```
   ```
   touch .zshrc
   ```
   ```
   echo 'export PATH=$PATH:/opt/homebrew/bin' >> .zshrc
   ```
5. Test that Homebrew has been added successfully in Terminal:
   ```
   brew doctor
   ```
   ```
   brew --version
   ```
6. Download the Camera_to_Drawing code: https://github.com/JoshuaPrstec/Camera_to_Drawing/archive/refs/heads/main.zip
7. Open VSCode and press `file`, `open folder`, and select the downloaded folder
8. In VSCode, install the Python language extension
11. Create a new virtual environment:
    ```
    python3 -m venv venv
    ```
    ```
    source venv/bin/activate
    ```
12. Change the interpreter to `Python [version] ('venv':venv)`
13. Press the run button (this will open a new terminal tab).
14. Install libraries:
    ```
    pip install opencv-python
    ```
    ```
    pip install pillow
    ```
15. Press the run button again to start the program.
