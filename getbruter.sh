#!/bin/bash
# getbruter.sh — defines the gbr() CLI

gbr() {
  local cmd="$1"
  shift

if [[ "$cmd" -eq "-h" || "$cmd" -eq "--help" ]]
then
echo "Usage: gbr [d, di, dc, ssti] [<urls_file>]"
echo ""
echo "INFO: all these are for working with parameters and their reflections mostly"
echo "INFO: You can not give 2nd arg, and input will be asked, but for automations you should prefer passing file as argument"
echo ""
echo "d - find reflections count for each param"
echo "di - inject \",',< and check escaping, for each risk is being +=1 from 0 (XSS finder helper)"
echo "dc - visit all given URLs, and check which params set cookies (handy in 2nd order XSS research, or in other cases...)"
echo "ssti - visit all urls, inject SSTI polyglot -> check for refections (RARE imo, but still)"
echo ""
echo "NOTE: gbr2 is for not following redirects ... (may later add all in one)"
return
fi

  case "$cmd" in
    d)
      python3 "$GETBRUTER_PATH/getbruter.py" --dynamit "$@"
      ;;
    dc)
      python3 "$GETBRUTER_PATH/getbruter.py" --dynamit-cookies "$@"
      ;;
    di)
      python3 "$GETBRUTER_PATH/getbruter.py" --dynamit-inject "$@"
      ;;
    ssti)
      python3 "$GETBRUTER_PATH/getbruter.py" --dynamit-ssti "$@"
      ;;
    *)
      python3 "$GETBRUTER_PATH/getbruter.py" "$cmd" "$@"
      ;;
  esac
}



gbr2() {
  local cmd="$1"
  shift

if [[ "$cmd" -eq "-h" || "$cmd" -eq "--help" ]]
then
echo "Check gbr -h, same works here"
return
fi

  case "$cmd" in
    d)
      python3 "$GETBRUTER_PATH/getbruter2.py" --dynamit "$@"
      ;;
    dc)
      python3 "$GETBRUTER_PATH/getbruter2.py" --dynamit-cookies "$@"
      ;;
    di)
      python3 "$GETBRUTER_PATH/getbruter2.py" --dynamit-inject "$@"
      ;;
    ssti)
      python3 "$GETBRUTER_PATH/getbruter2.py" --dynamit-ssti "$@"
      ;;
    *)
      python3 "$GETBRUTER_PATH/getbruter2.py" "$cmd" "$@"
      ;;
  esac
}
