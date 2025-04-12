import requests
import os
import re
from tqdm import tqdm
from urllib.parse import unquote
import mimetypes

def sanitize_filename(filename):
    """Clean filename from special characters and URL encoding"""
    filename = unquote(filename)
    filename = re.sub(r'[\\/*?:"<>|]', '', filename)
    return filename.strip()

def get_extension_from_content_type(content_type):
    """Map content types to file extensions"""
    type_map = {
        'video/mp4': '.mp4',
        'video/x-matroska': '.mkv',
        'video/webm': '.webm',
        'video/quicktime': '.mov',
        'video/mpeg': '.mpeg',
    }
    return type_map.get(content_type.split(';')[0], mimetypes.guess_extension(content_type) or '.bin')

def get_valid_filename(headers, url):
    """Extract filename from headers or URL with proper extension"""
    content_disp = headers.get('Content-Disposition', '')
    if content_disp:
        fnames = re.findall(r'filename\*?="?(.+?)"?(;|$)', content_disp)
        if fnames:
            filename = fnames[0][0].split("''")[-1]
            filename = sanitize_filename(filename)
            if '.' in filename:
                return filename

    url_path = url.split('?')[0].split('#')[0]
    filename = os.path.basename(url_path)
    filename = sanitize_filename(filename)

    if '.' not in filename:
        content_type = headers.get('Content-Type', 'application/octet-stream')
        extension = get_extension_from_content_type(content_type)
        filename += extension

    return filename

def download_video(url, save_dir='/content/videos'):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
        'Referer': 'https://www.google.com/'
    }

    try:
        with requests.Session() as session:
            response = session.head(url, headers=headers, allow_redirects=True, timeout=10)
            response.raise_for_status()
            
            final_url = response.url
            content_type = response.headers.get('Content-Type', 'application/octet-stream')
            
            filename = get_valid_filename(response.headers, final_url)
            
            os.makedirs(save_dir, exist_ok=True)
            save_path = os.path.join(save_dir, filename)
            
            counter = 1
            base, ext = os.path.splitext(filename)
            while os.path.exists(save_path):
                new_filename = f"{base}_{counter}{ext}"
                save_path = os.path.join(save_dir, new_filename)
                counter += 1
            
            response = session.get(final_url, headers=headers, stream=True, timeout=20)
            response.raise_for_status()
            
            total_size = int(response.headers.get('content-length', 0))
            
            with open(save_path, 'wb') as f, tqdm(
                total=total_size,
                unit='iB',
                unit_scale=True,
                desc=filename[:40],
                bar_format='{l_bar}{bar}| {n_fmt}/{total_fmt} [{elapsed}<{remaining}, {rate_fmt}]'
            ) as bar:
                for chunk in response.iter_content(chunk_size=1024*1024):
                    if chunk:
                        f.write(chunk)
                        bar.update(len(chunk))
            
            if total_size != 0 and os.path.getsize(save_path) != total_size:
                raise RuntimeError("File size mismatch - download incomplete")
            
            return save_path

    except Exception as e:
        print(f"\n❌ Error downloading {url}: {str(e)}")
        return None

# Interactive URL input
print("""
🔄 Video URL Input Mode
──────────────────────────
• Enter one URL per line
• Type 'e' when finished
• Press Enter after each URL
──────────────────────────
""")

video_urls = []
while True:
    url = input(f"Enter URL {len(video_urls)+1} (or 'e' to start download): ").strip()
    
    if url.lower() == 'e':
        break
        
    if url:
        # Basic URL validation
        if url.startswith(('http://', 'https://')):
            video_urls.append(url)
            print(f"✅ URL {len(video_urls)} added")
        else:
            print("⚠️ Invalid URL - must start with http:// or https://")
    else:
        print("⚠️ Empty input - please enter a valid URL or 'e'")

# Check if any URLs were entered
if not video_urls:
    print("\n❌ No URLs entered - exiting program")
    exit()

# Show confirmation
print("\n📋 URLs to download:")
for i, url in enumerate(video_urls, 1):
    print(f"{i:2}. {url}")

# Start downloading
download_dir = "/content/videos"
print(f"\n🚀 Starting download of {len(video_urls)} videos...\n")

successful = []
failed = []

for index, url in enumerate(video_urls, 1):
    print(f"📥 Downloading {index}/{len(video_urls)}")
    print(f"   URL: {url}")
    saved_file = download_video(url, download_dir)
    
    if saved_file:
        print(f"✅ Success: {saved_file}\n")
        successful.append((url, saved_file))
    else:
        print(f"❌ Failed: {url}\n")
        failed.append(url)

# Show final report
print("\n🔥 Download Summary")
print(f"──────────────────────────")
print(f"• Total URLs: {len(video_urls)}")
print(f"• Successful: {len(successful)}")
print(f"• Failed:     {len(failed)}")
print(f"──────────────────────────")

if successful:
    print("\n📁 Successfully downloaded files:")
    for url, path in successful:
        print(f"• {os.path.basename(path)}")
        print(f"  Source: {url}")
        print(f"  Path: {path}\n")

if failed:
    print("\n❌ Failed downloads:")
    for url in failed:
        print(f"• {url}")

print(f"\n📂 All files are saved in: {download_dir}")
print("👉 Access them from Colab's file browser (left panel)")
