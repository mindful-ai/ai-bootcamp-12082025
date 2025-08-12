Change to a new repository:
git remote set-url origin https://github.com/new-username/new-repo.git

If the new repo is empty:
git push -u origin main

If the new repo already has some files:
git pull origin main --rebase
git push -u origin main



git remove -v
git remote remove origin
git remote add origin https://github.com/new-username/new-repo.git
git push -u origin main