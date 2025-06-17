# HBnB API Project

## Project Structure

- `app/api/v1/`: Versioned API endpoints
- `app/models/`: Business logic and models
- `app/services/`: Facade pattern to coordinate logic
- `app/persistence/`: In-memory repository (replaces DB later)
- `run.py`: Entry point
- `config.py`: Environment configuration

## How to Run

```bash
pip install -r requirements.txt
python run.py

