# MobyGames Release Date Extractor

**MobyGames Release Date Extractor** is a Python-based tool designed to fetch and display release dates for video games using the MobyGames API. This tool provides a user-friendly interface to search for games, extract release dates, and manage settings.

## Table of Contents
- [Features](#features)
- [Installation](#installation)
- [Apply for a MobyGames.com API key](#apply-for-a-mobygamescom-api-key)
- [Usage](#usage)
  - [1. Load CSV of Games and Create Date List](#1-load-csv-of-games-and-create-date-list)
  - [2. Enter Game Title Manually and Get Release Dates](#2-enter-game-title-manually-and-get-release-dates)
  - [3. Change Settings](#3-change-settings)
  - [4. Exit Program](#4-exit-program)
- [Configuration](#configuration)
- [API Rate Limiting](#api-rate-limiting)
- [Contributing](#contributing)
- [License](#license)
- [Contact](#contact)

## Features
- **Load CSV of Games**: Import a list of games from a CSV file and fetch their release dates.
- **Manual Game Search**: Manually enter a game title to fetch its release dates.
- **Flexible Settings**: Configure API key, result limits, query matching, and date formatting.
- **API Rate Limiting**: Automatic handling of API rate limits.

## Installation
To use **MobyGames Release Date Extractor**, you need to have Python installed on your system. If you don't have Python installed, you can download it from the official Python [website](https://www.python.org/downloads/).\
The program was developed using Python 3.10.7, but it should be compatible with other Python 3.x versions.

1. Clone the repository or download the source code.
2. Install the required dependencies:\
```pip install requests```

### Apply for a MobyGames.com API key
1. Create an account on [MobyGames.com](https://www.mobygames.com/).
2. Head to your profile found in the upper right corner.
3. Click on "API" under your username.
4. Fill out the API request form and you will immediately receive an API key.

## Usage

### 1. Load CSV of Games and Create Date List
1. Prepare a CSV file with game titles in the first column and optionally platforms in the second column. Ensure that the CSV file has no header. When listing platforms, use the exact naming conventions as found in the [platforms section](https://www.mobygames.com/platform/) of MobyGames.com. Note that many common abbreviations for platforms are also accepted; these can be found within the [main.py](https://github.com/Aidan-Casselman/mobygames-release-date-extractor/blob/main/main.py) file.
2. Choose the "Load CSV of Games and Create Date List" option.
3. Enter the name of the CSV file and the desired output file name.
4. The program will fetch release dates for the listed games and save the results to the specified file. If only the game titles are provided it will create a list of dictionaries for the release date of each game for each platform. If both the titles and the platform are provided it will simply create a list of release dates in the order of the provided CSV file.

### 2. Enter Game Title Manually and Get Release Dates
1. Choose the "Enter Game Title Manually and Get Release Dates" option.
2. Enter the title of the game.
3. The program will display the release dates for the game on various platforms.

### 3. Change Settings
Configure the program settings including the API key, result limit, query matching, and date formatting.

### 4. Exit Program
Choose this option to exit the program.

## Configuration
Upon first run, the program will prompt you to enter your MobyGames API key. The key and default settings will be saved in save.txt and can be modified later through the settings menu.

## API Rate Limiting
The MobyGames API has a rate limit of 360 per hour. The program automatically handles this by pausing when the limit is reached, saving progress, and resuming once the limit is reset. If you prefer not to wait for the full hour, you have the option to terminate the program by pressing "Ctrl+C". Upon startup, the program records a timestamp and compares it with the timestamp from the previous session to monitor the number of API calls made within the hour.

## Contributing
Contributions to **MobyGames Release Date Extractor** are welcome. Please use the [Discussions Tab](https://github.com/Aidan-Casselman/mobygames-release-date-extractor/discussions/) of this repository.

## License
This project is licensed under the MIT License - see the [LICENSE](https://github.com/Aidan-Casselman/mobygames-release-date-extractor/blob/main/LICENSE) file for details.

## Contact
For questions, suggestions, or issues, please use the [Discussions Tab](https://github.com/Aidan-Casselman/mobygames-release-date-extractor/discussions/) of this repository.\
For professional inquiries, feel free to reach out to me via my [LinkedIn profile](https://www.linkedin.com/in/aidan-casselman-679616277).