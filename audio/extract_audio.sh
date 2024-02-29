#!/bin/bash

# Function to convert seconds to HH:MM:SS format
convert_seconds_to_time() {
    local total_seconds=$1
    local hours=$(echo "$total_seconds/3600" | bc)
    local minutes=$(echo "($total_seconds/60)%60" | bc)
    local seconds=$(echo "$total_seconds%60" | bc)
    printf "%02d:%02d:%02d\n" $hours $minutes $seconds
}

# Change directory to the one containing the video files 
cd ./2sound

# Loop through all MP4 files in the current directory
for file in *.mp4; do
    # Extract the date and week number from the file name
    date=$(echo $file | grep -oP '\d{4}-\d{2}-\d{2}')
    week=$(echo $file | grep -oP 'w\d{2}')

    # Extract the audio track from the video file
    ffmpeg -i "$file" -vn -acodec copy "${date}-${week}.m4a"

    # Get the duration of the audio file in seconds
    duration=$(ffmpeg -i "${date}-${week}.m4a" 2>&1 | grep Duration | awk '{print $2}' | tr -d , | awk -F ':' '{print ($1 * 3600) + ($2 * 60) + $3}')
    # Divide the duration by 4 to get the duration of each part
    split_duration=$(echo "scale=2; $duration / 4" | bc)

    for part in {1..4}; do
        # Calculate the start time for each part
        start_seconds=$(echo "scale=2; ($part - 1) * $split_duration" | bc)
        # Convert start time to HH:MM:SS format
        start_time=$(convert_seconds_to_time $start_seconds)
        # Calculate the duration of each segment in HH:MM:SS format
        segment_duration=$(convert_seconds_to_time $split_duration)

        # Extract a part of the audio file starting at start_time and lasting for segment_duration
        ffmpeg -i "${date}-${week}.m4a" -ss "$start_time" -t "$segment_duration" -acodec copy "${date}-${week}-$part.m4a"
    done

    # Remove the original audio file to clean up the directory
    rm "${date}-${week}.m4a"
done
