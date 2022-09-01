
# set url
git_url="https://github.com/geoffreygarrett/horses-for-sale"

# cd to out 
cd out

# initiate out/ directory as a repository
git init

# git add all files
git add .

# add remote repository on gh-pages branch
git remote add -f origin $git_url

# git pull
git pull origin gh-pages

# checkout gh-pages branch
git checkout -b gh-pages origin/gh-pages

# push to gh-pages branch
git push origin gh-pages