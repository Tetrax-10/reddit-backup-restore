import sys
import ini
import praw
import json

if 2 < len(sys.argv):
    mode = sys.argv[1]
    username = sys.argv[2]
else:
    print("Please specify the mode and username> python reddit.py <mode> <username>")
    sys.exit()

# Script version
version = "1.0.0"

# Load backup from backup.json
try:
    with open("backup.json", "r") as file:
        backup = json.load(file)

    # Upgrade backup if necessary
    if "version" not in backup or backup["version"] != version:
        from scripts.upgradeBackup import upgrade_backup_func

        backup = upgrade_backup_func(backup, version)

        # Save backup to backup.json
        with open("backup.json", "w") as file:
            json.dump(backup, file, indent=4)
except:
    if mode == "restore":
        print("Backup unavailable or corrupted")
        sys.exit()

# Load config
try:
    config = ini.parse(open("config.ini").read())
except:
    print("Config file unavailable or corrupted")
    sys.exit()

# Connect to Reddit
try:
    reddit = praw.Reddit(username)
    me = reddit.user.me()
except:
    print("Can't connect to Reddit with that username's credentials")
    sys.exit()

# Run script
if mode == "backup":
    from scripts.backup import backup_func

    backup_func(reddit, me, config["backup"], username, version)
elif mode == "restore":
    from scripts.restore import restore_func

    restore_func(reddit, config["restore"], username)
elif mode == "clear":
    from scripts.clear import clear_func

    clear_func(reddit, me, config["clear"], username)
else:
    print("Invalid mode")
