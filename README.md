# imgur-screenshot-tray
Add a GTK system tray app icon for easy access to imgur-screenshot.sh script.

This is a GTK system tray wrapper for the script at [https://github.com/jomo/imgur-screenshot](https://github.com/jomo/imgur-screenshot).

*NOTE: Currently, only free select functionality and anonymous Imgur upload is supported.*

## Dependencies
- Python (3.4+)
- GTK+
- libnotify

## Installation
```bash
./install.sh
```
The installation script will create the following files:
- `${INSTALL_DIR}`/bin/imgur-screenshot-tray.py
- `${INSTALL_DIR}`/bin/imgur-screenshot.sh (latest release from [https://github.com/jomo/imgur-screenshot](https://github.com/jomo/imgur-screenshot))
- `${INSTALL_DIR}`/share/icons/imgur.svg
- `${INSTALL_DIR}`/share/applications/imgur-screenshot.desktop

## Known Issues
- [Tray icon does not appear](https://github.com/TheRealJoeLinux/imgur-screenshot-tray/issues/1)
