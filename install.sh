#!/bin/bash


echo "============================================="
echo " InstaLikeComBot Installer "
echo "============================================="
echo 

echo -n "Checking python installation: "
if [ ! -z "$(python3 --version)" ]; then echo [OK]; else echo [FAILED]; exit; fi

# declare -a dirs=(logs drivers/chrome drivers/firefox)
declare -a dirs=(logs)
echo "Creatings directories..."
for dir in ${dirs[@]}
do
  checkdir="$PWD/$dir"
  echo -n "Check $checkdir: "
  if [ -d $checkdir ]; then echo [EXISTS]; else mkdir -p "$checkdir"; echo [CREATED]; fi
done

echo -n "Creating python environment..."
env_status=$(python3 -m venv env)
if [ "$env_status" == "ensurepip is not available" ]
then 
  echo
  echo "Error: python3-venv missing. Run sudo apt install python3-venv"
  exit
fi

if [ ! -d "$PWD/env" ]; then echo Python environment creation failed; exit; fi
echo [OK]

echo -n "Activating python environment..."
source env/bin/activate
echo [OK]

echo "Installing packages..."
pip install -r requirements.txt
echo
echo "Finished installation successfully"
