#!/bin/sh

set -ex

# Path to the file containing the version
version_file="version.txt"

# Check if the version file exists
if [ ! -f "$version_file" ]; then
    echo "Version file not found!"
    exit 1
fi

# Get the latest version from the file
latest_version=$(cat "$version_file")

# Get the first word of the latest commit message (case-insensitive)
latest_commit_msg=$(git log -1 --pretty=%B)
first_word=$(echo "$latest_commit_msg" | awk '{print toupper($1)}' | tr -d ':')

# Extract major, minor, and patch version from the latest version
major=$(echo "$latest_version" | sed 's/v\([0-9]*\)\.\([0-9]*\)\.\([0-9]*\)/\1/')
minor=$(echo "$latest_version" | sed 's/v\([0-9]*\)\.\([0-9]*\)\.\([0-9]*\)/\2/')
patch=$(echo "$latest_version" | sed 's/v\([0-9]*\)\.\([0-9]*\)\.\([0-9]*\)/\3/')

# Function to determine the next semantic version
calculate_version() {
    case $1 in
        "MAJOR") echo $(($major + 1)).0.0;;
        "MINOR") echo $major.$(($minor + 1)).0;;
        "PATCH") echo $major.$minor.$(($patch + 1));;
         *) echo "$latest_version";;
    esac
}

# Determine the next version based on the first word of the latest commit
next_version=$(calculate_version "$first_word")

if [ "$next_version" = "$latest_version" ]; then
    echo "$latest_version"
else
    echo "v$next_version"
    # Update the version file with the new version
    echo "v$next_version" > "$version_file"
fi