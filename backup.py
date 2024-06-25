import sys
import json
import praw

# ---------- CONFIG ----------

# value: True | False
BACKUP_SUBSCRIPTIONS = True
BACKUP_MULTIREDDITS = True
BACKUP_SAVED = True
BACKUP_UPVOTED = True
BACKUP_DOWNVOTED = True

# ---------- CONFIG ----------


if sys.argv[1]:
    username = sys.argv[1]
else:
    print("Please specify username: python backup.py <username>")
    sys.exit()

reddit = praw.Reddit(username)
backup = {"subreddits": [], "users": [], "multireddits": {}, "saved": [], "upvoted": [], "downvoted": []}
try:
    with open("backup.json", "r") as file:
        cache_backup = json.load(file)
except:
    cache_backup = None

print(f"Backing up {username}...\n")


# Backup subreddits
if BACKUP_SUBSCRIPTIONS:
    for subreddit in reddit.user.subreddits(limit=None):
        subreddit_name = subreddit.display_name
        if subreddit_name.startswith("u_"):
            backup["users"].append(subreddit_name)
        else:
            backup["subreddits"].append(subreddit_name)

    print(f"Backed up {len(backup['subreddits'])} subscribed subreddits.")
    print(f"Backed up {len(backup['users'])} followed users.")
elif cache_backup:
    backup["subreddits"] = cache_backup["subreddits"]
    backup["users"] = cache_backup["users"]


# Backup multireddits
if BACKUP_MULTIREDDITS:
    for multireddit in reddit.user.multireddits():
        multireddit_name = multireddit.display_name
        temp = {"subreddits": [], "users": []}
        for subreddit in multireddit.subreddits:
            subreddit_name = subreddit.display_name
            if subreddit_name.startswith("u_"):
                temp["users"].append(subreddit_name)
            else:
                temp["subreddits"].append(subreddit_name)

        backup["multireddits"][multireddit_name] = temp

    print(f"Backed up {len(backup['multireddits'])} multireddits.")
elif cache_backup:
    backup["multireddits"] = cache_backup["multireddits"]

me = reddit.user.me()

# Backup saved posts
if BACKUP_SAVED:
    for saved_post in me.saved(limit=None):
        backup["saved"].append(saved_post.id)

    print(f"Backed up {len(backup['saved'])} saved posts.")
elif cache_backup:
    backup["saved"] = cache_backup["saved"]


# Backup upvoted posts
if BACKUP_UPVOTED:
    for upvoted_post in me.upvoted(limit=None):
        backup["upvoted"].append(upvoted_post.id)

    print(f"Backed up {len(backup['upvoted'])} upvoted posts.")
elif cache_backup:
    backup["upvoted"] = cache_backup["upvoted"]


# Backup upvoted posts
if BACKUP_DOWNVOTED:
    for downvoted_post in me.downvoted(limit=None):
        backup["downvoted"].append(downvoted_post.id)

    print(f"Backed up {len(backup['downvoted'])} downvoted posts.")
elif cache_backup:
    backup["downvoted"] = cache_backup["downvoted"]


# Save backup to backup.json
with open("backup.json", "w") as file:
    json.dump(backup, file, indent=4)

print("\nBackup saved to backup.json")
