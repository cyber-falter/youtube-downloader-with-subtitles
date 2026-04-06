# 🎬 YouTube Video Downloader with Subtitles

A modern, professional desktop application for downloading YouTube videos with multiple quality options, subtitle support, and a beautiful GUI.

![Python](https://img.shields.io/badge/python-3.8+-blue.svg)
![License](https://img.shields.io/badge/license-MIT-green.svg)
![Platform](https://img.shields.io/badge/platform-Windows%20%7C%20macOS%20%7C%20Linux-lightgrey.svg)

## ✨ Features

- 🎥 **Multiple Quality Options** - Download in 360p, 720p, 1080p, 1440p, 4K (when available)
- 📊 **Detailed Info** - Shows resolution, frame rate, and file size for each quality
- 📝 **Subtitle Support** - Embed subtitles directly into the video
- 🎨 **Modern UI** - Clean, professional interface with dark and light themes
- 📈 **Real-time Progress** - Live progress bar with download speed and percentage
- 🗂️ **Custom Location** - Choose where to save your downloads
- 🧹 **Clean Downloads** - Automatically removes temporary files
- ⚡ **Fast & Reliable** - Uses pytubefix (works with 2025 YouTube API)

## 🖼️ Screenshots

### Dark Theme
Beautiful dark mode for comfortable viewing

### Light Theme  
Clean light mode for daytime use

## 📦 Installation

### Prerequisites

- **Python 3.8 or higher**
- **FFmpeg** (for merging high-quality videos and embedding subtitles)

### Step 1: Install Python Dependencies

```bash
pip install -r requirements.txt
```

### Step 2: Install FFmpeg

#### Windows
```bash
# Using Chocolatey
choco install ffmpeg

# OR download from:  https://www.gyan.dev/ffmpeg/builds/
# Extract and add to PATH
```

#### macOS
```bash
brew install ffmpeg
```

#### Linux (Ubuntu/Debian)
```bash
sudo apt update
sudo apt install ffmpeg
```

Verify FFmpeg installation:
```bash
ffmpeg -version
```

## 🚀 Usage

1. **Run the application:**
   ```bash
   python youtube_downloader.py
   ```

2. **Paste a YouTube URL** into the input field

3. **Click "Fetch Info"** to load video details and available qualities

4. **Select your desired quality** from the list (shows resolution, fps, and size)

5. **(Optional) Select subtitle language** to embed into the video

6. **Choose download location** (defaults to your Downloads folder)

7. **Click "Download Video"** and wait for completion! 

## 🎨 Themes

Toggle between dark and light themes using the theme button in the top-right corner: 
- **Dark Mode** 🌙 - Modern dark theme (default)
- **Light Mode** ☀️ - Clean light theme

## 📝 Quality Options Explained

### High Quality (Adaptive Streams)
- **1080p, 1440p, 2160p (4K)** - Best quality available
- Downloads video and audio separately, then merges them
- Takes slightly longer but provides superior quality

### Standard Quality (Progressive Streams)
- **360p, 480p, 720p** - Good quality, faster downloads
- Single file with built-in audio
- Marked with "(Standard)" label

## 🔧 Technical Details

### Libraries Used
- **pytubefix** - YouTube video downloading (2025 API compatible)
- **ttkbootstrap** - Modern UI components and themes
- **FFmpeg** - Video/audio merging and subtitle embedding
- **tkinter** - Base GUI framework

### File Handling
- Temp files are stored in system temp directory
- All temporary files are automatically cleaned up after download
- Final video is saved only to your chosen location
- No leftover files in Downloads folder

## 🐛 Troubleshooting

### "FFmpeg not found" Error
- Ensure FFmpeg is installed and in your system PATH
- Restart your terminal/command prompt after installation
- Test with: `ffmpeg -version`

### "HTTP Error 400: Bad Request"
- Update pytubefix:  `pip install --upgrade pytubefix`
- Check your internet connection
- Try a different video URL

### No Quality Options Available
- Video might be age-restricted or private
- Try a different video
- Update pytubefix to latest version

### Subtitle Embedding Fails
- Subtitle embedding is optional - video still downloads
- Check FFmpeg installation
- Some videos don't have subtitles available

## 📊 Supported Formats

- **Video:** MP4 (H.264)
- **Audio:** AAC
- **Subtitles:** SRT (embedded as hardcoded)

## ⚖️ Legal Notice

This tool is for **personal use only**. Please respect: 
- YouTube's Terms of Service
- Copyright laws
- Content creators' rights

Only download videos you have permission to download.

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## 📄 License

MIT License - Feel free to use and modify! 

## 🙏 Credits

- **pytubefix** - For maintaining YouTube download functionality
- **ttkbootstrap** - For beautiful modern UI components
- **FFmpeg** - For video processing capabilities

## 📧 Support

If you encounter issues:
1. Check the Troubleshooting section
2. Ensure all dependencies are installed
3. Update to the latest version:  `pip install --upgrade pytubefix ttkbootstrap`

---

**Made with ❤️ for the YouTube downloading community**
