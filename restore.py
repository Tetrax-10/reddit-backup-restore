import sys
import json
import praw

# ---------- CONFIG ----------

# value: True | False
RESTORE_SUBSCRIPTIONS = True
RESTORE_MULTIREDDITS = True
RESTORE_SAVED_POSTS = True
RESTORE_SAVED_COMMENTS = True
RESTORE_HIDDEN_POSTS = True
RESTORE_UPVOTED_POSTS = False
RESTORE_DOWNVOTED_POSTS = False

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


# Restore saved comments
if RESTORE_SAVED_COMMENTS and "saved_comments" in backup:
    backup["saved_comments"].reverse()
    for comment_id in backup["saved_comments"]:
        try:
            comment = reddit.comment(id=comment_id)
            comment.save()
        except:
            print("Can't save comment", comment_id)
    print("Restored saved comments.")


# Restore saved posts
if RESTORE_SAVED_POSTS and "saved_posts" in backup:
    backup["saved_posts"].reverse()
    for post_id in backup["saved_posts"]:
        try:
            submission = reddit.submission(id=post_id)
            submission.save()
        except:
            print("Can't save post", post_id)
    print("Restored saved posts.")


# Restore hidden posts
if RESTORE_HIDDEN_POSTS and "hidden_posts" in backup:
    backup["hidden_posts"].reverse()
    for post_id in backup["hidden_posts"]:
        try:
            submission = reddit.submission(id=post_id)
            submission.hide()
        except:
            print("Can't hide post", post_id)
    print("Restored hidden posts.")


# Restore upvoted posts
if RESTORE_UPVOTED_POSTS and "upvoted_posts" in backup:
    for post_id in backup["upvoted_posts"]:
        try:
            submission = reddit.submission(id=post_id)
            submission.upvote()
        except:
            print("Can't upvote post", post_id)
    print("Restored upvoted posts.")


# Restore downvoted posts
if RESTORE_DOWNVOTED_POSTS and "downvoted_posts" in backup:
    for post_id in backup["downvoted_posts"]:
        try:
            submission = reddit.submission(id=post_id)
            submission.downvote()
        except:
            print("Can't downvote post", post_id)
    print("Restored downvoted posts.")
