# Camera_to_Drawing
1. Install Command Line Tools in Terminal:
   ```
   xcode-select --install
   ```
2. Download VSCode: https://code.visualstudio.com/download
<a href="https://code.visualstudio.com/download" target="_blank">New Tab</a>

<a href="http://stackoverflow.com" target="_blank">Go</a>
3. Install Homebrew in Terminal:
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
9. In the Camera_to_Drawing VSCode workspace, install Python in the VSCode Terminal:
   ```
   brew install python
   ```
10. Test that Python has been installed successfully in VSCode Terminal:
    ```
    python --version
    ```
11. Create a new virtual environment:
    ```
    python -m venv venv
    ```
    ```
    source venv/bin/activate
    ```
12. Install libraries:
    ```
    pip install opencv-python
    ```
    ```
    pip install pillow
    ```
