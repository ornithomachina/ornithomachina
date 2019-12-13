# The Ornithomancer

Nonpartisan, machine learning-driven assessment of news stories built from a dataset containing false and true stories across the political spectrum

## Steps to run the project
1. Fork the project and clone it on your local machine
2. Make sure you have Miniconda or Anaconda installed
3. `cd` into the project repo, and open up environment.yml. Replace [path_to_conda] with your system path to your conda.
4. Set up the environment: `conda env create -f environment.yml`. This should install all of the dependencies you need.
5. Activate the environment: `conda activate myenv`
6. Conda should have Jupyter Notebook installed by default, so to run .ipynb files, simply type `jupyter notebook`
7. To run the pipeline:
   - Set up a Twitter developer account and create your own app.
   - Create a file called config.py in the same directory as pipeline.py
   - In config.py, define your `consumer_key`, `consumer_secret`, `access_token`, and `access_token_secret`
   - Now you should be able to run pipeline.py, responding to Twitter users in realtime.
