#!/bin/bash

# ==============================================================================
# Kali Linux Qtile Dotfiles Auto-Installer
# Author: Ge0
# Description: Updates system, installs packages, clones repo, and restores dotfiles.
# ==============================================================================

set -e # Exit immediately if a command exits with a non-zero status

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

echo -e "${GREEN}[+] Starting Kali Qtile Setup...${NC}\n"

# 1. System Update & Cleanup
echo -e "${YELLOW}[+] Updating system and installing packages...${NC}"
sudo apt update && sudo apt full-upgrade -y

# 2. Clean unused packages
echo -e "${YELLOW}[+] Celaning unused packages...${NC}"
sudo apt autoremove --purge -y
sudo apt clean

# 3. Install Dependencies
echo -e "${YELLOW}[+] Installing Dependencies...${NC}"
sudo apt install -y qtile alacritty rofi htop feh bat lsd eza zsh fzf ranger picom xtrlock spice-vdagent xsel unzip micro alsa-utils stow
sudo wget https://archive.kali.org/archive-keyring.gpg -O /usr/share/keyrings/kali-archive-keyring.gpg
sudo wget https://github.com/ryanoasis/nerd-fonts/releases/download/v3.1.0/Hack.zip -O /usr/local/share/fonts/Hack.zip
sudo unzip /usr/local/share/fonts/Hack.zip -d /usr/local/share/fonts
sudo rm /usr/local/share/fonts/Hack.zip
git clone --depth=1 https://github.com/romkatv/powerlevel10k.git ~/powerlevel10k

# 4. Clone dotfiles (only if folder doesn't exist)
echo -e "${YELLOW}[+] Setting up dotfiles...${NC}"

if [ -d "$HOME/dotfiles" ]; then
    echo "   Dotfiles folder already exists. Pulling latest changes..."
    cd ~/dotfiles && git pull
else
    echo "   Cloning dotfiles repository..."
    git clone https://github.com/pablogeovanny/dotfiles.git ~/dotfiles
fi

# 5. Restore Dotfiles with Stow
echo -e "${YELLOW}[+] Restoring dotfiles with Stow...${NC}"
cd "$HOME/dotfiles"

# 6. Unstow everything first
stow -D qtile rofi picom alacritty zsh p10k dmrc 2>/dev/null || true

# 7. Remove real files/folders
rm -rf ~/.config/qtile ~/.config/rofi ~/.config/picom ~/.config/alacritty 2>/dev/null || true
rm -f ~/.zshrc ~/.p10k.zsh ~/.dmrc 2>/dev/null || true

# 8. Stow cleanly
stow -v qtile rofi picom alacritty zsh p10k dmrc 2>/dev/null || true

echo -e "\n${GREEN}[+] Setup Complete!${NC}"

# 9. Reboot
while true; do
    read -rp "${RED}[!] Do you want to reboot now? [y/n]: ${NC}" answer
    case "$answer" in
        [yY])
            echo -e "\nRebooting now..."
            sudo reboot
            break
            ;;
        [nN])
            echo -e "\nReboot cancelled."
            break
            ;;
        *)
            echo "Please enter y or n."
            ;;
    esac
done
