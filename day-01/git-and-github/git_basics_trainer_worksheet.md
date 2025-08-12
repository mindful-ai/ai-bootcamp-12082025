# Git Basics Trainer Worksheet

## Exercise Goal
By the end of this exercise, you will:
- Initialize a Git repository
- Stage, commit, and view changes
- Explore commit history
- Create and merge branches
- Undo changes

---

## Step 1 – Initialize a Repository
**Command**
```bash
mkdir git_practice
cd git_practice
git init
```
**Expected Result**
```
Initialized empty Git repository in .../git_practice/.git/
```
**Trainer Tip:**  
This creates the `.git` folder where Git stores all history and metadata.

---

## Step 2 – Create Your First File and Commit
**Command**
```bash
echo "Hello Git" > file1.txt
git status
git add file1.txt
git commit -m "Initial commit with file1.txt"
```
**Expected Result**
- `git status` shows `file1.txt` as **new file** (untracked).
- Commit is saved with the message you provided.

---

## Step 3 – Modify and Commit Again
**Command**
```bash
echo "This is my second line" >> file1.txt
git diff
git add file1.txt
git commit -m "Added second line to file1.txt"
```
**Expected Result**
- `git diff` shows the added line starting with a `+`.
- A new commit appears in the history.

---

## Step 4 – Add Multiple Files
**Command**
```bash
echo "Some content" > file2.txt
echo "Another file" > file3.txt
git add .
git commit -m "Added file2.txt and file3.txt"
```
**Expected Result**
- All files are tracked in Git.
- Commit message appears in history.

---

## Step 5 – View Commit History
**Command**
```bash
git log
git log --oneline
git log --oneline --graph --decorate
```
**Expected Result**
- Full details with `git log`
- Compact list with `--oneline`
- Branch and merge visualization with `--graph`

---

## Step 6 – Branching and Switching
**Command**
```bash
git branch new-feature
git checkout new-feature
echo "Feature work" > feature.txt
git add feature.txt
git commit -m "Added feature.txt on new-feature branch"
```
**Expected Result**
- You are now on `new-feature` branch.
- Commit appears only in `new-feature` history.

---

## Step 7 – Merge a Branch
**Command**
```bash
git checkout main
git merge new-feature
```
**Expected Result**
- `feature.txt` is now part of the main branch.
- If there are no conflicts, you get a “Fast-forward” merge.

---

## Step 8 – View Changes Over Time
**Command**
```bash
git show
git diff HEAD~1 HEAD
```
**Expected Result**
- `git show` displays the latest commit changes.
- `git diff` between commits shows exactly what changed.

---

## Step 9 – Undo Changes
**Command**
```bash
echo "Temporary text" >> file1.txt
git restore file1.txt
```
**Expected Result**
- `file1.txt` is reverted to the last committed version.

---

## Step 10 – Cleanup
**Command**
```bash
git branch -d new-feature
git branch
```
**Expected Result**
- `new-feature` branch deleted.
- `git branch` shows only `main`.

---

✅ **End of Exercise**  
You have now learned:
- Initializing repositories
- Staging and committing
- Viewing history
- Branching and merging
- Undoing changes
