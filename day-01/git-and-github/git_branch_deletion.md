# Managing and Deleting Branches in Git & GitHub

When you merge a branch in GitHub, the branch will **still exist** unless you explicitly delete it.  
Keeping old branches around can clutter the repository and confuse team members.

---

## 1. Delete Branch on GitHub (Web UI)
After merging a Pull Request (PR), GitHub shows a **"Delete branch"** button on the PR page.

If you missed that:
1. Go to the **"Branches"** tab in your GitHub repo.
2. Find the branch you want to delete.
3. Click the **trash can icon** next to it to delete.

---

## 2. Delete Branch via Git CLI

### Delete remote branch:
```bash
git push origin --delete my-feature-branch
```

### Delete local branch:
```bash
git branch -d my-feature-branch        # Safe delete (only if merged)
git branch -D my-feature-branch        # Force delete (even if unmerged)
```

---

## 3. Automatic Branch Deletion in GitHub

To keep your repo clean:
1. Go to **Repository Settings** → **General**.
2. Scroll to **Merge button** section.
3. Enable **"Automatically delete head branches"** after PR merge.

---

## Best Practices for Teams
- Enable **automatic branch deletion** in GitHub settings.
- Delete local branches after merge to keep `git branch` output clean.
- Keep long-lived branches only for `main`, `develop`, and release branches.
