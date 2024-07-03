import sys
import praw


def clear_joined_subreddits_and_followed_users(reddit, is_joined_subreddits, is_followed_users):
    for subreddit in reddit.user.subreddits(limit=None):
        subreddit_name = subreddit.display_name
        try:
            if subreddit_name.startswith("u_"):
                if is_followed_users:
                    subreddit.unsubscribe()
            else:
                if is_joined_subreddits:
                    subreddit.unsubscribe()
        except:
            print(f"Can't {'unfollow' if subreddit_name.startswith('u_') else 'leave'}", subreddit.display_name)

    if is_joined_subreddits:
        print("Left all subreddits")
    if is_followed_users:
        print("Unfollowed all users")


def clear_multireddits(reddit):
    for multireddit in reddit.user.multireddits():
        try:
            multireddit.delete()
        except:
            print("Can't delete multireddit", multireddit.display_name)

    print("Deleted all multireddits")


def clear_saved_items(me, is_posts, is_comments):
    for saved_item in me.saved(limit=None):
        if isinstance(saved_item, praw.models.Submission):
            if is_posts:
                try:
                    saved_item.unsave()
                except:
                    print("Can't unsave saved post", saved_item.id)
        else:
            if is_comments:
                try:
                    saved_item.unsave()
                except:
                    print("Can't unsave saved comment", saved_item.id)

    if is_posts:
        print("Unsaved all saved posts")
    if is_comments:
        print("Unsaved all saved comments")


def clear_hidden_posts(me):
    for hidden_post in me.hidden(limit=None):
        try:
            hidden_post.unhide()
        except:
            print("Can't unhide hidden post", hidden_post.id)

    print("Unhid all hidden posts")


def clear_upvoted_posts(me):
    for upvoted_post in me.upvoted(limit=None):
        try:
            upvoted_post.clear_vote()
        except:
            print("Can't unvote upvoted post", upvoted_post.id)

    print("Unvoted all upvoted posts")


def clear_downvoted_posts(me):
    for downvoted_post in me.downvoted(limit=None):
        try:
            downvoted_post.clear_vote()
        except:
            print("Can't unvote downvoted post", downvoted_post.id)

    print("Unvoted all downvoted posts")


def clear_your_posts(me):
    for post in me.submissions.new(limit=None):
        try:
            post.delete()
        except:
            print("Can't delete post", post.id)

    print("Deleted all your posts")


def clear_your_comments(me):
    for comment in me.comments.new(limit=None):
        try:
            comment.delete()
        except:
            print("Can't delete comment", comment.id)

    print("Deleted all your comments")


def clear_func(reddit, me, config, username):
    # Ask for confirmation
    confirmation = input(f'Are you sure you want to clear {username}? Type "yes" to confirm: ').strip().lower()
    if confirmation != "yes":
        sys.exit()

    print(f"Clearing {username}...\n")

    if config["joined_subreddits"] or config["followed_users"]:
        clear_joined_subreddits_and_followed_users(reddit, config["joined_subreddits"], config["followed_users"])
    if config["multireddits"]:
        clear_multireddits(reddit)
    if config["saved_posts"] or config["saved_comments"]:
        clear_saved_items(me, config["saved_posts"], config["saved_comments"])
    if config["hidden_posts"]:
        clear_hidden_posts(me)
    if config["upvoted_posts"]:
        clear_upvoted_posts(me)
    if config["downvoted_posts"]:
        clear_downvoted_posts(me)
    if config["your_posts"]:
        clear_your_posts(me)
    if config["your_comments"]:
        clear_your_comments(me)

    print("\nDone")
