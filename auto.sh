# 1. Stage all your current changes
git add .

# 2. Commit them locally with a message
git commit -m "build: organize project structure and update documentation"

# 3. Now pull the remote changes (the LICENSE we added via gh)
git pull --rebase origin main

# 4. Finally, push everything back to GitHub
git push origin main