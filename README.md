# Chess Opening Recommender System
Thought of the idea of creating a chess opening recommendation system.

**Starting with a collaborative filtering model (compares user's opening choices to similar users' openings).**
This recommendation system uses the [Chess.com](https://chesscom.readthedocs.io/en/latest/) to analyze the user's openings.
User can easily be compared to other Chess.com users using a large Chess.com dataset (40,000 games)

In the future, if a content based filtering model were included *(making the entire system a hybrid system)*, then all opening positions in the ECO (Encyclopaedia of Chess Openings) would need to be vectorized in order to be compared to other openings

**Layout**
- [data_manipulation.py]([data_manipulation.py](https://github.com/JuliustheCreator/Opening-Recommendation/blob/master/system/data_manipulation.py)) is used to grab user's games, as well as to clean and prepare the data from the large Chess.com dataset.
