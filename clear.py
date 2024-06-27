import sys
import praw

# ---------- CONFIG ----------

# value: True | False
CLEAR_SUBSCRIBED_SUBREDDITS = True
CLEAR_FOLLOWED_USERS = True
CLEAR_MULTIREDDITS = True
CLEAR_SAVED_POSTS = True
CLEAR_SAVED_COMMENTS = True
CLEAR_HIDDEN_POSTS = True
CLEAR_UPVOTED_POSTS = False
CLEAR_DOWNVOTED_POSTS = False

# value: True | False
DELETE_YOUR_POSTS = False
DELETE_YOUR_COMMENTS = False

# ---------- CONFIG ----------

if sys.argv[1]:
    username = sys.argv[1]
else:
    print("Please specify username: python clear.py <username>")
    sys.exit()

reddit = praw.Reddit(username)

print(f"Clearing {username}...\n")

# Unsubscribe all subreddits and unfollow all users
if CLEAR_SUBSCRIBED_SUBREDDITS or CLEAR_FOLLOWED_USERS:
    for subreddit in reddit.user.subreddits(limit=None):
        subreddit_name = subreddit.display_name
        try:
            if subreddit_name.startswith("u_"):
                if CLEAR_FOLLOWED_USERS:
                    subreddit.unsubscribe()
            else:
                if CLEAR_SUBSCRIBED_SUBREDDITS:
                    subreddit.unsubscribe()
        except:
            print("Can't unsubscribe subreddit", subreddit.display_name)
    if CLEAR_SUBSCRIBED_SUBREDDITS:
        print("Unsubscribed all subreddits.")
    if CLEAR_FOLLOWED_USERS:
        print("Unfollowed all users.")


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
if CLEAR_SAVED_POSTS or CLEAR_SAVED_COMMENTS:
    for saved_item in me.saved(limit=None):
        if isinstance(saved_item, praw.models.Submission):
            if CLEAR_SAVED_POSTS:
                try:
                    saved_item.unsave()
                except:
                    print("Can't unsave saved post", saved_item.id)
        else:
            if CLEAR_SAVED_COMMENTS:
                try:
                    saved_item.unsave()
                except:
                    print("Can't unsave saved comment", saved_item.id)
    if CLEAR_SAVED_POSTS:
        print("Unsaved all saved posts.")
    if CLEAR_SAVED_COMMENTS:
        print("Unsaved all saved comments.")


# Unhide all hidden posts
if CLEAR_HIDDEN_POSTS:
    for hidden_post in me.hidden(limit=None):
        try:
            hidden_post.unhide()
        except:
            print("Can't unhide hidden post", hidden_post.id)
    print("Unhid all hidden posts.")


# Unvote all upvoted posts
if CLEAR_UPVOTED_POSTS:
    for upvoted_post in me.upvoted(limit=None):
        try:
            upvoted_post.clear_vote()
        except:
            print("Can't unvote upvoted post", upvoted_post.id)
    print("Unvoted all upvoted posts.")


# Unvote all downvoted posts
if CLEAR_DOWNVOTED_POSTS:
    for downvoted_post in me.downvoted(limit=None):
        try:
            downvoted_post.clear_vote()
        except:
            print("Can't unvote downvoted post", downvoted_post.id)
    print("Unvoted all downvoted posts.")


# Delete all your posts
if DELETE_YOUR_POSTS:
    for post in me.submissions.new(limit=None):
        try:
            post.delete()
        except:
            print("Can't delete post", post.id)
    print("Deleted all your posts.")


# Delete all your comments
if DELETE_YOUR_COMMENTS:
    for comment in me.comments.new(limit=None):
        try:
            comment.delete()
        except:
            print("Can't delete comment", comment.id)
    print("Deleted all your comments.")
