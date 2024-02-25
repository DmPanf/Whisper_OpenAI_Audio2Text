```markdown
# Audio Extractor from Video 🎥🎵

Welcome to the Audio Extractor from Video project! This tool is designed to help you easily extract audio tracks from your video files, split them into four equal parts, and save them with new filenames that include the date, week number, and part number. It's perfect for podcasters, video editors, and anyone looking to work with audio segments from video content.

## Features ✨

- **Audio Extraction**: Extracts the audio track from MP4 video files without re-encoding, preserving the original audio quality.
- **Auto-splitting**: Automatically splits the extracted audio into four equal parts, making it easier to manage and use for various purposes.
- **Smart Naming**: Saves the audio parts with filenames that include the video's original date, week number, and part number, keeping your files organized.
- **Batch Processing**: Processes all MP4 files in the specified directory, saving you time and effort.

## Requirements 🛠️

Before you start using this script, make sure you have the following installed on your system:
- `ffmpeg`: for handling video and audio processing.
- `bc`: for performing floating-point arithmetic in bash.

On Manjaro Linux (or any Arch-based distribution), you can install these with the following commands:
```bash
sudo pacman -Sy ffmpeg bc
```

## Installation 📦

1. Clone this repository to your local machine or download the script directly.
2. Navigate to the directory containing the script.
3. Make the script executable by running:
```bash
chmod +x extract_audio.sh
```

## Usage 🚀

1. Place your MP4 video files in a directory.
2. Open a terminal and navigate to the directory containing the `extract_audio.sh` script.
3. Run the script with:
```bash
./extract_audio.sh
```
4. The script will process all MP4 files in the specified directory (`./2sound` by default), extract the audio, split it into four parts, and save them in the same directory with the new naming scheme.

## Contributing 🤝

Contributions are what make the open-source community such an amazing place to learn, inspire, and create. Any contributions you make are **greatly appreciated**.

If you have a suggestion that would make this better, please fork the repo and create a pull request. You can also simply open an issue with the tag "enhancement".
Don't forget to give the project a star! Thanks again!

## License 📄

Distributed under the MIT License. See `LICENSE` for more information.

## Acknowledgements 🎉

- Thanks to all the contributors who spend their time to make this project better!
- Special thanks to the open-source community for providing the tools and libraries we rely on.

```

This `README.md` file includes a concise project description, installation and usage instructions, a call for contributions, licensing information, and acknowledgements, all formatted with Markdown for easy reading and organization on GitHub. Emojis are used throughout to add visual interest and highlight key sections.
