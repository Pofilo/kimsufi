# kimsufi
Last stable version [available here](https://git.pofilo.fr/pofilo/kimsufi/releases).

Sends an alert when your Kimsufi server is available.

## Requirements

+ The script uses **python 3.7**

## Purpose

The objective is to **send notifications** when the Kimsufi server you want is available in the zone(s) desired.
There is (for now) 3 types of notifications:
+ Email
+ HTTP request
+ Telegram message

A notification will be send to the notifiers configured when the server is available and when it's not anymore.

## Documentation

### References and zones

In `doc/`, you can find [the list of references](https://git.pofilo.fr/pofilo/kimsufi/src/branch/master/doc/list-references.md) and [the list of zones](https://git.pofilo.fr/pofilo/kimsufi/src/branch/master/doc/list-zones.md). Helpful to edit the configuration file according to the Kimsufi server you want.

### Telegram

You can [find here](https://git.pofilo.fr/pofilo/kimsufi/src/branch/master/doc/notice-telegram.md) the documentation helping you to setup the telegram notifier.

## Installation

+ Download the last stable version [available here](https://git.pofilo.fr/pofilo/kimsufi/releases)
+ `cd kimsufi`
+ Create virtual environment: `python3.7 -m venv .`
+ Source it: `source bin/activate`
+ Install dependencies: `pip install -r requirements.txt`
+ `cp config/kimsufi.sample.conf config/kimsufi.conf`
+ Edit *config/kimsufi.conf*
+ `cd src`
+ `python3.7 kimsufi.py` or `python3.7 -u kimsufi.py > log.txt &` if you want to use it as a daemon *(the PID is given in the first lines of the logs)*

### Options

+ `-c`, `--conf`
    + Specify the path of the configuration file (relative to `kimsufi/src` or absolute)
    + Default value is `../config/kimsufi.conf`

### Testing configuration

It would be too bad to not be notified because of a bad configuration.
To test it, in your configuration file, you can change your `API_URL` with `https://git.pofilo.fr/pofilo/kimsufi/raw/branch/master/doc/example-availability-file.json` (this is the file `example-availability-file.json` in `doc/`). In this file, the server `160sk2` is available in the zone `sgp`. If you start the script (`python3.7 kimsufi.py`), you should receive notifications by the notifiers you configured.

### Adding notifier

You can hack the script and add notifiers in the file `notifications.py`. Simply create a new function (in parameter, you can have the config and the boolean meaning if the server is found or not) and call it into `send_notifications(config, found)`, modify the configuration file if needed, et voilà!

## License

This project is licensed under the GNU GPL License. See the [LICENSE](https://git.pofilo.fr/pofilo/kimsufi/src/branch/master/LICENSE) file for the full license text.

## Credits

+ [@Pofilo](https://git.pofilo.fr/pofilo/)
+ [@c4s4](https://github.com/c4s4)

## Bugs

If you experience an issue, you have other ideas to the developpement or anything else, feel free to [report it](https://git.pofilo.fr/pofilo/kimsufi/issues) or  [fix it with a PR](https://git.pofilo.fr/pofilo/kimsufi/pulls)!

 