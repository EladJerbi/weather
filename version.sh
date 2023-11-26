#!/bin/sh

set -ex

# Get the latest git tag
latest_tag=$(git describe --tags --abbrev=0)

# Get the first word of the latest commit message (case-insensitive)
latest_commit_msg=$(git log -1 --pretty=%B)
first_word=$(echo "$latest_commit_msg" | awk '{print toupper($1)}' | tr -d ':')

# Extract major, minor, and patch version from the latest tag
major=$(echo "$latest_tag" | sed 's/v\([0-9]*\)\.\([0-9]*\)\.\([0-9]*\)/\1/')
minor=$(echo "$latest_tag" | sed 's/v\([0-9]*\)\.\([0-9]*\)\.\([0-9]*\)/\2/')
patch=$(echo "$latest_tag" | sed 's/v\([0-9]*\)\.\([0-9]*\)\.\([0-9]*\)/\3/')

# Function to determine the next semantic version
calculate_version() {
    case $1 in
        "MAJOR") echo $(($major + 1)).0.0;;
        "MINOR") echo $major.$(($minor + 1)).0;;
        "PATCH") echo $major.$minor.$(($patch + 1));;
         *) echo "$latest_tag";;
    esac
}

# Determine the next version based on the first word of the latest commit
next_version=$(calculate_version "$first_word")

if [ "$next_version" = "$latest_tag" ]; then
    echo "$latest_tag"
else
    echo "v$next_version"
    git tag "v$next_version"
fi
