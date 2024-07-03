import re


def transform_multireddit_name_to_id(input_string):
    cleaned_string = re.sub(r"[^a-zA-Z0-9\s]", "", input_string)
    words = cleaned_string.split()
    result = "_".join(words).lower()
    return result


def transform_structure(original_dict):
    transformed_dict = {}

    for key, value in original_dict.items():
        transformed_dict[transform_multireddit_name_to_id(key)] = {"name": key, "visibility": "public", "description_md": "", "is_favorited": False, "subreddits": value["subreddits"], "users": value["users"]}

    return transformed_dict


def upgrade_backup_func(backup, version):
    backup_structure = {"joined_subreddits": [], "followed_users": [], "multireddits": {}, "saved_posts": [], "saved_comments": [], "hidden_posts": [], "upvoted_posts": [], "downvoted_posts": []}

    if "version" not in backup:
        backup_structure["joined_subreddits"] = backup["subreddits"]
        backup_structure["followed_users"] = backup["users"]
        backup_structure["multireddits"] = transform_structure(backup["multireddits"])
        backup_structure["saved_posts"] = backup["saved"]
        backup_structure["hidden_posts"] = backup["hidden"]
        backup_structure["upvoted_posts"] = backup["upvoted"]
        backup_structure["downvoted_posts"] = backup["downvoted"]
        backup_structure["version"] = version

    print(f"Backup upgraded to version {version}\n")
    return backup_structure
