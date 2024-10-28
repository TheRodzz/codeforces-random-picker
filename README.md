# Codeforces Problem Finder

A desktop application that helps competitive programmers find suitable practice problems on Codeforces based on their rating range and solved problems history.

## Features

- **Problem Discovery**: Find unsolved problems within your specified rating range
- **Dark Mode**: Eye-friendly dark theme enabled by default
- **Smart Filtering**: Automatically excludes problems you've already solved
- **Customizable Search**:
  - Set minimum and maximum problem ratings
  - Limit the number of contests to search through
  - Sort problems by various criteria
- **Quick Access**: Double-click any problem to open it in your browser
- **Random Problem**: Get a random problem matching your criteria for practice
- **Real-time Updates**: Fetch and display problems with live status updates

## Installation

### Prerequisites
- Python 3.6 or higher
- pip (Python package installer)

### Required Libraries
```bash
pip install PyQt5 requests
```

### Running the Application
1. Clone the repository or download the source code
2. Navigate to the project directory
3. Run the application:
```bash
python main.py
```

## Usage

1. **Enter Your Codeforces Handle**:
   - Type your Codeforces username in the input field
   - This is used to exclude problems you've already solved

2. **Set Problem Parameters**:
   - Adjust the rating range (800-3500)
   - Set the contest limit to control how many contests to search through
   - Toggle dark mode on/off as needed

3. **Fetch Problems**:
   - Click "Fetch Problems" to retrieve problems matching your criteria
   - Wait for the status bar to indicate completion

4. **Interact with Problems**:
   - Sort problems using the dropdown menu
   - Double-click any problem to open it in your browser
   - Use "Open Random Problem" to get a random problem from the list

## Problem Table Columns

- **Name**: Problem title
- **Rating**: Difficulty rating of the problem
- **Contest ID**: Original contest identifier
- **Index**: Problem index within the contest
- **Tags**: Problem categories and topics

## Technical Details

- Built with PyQt5 for the graphical interface
- Uses Codeforces API for fetching problem data
- Implements threading for smooth UI responsiveness
- Supports system-native window decorations

## Error Handling

The application handles various error scenarios:
- Invalid usernames
- Network connectivity issues
- API access problems
- No matching problems found

## Contributing

Feel free to contribute to this project by:
1. Forking the repository
2. Creating a feature branch
3. Making your changes
4. Submitting a pull request

## License

This project is available under the MIT License. See the LICENSE file for details.

## Acknowledgments

- Thanks to Codeforces for providing the API
- Built for competitive programmers by competitive programmers

## Support

If you encounter any issues or have suggestions:
1. Check the existing issues on GitHub
2. Create a new issue with detailed information about your problem
3. Include steps to reproduce the issue

---

*Note: This application is not officially affiliated with Codeforces.*