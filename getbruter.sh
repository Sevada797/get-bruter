#!/bin/bash
# getbruter.sh — defines the gbr() CLI

gbr() {
  local cmd="$1"
  shift

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
    de)
      python3 "$GETBRUTER_PATH/getbruter.py" --dynamit-enc "$@"
      ;;
    *)
      python3 "$GETBRUTER_PATH/getbruter.py" "$cmd" "$@"
      ;;
  esac
}



gbr2() {
  local cmd="$1"
  shift

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
    de)
      python3 "$GETBRUTER_PATH/getbruter2.py" --dynamit-enc "$@"
      ;;
    *)
      python3 "$GETBRUTER_PATH/getbruter2.py" "$cmd" "$@"
      ;;
  esac
}
