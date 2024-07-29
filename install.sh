pkg upgrade -y
pkg install git -y
pkg install python -y
pip install cython
pkg install libxml2 libxslt -y
pkg install -y python ndk-sysroot clang make libjpeg-turbo -y
pkg install clang -y
pip install lxml
pip install --pre uiautomator2

pip install pure-python-adb

pip install flask 

pkg update -y
pkg install git
git clone https://github.com/Yisus7u7/termux-ngrok

cd termux-ngrok
bash install.sh
