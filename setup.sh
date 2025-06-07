#!/bin/bash
# setup.sh — sets up GetBruter environment

echo -e "\n## GetBruter setup 🐍" >> ~/.bashrc
echo "export GETBRUTER_PATH=\"$(pwd)\"" >> ~/.bashrc
echo "source \"\$GETBRUTER_PATH/getbruter.sh\"" >> ~/.bashrc

echo -e "\n✅ Setup done!"
echo "🔁 Reload shell or run: source ~/.bashrc"
echo "📟 To use, type: gbr"
