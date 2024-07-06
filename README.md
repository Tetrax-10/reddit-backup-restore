# Reddit Backup Restore

Script to backup and restore your joined subreddits, multireddits, followed users, saved posts, saved comments, hidden posts, upvoted posts and downvoted posts.

## Why, I made this?

Reddit shadow banned my secondary account without specifying any reasons. Therefore, I wanted to transfer my 700+ subreddits, 50+ multireddits, 300+ followed users, 100+ saved posts and 150+ upvoted posts to a new account. I made this script to transfer all these data to my new account and start fresh. **It's always good to have a backup of your account's user data** because anyone can get banned on Reddit at any time without any justifiable reason.

</br>

## Setup

1. Make sure you have [python](https://www.python.org) installed.

2. Download the [latest release](https://github.com/Tetrax-10/reddit-backup-restore/releases/latest)

3. Open a terminal inside the `reddit-backup-restore` folder and run: `pip install -r requirements.txt`.

4. Replace the placeholders inside `praw.ini` file.

    _Note:_ To get `client_id` and `client_secret`, go [here](https://www.reddit.com/prefs/apps) and create an app with [these values](https://raw.githubusercontent.com/Tetrax-10/reddit-backup-restore/main/assets/app_data.png). After creating the app you can see the [`client_id` and `client_secret`](https://raw.githubusercontent.com/Tetrax-10/reddit-backup-restore/main/assets/form.png).

5. You need to create two apps, one on the account you want to backup and one on the account you want to restore.

</br>

## Usage

### 1. Run this to backup your main account

This will create a `backup.json` where all `account_1_username`'s user data will be stored.

```sh
python reddit.py backup account_1_username
```

<img src="https://raw.githubusercontent.com/Tetrax-10/reddit-backup-restore/main/assets/backup.png" width="400px"></img>

_Note:_ **Followed multireddits** will not be backed due to reddit's API limitation.

</br>

### 2. **Run this to restore the backup to your secondary account**

This will restore all `account_1_username`'s user data which was backed up to `backup.json` to `account_2_username`.

```sh
python reddit.py restore account_2_username
```

<img src="https://raw.githubusercontent.com/Tetrax-10/reddit-backup-restore/main/assets/restore.png" width="400px"></img>

_Note:_ By default, **upvoted and downvoted posts will not be restored**. Modifying upvotes and downvotes in bulk may trigger _Reddit's automated vote manipulation detector_, which may lead to **permanent ban**. **_Use at your own risk_**. You can modify the `config.ini` to enable this feature.

</br>

### 3. Extra feature (clear an account's user data):

If you want to unsubscribe all joined subreddits, unfollow all users, delete all multireddits, saved posts, saved comments and hidden posts, run:

```sh
python reddit.py clear account_username
```

<img src="https://raw.githubusercontent.com/Tetrax-10/reddit-backup-restore/main/assets/clear.png" width="400px"></img>

Again, upvoted posts and downvoted posts will not be cleared by default. You can modify the `config.ini` to enable this feature.

You can also delete all your posts and comments by modifying the `config.ini`. By default, **your posts and comments will not be deleted**.

</br>

### Caution: Use at Your Own Risk

This script is provided as-is, without any guarantees or warranties. By using this script, you acknowledge and agree that the author will not be responsible or liable for any bans, data loss, or other issues that may arise. Use this script at your own risk. Always ensure you comply with Reddit's terms of service and guidelines when using this script.
