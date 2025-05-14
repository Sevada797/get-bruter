if [[ -z $(sudo apt list --installed 2>/dev/null | grep php) ]]; then
  echo "No PHP installed, run 'sudo apt install php' and try again :)"
else
  echo "Running test server on 127.0.0.1:8000"
  php -S 127.0.0.1:8000 -t ./
fi

