# Use an official PostgreSQL runtime as a parent image
FROM postgres:latest

# Set the working directory in the container
WORKDIR /esg_returns

# Copy the current directory contents into the container
COPY . /esg_returns/

# Install any needed packages specified in requirements.txt
RUN apt-get update && apt-get install -y python3 python3-pip
COPY /requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# Make ports available to the world outside this container
EXPOSE 5432

# Define environment variable
ENV POSTGRES_DB=my_database
ENV POSTGRES_USER=my_user
ENV POSTGRES_PASSWORD=my_password

# Copy the data dump to the container
COPY data/esg_data.sql /docker-entrypoint-initdb.d/

# Run analysis when the container launches
# CMD ["python3", "./analysis/script1.py"]
