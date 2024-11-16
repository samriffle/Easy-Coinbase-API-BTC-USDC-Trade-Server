Prerequisite Installs
1) pip install pyinstaller
2) pip install coinbase-advancedtrade-python

Prerequisite Setup (Windows)
1) Visit https://www.coinbase.com/settings/api
2) Click the Create API Key button on the top right side of the window.
3) Give your key a name and select any portfolio that you want (I used the default). Tick the view, trade, and transfer permission boxes.
4) Fill in the IP whitelist with your external IP for security purposes, or leave it blank if you do not need the extra layer of protection.
5) Click the Create and Download button, which will save your cdp_api_key.json file
6) Open cmd(admin) and navigate to the directory server.py is in
7) pyinstaller --onefile server.py
9) Find and move cdp_api_key.json to the newly generated dist directory
10) Run the .exe

Notes
1) This program is designed to me interrupted by human input. It facilitates easy trades hourly, but it is not automated.
2) This is a hobby project, so if you have more suggestions on how to improve the algorithm please let me know! Ill try to commit updates I make as I get to them.

Credits
1) https://github.com/rhettre/coinbase-advancedtrade-python
2) https://github.com/samchaaa/simple_btc_algo/tree/main
