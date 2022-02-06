# CLI tools

Currently, there is a single CLI tool which allows filtering empty videos.
The current filter is a naive algorithm which checks for difference between two adjacent frames for a specific threshold.
It is currently set hardcoded to 50.

## Usage

### Getting started
`python -m pip install pipenv`

`pipenv sync --dev`

`pipenv shell`

`python src/filter_empty_videos.py --help`

### Dry-Run

`python src/filter_empty_videos.py --dry-run --src myvideos --dest filtered_videos`

### Run

`python src/filter_empty_videos.py --src myvideos --dest filtered_videos`
