import network
import urequests
import badger2040
import ujson
import os


# url = 'http://192.168.4.143:8000/response_news.json'
url = 'https://tomwhitwell.github.io/dad_poems/response_news.json'

# Initialize the Badger2040
badger = badger2040.Badger2040()
badger.set_pen(15)
badger.clear()
badger.led(5)
badger.set_update_speed(1)

def file_exists(filename):
    try:
        with open(filename, 'r'):
            return True
    except OSError:
        return False


# Function to save JSON data to a file
def save_json_data(url, filename):
    response = urequests.get(url)
    if response.status_code == 200:
        with open(filename, 'w') as file:
            file.write(response.text)
        return "JSON saved successfully"
    else:
        return "Failed to download JSON"

# Function to read JSON data from a file
def read_json_data(filename):
    try:
        with open(filename, 'r') as file:
            json_data = ujson.loads(file.read())
            poet = json_data.get('poet', 'Unknown poet')
            mood = json_data.get('mode', 'unknown mood')
            news = json_data.get('news', 'did something unrecorded')
            return f"A poem by {poet} in a {mood} mood about:\n\n{news}"
    except OSError:
        return "Failed to read JSON file"



# Function to read WiFi configuration
def read_wifi_config():
    try:
        with open('WIFI_CONFIG.py', 'r') as file:
            config = {}
            exec(file.read(), config)
            return config
    except OSError:
        return None

# Connect to WiFi
def connect_wifi(ssid, psk):
    badger.set_pen(15)
    badger.clear()
    badger.set_pen(0)
    badger.set_font("bitmap8")
    badger.text("Connecting to " + ssid, 2, 60, scale=1)
    badger.update()

    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    wlan.connect(ssid, psk)
    while not wlan.isconnected():
        pass
    badger.set_pen(15)
    badger.clear()
    badger.set_pen(0)
    return wlan

# Download JSON and extract message
def download_and_extract_poem(url):
    response = urequests.get(url)
    if response.status_code == 200:
        json_data = ujson.loads(response.text)
        return json_data.get('poem', 'No message found')
    else:
        return "Failed to download JSON"

# Download the news background and prompt information 
def download_and_extract_context(url):
    response = urequests.get(url)
    if response.status_code == 200:
        json_data = ujson.loads(response.text)
        poet = json_data.get('poet', 'Unknown poet')
        mood = json_data.get('mode', 'unknown mood')
        news = json_data.get('news', 'did something unrecorded')
        return f"A poem by {poet} in a {mood} mood about:\n\n{news}"
    else:
        return "Failed to download JSON"


def extract_poem(filename, remove_first_n_lines=0):
    try:
        with open(filename, 'r') as file:
            json_data = ujson.loads(file.read())
            poem = json_data.get('poem', 'No message found')
            if remove_first_n_lines > 0:
                poem_lines = poem.split('\n')
                poem = '\n'.join(poem_lines[remove_first_n_lines:])
            return poem
    except OSError:
        return "Failed to read JSON file"


def extract_context(filename):
    try:
        with open(filename, 'r') as file:
            json_data = ujson.loads(file.read())
            poet = json_data.get('poet', 'Unknown poet')
            mood = json_data.get('mode', 'unknown mood')  
            news = json_data.get('news', 'did something unrecorded')
            return f"A poem by {poet} in a {mood} mood about:\n\n{news}"
    except OSError:
        return "Failed to read JSON file"

# Function to add line breaks every 60 characters, preserving existing line breaks
def add_line_breaks(text, line_length=60):
    lines = []
    for paragraph in text.split('\n'):
        words = paragraph.split()
        current_line = ''
        for word in words:
            if len(current_line) + len(word) <= line_length:
                current_line += word + ' '
            else:
                lines.append(current_line.rstrip())
                current_line = word + ' '
        lines.append(current_line.rstrip())
    return '\n'.join(lines)

def remove_special_characters(text):
    return ''.join(char for char in text if ord(char) < 128)

# Main script
config = read_wifi_config()
if config:
    badger.set_pen(0)
    badger.set_font("bitmap8")
    y = 2

    json_filename = 'response_news.json'
    if not file_exists(json_filename):
        wlan = connect_wifi(config['SSID'], config['PSK'])
        save_message = save_json_data(url, json_filename)
        # Handle save_message as needed

    if badger2040.woken_by_rtc() or badger2040.pressed_to_wake_get_once(15):
        wlan = connect_wifi(config['SSID'], config['PSK'])
        save_message = save_json_data(url, json_filename)
        badger.text("Explain", 235, 120, scale=1)

    if badger2040.pressed_to_wake_get_once(14):
        message = extract_context(json_filename)
        badger.text("Back", 35, 120, scale=1)
    elif badger2040.pressed_to_wake_get_once(13):
        import badger_os
        badger_os.launch('examples/qrgen.py')
    elif badger2040.pressed_to_wake_get_once(11):
        message = extract_poem(json_filename, remove_first_n_lines=8)
        badger.text("Explain", 235, 120, scale=1)
        badger.text("Back", 35, 120, scale=1)

    else:  
        message = extract_poem(json_filename)
        badger.text("Explain", 235, 120, scale=1)

    clean_message = remove_special_characters(message)
    formatted_message = add_line_breaks(clean_message)
    # Display the formatted message
    for line in formatted_message.split('\n'):
        badger.text(line, 2, y, scale=1)
        y += 11  # Adjust this value based on your font size and display
    if y > 123:
        badger.text("MORE>", 270, 92, scale=1)
    badger.update()
    

else:
    badger.set_pen(0)
    badger.text("WiFi config not found", 2, 2, scale=1)
    badger.update()

badger.led(0)
#badger2040.turn_off()
badger2040.sleep_for(25)


