import requests
import os

# Create sounds directory if it doesn't exist
if not os.path.exists('sounds'):
    os.makedirs('sounds')

# Download a cheerful children's music track
url = "https://www.bensound.com/royalty-free-music/download/ukulele-background"
music_file = "sounds/ukulele_background.mp3"

print(f"Downloading music from {url}")
response = requests.get(url)

if response.status_code == 200:
    with open(music_file, 'wb') as f:
        f.write(response.content)
    print(f"Successfully downloaded music to {music_file}")
else:
    print(f"Failed to download music. Status code: {response.status_code}")
