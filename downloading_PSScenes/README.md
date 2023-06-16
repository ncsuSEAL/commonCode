# Walkthrough of downloading Planet imagery
#### Last edited June 16, 2023
#### Editors: Izzi

## Step 1: Create a virtual environment and install the Planet SDK for Python
NOTE: You need to be using Python3 for this.
If you don't have the Planet SDK: 
1. In your terminal, type: `python3 -m venv ~/.venv/planet-v2`
2. Then, type `source ~/.venv/planet-v2/bin/activate` to activate the virtual environment
3. Type `pip install planet --pre` to install the Planet SDK in the virtual environment
4. Type `planet --version` to ensure that you have installed version 2 of the SDK
5. Type `planet auth init` to sign on to your Planet account, entering the email and password of your Planet account when prompted. It should say "Initialized" once you have logged in.
6. Find your authentication key with: `planet auth value`, and optionally save it as an environment variable with `export PL_API_KEY=<your api key>`. Check that it worked with `echo $PL_API_KEY`

You now have access to Planet's SDK. See all commands with `planet --help`, but the ones I use most are: 
- `auth` for working with Planet authentication (like we did to log in on step 5 above)
- `data` for interacting with the Data API
- `orders` for interacting with the Orders API

This is the tl;dr version; find Planet's more thorough walkthrough [here](https://planet-sdk-for-python-v2.readthedocs.io/en/latest/get-started/quick-start-guide/#step-1-install-python-37-and-a-virtual-environment).
