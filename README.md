# TextLens — File Analyzer

A powerful text analysis web application built with Flask that provides comprehensive linguistic and statistical insights into any text input.

## Overview

TextLens analyzes text and returns detailed metrics including:
- **Character & Word Counts** — Total characters, words, unique words, and more
- **Readability Metrics** — Average word length, sentence length, and reading time estimates
- **Word Frequency Analysis** — Top 10 meaningful words with their occurrence counts
- **Text Structure** — Sentence, line, and paragraph counts
- **Character Breakdown** — Letters, digits, spaces, and punctuation distribution
- **Lexical Diversity** — Percentage of unique words relative to total word count
- **Reading Time Estimation** — Based on average reading speed of 200 words per minute

## Features

- Clean, elegant web interface with a serif/monospace design
- Real-time text analysis
- Stop-word filtering for meaningful word frequency analysis
- Responsive design for desktop and mobile
- JSON API for programmatic access

## Technology Stack

- **Language:** Python 3.11
- **Framework:** Flask
- **Containerization:** Docker
- **Port:** 8000

## Getting Started

### Prerequisites

- Docker installed on your system

### Installation & Running

#### Option 1: Using Docker (Recommended)

1. Build the Docker image:
```bash
docker build -t textlens .
```

2. Run the container:
```bash
docker run -p 8000:8000 textlens
```

3. Open your browser and navigate to:
```
http://localhost:8000
```

#### Option 2: Local Development

1. Install Python 3.11+

2. Install dependencies:
```bash
pip install flask
```

3. Navigate to the src directory and run:
```bash
python app.py
```

4. Access the application at:
```
http://localhost:8000
```

## Project Structure

```
.
├── dockerfile          # Docker configuration for containerization
├── src/
│   └── app.py         # Main Flask application
└── README.md          # This file
```

## Usage

1. Open the application in your browser
2. Enter or paste text into the analysis box
3. Submit to receive comprehensive text analytics
4. View detailed statistics and word frequency analysis

## API Endpoints

- `GET /` — Main application interface
- `POST /analyze` — Submit text for analysis (returns JSON)

## How It Works

The application uses natural language processing techniques to:
- Tokenize text into words and sentences
- Filter out common stop words for meaningful analysis
- Calculate lexical diversity and readability metrics
- Generate word frequency distributions

## Performance Considerations

- Reading time is estimated based on an average reading speed of 200 words per minute
- Stop-word filtering includes 36 common English words to focus on meaningful content
- Handles texts of any length with minimal processing overhead

## Future Enhancements

- Multi-language support
- Sentiment analysis
- Named entity recognition
- Text similarity comparison
- Batch file upload and analysis

## License

This project is open source and available for personal and commercial use.

## Contributing

Contributions are welcome! Feel free to submit issues or pull requests.

---

**Built with ❤️ using Flask and Python**
