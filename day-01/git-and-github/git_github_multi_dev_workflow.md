# Git & GitHub Workshop – Multi-Developer + Tester Workflow (Python Project Example)

## Step 0 – Project Directory Structure
We’ll simulate a small Python web app project:

```
team_project/
├── src/
│   ├── app.py
│   ├── auth.py
│   └── utils.py
├── tests/
│   └── test_auth.py
├── requirements.txt
└── README.md
```

---

## Step 1 – Project Creation (Lead Developer)
```bash
# Create project folder
mkdir team_project && cd team_project

# Create subfolders
mkdir src tests

# Create files
echo "# Team Project" > README.md
echo "flask
pytest" > requirements.txt
echo "from flask import Flask
app = Flask(__name__)

@app.route('/')
def home():
    return 'Hello, World!'" > src/app.py
echo "def login(username, password):
    if not username or not password:
        return False
    return True" > src/auth.py
echo "def format_message(msg):
    return msg.strip().title()" > src/utils.py
echo "from src.auth import login

def test_login():
    assert login('user', 'pass') == True
    assert login('', '') == False" > tests/test_auth.py

# Initialize Git
git init
git add .
git commit -m "Initial commit with project structure"

# Push to GitHub
git remote add origin https://github.com/<org_or_username>/team_project.git
git branch -M main
git push -u origin main
```

---

## Step 2 – Create a `develop` Branch
```bash
git checkout -b develop
git push -u origin develop
```

---

## Step 3 – Developer Adds a New Feature
**Developer A** works on a login system enhancement:
```bash
git checkout develop
git pull
git checkout -b feature/login-system

# Modify src/auth.py
echo "\n# Added logging\nprint('Login attempted')" >> src/auth.py

git add src/auth.py
git commit -m "Enhanced login system with logging"
git push -u origin feature/login-system
```

**On GitHub**: Create Pull Request → target `develop` → request review.

---

## Step 4 – Code Review & Merge
**Reviewer**:
```bash
git fetch origin
git checkout feature/login-system
# Test the feature locally
pytest
```
Approve PR → Merge into `develop` (via GitHub or CLI):
```bash
git checkout develop
git pull
git merge --no-ff feature/login-system -m "Merge login feature"
git push origin develop
```

---

## Step 5 – Tester Creates a Release Branch
**Tester**:
```bash
git checkout develop
git pull
git checkout -b release/v1.0
git push -u origin release/v1.0
```
Run tests:
```bash
pytest
```
If bugs are found → create GitHub Issues.

---

## Step 6 – Bug Fix
**Developer B** fixes a crash:
```bash
git checkout develop
git pull
git checkout -b bugfix/login-crash

# Fix in src/auth.py
echo "# Fixed NoneType issue" >> src/auth.py

git add src/auth.py
git commit -m "Fixed crash when username/password is None"
git push -u origin bugfix/login-crash
```
PR → Merge into `develop`.

---

## Step 7 – Release to Production
**Lead Developer**:
```bash
git checkout main
git pull
git merge --no-ff release/v1.0 -m "Release v1.0 to production"
git push origin main

# Tag release
git tag -a v1.0 -m "Release v1.0"
git push origin v1.0
```

---

## Step 8 – Keeping Branches Updated
Developers should rebase frequently:
```bash
git checkout feature/some-feature
git fetch origin
git rebase origin/develop
```

---

## Step 9 – Useful Commands for Teams
- **Check who changed a line**:
```bash
git blame src/auth.py
```
- **Temporarily save work**:
```bash
git stash
git checkout develop
git stash pop
```
- **Clean up untracked files**:
```bash
git clean -f
```

---

## Branching Strategy Recap
```
main ────●─────────────●─────────────●──────
         \             \             \
develop   ●──●──●──●───●──●──●──●─────●────
           \  \  \  \    \  \  \  \
feature/   ●  ●  ●  ●    ●  ●  ●  ●
bugfix/             ●
release/                       ●
```

---

## Final Workflow Summary
1. **Developers**: Work on `feature/*` → PR → `develop`
2. **Testers**: Test `release/*` branches
3. **Bug fixes**: Go to `bugfix/*` → merge into `develop`
4. **Releases**: Merge `release/*` → `main`
5. **Tags**: Mark releases for tracking

---
