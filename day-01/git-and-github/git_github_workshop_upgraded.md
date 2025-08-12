# Git & GitHub Workshop (2 Hours)

## Part 1 – Introduction (10 mins)
**What is Git?**
- Version control system for tracking changes in code

**What is GitHub?**
- Remote repository hosting service for Git
- Enables collaboration

**Why use Git & GitHub?**
- Backup, history, teamwork

**Local vs Remote Workflow**:
```
Working Directory → Staging Area → Commit → Push to Remote
```

---

## Part 2 – Setting Up & Configurations (5 mins)
```bash
git --version
git config --global user.name "Your Name"
git config --global user.email "your.email@example.com"
git config --list
```

---

## Part 3 – Creating a Project & Repository (15 mins)

**Directory Structure:**
```
my_project/
    ├── README.md
    ├── src/
    │     └── main.py
    └── data/
          └── sample.txt
```

**Commands:**
```bash
mkdir my_project && cd my_project
echo "# My Project" > README.md
mkdir src data
echo "print('Hello World')" > src/main.py
echo "Sample data" > data/sample.txt

git init
git status
git add README.md src/main.py
git commit -m "Initial commit with README and main.py"
git add .
git commit -m "Added data/sample.txt"
```

---

## Part 4 – Viewing History & Changes (10 mins)
```bash
git log
git log --oneline --graph --decorate
git diff
git diff --staged
```

---

## Part 5 – Branching & Merging (20 mins)
```bash
git checkout -b feature-1
echo "print('Feature 1')" >> src/main.py
git add src/main.py
git commit -m "Added Feature 1"
git checkout main
git merge feature-1
git branch -d feature-1
```

---

## Part 6 – Working with GitHub (30 mins)
1. On GitHub, create a new repo (no README, license, .gitignore)
2. Link local repo:
```bash
git remote add origin https://github.com/<username>/<repo-name>.git
git branch -M main
git push -u origin main
```
3. Subsequent pushes:
```bash
git push
```
4. Clone existing repo:
```bash
git clone https://github.com/<username>/<repo-name>.git
```

---

## Part 7 – Collaboration & Pull Requests (15 mins)
```bash
git clone https://github.com/<your-username>/<repo>.git
git checkout -b bugfix-typo
# Make changes
git add .
git commit -m "Fixed typo in README"
git push origin bugfix-typo
```
- Create Pull Request on GitHub

---

## Part 8 – .gitignore & Best Practices (5 mins)

**Example .gitignore**:
```
__pycache__/
*.pyc
data/*.csv
```

```bash
echo "__pycache__/" > .gitignore
git add .gitignore
git commit -m "Added .gitignore"
```

---

## Part 9 – Undoing Mistakes
```bash
git restore file.txt
git reset HEAD file.txt
git revert <commit_hash>
```

---

## Final Flow Recap
1. `git init`
2. `git add`
3. `git commit`
4. `git branch` / `git checkout -b`
5. `git merge`
6. `git remote add origin`
7. `git push` / `git pull`
8. `.gitignore`
9. Pull Request workflow


---

## Additional Important Git Commands for Software Development

### 1. Viewing Commit History in Different Formats
```bash
git log --oneline                 # Compact view
git log --stat                    # Shows changes per file
git log -p                        # Shows patches (code changes)
git log --author="Name"           # Filter by author
```

### 2. Checking Status and Tracking
```bash
git status                        # Current repo status
git show <commit_hash>            # Show details of a commit
git shortlog                       # Summary of commits per author
```

### 3. Stashing Changes (Temporary Save)
```bash
git stash                         # Save uncommitted changes
git stash list                    # List stashes
git stash apply                   # Reapply last stash
git stash drop                    # Delete stash
git stash pop                     # Apply and remove stash
```

### 4. Tagging Versions (Releases)
```bash
git tag v1.0                      # Lightweight tag
git tag -a v1.0 -m "Version 1.0"  # Annotated tag
git push origin v1.0              # Push tag to remote
git tag                           # List tags
```

### 5. Resetting Commits (Use with Caution)
```bash
git reset --soft HEAD~1           # Undo last commit but keep changes staged
git reset --mixed HEAD~1          # Undo last commit and unstage changes
git reset --hard HEAD~1           # Completely remove last commit
```

### 6. Cherry-Picking Commits
```bash
git cherry-pick <commit_hash>     # Apply a specific commit from another branch
```

### 7. Pulling with Rebase
```bash
git pull --rebase                 # Avoid unnecessary merge commits
```

### 8. Checking Differences Between Branches
```bash
git diff branch1..branch2         # Show changes between branches
```

### 9. Cleaning Up Untracked Files
```bash
git clean -n                      # Dry run
git clean -f                      # Remove untracked files
```

### 10. Bisecting to Find Bugs
```bash
git bisect start
git bisect bad                    # Mark current commit as bad
git bisect good <commit_hash>     # Mark a commit as good
# Git will guide you to test commits and find where bug was introduced
git bisect reset
```

---

These commands help in **real-world software development** where you often need to debug, manage releases, handle partial changes, and collaborate effectively.
