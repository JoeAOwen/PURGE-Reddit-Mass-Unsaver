# PURGE - Post Unsave + Reddit Garbage Eraser
By Joe

A tool for erasing all your unwanted Reddit saves.
 
 -----

 ## Overview

 Reddit saves are annoying. Over the years you save too many posts and it quickly becomes filled and cluttered. This is a tool designed to unsave posts from your account in bulk so you can start from a clean slate and save only what is important.

 This tool comes free to use as is. Feel free to incorporate it in any other projects as you see fit. All I ask is that I am credited for the work carried out here and you link to this GitHub page.

 This was built and tested on Python 3.11.10. Yes I know it's old but I can't be bothered to update my python version on my laptop and I built this in one evening so you can't be picky.

 -----

 ## Prerequisites

 Python 3.11.10 (might work on others but I'm only testing for what I have)
 This has been tested on a Mac running Firefox. It probably works on other device / browser combos but I make no guarentees.

-----

## Setup

 In the repo root run:
 
 ```pip install -r requirements.txt```

 -----

 ## Usage

 Running the script will open a new browser window with a reddit login page. In this window enter your Reddit credentials, login, and then press enter in the terminal and the script will run.

 **Important Note:** As the behaviour of the script inherently looks bot-like, Reddit will sometimes rate limit you temporarily. When this happens the script will exit as there is nothing it can find. Wait a few minutes and then rerun the script to continue the unsaving.

 **Example Commands:**

 ```python reddit-unsaver.py --browser firefox --include askreddit --dry-run```

 This command would remove all saves on your account that are in the r/askreddit subreddit. As it has the --dry-run tag it will not actually unsave anything and instead state what would be unsaved and the total number at the end.

 ```python reddit-unsaver.py --browser firefox --exclude learnpython gaming```

 This command would remove all saves on your account that are not in the r/learnpython or r/gaming subreddits. 
 
 Both the include and exclude params can take as many subreddits as you wish simply adding a space between them. You cannot use both at the same time as that wouldn't make sense.

 ```python reddit-unsaver.py --browser firefox --dry-run```

 A dry run of removing all saves from your account regardless of subreddit.

 ```python reddit-unsaver.py --browser firefox --delay 2.5```

 Removing all saves from your account with an average delay between unsaves of 2.5 seconds. Different delays you may find rate limits you less frequently.

 -----

 ## Conclusion

 Hope you enjoy using this tool. Feel free to give this repo a star if you do.

 Additionally feel free to request additional features if you can think of any. This is fairly barebones as is just for my current usecase.

 Happy PURGE-ing :)
