echo -e "\n## Get-Bruter setup 🐍
gbr() {
  if [ \"\$1\" == \"d\" ]; then
    shift
    python3 $(pwd)/getbruter.py --dynamit \"\$@\"
  elif [ \"\$1\" == \"dc\" ]; then
    shift
    python3 $(pwd)/getbruter.py --dynamit-cookies \"\$@\"
  else
    python3 $(pwd)/getbruter.py \"\$@\"
  fi
}
export GETBRUTER_PATH=$(pwd)
# 📟 To use, type: gbr
" >> ~/.bashrc && echo -e "\n✅ Setup done! Reload shell or run: source ~/.bashrc" && echo "📟 To use, type: gbr"
