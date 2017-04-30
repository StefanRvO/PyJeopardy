sudo pacman -Syy
sudo pacman -S tar reflector --noconfirm --needed
sudo reflector --latest 100 --protocol http --protocol https --sort rate --save /etc/pacman.d/mirrorlist
sudo pacman -Su --noconfirm
yaourt -Syy python35 vlc make base-devel --noconfirm --needed
sudo pip3.5 --version
sudo pip3.5 -U pip
sudo pip3.5 --version
cd /travis
sudo pip3.5 install -r requirements.txt
sudo pip3.5 install pyinstaller
pyinstaller PyJeopardy_Linux.spec
tar -zcvf $RELEASE_NAME -C dist .
