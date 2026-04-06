import tkinter as tk
from tkinter import filedialog, messagebox
import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from pytubefix import YouTube
import threading
import os
import subprocess
from pathlib import Path
import re
import tempfile

class YouTubeDownloader:  
    def __init__(self, root):
        self.root = root
        self.root.title("YouTube Downloader")
        self.root.geometry("950x720")
        self.root.minsize(850, 650)
        
        # Variables
        self.url_var = tk.StringVar()
        self.download_path = tk.StringVar(value=str(Path.home() / "Downloads"))
        self.current_yt = None
        self.quality_options = {}
        self.subtitle_languages = {}
        self. selected_subtitle = tk.StringVar(value="None")
        self.is_downloading = False
        self.download_cancelled = False
        self.current_theme = tk.StringVar(value="darkly")
        
        # Temp file tracking
        self.temp_files = []
        
        # Setup GUI
        self.setup_ui()
        
    def setup_ui(self):
        """Create the main user interface"""
        # Main container with padding
        main_frame = ttk.Frame(self.root, padding=20)
        main_frame. pack(fill=BOTH, expand=YES)
        
        # ===== HEADER WITH THEME TOGGLE =====
        header_frame = ttk.Frame(main_frame)
        header_frame.pack(fill=X, pady=(0, 20))
        
        header = ttk.Label(header_frame, text="🎬 YouTube Downloader", 
                          font=("Segoe UI", 18, "bold"))
        header.pack(side=LEFT)
        
        # Theme toggle button
        self.theme_btn = ttk.Button(
            header_frame, 
            text="☀️ Light Mode", 
            command=self. toggle_theme,
            bootstyle="secondary-outline",
            width=15
        )
        self.theme_btn.pack(side=RIGHT)
        
        # ===== URL INPUT SECTION =====
        url_frame = ttk.Frame(main_frame)
        url_frame.pack(fill=X, pady=(0, 15))
        
        ttk. Label(url_frame, text="Video URL", font=("Segoe UI", 10, "bold")).pack(anchor=tk.W, pady=(0, 5))
        
        url_input_frame = ttk.Frame(url_frame)
        url_input_frame.pack(fill=X)
        
        url_entry = ttk.Entry(url_input_frame, textvariable=self.url_var, 
                             font=("Segoe UI", 11))
        url_entry.pack(side=LEFT, fill=X, expand=YES, padx=(0, 10))
        
        fetch_btn = ttk.Button(url_input_frame, text="Fetch Info", 
                               command=self.fetch_video_info, 
                               bootstyle="primary",
                               width=15)
        fetch_btn.pack(side=LEFT)
        
        # ===== VIDEO INFO SECTION =====
        info_frame = ttk.Frame(main_frame)
        info_frame.pack(fill=X, pady=(0, 15))
        
        ttk.Label(info_frame, text="Video Information", 
                 font=("Segoe UI", 10, "bold")).pack(anchor=tk.W, pady=(0, 5))
        
        # Info container
        info_container = ttk.Frame(info_frame, bootstyle="secondary")
        info_container.pack(fill=X)
        
        self.info_text = tk.Text(info_container, height=4, wrap=tk.WORD, 
                                font=("Segoe UI", 10),
                                relief=tk.FLAT, 
                                state=tk.DISABLED,
                                padx=15, pady=10)
        self.info_text.pack(fill=BOTH, expand=YES)
        self.update_info_text_colors()
        
        # ===== QUALITY SELECTION SECTION =====
        quality_frame = ttk.Frame(main_frame)
        quality_frame.pack(fill=BOTH, expand=YES, pady=(0, 15))
        
        ttk.Label(quality_frame, text="Select Quality", 
                 font=("Segoe UI", 10, "bold")).pack(anchor=tk.W, pady=(0, 5))
        
        # Quality listbox with scrollbar
        list_container = ttk.Frame(quality_frame)
        list_container.pack(fill=BOTH, expand=YES)
        
        scrollbar = ttk.Scrollbar(list_container, bootstyle="primary-round")
        scrollbar.pack(side=RIGHT, fill=Y, padx=(5, 0))
        
        self.quality_listbox = tk.Listbox(
            list_container, 
            font=("Segoe UI", 11),
            yscrollcommand=scrollbar.set,
            selectmode=tk.SINGLE, 
            height=8,
            relief=tk.FLAT,
            highlightthickness=0,
            activestyle='none',
            borderwidth=0
        )
        self.quality_listbox.pack(side=LEFT, fill=BOTH, expand=YES)
        scrollbar.config(command=self. quality_listbox.yview)
        self.update_listbox_colors()
        
        # ===== SUBTITLE AND PATH IN TWO COLUMNS =====
        options_frame = ttk.Frame(main_frame)
        options_frame.pack(fill=X, pady=(0, 15))
        
        # Left column - Subtitles
        subtitle_frame = ttk.Frame(options_frame)
        subtitle_frame.pack(side=LEFT, fill=X, expand=YES, padx=(0, 10))
        
        ttk. Label(subtitle_frame, text="Subtitles (Embedded)", 
                 font=("Segoe UI", 10, "bold")).pack(anchor=tk.W, pady=(0, 5))
        
        self.subtitle_combo = ttk.Combobox(
            subtitle_frame, 
            textvariable=self.selected_subtitle,
            state="readonly", 
            font=("Segoe UI", 10)
        )
        self.subtitle_combo.pack(fill=X)
        self.subtitle_combo['values'] = ["None"]
        self.subtitle_combo. current(0)
        
        # Right column - Download Path
        path_frame = ttk.Frame(options_frame)
        path_frame.pack(side=LEFT, fill=X, expand=YES)
        
        ttk.Label(path_frame, text="Save Location", 
                 font=("Segoe UI", 10, "bold")).pack(anchor=tk.W, pady=(0, 5))
        
        path_input_frame = ttk.Frame(path_frame)
        path_input_frame.pack(fill=X)
        
        path_entry = ttk.Entry(path_input_frame, 
                              textvariable=self.download_path, 
                              font=("Segoe UI", 9), 
                              state=tk.DISABLED)
        path_entry.pack(side=LEFT, fill=X, expand=YES, padx=(0, 10))
        
        browse_btn = ttk.Button(path_input_frame, text="Browse", 
                               command=self. browse_folder, 
                               bootstyle="secondary-outline",
                               width=10)
        browse_btn.pack(side=LEFT)
        
        # ===== PROGRESS SECTION =====
        progress_frame = ttk.Frame(main_frame)
        progress_frame.pack(fill=X, pady=(0, 20))
        
        self.progress_bar = ttk. Progressbar(
            progress_frame, 
            mode='determinate', 
            bootstyle="success-striped",
            length=400
        )
        self.progress_bar.pack(fill=X, pady=(0, 8))
        
        self.status_label = ttk.Label(
            progress_frame, 
            text="Ready to download", 
            font=("Segoe UI", 10),
            foreground="#7f8c8d"
        )
        self.status_label.pack(anchor=tk.W)
        
        # ===== DOWNLOAD BUTTON =====
        button_frame = ttk.Frame(main_frame)
        button_frame.pack(fill=X)
        
        self.download_btn = ttk.Button(
            button_frame, 
            text="⬇ Download Video", 
            command=self. start_download,
            bootstyle="success",
            width=25
        )
        self.download_btn.pack()
        self.download_btn.config(state=tk.DISABLED)
        
    def toggle_theme(self):
        """Toggle between light and dark themes"""
        if self.current_theme.get() == "darkly":
            self.root.style.theme_use("flatly")
            self.current_theme.set("flatly")
            self.theme_btn.config(text="🌙 Dark Mode")
        else:
            self.root.style.theme_use("darkly")
            self.current_theme.set("darkly")
            self.theme_btn.config(text="☀️ Light Mode")
        
        # Update custom colors
        self.update_info_text_colors()
        self.update_listbox_colors()
    
    def update_info_text_colors(self):
        """Update info text colors based on theme"""
        if self.current_theme.get() == "darkly":
            self.info_text.config(bg="#2b3e50", fg="#ffffff")
        else:
            self.info_text.config(bg="#ecf0f1", fg="#2c3e50")
    
    def update_listbox_colors(self):
        """Update listbox colors based on theme"""
        if self.current_theme. get() == "darkly":
            self.quality_listbox. config(
                bg="#34495e",
                fg="#ecf0f1",
                selectbackground="#3498db",
                selectforeground="#ffffff"
            )
        else:
            self.quality_listbox.config(
                bg="#ffffff",
                fg="#2c3e50",
                selectbackground="#3498db",
                selectforeground="#ffffff"
            )
        
    def fetch_video_info(self):
        """Fetch video information and available qualities"""
        url = self.url_var.get().strip()
        if not url: 
            messagebox.showerror("Error", "Please enter a YouTube URL")
            return
        
        # Show loading status
        self.status_label. config(text="⏳ Fetching video information...")
        self.quality_listbox.delete(0, tk.END)
        self.download_btn.config(state=tk.DISABLED)
        
        # Run in thread to prevent UI freeze
        thread = threading.Thread(target=self._fetch_video_info_thread, args=(url,))
        thread.daemon = True
        thread.start()
        
    def _fetch_video_info_thread(self, url):
        """Background thread for fetching video info"""
        try:
            self.current_yt = YouTube(
                url,
                on_progress_callback=self.on_progress,
                use_oauth=False,
                allow_oauth_cache=True
            )
            
            # Force load all data
            _ = self.current_yt. streams
            
            # Update UI
            self.root.after(0, self.display_video_info)
            self.root.after(0, self.populate_quality_options)
            self.root.after(0, self.populate_subtitles)
            
            self.root.after(0, lambda: self.status_label.config(text="✅ Video loaded successfully! "))
            self.root.after(0, lambda: self.download_btn.config(state=tk.NORMAL))
            
        except Exception as e:
            error_msg = f"Error fetching video:  {str(e)}\n\nTry:  pip install --upgrade pytubefix"
            self.root.after(0, lambda: messagebox.showerror("Error", error_msg))
            self.root.after(0, lambda: self.status_label.config(text="❌ Failed to fetch video"))
            
    def display_video_info(self):
        """Display video information"""
        self.info_text.config(state=tk.NORMAL)
        self.info_text.delete(1.0, tk.END)
        
        try:
            duration_seconds = self.current_yt. length
            duration = f"{duration_seconds // 60}m {duration_seconds % 60}s"
            views = f"{self.current_yt.views: ,}"
            
            info = f"📹 {self.current_yt.title}\n"
            info += f"👤 {self.current_yt.author}  •  ⏱️ {duration}  •  👁️ {views} views"
            
            self. info_text.insert(1.0, info)
        except Exception as e:
            self.info_text.insert(1.0, f"Could not load video info: {str(e)}")
        
        self.info_text.config(state=tk.DISABLED)
        
    def populate_quality_options(self):
        """Populate quality options listbox"""
        self.quality_listbox.delete(0, tk.END)
        self.quality_options. clear()
        
        try:
            index = 0
            seen_qualities = set()
            
            # Get adaptive streams (higher quality)
            try:
                adaptive_streams = self.current_yt.streams.filter(
                    adaptive=True,
                    file_extension='mp4',
                    type='video'
                ).order_by('resolution').desc()
                
                for stream in adaptive_streams:
                    if stream.resolution:
                        try:
                            size_mb = stream.filesize / (1024 * 1024) if stream.filesize else 0
                        except:
                            size_mb = 0
                        
                        fps = getattr(stream, 'fps', 30) or 30
                        resolution = stream.resolution
                        quality_key = f"{resolution}_{fps}"
                        
                        if quality_key not in seen_qualities: 
                            seen_qualities.add(quality_key)
                            size_text = f"{size_mb:.0f}MB" if size_mb > 0 else "~"
                            quality_text = f"  {resolution}  •  {fps}fps  •  {size_text}"
                            
                            self.quality_listbox.insert(tk.END, quality_text)
                            self.quality_options[index] = ('adaptive', stream)
                            index += 1
            except Exception as e:
                print(f"Error loading adaptive streams: {e}")
            
            # Get progressive streams (standard quality)
            try:
                progressive_streams = self.current_yt.streams.filter(
                    progressive=True,
                    file_extension='mp4'
                ).order_by('resolution').desc()
                
                for stream in progressive_streams:
                    if stream.resolution:
                        try:
                            size_mb = stream.filesize / (1024 * 1024) if stream.filesize else 0
                        except:
                            size_mb = 0
                        
                        fps = getattr(stream, 'fps', 30) or 30
                        resolution = stream.resolution
                        quality_key = f"{resolution}_{fps}_prog"
                        
                        if quality_key not in seen_qualities:
                            seen_qualities. add(quality_key)
                            size_text = f"{size_mb:.0f}MB" if size_mb > 0 else "~"
                            quality_text = f"  {resolution}  •  {fps}fps  •  {size_text}  (Standard)"
                            
                            self.quality_listbox.insert(tk.END, quality_text)
                            self.quality_options[index] = ('progressive', stream)
                            index += 1
            except Exception as e: 
                print(f"Error loading progressive streams: {e}")
            
            if self.quality_listbox.size() > 0:
                self.quality_listbox.selection_set(0)
            else:
                self.quality_listbox.insert(tk.END, "  No quality options available")
                
        except Exception as e:
            self.quality_listbox.insert(tk.END, f"  Error:  {str(e)}")
            
    def populate_subtitles(self):
        """Populate subtitle options"""
        try:
            captions = self.current_yt.captions
            subtitle_list = ["None"]
            self.subtitle_languages. clear()
            
            for caption in captions:
                try:
                    lang_name = caption.name
                    lang_code = caption.code
                    subtitle_list.append(f"{lang_name} ({lang_code})")
                    self.subtitle_languages[f"{lang_name} ({lang_code})"] = caption
                except:
                    continue
            
            self.subtitle_combo['values'] = subtitle_list
            self.subtitle_combo.current(0)
            
        except Exception as e: 
            print(f"Subtitle loading:  {e}")
            self.subtitle_combo['values'] = ["None"]
            
    def browse_folder(self):
        """Browse for download folder"""
        folder = filedialog.askdirectory(initialdir=self.download_path.get())
        if folder:
            self.download_path.set(folder)
            
    def start_download(self):
        """Start download process"""
        selection = self.quality_listbox. curselection()
        if not selection:
            messagebox.showerror("Error", "Please select a quality option")
            return
        
        if self.is_downloading:
            messagebox.showwarning("Warning", "Download already in progress")
            return
        
        self.is_downloading = True
        self.download_cancelled = False
        self.download_btn.config(state=tk.DISABLED)
        self.progress_bar['value'] = 0
        self.temp_files = []
        
        # Run in thread
        thread = threading.Thread(target=self._download_thread, args=(selection[0],))
        thread.daemon = True
        thread.start()
        
    def _download_thread(self, selected_index):
        """Background download thread with proper cleanup"""
        video_temp = None
        audio_temp = None
        srt_temp = None
        video_no_subs = None
        
        try:
            stream_type, stream = self.quality_options[selected_index]
            download_path = self.download_path.get()
            safe_title = self.sanitize_filename(self.current_yt. title)
            
            # Final output file
            final_output = os.path.join(download_path, f"{safe_title}.mp4")
            
            self.root.after(0, lambda: self.status_label.config(text="⬇️ Downloading video..."))
            
            if stream_type == 'progressive':
                # Simple progressive download
                stream.download(output_path=download_path, filename=f"{safe_title}.mp4")
                current_file = final_output
                
            else:
                # Adaptive:  download video + audio, then merge
                self.root.after(0, lambda: self.status_label.config(text="⬇️ Downloading video stream..."))
                
                # Use temp directory
                temp_dir = tempfile.gettempdir()
                video_temp = os.path.join(temp_dir, f"{safe_title}_video_{os.getpid()}.mp4")
                
                stream.download(output_path=temp_dir, filename=os.path.basename(video_temp))
                
                if self.download_cancelled:
                    return
                
                self.root.after(0, lambda: self.status_label.config(text="🎵 Downloading audio stream..."))
                
                # Get best audio
                audio_stream = self.current_yt.streams. filter(
                    only_audio=True,
                    file_extension='mp4'
                ).order_by('abr').desc().first()
                
                if not audio_stream:
                    audio_stream = self.current_yt.streams.filter(only_audio=True).first()
                
                audio_temp = os.path.join(temp_dir, f"{safe_title}_audio_{os.getpid()}.mp4")
                audio_stream.download(output_path=temp_dir, filename=os.path.basename(audio_temp))
                
                if self. download_cancelled:
                    return
                
                # Merge
                self.root.after(0, lambda: self.status_label.config(text="🔄 Merging video and audio..."))
                self.merge_video_audio(video_temp, audio_temp, final_output)
                
                current_file = final_output
            
            # Handle subtitles
            if self.selected_subtitle.get() != "None":
                self.root.after(0, lambda: self.status_label.config(text="📝 Embedding subtitles..."))
                try:
                    selected_lang = self.selected_subtitle.get()
                    caption = self.subtitle_languages.get(selected_lang)
                    
                    if caption:
                        # Download subtitle
                        temp_dir = tempfile.gettempdir()
                        srt_temp = os.path. join(temp_dir, f"{safe_title}_sub_{os.getpid()}.srt")
                        
                        srt_content = caption.generate_srt_captions()
                        with open(srt_temp, 'w', encoding='utf-8') as f:
                            f.write(srt_content)
                        
                        # Embed subtitles
                        video_no_subs = current_file
                        final_with_subs = os.path. join(download_path, f"{safe_title}_final. mp4")
                        
                        self.embed_subtitles_ffmpeg(current_file, srt_temp, final_with_subs)
                        
                        # Replace original with subtitled version
                        if os.path.exists(final_with_subs):
                            if os.path.exists(final_output):
                                os. remove(final_output)
                            os.rename(final_with_subs, final_output)
                        
                except Exception as e:
                    print(f"Subtitle embedding failed: {e}")
            
            # Success
            self.root.after(0, lambda: self.progress_bar.config(value=100))
            self.root.after(0, lambda: self.status_label.config(
                text=f"✅ Download complete!  Saved:  {os.path.basename(final_output)}"))
            
            self.root.after(0, lambda: messagebox.showinfo(
                "Success", f"Video downloaded successfully!\n\n📁 {final_output}"))
            
        except Exception as e:
            error_msg = f"Download failed: {str(e)}"
            self.root.after(0, lambda: messagebox.showerror("Error", error_msg))
            self.root.after(0, lambda: self.status_label.config(text="❌ Download failed"))
        
        finally:
            # CLEANUP ALL TEMP FILES
            self.cleanup_temp_files([video_temp, audio_temp, srt_temp, video_no_subs])
            
            self.is_downloading = False
            self.root.after(0, lambda: self.download_btn.config(state=tk.NORMAL))
    
    def cleanup_temp_files(self, file_list):
        """Clean up all temporary files"""
        for file_path in file_list:
            if file_path and os.path.exists(file_path):
                try:
                    os.remove(file_path)
                    print(f"Cleaned up: {file_path}")
                except Exception as e:
                    print(f"Could not remove {file_path}: {e}")
            
    def merge_video_audio(self, video_file, audio_file, output_file):
        """Merge video and audio using FFmpeg"""
        try: 
            cmd = [
                'ffmpeg', '-i', video_file, '-i', audio_file,
                '-c:v', 'copy', '-c:a', 'aac',
                '-y', output_file,
                '-loglevel', 'error'
            ]
            subprocess.run(cmd, check=True, capture_output=True)
        except FileNotFoundError:
            raise Exception("FFmpeg not found. Install:  choco install ffmpeg (Windows) or brew install ffmpeg (macOS)")
        except subprocess. CalledProcessError as e: 
            raise Exception(f"FFmpeg error: {e.stderr. decode()}")
    
    def embed_subtitles_ffmpeg(self, video_file, srt_file, output_file):
        """Embed subtitles using FFmpeg"""
        try:
            # Windows path fix
            srt_escaped = srt_file.replace('\\', '/').replace(':', '\\:')
            
            cmd = [
                'ffmpeg', '-i', video_file,
                '-vf', f"subtitles='{srt_escaped}'",
                '-c:a', 'copy',
                '-y', output_file,
                '-loglevel', 'error'
            ]
            subprocess.run(cmd, check=True, capture_output=True)
        except subprocess.CalledProcessError as e:
            raise Exception(f"Subtitle embedding error: {e.stderr.decode()}")
            
    def on_progress(self, stream, chunk, bytes_remaining):
        """Progress callback"""
        try:
            total_size = stream.filesize
            bytes_downloaded = total_size - bytes_remaining
            percentage = (bytes_downloaded / total_size) * 100
            
            self.root.after(0, lambda: self.progress_bar.config(value=percentage))
            
            mb_downloaded = bytes_downloaded / (1024 * 1024)
            mb_total = total_size / (1024 * 1024)
            
            status = f"⬇️ Downloading: {percentage:.1f}% ({mb_downloaded:.1f}MB / {mb_total:.1f}MB)"
            self.root. after(0, lambda: self. status_label.config(text=status))
        except: 
            pass
        
    def sanitize_filename(self, filename):
        """Remove invalid characters from filename"""
        return re.sub(r'[<>:"/\\|?*]', '', filename)[:150]

def main():
    root = ttk.Window(themename="darkly")
    app = YouTubeDownloader(root)
    root.mainloop()

if __name__ == "__main__": 
    main()
