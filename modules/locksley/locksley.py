import urllib.request
import os
import os.path
from facebook_scraper import get_posts
import shutil
import imagehash
from PIL import Image
import sqlite3


temp = "temp"
meme_directory = "memes/"
image_signatures = {}
pages = {"LMG - Memes": "LMGMemes1"}
found = False

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
db_path = os.path.join(BASE_DIR, "memes.db")

connection = sqlite3.connect(db_path, check_same_thread=False)
cursor = connection.cursor()

cursor.execute("CREATE TABLE IF NOT EXISTS memes(name TEXT, post_id TEXT, viewed INTEGER)")
cursor.execute("CREATE TABLE IF NOT EXISTS temp_memes(name TEXT, post_id TEXT, viewd INTEGER)")
connection.commit()
connection.close()

connection = sqlite3.connect(db_path, check_same_thread=False)
cursor = connection.cursor()


def refresh(log):

    found = False

    for page, page_url in pages.items():

        for post in get_posts(page_url, pages=3):

            # Download each image to temp folder for comparison

            temp_filename = temp + "/" + post["post_id"]

            try:
                urllib.request.urlretrieve(post["image"], temp_filename)

                meme_hash = imagehash.average_hash(Image.open(temp_filename))
                meme_hash = str(meme_hash)
                os.rename((temp_filename), ("temp/" + meme_hash))

                url = post["image"]

                cursor.execute("INSERT INTO temp_memes VALUES(?,?,0)", (meme_hash, url))
                connection.commit()
            except Exception as e:
                log.debug(e)

            # compare against all other images

            cursor.execute("SELECT * FROM memes")
            for row in cursor:

                old_meme_hash = row[0]

                if "meme_hash" in locals():

                    if old_meme_hash == meme_hash:
                        # If meme is in folder already, delete
                        try:
                            os.remove("temp/" + meme_hash)
                            cursor.execute("DELETE FROM temp_memes")
                            connection.commit()
                            found = True
                            break
                        except Exception as e:
                            log.debug(e)
                    else:
                        pass

            # If image is new, move to meme folder

            if found is False:
                try:
                    shutil.move(("temp/" + meme_hash), "memes")

                    cursor.execute("INSERT INTO memes SELECT * FROM temp_memes")
                    connection.commit()
                except Exception as e:
                    log.debug(e)
    log.info("locksley completed")
