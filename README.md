# www
Conference website: https://th.pycon.org/

Netlify is watching this repo. When you push to it, the site will be built.
For now, the URL is https://serene-mestorf-5c91d0.netlify.com/ 

Netlify also builds previews for pull requests.
To see the preview, click on **Details** to the right of the _**deploy/netlify** Deploy preview ready!_ notification on the pull request.

## Contributing to the design

- pick a task from https://trello.com/b/K8WFAo0w/pycon-thailand-website
- add your name to it
- create a PR
- submit for review

## How to a add a new post

official way - https://getnikola.com/handbook.html#creating-a-blog-post

1. Ensure you have a github account
2. Go to https://github.com/PyConTH/www/tree/master/site/posts 
3. First check there is not a draft already for the post you want to make
   - If there is just edit to remove draft and update publish date
3. Add two files in github. English and Thai
   - Click "Add new File". 
   - Ensure you name X.en.rst and X.th.rst (or .md for markdown)
3. Put metadata at the top of the file. min is title, slug, date
4. Use these instructions for formatting text
   - .rst http://docutils.sourceforge.net/docs/user/rst/quickref.html
   - .md https://en.support.wordpress.com/markdown-quick-reference/
4. Copy the english text to the thaiversion ready for translation
5. Commit new changes as "Create new branch and start a pull request"
6. Wait for netlify check to finish and click "details" to see site preview
8. Select "request review" and pick translator. Also contact them directly
9. Translator will edit the empty translation file
10. Request review of jean or djay to merge into site

## How to edit a page on the website

1. ...
7. if not in the menu
   - Edit https://github.com/PyConTH/www/blob/master/site/conf.py and ensure your page is in both menus


## Places to share a post
- FB: https://www.facebook.com/Pyconthailand/ and then share this to
   - https://www.facebook.com/groups/admin.py.dev
   - https://www.facebook.com/groups/thaipybkk/
   - https://www.facebook.com/groups/ThaiPGAssociateSociety
   - https://www.facebook.com/groups/198151340250987 (python thailand)
   - https://www.facebook.com/groups/pyasiapac
   - https://www.facebook.com/groups/109676182999340 (MicroPython:Thailand)
   - https://www.facebook.com/groups/thai.ros
   - https://www.facebook.com/groups/ilovedata
   - https://www.facebook.com/groups/thainlp
   - https://www.facebook.com/groups/codingth
   - https://www.facebook.com/groups/941490879222335 (Thailand Machine Learning & Artificial Intelligence)
   - https://www.facebook.com/groups/dsbkkgroup
   - https://www.facebook.com/groups/OpenDataInTh
   - https://www.facebook.com/groups/CoderDojoTH
   - https://www.facebook.com/groups/164204783609455 (Thailand's Machine Learning Research)
   - https://www.facebook.com/groups/pythonvn
   - https://www.facebook.com/groups/720597038025424 (devops thailand)
   
- Twitter: https://twitter.com/pyconthailand
- Last years attendee list - https://us18.admin.mailchimp.com/audience/ "pyconth"
- TPA list of all event attendees
- Ask TDPK to share



## Get copy from old site

Go to https://github.com/PyConTH/www/tree/8f00bd93a86c30962479cfe4ebcb753080ca44ba

## How to build

Note: You don't need to do this to edit the site

```
pip install --user -r requirements.txt
cd site
nikola build
```
