# darkboss1bd-perosnal-nmap-scaner
All Network Scaner Type Tools 

Tool to use Personal Nmap, in Flask with different types of scans Woldwide. 👁

[![Contact Me ](https://i.ibb.co.com/Ps8YMDVL/personal-nmap.png)](https://t.me/darkvaiadmin)



> **The project is open to partners.**

# SUPPORTED DISTRIBUTIONS
|Distribution | Version Check | supported | status |
----------|-------|------|-------|
|Kali Linux| 2025.2| yes| working   |
|Parrot Security OS| 6.0| yes | working   |
|Windows| 11 | yes | working   |
|BackBox| 8.1 | yes | working   |
|Arch Linux| 2024.06.01 | yes | working   |

[![Website Visit ](https://i.ibb.co.com/V0Kvyh1T/ter.png)](https://serialkey.top/)

# Root privileges:
To run some types of advanced scans with Nmap (such as -sS, -O, -A), sudo is required. Make sure that the user running the application has the necessary permissions or configure sudo to not prompt for a password when running Nmap (this should be done with caution).

# System Settings:
Sudo permissions without password (optional): If you want to prevent Flask from requesting the sudo password when running certain scans, you can configure sudo to allow the user to run nmap without a password:
```
sudo nano
```

# Solutions:
Run the program as sudo: Since the Flask application is running the Nmap command and it needs root permissions, a straightforward solution is to run Flask with sudo:

## Example:
```
sudo python3 darkboss1bd-perosnal-nmap-scaner.py
```

However, this is not the most secure solution, especially in a production environment. If you decide to use this method, make sure it is only enabled in controlled environments.

Assign specific permissions to Nmap using setcap: If you want to avoid running the entire Flask script with sudo, you can grant specific permissions to Nmap to run without needing root permissions for certain scans:
```
sudo setcap cap_net_raw,cap_net_admin,cap_net_bind_service+eip $(which nmap)
```
# USAGE
```
git clone https://github.com/darkboss1bd/darkboss1bd-perosnal-nmap-scaner.git
```
```
cd darkboss1bd-perosnal-nmap-scaner
```
```
python3 darkboss1bd-perosnal-nmap-scaner.py
```
# REQUIREMENTS
```
pip install -r requirements.txt
```
# SUPPORT
Questions, bugs or suggestions to : darkboss1bd@gmail.com


We need partners and sponsors, if you're interested in support or help contact.

