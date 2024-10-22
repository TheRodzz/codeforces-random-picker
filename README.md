# Codeforces Problem Finder

A desktop application that helps competitive programmers find suitable practice problems on Codeforces. It allows users to filter problems by rating range and excludes problems they've already solved.



## Features

- **Problem Rating Filter**: Search for problems within a specific rating range (800-3500)
- **Username Integration**: Filter out problems you've already solved by entering your Codeforces handle
- **Flexible Sorting**: Sort problems by:
  - Rating
  - Contest ID
  - Solved Count
  - Difficulty
- **Problem Tags**: View problem categories and types
- **Direct Access**: Double-click any problem to open it in your default browser
- **User-Friendly Interface**: Clean and intuitive GUI built with tkinter

## Prerequisites

- Python 3.6 or higher
- Internet connection for accessing the Codeforces API

## Required Python Packages

```bash
pip install requests
```

Note: `tkinter` comes pre-installed with Python on most systems.

## Installation

1. Clone the repository or download the source code:
```bash
git clone https://github.com/yourusername/codeforces-problem-finder.git
cd codeforces-problem-finder
```

2. Install required packages:
```bash
pip install -r requirements.txt
```

## Usage

1. Run the application:
```bash
python codeforces_finder.py
```

2. Using the interface:
   - (Optional) Enter your Codeforces username to exclude solved problems
   - Select your desired rating range using the dropdown menus
   - Choose how you want to sort the problems
   - Toggle problem tags display using the checkbox
   - Click "Find Problems" to search
   - Double-click any problem to open it in your browser

## Application Controls

- **Username Field**: Enter your Codeforces handle to filter out solved problems
- **Rating Range**: 
  - "From": Minimum problem rating (default: 800)
  - "To": Maximum problem rating (default: 3500)
- **Sort By**: 
  - Rating: Sort by problem difficulty
  - Contest ID: Sort by competition number
  - Solved Count: Sort by number of users who solved it
  - Difficulty: Alternative sort by rating
- **Ascending Checkbox**: Toggle sort order
- **Show Tags Checkbox**: Toggle display of problem categories
- **Find Problems Button**: Fetch and display problems matching criteria

## Problem Display

The main view shows a table with the following columns:
- Problem Name
- Rating
- Solved Count (number of users who solved it)
- Tags (problem categories and types)

## Error Handling

The application handles various error cases:
- Invalid username
- Network connection issues
- API request failures
- Invalid rating range selections

## Limitations

- Requires active internet connection
- Subject to Codeforces API rate limits
- May have slight delays when fetching large amounts of data

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments

- Built using the [Codeforces API](https://codeforces.com/apiHelp)
- Thanks to the Codeforces platform for providing the programming competition infrastructure

## Support

If you encounter any problems or have suggestions:
1. Check the existing issues
2. Create a new issue with a detailed description
3. Include steps to reproduce any bugs