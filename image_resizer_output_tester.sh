#!/bin/bash

# Color definitions
BLUE='\033[0;34m'
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color
BOLD='\033[1m'

# Input image path
INPUT_IMAGE="data/face_images/annoyed_girl.png"

# Get original file size
ORIGINAL_SIZE=$(stat -f "%z" "$INPUT_IMAGE" | awk '{print $1/1024}')

# Target sizes in KB
TARGET_SIZES=(
    10 20 30 40 50 60 70 80 90 100
    150 200 250 300 350 400 450 500 550 600
)

# Print table header
printf "\n${BOLD}Image Resizer Test Results${NC}\n\n"
printf "${BOLD}%-15s | %-15s | %-15s | %-15s | %-15s${NC}\n" "Target (KB)" "Output (KB)" "Error (%)" "Original (KB)" "Runtime (s)"
printf "%.s-" {1..85}
printf "\n"

# Run tests for each target size
for target in "${TARGET_SIZES[@]}"; do
    # Run image resizer and capture runtime
    start_time=$(date +%s.%N)
    python scripts/image_resizer.py -f "$INPUT_IMAGE" --size "$target" -v >/dev/null 2>&1
    end_time=$(date +%s.%N)
    runtime=$(echo "$end_time - $start_time" | bc)
    
    # Get output file size
    output_size=$(stat -f "%z" "data/face_images/annoyed_girl_output.png" | awk '{print $1/1024}')
    
    # Calculate error percentage
    error=$(echo "scale=2; abs($output_size - $target)/$target * 100" | bc)
    
    # Color coding for error
    if (( $(echo "$error < 5" | bc -l) )); then
        error_color=$GREEN
    elif (( $(echo "$error < 10" | bc -l) )); then
        error_color=$YELLOW
    else
        error_color=$RED
    fi
    
    # Print results row
    printf "%-15.2f | %-15.2f | ${error_color}%-15.2f${NC} | %-15.2f | %-15.2f\n" \
        "$target" "$output_size" "$error" "$ORIGINAL_SIZE" "$runtime"
done

printf "%.s-" {1..85}
printf "\n"
