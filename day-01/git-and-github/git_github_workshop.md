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
