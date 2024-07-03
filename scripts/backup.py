import json
import praw

# Backup structure
backup = {"joined_subreddits": [], "followed_users": [], "multireddits": {}, "saved_posts": [], "saved_comments": [], "hidden_posts": [], "upvoted_posts": [], "downvoted_posts": []}

# Load backup from backup.json if available
try:
    with open("backup.json", "r") as file:
        cache_backup = json.load(file)
except:
    cache_backup = False


def backup_joined_subreddits_and_followed_users(reddit, is_joined_subreddits, is_followed_users):
    for subreddit in reddit.user.subreddits(limit=None):
        subreddit_name = subreddit.display_name
        if subreddit_name.startswith("u_"):
            if is_followed_users:
                backup["followed_users"].append(subreddit_name)
        else:
            if is_joined_subreddits:
                backup["joined_subreddits"].append(subreddit_name)

    if is_joined_subreddits:
        print(f"Backed up {len(backup['joined_subreddits'])} joined subreddits")
    if is_followed_users:
        print(f"Backed up {len(backup['followed_users'])} followed users")


def backup_multireddits(reddit):
    for multireddit in reddit.user.multireddits():
        temp = {"name": multireddit.display_name, "visibility": multireddit.visibility, "description_md": multireddit.description_md, "is_favorited": multireddit.is_favorited, "subreddits": [], "users": []}
        for subreddit in multireddit.subreddits:
            subreddit_name = subreddit.display_name
            if subreddit_name.startswith("u_"):
                temp["users"].append(subreddit_name)
            else:
                temp["subreddits"].append(subreddit_name)

        backup["multireddits"][multireddit.name] = temp

    print(f"Backed up {len(backup['multireddits'])} multireddits")


def backup_saved_items(me, is_posts, is_comments):
    for saved_item in me.saved(limit=None):
        if isinstance(saved_item, praw.models.Submission):
            if is_posts:
                backup["saved_posts"].append(saved_item.id)
        else:
            if is_comments:
                backup["saved_comments"].append(saved_item.id)

    if is_posts:
        print(f"Backed up {len(backup['saved_posts'])} saved posts")
    if is_comments:
        print(f"Backed up {len(backup['saved_comments'])} saved comments")


def backup_hidden_posts(me):
    for hidden_post in me.hidden(limit=None):
        backup["hidden_posts"].append(hidden_post.id)

    print(f"Backed up {len(backup['hidden_posts'])} hidden posts")


def backup_upvoted_posts(me):
    for upvoted_post in me.upvoted(limit=None):
        backup["upvoted_posts"].append(upvoted_post.id)

    print(f"Backed up {len(backup['upvoted_posts'])} upvoted posts")


def backup_downvoted_posts(me):
    for downvoted_post in me.downvoted(limit=None):
        backup["downvoted_posts"].append(downvoted_post.id)

    print(f"Backed up {len(backup['downvoted_posts'])} downvoted posts")


def backup_func(reddit, me, config, username, version):
    print(f"Backing up {username}...\n")

    if config["joined_subreddits"] or config["followed_users"]:
        backup_joined_subreddits_and_followed_users(reddit, config["joined_subreddits"], config["followed_users"])
    elif cache_backup:
        if "joined_subreddits" in cache_backup:
            backup["joined_subreddits"] = cache_backup["joined_subreddits"]
        else:
            backup["joined_subreddits"] = []
        if "followed_users" in cache_backup:
            backup["followed_users"] = cache_backup["followed_users"]
        else:
            backup["followed_users"] = []

    if config["multireddits"]:
        backup_multireddits(reddit)
    elif cache_backup:
        if "multireddits" in cache_backup:
            backup["multireddits"] = cache_backup["multireddits"]
        else:
            backup["multireddits"] = {}

    if config["saved_posts"] or config["saved_comments"]:
        backup_saved_items(me, config["saved_posts"], config["saved_comments"])
    elif cache_backup:
        if "saved_posts" in cache_backup:
            backup["saved_posts"] = cache_backup["saved_posts"]
        else:
            backup["saved_posts"] = []
        if "saved_comments" in cache_backup:
            backup["saved_comments"] = cache_backup["saved_comments"]
        else:
            backup["saved_comments"] = []

    if config["hidden_posts"]:
        backup_hidden_posts(me)
    elif cache_backup:
        if "hidden_posts" in cache_backup:
            backup["hidden_posts"] = cache_backup["hidden_posts"]
        else:
            backup["hidden_posts"] = []

    if config["upvoted_posts"]:
        backup_upvoted_posts(me)
    elif cache_backup:
        if "upvoted_posts" in cache_backup:
            backup["upvoted_posts"] = cache_backup["upvoted_posts"]
        else:
            backup["upvoted_posts"] = []

    if config["downvoted_posts"]:
        backup_downvoted_posts(me)
    elif cache_backup:
        if "downvoted_posts" in cache_backup:
            backup["downvoted_posts"] = cache_backup["downvoted_posts"]
        else:
            backup["downvoted_posts"] = []

    # Add version
    backup["version"] = version

    # Save backup to backup.json
    with open("backup.json", "w") as file:
        json.dump(backup, file, indent=4)

    print("\nBackup saved to backup.json")
