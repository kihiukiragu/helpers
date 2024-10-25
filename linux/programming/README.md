# Software Development Setup

## Version Control - git:
1. Install git:
   ```
   sudo apt install git
   ```
2. Configure:
   - Set your email and name:
   ```
   git config --global user.email “<YourEmail@email.com>”
   git config --global user.name “Firstname Lastname”
   ```
   - Set the editor of your choice:
   ```
   sudo update-alternatives --config editor
   ```
   OR
   ```
   git config --global core.editor "vim" #if not using Debian based distro
   ```

## Install Java (for Java Developers)
1. Install Java JDK:
    ```
    sudo apt-get install default-jre
    sudo apt-get install default-jdk
    ```
2. Gradle: sudo apt-get install gradle

## Install node:
1. Install nvm:
```
curl -o- https://raw.githubusercontent.com/creationix/nvm/v0.35.3/install.sh | bash
```
2. If using zsh, edit .zshrc and add:
```
export NVM_DIR=~/.nvm
  [ -s "$NVM_DIR/nvm.sh" ] && . "$NVM_DIR/nvm.sh"
```
3. `source ./zshrc`
4. `nvm install node`

## Install an IDE
There are several IDEs to pick from

### Visual Code
1. Prepare sources:
```
curl https://packages.microsoft.com/keys/microsoft.asc | gpg --dearmor > microsoft.gpg
sudo install -o root -g root -m 644 microsoft.gpg /usr/share/keyrings/microsoft-archive-keyring.gpg
sudo sh -c 'echo "deb [arch=amd64,arm64,armhf signed-by=/usr/share/keyrings/microsoft-archive-keyring.gpg] https://packages.microsoft.com/repos/vscode stable main" > /etc/apt/sources.list.d/vscode.list'
```
2. Install:
```
sudo apt-get install apt-transport-https
sudo apt-get update
sudo apt-get install code
```

### Install IntelliJ
1. Install snaps (use this to manage IntelliJ installs) - sudo apt install snapd
2. Install IntelliJ - sudo snap install intellij-idea-community --classic

### (Outdated) Install Eclipse 2020-06:
1. Download: 
   ```
   curl -O http://ftp.jaist.ac.jp/pub/eclipse/technology/epp/downloads/release/neon/2/eclipse-java-neon-2-linux-gtk-x86_64.tar.gz
   ```

2. Extract to /usr/ (So users can use it): sudo tar -zxvf eclipse-java-neon*.tar.gz -C /usr/
3. Symlink to bin: sudo ln -s /usr/eclipse/eclipse /usr/bin/eclipse
4. Create Icon:
   1. `sudo vi /usr/share/applications/eclipse.desktop`
   2. Copy and paste ini type of info:
      ```
      [Desktop Entry]
      Encoding=UTF-8
      Name=Eclipse 4.7
      Comment=Eclipse Neon
      Exec=/usr/bin/eclipse
      Icon=/usr/eclipse/icon.xpm
      Categories=Application;Development;Java;IDE
      Version=1.0
      Type=Application
      Terminal=0
      ```
   3. Save and exit
