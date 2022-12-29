1. Install ZED-SDK (https://www.stereolabs.com/docs/installation/windows/#download-the-zed-sdk)
2. Download Python 3.7.9 (https://www.python.org/ftp/python/3.7.9/python-3.7.9-amd64.exe)
3. Clone this Repo 
4. Create python virtual env inside repo 
     -With PS/CMD cd into repo folder (cd C:\Users\...\ZED)
    - "python -m venv ." (If multiple python version are installed make sure you are using python3.7.9 +64 version)
5. Activate venv
    - With PS/CMD cd into repo folder (cd C:\Users\...\ZED)
    - Type ".\Scripts\activate" into PS/CMD and press ENTER
6. Install required python packages
    - (Make sure that python venv is active)
    - "pip install -r requirements.txt"
7. Install ZED Python API
    - (Make sure that python venv is active)
    - run "python get_python_api.py"
8. Run main.py 
    - with "python Zed/main.py" from repo root folder
