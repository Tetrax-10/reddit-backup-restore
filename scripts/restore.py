import sys
import json
import praw

# Load backup from backup.json
try:
    with open("backup.json", "r") as file:
        backup = json.load(file)
except:
    print("Backup unavailable or corrupted")
    sys.exit()


def restore_joined_subreddits_and_followed_users(reddit, is_joined_subreddits, is_followed_users):
    subreddit_to_join = []
    if is_joined_subreddits:
        subreddit_to_join += backup["joined_subreddits"]
    if is_followed_users:
        subreddit_to_join += backup["followed_users"]

    subreddit_count = 0
    user_count = 0
    for subreddit in subreddit_to_join:
        try:
            reddit.subreddit(subreddit).subscribe()
            if subreddit.startswith("u_"):
                user_count += 1
            else:
                subreddit_count += 1
        except:
            print(f"Can't {'follow' if subreddit_name.startswith('u_') else 'join'}", subreddit)
    if is_joined_subreddits:
        print(f"Restored {subreddit_count}/{len(backup['joined_subreddits'])} joined subreddits")
    if is_followed_users:
        print(f"Restored {user_count}/{len(backup['followed_users'])} followed users")


def star_multireddit(reddit, multireddit, make_favorite=True):
    try:
        reddit.post(
            "/api/multi/favorite?raw_json=1&gilding_detail=1",
            params={
                "multipath": multireddit,
                "make_favorite": "true" if make_favorite else "false",
                "api_type": "json",
            },
        )
    except:
        print("Can't star multireddit", multireddit)


def restore_multireddits(reddit, overridden_multireddits_visibility):
    user_multireddits = reddit.user.multireddits()

    count = 0
    for multi_id, multi_data in backup["multireddits"].items():
        existing_multireddit = next((m for m in user_multireddits if m.name == multi_id), None)
        subreddits = multi_data["subreddits"] + multi_data["users"]
        if existing_multireddit and existing_multireddit.can_edit:
            try:
                existing_multireddit.update(display_name=(multi_data["name"]), subreddits=subreddits, description_md=multi_data["description_md"], visibility=multi_data["visibility"] if overridden_multireddits_visibility == None else overridden_multireddits_visibility)
                count += 1
                if multi_data["is_favorited"] and (not existing_multireddit.is_favorited):
                    star_multireddit(reddit, existing_multireddit)
                elif (not multi_data["is_favorited"]) and existing_multireddit.is_favorited:
                    star_multireddit(reddit, existing_multireddit, make_favorite=False)
            except:
                print("Can't update multireddit", multi_data["name"])
        else:
            try:
                multireddit = reddit.multireddit.create(display_name=(multi_data["name"]), subreddits=subreddits, description_md=multi_data["description_md"], visibility=multi_data["visibility"] if overridden_multireddits_visibility == None else overridden_multireddits_visibility)
                count += 1
                if multi_data["is_favorited"]:
                    star_multireddit(reddit, multireddit)
            except:
                print("Can't create multireddit", multi_data["name"])
    print(f"Restored {count}/{len(backup['multireddits'])} multireddits")


def restore_saved_comments(reddit):
    backup["saved_comments"].reverse()
    count = 0
    for comment_id in backup["saved_comments"]:
        try:
            reddit.comment(id=comment_id).save()
            count += 1
        except:
            print("Can't save comment", comment_id)
    print(f"Restored {count}/{len(backup['saved_comments'])} saved comments")


def restore_saved_posts(reddit):
    backup["saved_posts"].reverse()
    count = 0
    for post_id in backup["saved_posts"]:
        try:
            reddit.submission(id=post_id).save()
            count += 1
        except:
            print("Can't save post", post_id)
    print(f"Restored {count}/{len(backup['saved_posts'])} saved posts")


def restore_hidden_posts(reddit):
    backup["hidden_posts"].reverse()
    count = 0
    for post_id in backup["hidden_posts"]:
        try:
            reddit.submission(id=post_id).hide()
            count += 1
        except:
            print("Can't hide post", post_id)
    print(f"Restored {count}/{len(backup['hidden_posts'])} hidden posts")


def restore_upvoted_posts(reddit):
    count = 0
    for post_id in backup["upvoted_posts"]:
        try:
            reddit.submission(id=post_id).upvote()
            count += 1
        except:
            print("Can't upvote post", post_id)
    print(f"Restored {count}/{len(backup['upvoted_posts'])} upvoted posts")


def restore_downvoted_posts(reddit):
    count = 0
    for post_id in backup["downvoted_posts"]:
        try:
            reddit.submission(id=post_id).downvote()
            count += 1
        except:
            print("Can't downvote post", post_id)
    print(f"Restored {count}/{len(backup['downvoted_posts'])} downvoted posts")


def restore_func(reddit, config, username):
    print(f"Restoring backup on {username}...\n")

    if (config["joined_subreddits"] and "joined_subreddits" in backup) or (config["followed_users"] and "followed_users" in backup):
        restore_joined_subreddits_and_followed_users(reddit, config["joined_subreddits"], config["followed_users"])
    if config["multireddits"] and "multireddits" in backup:
        restore_multireddits(reddit, config["overridden_multireddits_visibility"])
    if config["saved_comments"] and "saved_comments" in backup:
        restore_saved_comments(reddit)
    if config["saved_posts"] and "saved_posts" in backup:
        restore_saved_posts(reddit)
    if config["hidden_posts"] and "hidden_posts" in backup:
        restore_hidden_posts(reddit)
    if config["upvoted_posts"] and "upvoted_posts" in backup:
        restore_upvoted_posts(reddit)
    if config["downvoted_posts"] and "downvoted_posts" in backup:
        restore_downvoted_posts(reddit)

    print("\nDone")
