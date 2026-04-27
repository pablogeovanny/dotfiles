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
sudo apt install -y qtile rofi htop feh bat lsd eza zsh fzf ranger picom xtrlock spice-vdagent xsel unzip micro alsa-utils stow

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
stow --adopt -v -R .

echo -e "\n${GREEN}[+] Setup Complete!${NC}"

# 6. Reboot
echo -e "The system will reboot in 10 seconds..."
echo -e "Press Ctrl + C at any time to cancel the reboot.\n"

# Countdown with progress
for i in {10..1}; do
    printf "${RED}Rebooting in %2d seconds... (Ctrl+C to cancel)${NC}\r" $i
    sleep 1
done

echo -e "\n\nRebooting now! 🚀\n"
sleep 1
sudo reboot
