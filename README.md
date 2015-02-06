# pyhpoa
A python script which automates firmware upgrades to a large number of HP Blade System Onboard Administrator modules.

The program has a self contained FTP server whch can serve update files from the directory outlined in the config file.

The program relies on paramiko for SSH connections and pyftpdlib for serving files.
