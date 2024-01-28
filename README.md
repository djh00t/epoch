# Epoch - Timelapse Video Creator

## Overview
Epoch is a web-based application designed to create high-quality timelapse videos from a series of metadata time-stamped photos. It intelligently groups photos based on date, time, and location, identifies primary subjects using advanced image processing techniques, and compiles these into a smooth timelapse video. Users can provide feedback on subject identification and image adjustments to ensure the final video meets their expectations.

## Features
- File Upload: Supports uploading multiple large images.
- Image Sorting: Sorts images based on the date captured.
- Subject Identification: Identifies and highlights subjects in photos.
- User Interaction: Allows users to verify the identified subjects.
- Image Adjustment: Cropping and zooming for consistency.
- Report Generation: Summarizes the photo selection process.
- Timelapse Video: Compiles images into a timelapse video.

## Detailed Functionality
- Subject Identification: Utilizes computer vision or machine learning to identify the primary subject in each photo.
- User Feedback: Allows users to correct the AI's subject identification, ensuring accuracy for future identifications.
- Image Adjustment: Provides tools for cropping, zooming, and optionally removing the background to focus on the subject.
- User Control: Users can specify the number of photos per day, frames per second, and minimum video length.
- Video Quality: Offers video resolution options including 720p, 1080p, and 4K, with intelligent scaling to match the source images.

## Installation
- Requirements: Python 3.x, Flask, OpenCV, and other dependencies listed in `requirements.txt`.
- Setup: Instructions on setting up the environment and running the Flask app.

## Usage
- How to upload files, review subjects, and generate the timelapse video.
- Detailed guide on user interaction points.
- Uploading Files: Step-by-step instructions for uploading images, including large files and zip/gzip archives.
- Reviewing Subjects: Guidelines for verifying and correcting subject identification in images.
- Generating Timelapse: Procedures for adjusting image settings and compiling the final timelapse video.

## API Reference
- Documentation of the RESTful API endpoints.

## Contributing
- Guidelines for contributing to the project.

## Development and Collaboration
- Modular Design: Each module of the application is designed to be standalone for ease of development and maintenance.
- Best Practices: Adherence to Python PEP 8 style guide, microservices architecture, and Docker containerization.
- Security: Emphasis on secure file handling and data processing.
- Future Integration: Prepared for potential future mobile app integration.

## License
- Details of the project's open-source license.

## Authors and Acknowledgment
- Credits to the development team and contributors.

## Project Status and Future Plans
- Current Status: Information on the latest release and ongoing development.
- Future Plans: Insights into upcoming features and enhancements.

## Project Status
- Information on the current status and future plans.
