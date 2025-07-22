#!/bin/bash
# setup.sh — sets up GetBruter environment

echo -e "\n🐍 Starting GetBruter setup..."

# Determine which shell config file to use
SHELL_NAME=$(basename "$SHELL")
if [ "$SHELL_NAME" = "zsh" ]; then
    RC_FILE="$HOME/.zshrc"
elif [ "$SHELL_NAME" = "bash" ]; then
    RC_FILE="$HOME/.bashrc"
else
    # Default fallback to bash
    RC_FILE="$HOME/.bashrc"
fi

# Only add if not already present
if ! grep -q "GETBRUTER_PATH" "$RC_FILE"; then
    echo -e "\n## GetBruter setup 🐍" >> "$RC_FILE"
    echo "export GETBRUTER_PATH=\"$(pwd)\"" >> "$RC_FILE"
    echo "source \"\$GETBRUTER_PATH/getbruter.sh\"" >> "$RC_FILE"
    echo "✅ GetBruter config added to $RC_FILE"
else
    echo "ℹ️ GetBruter already configured in $RC_FILE"
fi

echo -e "\n✅ Setup done!"
echo "🔁 Reload your shell or run: source $RC_FILE"
echo "📟 To use, type: gbr"

