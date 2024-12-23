# Getting started with Python

## Python Dependencies
Starting with Debian 12.X(Bookworm) and newer Linux Distros, it's best to use a venv (Virtual Environment for Python due to PEP-668 issue)'
Install Python dependencies needed for the scripts using:
`sudo apt install python3-pip python3.11-venv`

Install a Python virtual environment:
`python3 -m venv ~/.venv/my-venv`

Load the venv: `source ~/.venv/my-venv/bin/activate`

NB: Adjust `my-venv` to anything you prefer.

## Running Python scripts with Virtual Environments
Several options
1. Load the venv and then run the script using the `python` interpreter as follows:
   1. Load the venv:
      ```commandline
      source ~/.venv/my-venv/bin/activate
      ```
   2. Run the script:
      ```commandline
      python my_script.py
      ```
2. Add a shebang statement and make the script executable on it's own:
   1. Shebang example:
      ```commandline
      #!/home/kkiragu/.venv/my-venv/bin/python3
      ```
   2. Make the python script executable:
      ```commandline
      chmod +x my_script.py
      ```
   3. Run the script without explicitly indicating the `python` interpreter as follows:
      ```commandline
      ./my_script.py
      ```

