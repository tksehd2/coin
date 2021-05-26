git reset --hard
git pull

sudo systemctl stop coin_notify
sudo systemctl start coin_notify
sudo systemctl status coin_notify
