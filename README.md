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
6. Once Hombrew has been added to the path, install python in Terminal:
   ```
   brew install python
   ```
7. 
