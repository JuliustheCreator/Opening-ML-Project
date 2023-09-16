# Chess Opening Recommendation System

This project aims to create a chess opening recommendation system for chess players. It is built to help chess enthusiasts and learners identify openings that they might find interesting or useful.

## Getting Started
1. Clone the repository.
2. Install necessary dependencies.
3. Run main.py to initialize the system.

## File Structure

`main/`
- `main.py` **- main driver of the program**
  
- `api.py` **- interface for the chess.com api**
  
- `engine.py` **- (under development) the core recommendation system**
  
- `processing.py` **- data transformation and preprocessing utilities**
  
- `data/`
  
    - `dataset.parquet` **- processed dataset in Parquet format**
      
    - `dataset.py` **- script used to build the dataset**
      
- `misc/`
  
    - `legacy.py` **- holds deprecated code for reference**

## Current Work
- **Recommendation Engine:** The core recommendation system, potentially leveraging PyTorch for deep learning, is still under active development.
  
- **Data Exploration:** Plans to dive deeper into the dataset to extract more insights and refine the recommendation process.
  
- **Web Deployment:** Post completion, the engine will be wrapped into a web interface using Django, making it accessible to a wider audience.

## Contributions
This project is a personal passion project. However, feedback, insights, or pull requests are always welcome.

## License
This project is open source. Feel free to use, modify, and distribute as you see fit.

