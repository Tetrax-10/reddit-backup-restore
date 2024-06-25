import sys
import json
import praw

# ---------- CONFIG ----------

# value: True | False
RESTORE_SUBSCRIPTIONS = True
RESTORE_MULTIREDDITS = True
RESTORE_SAVED = True
RESTORE_HIDDEN = True
RESTORE_UPVOTED = False
RESTORE_DOWNVOTED = False

# value: private | public | hidden
MULTIREDDIT_VISIBILITY = "private"

# ---------- CONFIG ----------


if sys.argv[1]:
    username = sys.argv[1]
else:
    print("Please specify username: python restore.py <username>")
    sys.exit()

reddit = praw.Reddit(username)
try:
    with open("backup.json", "r") as file:
        backup = json.load(file)
except:
    print("Backup unavailable or corrupted.")
    sys.exit()

print(f"Restoring backup on {username}...\n")


# Subscribe to subreddits and follow users
if RESTORE_SUBSCRIPTIONS and "subreddits" in backup and "users" in backup:
    subreddit_to_subscribe = backup["subreddits"] + backup["users"]

    for subreddit in subreddit_to_subscribe:
        try:
            reddit.subreddit(subreddit).subscribe()
        except:
            print("Can't subscribe to", subreddit)
    print("Restored subscribed subreddits and followed users.")


# Create multireddits and add subreddits and users
if RESTORE_MULTIREDDITS and "multireddits" in backup:
    for multi_name, multi_data in backup["multireddits"].items():
        subreddits = multi_data["subreddits"] + multi_data["users"]
        try:
            reddit.multireddit.create(display_name=multi_name, subreddits=subreddits, visibility=MULTIREDDIT_VISIBILITY)
        except:
            print("Can't create multireddit", multi_name)
    print("Restored multireddits.")


# Restore saved posts
if RESTORE_SAVED and "saved" in backup:
    backup["saved"].reverse()
    for post_id in backup["saved"]:
        try:
            submission = reddit.submission(id=post_id)
            submission.save()
        except:
            print("Can't save post", post_id)
    print("Restored saved posts.")


# Restore hidden posts
if RESTORE_HIDDEN and "hidden" in backup:
    backup["hidden"].reverse()
    for post_id in backup["hidden"]:
        try:
            submission = reddit.submission(id=post_id)
            submission.hide()
        except:
            print("Can't hide post", post_id)
    print("Restored hidden posts.")


# Restore upvoted posts
if RESTORE_UPVOTED and "upvoted" in backup:
    for post_id in backup["upvoted"]:
        try:
            submission = reddit.submission(id=post_id)
            submission.upvote()
        except:
            print("Can't upvote post", post_id)
    print("Restored upvoted posts.")


# Restore downvoted posts
if RESTORE_DOWNVOTED and "downvoted" in backup:
    for post_id in backup["downvoted"]:
        try:
            submission = reddit.submission(id=post_id)
            submission.downvote()
        except:
            print("Can't downvote post", post_id)
    print("Restored downvoted posts.")
