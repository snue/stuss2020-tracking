#!/bin/bash

# No screen blanking / display power management
xset s noblank
xset s off
xset -dpms

# No chromium crash notifications
sed -i 's/"exited_cleanly":false/"exited_cleanly":true/' /home/pi/.config/chromium/Default/Preferences
sed -i 's/"exit_type":"Crashed"/"exit_type":"Normal"/' /home/pi/.config/chromium/Default/Preferences

# launch chromium in kiosk mode
/usr/bin/chromium-browser --noerrdialogs --disable-infobars --kiosk https://localhost:5000 https://localhost:19999 &

