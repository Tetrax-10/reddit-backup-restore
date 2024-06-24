# Reddit Backup Restore

Script to backup and restore your joined subredits, multireddits, followed users, saved posts, upvoted posts and downvoted posts.

## Why, I made this?

Reddit shadow banned my secondary account without specifying any reasons. Therefore, I wanted to transfer my 700+ subreddits, 50+ multireddits, 300+ followed users, 100+ saved posts, 150+ upvoted posts, and 0 downvoted posts to a new account. I made this script to transfer all this data to the new account and start fresh. **It's always good to have a backup of your account's user data** because anyone can get banned on Reddit at any time without any reason.

</br>

## Setup

1. [Download this repo](https://github.com/Tetrax-10/reddit-backup-restore/archive/refs/heads/main.zip) or clone this repository

2. Make sure you have [python](https://www.python.org) installed.

3. Open a terminal inside the `reddit-backup-restore` folder and run: `pip install praw`.

4. Replace the placeholders inside `praw.ini` file.

    _Note:_ To get `client_id` and `client_secret`, go [here](https://www.reddit.com/prefs/apps) and create an app with [these values](https://raw.githubusercontent.com/Tetrax-10/reddit-backup-restore/main/assets/app_data.png). After creating the app you can see the [`client_id` and `client_secret`](https://raw.githubusercontent.com/Tetrax-10/reddit-backup-restore/main/assets/form.png).

5. You need to create two apps, one on the account you want to backup and one on the account you want to restore.

</br>

## Usage

### 1. Run this to backup your main account

This will create a `backup.json` where all your joined subreddits, multireddits, followed users, saved posts, upvoted posts and downvoted posts will be stored.

```sh
python backup.py account_1_username
```

![backup](https://raw.githubusercontent.com/Tetrax-10/reddit-backup-restore/main/assets/backup.png)

</br>

### 2. **Run this to restore the backup to your secondary account**

This will restore all your joined subreddits, multireddits, followed users and saved posts from `backup.json`.

```sh
python restore.py account_2_username
```

![restore](https://raw.githubusercontent.com/Tetrax-10/reddit-backup-restore/main/assets/restore.png)

**_Note:_** By default, **upvoted and downvoted posts** will not be restored. Modifying upvotes and downvotes in bulk may trigger _Reddit's automated vote manipulation detector_, which may lead to **permanent ban**. **_Use at your own risk_**. You can modify the config section inside `restore.py` to enable this feature.

</br>

### 3. Extra feature:

If you want to clear an account's user data (unsubscribe all joined subreddits, unfollow all users, delete all multireddits and saved posts), run:

```sh
python clear.py account_username
```

![clear](https://raw.githubusercontent.com/Tetrax-10/reddit-backup-restore/main/assets/clear.png)

again, upvoted posts and downvoted posts will not be cleared by default. You can modify the config section inside `clear.py` to enable this feature.

</br>

### Caution: Use at Your Own Risk

This script is provided as-is, without any guarantees or warranties. By using this script, you acknowledge and agree that the author will not be responsible or liable for any bans, data loss, or other issues that may arise. Use this script at your own risk. Always ensure you comply with Reddit's terms of service and guidelines when using this script.
