FROM python

# Set the working directory in the container
WORKDIR /home

# Install LaTeX
RUN apt-get update && apt-get install -y \
    texlive \
    texlive-fonts-recommended \
    texlive-latex-extra \
    && rm -rf /var/lib/apt/lists/*

RUN apt-get --no-install-recommends install 

# Copy the current directory contents into the container
COPY . /esg-returns

# Navigate to the project folder
WORKDIR /esg-returns

# Install the Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Make ports available to the world outside this container
EXPOSE 5432

