# Flask API for Climate Analysis

This project involves analyzing climate data for Honolulu, Hawaii using Python, SQLAlchemy ORM queries, Pandas, and Matplotlib in a jupyter notebook. The analysis includes a precipitation analysis and a station analysis. A Flask API was also created to easily view the results.

## Installation

To run this project, you need to have the following installed:

   * Python 3.x or higher
   * Pandas
   * SQLAlchemy
   * Flask

## Usage

To use this project:

   * Clone this repository to your local machine
   * Navigate to the project directory using the command prompt
   * Run climate.ipynb to open the Jupyter Notebook file
   * Follow the instructions in the notebook to analyze the climate data
   * After analyzing the data, run python app.py to start the Flask server
   * Use the endpoints specified in the Routes section to access the data via the API

## Routes

The following endpoints are available in the Flask API:

1. `/`
    * Displays a list of all available routes in the API.

2. `/api/v1.0/precipitation`
    * Returns the precipitation data for the last 12 months in JSON format.

3. `/api/v1.0/stations`
    * Returns a list of all the weather stations in JSON format.

4. `/api/v1.0/tobs`
    * Returns the temperature observations for the most active station for the last 12 months in JSON format.

5. `/api/v1.0/<start>`
    * Returns the minimum, maximum and average temperature for all dates greater than or equal to the start date (YYYY-MM-DD) in JSON format.

6. `/api/v1.0/<start>/<end>`
    * Returns the minimum, maximum and average temperature for all dates between the start and end date (YYYY-MM-DD) inclusive, in JSON format.

## References
Menne, M.J., I. Durre, R.S. Vose, B.E. Gleason, and T.G. Houston, 2012: An overview of the Global Historical Climatology Network-Daily Database. Journal of Atmospheric and Oceanic Technology, 29, 897-910, [https://doi.org/10.1175/JTECH-D-11-00103.1](https://doi.org/10.1175/JTECH-D-11-00103.1)
