#!/bin/sh
wget https://get.videolan.org/vlc/2.2.4/win32/vlc-2.2.4-win32.exe -O vlc.exe
apt-get install p7zip-full -y
7z x vlc.exe -ovlc
mv vlc/\$_OUTDIR/plugins/ plugins
pyinstaller --version
echo "test"
pyinstaller /src/PyJeopardy_Wine.spec
