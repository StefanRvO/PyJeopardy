sudo su -c 'echo "[multilib]" >> /etc/pacman.conf'
sudo su -c 'echo "Include = /etc/pacman.d/mirrorlist" >> /etc/pacman.conf'
sudo pacman -Syy
sudo pacman -S tar reflector --noconfirm --needed
sudo reflector --latest 100 --protocol http --protocol https --sort rate --save /etc/pacman.d/mirrorlist
sudo pacman -Su --noconfirm
yaourt -Syy python35 wine xorg-server-xvfb wget vlc make base-devel --noconfirm --needed
pip3.5 --version
pip3.5 -U pip
pip3.5 --version
cd /travis
sudo pip3.5 install -r requirements.txt
sudo pip3.5 install cx_Freeze
python3.5 build_deployable.py build
tar -zcvf release.tar.gz -C build .
rm build -Rf
#Create Windows release
export DISPLAY=:99.0
export WINEDLLOVERRIDES="mscoree,mshtml="
echo $WINEDLLOVERRIDES
Xvfb $DISPLAY &
sleep 3
wget https://sourceforge.net/projects/winpython/files/WinPython_3.5/3.5.3.1/WinPython-32bit-3.5.3.1Zero.exe/download -O py35.exe
wine py35.exe /S /D=C:\py35
wine WinPython-32bit-3.5.3.1Zero/python-3.5.3/python.exe -m pip install -U pip
wine WinPython-32bit-3.5.3.1Zero/python-3.5.3/python.exe -m pip install setuptools
wine WinPython-32bit-3.5.3.1Zero/python-3.5.3/python.exe -m pip install cx_freeze
wine WinPython-32bit-3.5.3.1Zero/python-3.5.3/python.exe -m pip install -r requirements.txt
wine WinPython-32bit-3.5.3.1Zero/python-3.5.3/python.exe build_deployable.py bdist_msi
mv dist/*.msi release.msi
