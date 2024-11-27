# Changelog

All notable changes to this project will be documented in this file.

<!-- The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html). -->

## [0.2.2] - 2024-11-27

### Fixed

- Fix Internal Server Error when body contained non-ASCII characters [#73](https://github.com/scaleway/serverless-functions-python/issues/73)

### Changed

- Removed support for Python 3.8 as it has reached its end of life

## [0.2.1] - 2024-07-15

### Fixed

- Returning a base64 encoded response would not be decoded by the framework

## [0.2.0] - 2023-04-23

### Added

- Added a simple server to test with multiple handlers

## [0.1.1] - 2023-04-14

### Changed

- Update README with link to Serverless Functions Node

### Fixed

- Fix typos in headers injected by Envoy

## [0.1.0] - 2023-03-02

### Added

- Initial project setup
- Local testing utils
- Repository setup
