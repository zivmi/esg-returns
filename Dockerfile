FROM python
# Set the working directory in the container
WORKDIR /home

# Install LaTeX
RUN apt-get update && apt-get install -y \
    texlive \
    #texlive-fonts-recommended \
    texlive-latex-extra \
    texlive-bibtex-extra \
    biber \
    && rm -rf /var/lib/apt/lists/*

# Copy the current directory contents into the container
COPY . /esg-returns

# Install the Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Make ports available to the world outside this container
EXPOSE 5432
