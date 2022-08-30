

# init git repo
git init

# set remote to the url https://github.com/geoffreygarrett/horses-for-sale.git
git remote add origin https://github.com/geoffreygarrett/horses-for-sale.git

# verify
git remote -v

# add all files to the repo
git add .

# commit changes
git commit -m "initial commit"
 
# force push to remote repo
git push -f origin master
