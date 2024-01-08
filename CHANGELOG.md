# Changelog

## [0.1] - 2023-07-30
### Added
- Initial version of the project
- Basic extraction of year of game release
- Working save file and settings
- Lengthy process of finding game ids and then finding release dates

## [0.2] - 2023-08-08
### Added
- Limited exception handling of errors
- Tracking of hourly API calls and ability to wait for more

## [1.0] - 2023-10-29
### Added
- More settings i.e., exact query match, year only
- Ability to specify platform in csv file
- Ability to accept single column csv files
- Mappings of platform abbreviations
- Enhanced exception handling

### Changed
- Much faster and more efficient method that only takes 1 API call per game
- Accepts csv as input rather than txt

### Removed
- Unused settings and functions

## [1.0 Release] - 2024-01-02
### Added
- 1.0 Release of MobyGames Release Date Extractor

### Changed
- Refined Git commit history to unify authorship

## [1.1] - 2024-01-08
### Fixed
- Fixed 'year_only' bug truncating YYYY-MM dates to first character
- Fixed progress display bug unnecessarily creating new lines in terminal