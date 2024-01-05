# sqlalchemy-challenge
# Part 1: Analyze and Explore the Climate Data
## Precipitation Analysis
1. Find the most recent date in the dataset.
   - Pulled these results by using session.query and order by the most recent date in the database in descending order.
   - I then took the first value from that column

         recent_date = session.query(measurement.date).order_by(measurement.date.desc()).first()
         recent_date
     
   - **Code for this was taken from activities performed in class**
     
2. Using that date, get the previous 12 months of precipitation data by querying the previous 12 months of data.
    - I was having trouble with this portion so I first had to format the date what I was pulling as the most recent date
    - I then calculated the date a year from the most recent date by subtracting by 365 days using datetime
    - I then performed the query looking for date and precipiation data greater than the one year ago date.

          # Starting from the most recent data point in the database. 
          most_recent_date = session.query(measurement.date).order_by(measurement.date.desc()).first()[0]
          # Converted to datetime so that I could take it as a date format to use in the calculation from one year ago
          most_recent_date = dt.datetime.strptime(most_recent_date, "%Y-%m-%d")
          most_recent_date = most_recent_date.date()
          # Calculate the date one year from the last date in data set.
          one_year_ago = most_recent_date - dt.timedelta(days=365)
          # Perform a query to retrieve the data and precipitation scores
          precipitation_data = session.query(measurement.date, measurement.prcp).\
            filter(measurement.date >= one_year_ago).all()

    - **Code for the formatting was taken from ChatGPT. It helped me return the results in the desired format. Code to perform the query was taken from activities performed in class**

3. Select only the "date" and "prcp" values.
    - Put together my query to only pull date and prcp values

           # Perform a query to retrieve the data and precipitation scores
           precipitation_data = session.query(measurement.date, measurement.prcp).\
              filter(measurement.date >= one_year_ago).all()

    - **Code taken from activities performed in class**
      
4. Load the query results into a Pandas DataFrame. Explicitly set the column names.
    - Converted the results into a dataframe and named the columns
  
          # Save the query results as a Pandas DataFrame. Explicitly set the column names
          precipitation_df = pd.DataFrame(precipitation_data, columns=['Date', 'Precipitation'])

    - **ChatGPT helped me with naming the Date and precipitation columns but we also learned it in class**
      
5. Sort the DataFrame values by "date".
    - I sorted the values by date and then set the index
  
          # Sort the dataframe by date and set the index so that I could graph the results accurately
          precipitation_df.sort_values(by='Date', inplace=True)
          precipitation_df.set_index('Date', inplace=True)

    - **The sort was taken from class activities but I was having trouble getting it to work so chatGPT helped me by setting the index**
      
6. Plot the results by using the DataFrame plot method, as the following image shows:
    - Plotted the results of the dataframe, set some labels, and then set the xticks at 90 degrees
   
          # Use Pandas Plotting with Matplotlib to plot the data
          precipitation_df.plot(y='Precipitation', figsize=(7, 5))
          plt.xlabel('Date')
          plt.ylabel('Inches')
          plt.xticks(rotation=90)
          plt.show()

## Station Analysis
1. Design a query to calculate the total number of stations in the dataset.
    - This was performed using func to count the distinct stations
  
          total_stations = session.query(func.distinct(station.station)).count()
          total_stations

   - **Code taken from activities performed in class**

2. Design a query to find the most-active stations (that is, the stations that have the most rows). To do so, complete the following steps:
- List the stations and observation counts in descending order.
    - used func, groupby, and orderby to get the necessary results in the proper order

          # List the stations and their counts in descending order.
          station_row_counts = session.query(measurement.station, func.count()).\
              group_by(measurement.station).\
              order_by(func.count().desc()).all()
          station_row_counts

    - **Code taken from activities performed in class**
- Answer the following question: which station id has the greatest number of observations?
    - station 'USC00519281' had the highest number of observations, which you can see in the results from the above query
 
