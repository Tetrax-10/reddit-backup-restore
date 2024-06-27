import sys
import json
import praw

# ---------- CONFIG ----------

# value: True | False
BACKUP_SUBSCRIPTIONS = True
BACKUP_MULTIREDDITS = True
BACKUP_SAVED_POSTS = True
BACKUP_SAVED_COMMENTS = True
BACKUP_HIDDEN_POSTS = True
BACKUP_UPVOTED_POSTS = True
BACKUP_DOWNVOTED_POSTS = True

# ---------- CONFIG ----------


if sys.argv[1]:
    username = sys.argv[1]
else:
    print("Please specify username: python backup.py <username>")
    sys.exit()

reddit = praw.Reddit(username)
backup = {"subreddits": [], "users": [], "multireddits": {}, "saved_posts": [], "saved_comments": [], "hidden_posts": [], "upvoted_posts": [], "downvoted_posts": []}
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
    if "subreddits" in cache_backup:
        backup["subreddits"] = cache_backup["subreddits"]
    else:
        backup["subreddits"] = []
    if "users" in cache_backup:
        backup["users"] = cache_backup["users"]
    else:
        backup["users"] = []


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
    if "multireddits" in cache_backup:
        backup["multireddits"] = cache_backup["multireddits"]
    else:
        backup["multireddits"] = {}

me = reddit.user.me()

# Backup saved posts
if BACKUP_SAVED_POSTS or BACKUP_SAVED_COMMENTS:
    for saved_item in me.saved(limit=None):
        if isinstance(saved_item, praw.models.Submission):
            if BACKUP_SAVED_POSTS:
                backup["saved_posts"].append(saved_item.id)
        else:
            if BACKUP_SAVED_COMMENTS:
                backup["saved_comments"].append(saved_item.id)
    if BACKUP_SAVED_POSTS:
        print(f"Backed up {len(backup['saved_posts'])} saved posts.")
    if BACKUP_SAVED_COMMENTS:
        print(f"Backed up {len(backup['saved_comments'])} saved comments.")
elif cache_backup:
    if "saved_posts" in cache_backup:
        backup["saved_posts"] = cache_backup["saved_posts"]
    else:
        backup["saved_posts"] = []
    if "saved_comments" in cache_backup:
        backup["saved_comments"] = cache_backup["saved_comments"]
    else:
        backup["saved_comments"] = []


# Backup hidden posts
if BACKUP_HIDDEN_POSTS:
    for hidden_post in me.hidden(limit=None):
        backup["hidden_posts"].append(hidden_post.id)

    print(f"Backed up {len(backup['hidden_posts'])} hidden posts.")
elif cache_backup:
    if "hidden_posts" in cache_backup:
        backup["hidden_posts"] = cache_backup["hidden_posts"]
    else:
        backup["hidden_posts"] = []


# Backup upvoted posts
if BACKUP_UPVOTED_POSTS:
    for upvoted_post in me.upvoted(limit=None):
        backup["upvoted_posts"].append(upvoted_post.id)

    print(f"Backed up {len(backup['upvoted_posts'])} upvoted posts.")
elif cache_backup:
    if "upvoted_posts" in cache_backup:
        backup["upvoted_posts"] = cache_backup["upvoted_posts"]
    else:
        backup["upvoted_posts"] = []


# Backup upvoted posts
if BACKUP_DOWNVOTED_POSTS:
    for downvoted_post in me.downvoted(limit=None):
        backup["downvoted_posts"].append(downvoted_post.id)

    print(f"Backed up {len(backup['downvoted_posts'])} downvoted posts.")
elif cache_backup:
    if "downvoted_posts" in cache_backup:
        backup["downvoted_posts"] = cache_backup["downvoted_posts"]
    else:
        backup["downvoted_posts"] = []


# Save backup to backup.json
with open("backup.json", "w") as file:
    json.dump(backup, file, indent=4)

print("\nBackup saved to backup.json")
