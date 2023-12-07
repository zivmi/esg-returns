FROM python:3.8

# Set the working directory in the container
WORKDIR /esg-returns

# Copy the current directory contents into the container
COPY . /esg-returns

# Install the Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Make ports available to the world outside this container
EXPOSE 5432

CMD ["python", "src/run_main.py"]
