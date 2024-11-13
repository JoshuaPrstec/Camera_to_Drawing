# Camera_to_Drawing
1. Install Command Line Tools in Terminal:
   ```
   xcode-select --install
   ```
2. Install Homebrew in Terminal:
   ```bash
   /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
   ```
3. Download VSCode: https://code.visualstudio.com/download
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
8. In the Camera_to_Drawing VSCode workspace, install Python in the VSCode Terminal:
   ```
   brew install python
   ```
9. Test that Python has been installed successfully in VSCode Terminal:
   ```
   python --version
   ```
10. 
