# Chess Opening Recommendation System

This project aims to create a chess opening recommendation system for chess players. Currently, the focus is on cleaning and preparing the dataset. The next phases of development will involve implementing a collaborative filtering model, content-based filtering model, and building the recommendation engine.

## Features

1. Chess.com API integration to analyze the user's openings.
2. A dataset of 40,000 Chess.com games for comparison and recommendations.

## File Structure

- `system/`
    - `engine.py` (planned file for the recommendation system)
    - `data_exploration.ipynb` (basic visualization of the dataset)
    - `data/`
        - `chesscomgames.csv` (dataset of 40,000 Chess.com games)
        - `data_manipulation.py` (data cleaning and preparation)

## Dependencies

- pandas
- sys
- requests
- chessdotcom
- chess
- io.StringIO

## Current Work

1. Cleaning and preparing the dataset for use in the recommendation system.

## Future Plans

1. Implement a collaborative filtering model to recommend openings based on similar users.
2. Develop a content-based filtering model for a hybrid recommendation system.
3. Build a recommendation engine to provide accurate and relevant opening suggestions for users.
