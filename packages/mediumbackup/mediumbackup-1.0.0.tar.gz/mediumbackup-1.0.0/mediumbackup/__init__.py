import os
import logging

import medium
from markdownify import markdownify as md

MAX_FILENAME_LENGTH = 30 # Ignores date and extension, e.g. 2020-10-31<-- 30 characthers -->.md

def backup_stories(username, backup_dir=None, format=None):
    """ Download all the public stories by username.
    
    Keyword arguments:
    backup_dir -- destination directory name, default "backup"
    format     -- "html" or "md" for markdown, defualt "html"
    """
    
    # Check user input
    backup_dir = "backup" if backup_dir is None else backup_dir
    format = "html" if format is None else format
    if format not in ["html", "md"]:
        logging.warning("Format {} note recognized, html will be used instead.".format(format))
        
    # Create backup directroy if not existent
    if not os.path.exists(backup_dir):
        os.mkdir(backup_dir)
    
    # Get the stories list through a medium client, 
    # authentication is not required in this case 
    mclient = medium.Client()
    list_stories = mclient.list_articles(username=username)
    
    # For each story, crate a backup file
    for story in list_stories:
        
        # Retrieve story information
        pub_date = story["pubDate"][:len("yyyy-mm-dd")]
        title = story["title"]
        link = story["link"]
        content = story["content"]
        
        # Add story title to the content
        content = "<h1>{}</h1>{}".format(title, content)
        if format == "md":
            content = md(content, heading_style="ATX")
        
        # Find the url path portion of the story url 
        # (i.e. whatever comes after the last /)
        # and remove invalid filename characthers
        url_path = link.split("/")[-1]
        for char in "?":
            url_path = url_path.replace(char, "")
        
        # Build the filename and save the file
        filename = "".join([pub_date, " ", url_path[:MAX_FILENAME_LENGTH], ".", format])
        with open(os.path.join(backup_dir, filename), "wt", encoding="utf8") as f:
            f.write(content)
    return
    
    