# Crop and Soil Predictor

A video description of the project can be found <a href='https://drive.google.com/file/d/1zB4A5PV9KhoHtUvQybbAxcHbsR6PCrBP/view?usp=sharing' target='_blank'>here</a>.

This is a system that is intended to provide various kinds of information to farmers regarding soil types and parameters (N, P, K concentration and the pH value) conducive to growing a particular crop.

Currently the system supports all crop types that it was trained alongside.

## Running the demo

The system has a 2 - server architecture. The first is an API based flask server, and the other is a nodejs server.

To run the demo, first clone the repository onto your local machine. Then, `cd` into the newly cloned folder, and run the following commands:

1. `npm i`
2. `pip install flask numpy pandas scikit-learn`

> Make sure you have `pip`, `node` and `npm` installed.

Now, within the same root folder, open up 2 terminals:

1. In the first, run `node app.js`.
2. In the other, run `python server.py`. (You might have to `conda activate base` your base conda environment, or some other conda environment at this point.)

Upon successful execution, both servers should be up and running. The python server serves as an API endpoint, and the Javascript server serves us the web pages for the UI.

Now, access the home page (the only page of the website) from: `http://localhost:3000/`.

## Using the interface

The interface contains some charts and a table, along with an input form.

The varoius fields of the form are detailed in the video demo. In a nutshell, the various fields input the different parameters wrt the farmer. These include:

1. crop name: Used to determine the best soil parameters (N, P, K, pH) to grow this crop. The environmental conditions from the user's entered location are also taken into account.
2. soil parameters (N, P, K, pH): Used to predict the best crops to grow on the current soil.
3. location: Used to get the user's environment conditions, and to plot rainfall patterns. The user's location is also used to display in a tabular fasion the in - demand crops in that location, at the lower right section of the interface.