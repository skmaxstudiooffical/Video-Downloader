# 🚀 Advanced Video Downloader With Python

![Python Version](https://img.shields.io/badge/python-3.8%2B-blue)
![License](https://img.shields.io/badge/license-Apache%202.0-blue)
![Dependencies](https://img.shields.io/badge/dependencies-requests%20tqdm-orange)

A professional-grade video downloader with enterprise-level features for content preservation and media archiving. Built for reliability and recovery handling.

## 🌟 Features <a name="-features"></a>

| Category              | Capabilities                                                                 |
|-----------------------|-----------------------------------------------------------------------------|
| **Network**           | HTTPS/TLS 1.2+, Auto-redirect handling, Chunked transfers (1MB blocks)      |
| **Metadata**          | Content-Disposition parsing, MIME type detection, URL fallback naming       |
| **Safety**            | 3-level filename sanitization, Duplicate prevention, Size validation       |
| **Performance**       | Session reuse, Connection pooling, Parallel-ready structure                |
| **UI/UX**             | Interactive input, Colorized progress bars, Post-download verification     |

## 🛠️ Installation <a name="-installation"></a>

### Base requirements
```
pip install requests tqdm
```

## 🖥️ Usage <a name="-usage"></a>
Basic Operation:
```
python main.py
```

## 🔄 Video URL Input Mode
──────────────────────────

• Enter one URL per line

• Type 'e' when finished

• Press Enter after each URL

──────────────────────────
```
Enter URL 1 (or 'e' to start download): https://example.com/video.mp4
```
✅ URL 1 added
```
Enter URL 2 (or 'e' to start download): e
```

```
📋 URLs to download:
 1. https://example.com/video.mp4

🚀 Starting download of 1 videos...

📥 Downloading 1/1
   URL: https://cdn.example/streaming.php?id=123
✅ Success: /content/videos/streaming_123_1.mp4
```


Copyright (c) 2025 [@skmaxstudioofficial]