3. Design a query that calculates the lowest, highest, and average temperatures that filters on the most-active station id found in the previous query.
    - Used sel to create the variable of what I was looking for and then called it in my query and filtered for the results of the station name listed above.
  
            # Using the most active station id from the previous query, calculate the lowest, highest, and average     temperature.
            sel = [measurement.station,
                  func.min(measurement.tobs),
                  func.max(measurement.tobs),
                  func.avg(measurement.tobs)]
            most_active_station = session.query(*sel).\
                filter(measurement.station == 'USC00519281').all()
            most_active_station

   - **Code was taken from activities performed in class**

4. Design a query to get the previous 12 months of temperature observation (TOBS) data. To do so, complete the following steps:
- Filter by the station that has the greatest number of observations.
    - in my code I used a filter to pull results for the most active station previously identified
- Query the previous 12 months of TOBS data for that station.
    - used similar code as earlier to pull last 12 months of data filtering by station and date
- Plot the results as a histogram with bins=12, as the following image shows:
    - Plotted results using plt.hist of just the temperature column, set the labels, and showed the legend. Added bins to bin the results in 12 bins.
 
            # Calculate the date one year ago from the last date in data set
            most_active_station_last_date = session.query(func.max(measurement.date)).\
                filter(measurement.station == 'USC00519281').scalar()
            
            most_active_station_last_date = dt.datetime.strptime(most_active_station_last_date, '%Y-%m-%d')
            one_year_ago = most_active_station_last_date - dt.timedelta(days=365)
            
            # Query temperature observation data for the last 12 months for the most active station
            temperature_data = session.query(measurement.date, measurement.tobs).\
                filter(measurement.station == 'USC00519281').\
                filter(measurement.date >= one_year_ago).all()
            
            # Save the query results as a Pandas DataFrame
            temperature_df = pd.DataFrame(temperature_data, columns=['Date', 'Temperature'])
            
            # Plot the results as a histogram
            plt.figure(figsize=(8, 5))
            plt.hist(temperature_df['Temperature'], bins=12, edgecolor='black', label='tobs')
            plt.xlabel('Temperature')
            plt.ylabel('Frequency')
            plt.legend()
            plt.show()
  

    - **Used slightly different code to return the stations last date and one year ago date that I got from chatGPT. Everything else was what we learned in class**
 
## Part 2: Design Your Climate App
Now that you’ve completed your initial analysis, you’ll design a Flask API based on the queries that you just developed. To do so, use Flask to create your routes as follows:

