#!/usr/bin/env python3
import gi
gi.require_version('Gtk', '3.0')
gi.require_version('AppIndicator3', '0.1')

import os
import signal
import subprocess
from gi.repository import AppIndicator3 as appindicator, Gtk, Notify


APPINDICATOR_ID = 'ImgurScreenshot'
IMGUR_BIN = 'imgur-screenshot.sh'


def quit(event):
    Notify.uninit()
    Gtk.main_quit()


def screenshot(event):
    global IMGUR_BIN

    cmd = which(IMGUR_BIN)
    try:
        res = subprocess.check_call(cmd, stderr=subprocess.STDOUT)
    except subprocess.CalledProcessError as e:
        msg = "Error while taking screenshot:\n\n\"%s\"" % str(e)
        notify_send(msg, 'error')
    except Exception as e:
        msg = "Error while taking screenshot:\n\n\"%s\"" % str(e)
        notify_send(msg, 'error')
    return


def build_menu():
    menu = Gtk.Menu()

    # take screenshot
    item_screenshot = Gtk.MenuItem('Take screenshot')
    item_screenshot.connect('activate', screenshot)

    # quit option
    item_quit = Gtk.MenuItem('Quit')
    item_quit.connect('activate', quit)

    # build menu
    menu.append(item_screenshot)
    menu.append(item_quit)
    menu.show_all()

    return menu


def which(name):
    """Check for `name` program in $PATH."""
    def is_exe(fpath):
        return os.path.isfile(fpath) and os.access(fpath, os.X_OK)

    fpath, fname = os.path.split(name)
    if fpath:
        if is_exe(name):
            return name
    else:
        for path in os.environ['PATH'].split(os.pathsep):
            path = path.strip('"')
            exe_file = os.path.join(path, name)
            if is_exe(exe_file):
                return exe_file
        # check this dir, just in case
        curdir_path = os.path.abspath(os.path.join(os.path.dirname(__file__), name))
        if is_exe(curdir_path):
            return curdir_path

    # if we get here, `name` was not found in $PATH
    return None


def install_into(dir):
    """Install the imgur-screenshot.sh script into $PATH."""
    global IMGUR_BIN

    # importing these here because we'll only ever need them once
    import json
    import stat
    from urllib.request import urlopen

    api_base = 'https://api.github.com'
    repo_name = 'jomo/imgur-screenshot'
    release_url = '%s/repos/%s/releases/latest' % (api_base, repo_name)
    latest_download = 'https://github.com/%s/releases/download/%s/imgur-screenshot.sh'

    gh_resp = urlopen(release_url)
    if not gh_resp.status < 400:
        raise Exception("Received a %s status from GitHub when checking releases" % gh_resp.status)
    releases = json.loads(gh_resp.read().decode('utf8'))  # we catch this in main()
    latest_version = releases['name']  # should give us the latest version

    download_url = latest_download % (repo_name, latest_version)
    file_resp = urlopen(download_url)
    if not file_resp.status < 400:
        raise Exception("Received a %s status from GitHub when downloading file" % file_resp.status)
    file_contents = file_resp.read()
    filepath = os.path.join(dir, IMGUR_BIN)
    with open(filepath, 'w') as output:
        output.write(file_contents.decode('utf8'))
    st = os.stat(filepath)
    os.chmod(filepath, st.st_mode | stat.S_IEXEC)


def check_installation():
    global IMGUR_BIN

    # check for the command in $PATH
    ready_for_use = True
    if not which(IMGUR_BIN):
        ready_for_use = False
        install_dir = "%s/.local/bin" % os.environ['HOME']
        if not os.path.isdir(install_dir):
            install_dir = os.environ['HOME']  # do what we can
        install_into(install_dir)
        ready_for_use = True  # if we got here, we're okay
    if ready_for_use:
        ready_for_use = check_deps()  # also check dependencies
    return ready_for_use


def check_deps():
    global IMGUR_BIN

    cmd = which(IMGUR_BIN)
    if not cmd:
        # check relative dir if we installed it
        cmd = os.path.abspath(os.path.join(os.path.dirname(__file__), IMGUR_BIN))
    res = subprocess.Popen("%s --check" % cmd, shell=True, stdout=subprocess.PIPE,
                           stderr=subprocess.PIPE)
    output, error = res.communicate()
    deps_ok = False
    if output:
        lines = output.decode('utf8').split('\n')
        # missing dependencies start with 'ERROR'
        bad_lines = [bad for bad in lines if bad.startswith('ERROR')]
        if bad_lines:
            msg = "There are missing required dependencies:\n\n%s"
            notify_send(msg % "\n".join(bad_lines), 'error')
        else:
            deps_ok = True
    if error:
        msg = "There was an error while checking dependencies:\n\n\"%s\"" % error.strip()
        notify_send(msg, 'error')
    return deps_ok


def notify_send(msg, dialog_type='information'):
    global APPINDICATOR_ID

    Notify.Notification.new(APPINDICATOR_ID, msg, "dialog-%s" % dialog_type).show()


def main():
    indicator = appindicator.Indicator.new(APPINDICATOR_ID,
                                           os.path.abspath(os.path.join('assets', 'imgur.svg')),
                                           appindicator.IndicatorCategory.SYSTEM_SERVICES)
    indicator.set_status(appindicator.IndicatorStatus.ACTIVE)
    indicator.set_menu(build_menu())

    # ctrl+c support
    signal.signal(signal.SIGINT, signal.SIG_DFL)

    # verify that imgur-screenshot exists
    Notify.init(APPINDICATOR_ID)
    try:
        ready = check_installation()
        if ready:
            # start application
            Gtk.main()
        else:
            msg = "%s was downloaded into your $HOME directory. Please move it into your $PATH and re-run this program." % IMGUR_BIN
            notify_send(msg)
    except Exception as e:
        msg = "There was an error while checking for %s on your system:\n\n\"%s\""
        notify_send(msg % (APPINDICATOR_ID, str(e)), 'error')


if __name__ == "__main__":
    main()
