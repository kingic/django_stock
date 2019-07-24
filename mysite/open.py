import webbrowser


"""
web browser opener.
command : pyinstaller --noconsole --onefile --icon=path/to/icon.ico open.py
"""

def main():
    url = 'http://localhost:8080/polls/stock'
    chrome_path = 'C:/Program Files (x86)/Google/Chrome/Application/chrome.exe %s'
    webbrowser.get(chrome_path).open(url)


if __name__ == '__main__':
    main()
