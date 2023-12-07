# Use an official Python runtime as a parent image
FROM python:3.8

# Set the working directory in the container
WORKDIR /esg-returns

# Copy the current directory contents into the container
COPY . /esg-returns

# Install the Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Install LaTeX with minimal additional packages
RUN apt-get update && \
    apt-get install -y --no-install-recommends texlive-latex-extra texlive-bibtex-extra biber && \
    rm -rf /var/lib/apt/lists/*

# Make ports available to the world outside this container
EXPOSE 5432

CMD ["python", "build_project.py"]
