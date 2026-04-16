# 1. Create the project structure
mkdir -p src/attacker src/gateway hardware docs media

# 2. Move your existing files into the new folders
mv attacker.ino src/attacker/
mv aegis_logic.py src/gateway/
mv research_reference.md docs/
mv parts.jpg media/
mv setup.jpg media/
mv hardware_mechnaism.csv hardware/parts_list.csv

# 3. Initialize Git
git init
git add .
git commit -m "Initial upload of Aegis Gateway project files"

# 4. Create the repo on GitHub and push everything
# (This creates a PUBLIC repo. Change --public to --private if you want it hidden)
gh repo create Aegis-Gateway --public --source=. --remote=origin --push