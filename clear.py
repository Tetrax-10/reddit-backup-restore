import sys
import praw

# ---------- CONFIG ----------

# value: True | False
CLEAR_SUBSCRIPTIONS = True
CLEAR_MULTIREDDITS = True
CLEAR_SAVED = True
CLEAR_UPVOTED = False
CLEAR_DOWNVOTED = False

# ---------- CONFIG ----------

if sys.argv[1]:
    username = sys.argv[1]
else:
    print("Please specify username: python clear.py <username>")
    sys.exit()

reddit = praw.Reddit(username)

print("Clearing account...")

# Unsubscribe all subreddits and unfollow all users
if CLEAR_SUBSCRIPTIONS:
    for subreddit in reddit.user.subreddits(limit=None):
        try:
            subreddit.unsubscribe()
        except:
            print("Can't unsubscribe subreddit", subreddit.display_name)
    print("Unsubscribed all subreddits and unfollowed all users.")

# Delete all multireddits
if CLEAR_MULTIREDDITS:
    for multireddit in reddit.user.multireddits():
        try:
            multireddit.delete()
        except:
            print("Can't delete multireddit", multireddit.display_name)
    print("Deleted all multireddits.")

me = reddit.user.me()

# Unsave all saved posts
if CLEAR_SAVED:
    for saved_post in me.saved(limit=None):
        try:
            saved_post.unsave()
        except:
            print("Can't unsave saved post", saved_post.id)
    print("Unsaved all saved posts.")


# Unvote all upvoted posts
if CLEAR_UPVOTED:
    for upvoted_post in me.upvoted(limit=None):
        try:
            upvoted_post.clear_vote()
        except:
            print("Can't unvote upvoted post", upvoted_post.id)
    print("Unvoted all upvoted posts.")


# Unvote all downvoted posts
if CLEAR_DOWNVOTED:
    for downvoted_post in me.downvoted(limit=None):
        try:
            downvoted_post.clear_vote()
        except:
            print("Can't unvote downvoted post", downvoted_post.id)
    print("Unvoted all downvoted posts.")
