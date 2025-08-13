
# How to Create a Pull Request on GitHub

## 1. Fork or Clone the Repository
- **If you don't own the repository**: Fork it from GitHub.
- **If you own or have access**: Clone it locally.

```bash
git clone https://github.com/username/repo-name.git
cd repo-name
```

---

## 2. Create a New Branch
Never work directly on `main` for PRs.

```bash
git checkout -b feature/my-new-feature
```

---

## 3. Make Your Changes
- Edit or add files.
- Stage your changes:

```bash
git add .
```

- Commit your changes:

```bash
git commit -m "Add new feature: description"
```

---

## 4. Push the Branch to GitHub
```bash
git push origin feature/my-new-feature
```

---

## 5. Create the Pull Request on GitHub
1. Go to your repository on GitHub.
2. You’ll see a **Compare & pull request** button for your branch — click it.
3. Fill in:
   - **Title** (short description)
   - **Description** (why and what you changed)
4. Select the **base branch** (usually `main`) and the **compare branch** (your feature branch).
5. Click **Create pull request**.

---

## 6. Collaborate & Merge
- Review feedback from maintainers.
- Update your branch if needed.
- Once approved, merge the PR into the base branch.

---

## Pro Tips
- Keep PRs **small and focused**.
- Sync with the base branch before opening the PR:

```bash
git fetch origin
git checkout main
git pull origin main
git checkout feature/my-new-feature
git rebase main
```

---

**References:**
- [GitHub Pull Requests Documentation](https://docs.github.com/pull-requests)
