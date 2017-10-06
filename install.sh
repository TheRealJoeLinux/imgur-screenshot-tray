# available system notifier
NOTIFY_BIN=$(which notify-send)
if [ -z $NOTIFY_BIN ]; then
    ZENITY=$(which zenity)
    if [ ! -z $ZENITY ]; then
        NOTIFY_BIN="${ZENITY} --info --text"
    else
        # we have nothing, just print
        NOTIFY_BIN=$(which echo)
    fi
fi

# find the right configuration dir
# running as root (hopefully not)?
USER_ID=$(id -u)
INSTALL_DIR=/usr/local
if [ $USER_ID -ne 0 ]; then
    # install into local dirs
    INSTALL_DIR=$HOME/.local
fi
BIN_DIR=${INSTALL_DIR}/bin
APP_DIR=${INSTALL_DIR}/share/applications
ICON_DIR=${INSTALL_DIR}/share/icons

# ensure dirs exist
[ ! -d $BIN_DIR ] && mkdir -p $BIN_DIR
[ ! -d $APP_DIR ] && mkdir -p $APP_DIR
[ ! -d $ICON_DIR ] && mkdir -p $ICON_DIR

# install stuff
installed=0
cp src/imgur-screenshot-tray.py $BIN_DIR/imgur-screenshot-tray.py
chmod +x $BIN_DIR/imgur-screenshot-tray.py
if [ $? -ne 0 ]; then
    echo "Error while copying imgur-screenshot-tray.py to ${BIN_DIR}. Exiting."
    exit 1
else
    installed=$((installed + 1))
fi
cp assets/imgur.svg $ICON_DIR/imgur.svg
if [ $? -ne 0 ]; then
    echo "Error while copying imgur.svg to ${ICON_DIR}. Exiting."
    exit 3
else
    installed=$((installed + 1))
fi
cat >$APP_DIR/imgur-screenshot.desktop <<EOF
[Desktop Entry]
Comment=Take screenshots of a selected region and automatically upload to Imgur
Terminal=false
Name=ImgurScreenshot
Exec=${BIN_DIR}/imgur-screenshot-tray.py
Type=Application
Icon=${INSTALL_DIR}/share/icons/imgur.svg
EOF
installed=$((installed + 1))
# config override
config_path=$HOME/.config/imgur-screenshot/settings.conf
config_dir=$(dirname $config_path)
if [ ! -f $config_path ]; then
    [ -d $config_dir ] || mkdir -p $config_dir
    echo "imgur_icon_path=${ICON_DIR}/imgur.svg" >> $config_path
    installed=$((installed + 1))
else
    sed -i "s,^imgur_icon_path=.*$,imgur_icon_path=${ICON_DIR}/imgur.svg,g" $config_path
    installed=$((installed + 1))
fi

# finished!
$NOTIFY_BIN "Installed ${installed} files into ${INSTALL_DIR}!"
