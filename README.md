# GitTrack 📊

A serverless analytics dashboard for tracking student coding activity.

## 🚀 Getting Started

```bash
# Clone the repository
git clone https://github.com/precise18/GitTrack.git
cd GitTrack

# Create virtual environment
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Set up environment
# Edit .env file with your configuration

# Generate mock data
python scripts/generate_mock_data.py

# Test the setup
python scripts/test_setup.py

# Fetch commits
python scripts/fetch_commits.py
## 📁 Project Structure

GitTrack/
├── src/ # Source code
│ ├── config.py # Configuration
│ └── models.py # Data models
├── scripts/ # Utility scripts
│ ├── fetch_commits.py
│ └── generate_mock_data.py
├── data/ # Data files
├── docs/ # Documentation
└── tests/ # Unit tests

## 📊 Features

- [x] Mock data generation for testing
- [x] GitLab commit fetching
- [x] Student activity metrics
- [ ] AWS Lambda integration
- [ ] DynamoDB storage
- [ ] Web dashboard

## 📝 License

MIT License

## 🤝 Contributing

This is a personal learning project.

## 📞 Contact

- GitHub: [@precise18](https://github.com/precise18)
- Project Link: https://github.com/precise18/GitTrack
