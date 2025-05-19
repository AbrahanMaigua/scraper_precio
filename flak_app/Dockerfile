FROM python:3.9-slim

# Set the working directory to /app
WORKDIR /app
# Copy the current directory contents into the container at /app
COPY . /app/
# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt
# Make port 80 available to the world outside this container

# Expose the port Flask will run on
EXPOSE 5000

# Use gunicorn for production
#CMD ["gunicorn", "--bind", "0.0.0.0:5000", "server:app"]
# Run app.py when the container launches    
CMD ["python", "server.py"]
# Use the following command to build the Docker image
# docker build -t my-python-app .
# Use the following command to run the Docker container
# docker run -p 4000:80 my-python-app
# Use the following command to run the Docker container in detached mode
# docker run -d -p 4000:80 my-python-app