1. /
      - Start at the homepage.
      - List all the available routes.
          - set my homepage results

                @app.route("/")
                def welcome():
                    """List all available api routes."""
                    return (
                        f"Available Routes:<br/>"
                        f"/api/v1.0/precipitation<br/>"
                        f"/api/v1.0/stations<br/>"
                        f"/api/v1.0/tobs<br/>"
                        f"/api/v1.0/start_date/2015-08-01<br/>"
                        f"/api/v1.0/start_date/2015-08-01/end_date/2016-08-01"
            
          - **Code taken from activities performed in class**

2. /api/v1.0/precipitation
      - Convert the query results from your precipitation analysis (i.e. retrieve only the last 12 months of data) to a dictionary using date as the key and prcp as the value.
      - Return the JSON representation of your dictionary.

              @app.route("/api/v1.0/precipitation")
              def precipitation():
                  # Query of precipitation data
                  # Perform a query to retrieve the data and precipitation scores
                  # Used the specific date to go back to rather than a variable because I couldn't make it work
                  # Only return data for the last year in the database. Date is one year from end of data
                  precipitation_data = session.query(measurement.date, measurement.prcp).\
                      filter(measurement.date >= '2016-08-23').all()
                  # Close the opened session
                  session.close()
                  # Create a dictionary from the query results
                  all_precipitation = []
                  for date, prcp in precipitation_data:
                      precipitation_dict = {}
                      precipitation_dict["date"] = date
                      precipitation_dict["prcp"] = prcp
                      all_precipitation.append(precipitation_dict)
                  # Return jsonified results
                  return jsonify(all_precipitation)

      - **Code for this was taken from activities we performed in class on how to create a dictionary from the results**

3. /api/v1.0/stations
    - Return a JSON list of stations from the dataset.

            @app.route("/api/v1.0/stations")
            def stations():
                # List out all the stations. Also added the station name here because the station
                # wasn't unique enough to identify
                results = session.query(station.station, station.name).all()
                # close the session
                session.close()
                # Convert results into a list as stated in the instructions
                all_stations = list(np.ravel(results))
                # Return jsonified results
                return jsonify(all_stations)

      - **Code for this was taken from activities we performed in class on how to create a list from the results**

4. /api/v1.0/tobs
    - Query the dates and temperature observations of the most-active station for the previous year of data.
    - Return a JSON list of temperature observations for the previous year.
       - see comments in code below
  
              @app.route("/api/v1.0/tobs")
              def temperature():
                  # Query of temperature data
                  # Perform a query to retrieve the date and temperature scores
                  # Used the specific date to go back to rather than a variable because I couldn't make it work
                  # Pull the results from station USC00519281 and only returns data from the last year of data
                  temperature_data = session.query(measurement.date, measurement.tobs).\
                      filter(measurement.station == 'USC00519281').\
                      filter(measurement.date >= '2016-08-23').all()
                  # Close the session
                  session.close()
                  # Convert results into a normal list as stated in instructions
                  temperatures = list(np.ravel(temperature_data))
                  # Return jsonified results
                  return jsonify(temperatures)


      - **Code also taken from activities we performed in class**

5. /api/v1.0/<start>
    - Return a JSON list of the minimum temperature, the average temperature, and the maximum temperature for a specified start or start-end range.
    - For a specified start, calculate TMIN, TAVG, and TMAX for all the dates greater than or equal to the start date.
    - For a specified start date and end date, calculate TMIN, TAVG, and TMAX for the dates from the start date to the end date, inclusive.
        - Separated out this code for start and end
        - See comments in code below about reasoning behind code

                  @app.route("/api/v1.0/start_date/<start_date>")
                  def start_date(start_date):
                      # Fetch the results whose going back to the start date
                      entered_start_date = datetime.strptime(start_date, "%Y-%m-%d")
                      # The instructions just said to pull the results from the provided start date in a list
                      # so I pulled the results into a list instead of a dictionary
                      # Used sel to create my variable for the min, max, and avg
                      sel = [func.min(measurement.tobs),
                          func.max(measurement.tobs),
                          func.avg(measurement.tobs)]
                      temp_averages = session.query(*sel).\
                          filter(measurement.date >= entered_start_date).all()
                      # Close the session
                      session.close()
                      # Convert the results into a list as specified in the assignment
                      averages = list(np.ravel(temp_averages))
                  
                      # Return jsonified results
                      return jsonify(averages)

        - **Code was taken most from activities in class. But ChatGPT helped me finish the code when I ran into some issues. Spent a lot of time tryig to troubleshoot to realize the code was right the first time and I was adding dates that weren't in the code :)**



6. /api/v1.0/<start>/<end>
    - Return a JSON list of the minimum temperature, the average temperature, and the maximum temperature for a specified start or start-end range.
    - For a specified start, calculate TMIN, TAVG, and TMAX for all the dates greater than or equal to the start date.
    - For a specified start date and end date, calculate TMIN, TAVG, and TMAX for the dates from the start date to the end date, inclusive.
      - see comments in code below

              @app.route("/api/v1.0/start_date/<start_date>/end_date/<end_date>")
              def start_end_date(start_date, end_date):
                  # Code to create the provided start date
                  start_date = datetime.strptime(start_date, "%Y-%m-%d")
                  # Code to create the provided end date
                  end_date = datetime.strptime(end_date, "%Y-%m-%d")
                  # Used sel to create my variable for the min, max, and avg
                  # Used the provided start and end date to return the results
                  sel = [func.min(measurement.tobs),
                      func.max(measurement.tobs),
                      func.avg(measurement.tobs)]
                  temp_averages_range = session.query(*sel).\
                      filter(measurement.date >= start_date).\
                      filter(measurement.date <= end_date).all()
                  # Close the session
                  session.close()
                  # Convert the results into a list. Again it said list instead of dictionary in the assignment
                  averages_range = list(np.ravel(temp_averages_range))
              
                  # Return jsonified results
                  return jsonify(averages_range)

      - **Mostly was able to use code from class activities, but I did have to run it through chatGPT to make it work when I was running into issues.**

