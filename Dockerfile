# Use an official Python runtime as a parent image
FROM python:3.6-stretch

# Set the working directory to /OncoServe
WORKDIR /OncoServe

# Copy the current directory contents into the container at /OncoServe
ADD . /OncoServe

# Install any needed packages specified in requirements.txt
RUN apt-get update
RUN apt-get --yes --force-yes install dcmtk
RUN apt-get --yes --force-yes install freetds-dev freetds-bin
RUN pip install -r OncoQueries/requirements.txt
RUN pip install -r OncoData/requirements.txt
RUN pip install -r OncoNet/requirements.txt
RUN pip install -r requirements.txt
# Remove git hist
RUN rm -rf .git OncoNet/.git OncoData/.git OncoQueries/.git
# Remove unecessary dirs
RUN rm -rf OncoNet/configs OncoNet/doc OncoNet/scripts


# Make port 5000 available to the world outside this container
EXPOSE 5000
EXPOSE 80

# Define environment variable
ENV NAME OncoServe

# Run app.py when the container launches
CMD gunicorn -t 360 --bind 0.0.0.0:5000 wsgi:app
