# www
Conference website

Netlify is watching this repo. When you push to it, the site will be built.
For now, the URL is https://serene-mestorf-5c91d0.netlify.com/ 

Netlify also builds previews for pull requests.
To see the preview, click on **Details** to the right of the _**deploy/netlify** Deploy preview ready!_ notification on the pull request. 

## How to a add a new page

1. Ensure you have a github account
2. Go to https://github.com/PyConTH/www/tree/master/site/pages and click "Add new File". Ensure you name X.en.rst or X.th.rst (or .md for markdown)
3. Put metadata at the top of the file. min is title, slug, date
4. Use these instructions for formatting text
5. Commit new changes as "Create new branch and start a pull request"
6. Create another file for the translation in the same PR
7. Edit https://github.com/PyConTH/www/blob/master/site/conf.py and ensure your page is in both menus
8. Select "request review" and pick translator. Also contact them directly
9. Translator will edit the empty translation file
10. Request review of jean or djay to merge into site

## How to add a news post

- Similar to above put put in /posts.
- Add publish date

Once merged do the following
1. Merge message into a single post with thai first and english second
2. Post onto https://www.facebook.com/Pyconthailand/
   - share into the following groups...
3. Post on https://twitter.com/pyconthailand. Likely have to short the text.
4. If important post to mailchimp....


## How to build

Note: You don't need to do this to edit the site

```
pip install --user -r requirements.txt
cd site
nikola build
```
