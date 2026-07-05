# 1. Start with a base image
# We use an official Python image from Docker Hub. 'python:3.9-slim' is a lightweight
# version of Python 3.9, which is great for production as it reduces the final image size.
FROM python:3.13-slim

# 2. Set the working directory inside the container
# This command sets the default directory for all subsequent commands (like COPY and RUN).
# It's a best practice to keep your application code in a dedicated directory.
WORKDIR /app

# 3. Copy the requirements file and install dependencies
# We copy the requirements file first. Docker builds in layers, and this is an
# optimization. If our Python code changes but our requirements don't, Docker can
# reuse the cached layer with all the installed packages, making future builds much faster.
COPY requirements.txt .

# RUN executes a command during the build process. Here, we're installing all the
# Python packages listed in our requirements.txt file.
# The '--no-cache-dir' flag tells pip not to store the download cache, which helps
# keep the final image size smaller.
RUN pip install --no-cache-dir -r requirements.txt

# This is a critical step for NLTK. In a non-interactive environment like a Docker
# container, we can't have our Python script try to download data. We must download
# it during the build process itself so it's included in the image.
RUN python -m nltk.downloader stopwords wordnet

# 4. Copy the rest of the application code
# The first '.' refers to the current directory on your host machine (where the Dockerfile is).
# The second '.' refers to the current working directory inside the container, which we
# set to '/app' with the WORKDIR command. This copies app.py, the .pkl files, etc.
COPY . .

# 5. Expose the port the app runs on
# This command informs Docker that the container will listen on port 5000 at runtime.
# This is mainly for documentation and inter-container communication; it doesn't actually
# publish the port to the host machine.
EXPOSE 5000

# 6. Define the command to run the application
# This is the command that will be executed when the container starts.
# We use 'gunicorn' to run our production-ready server.
# 'app:app' means: in the file 'app.py', find the Flask instance named 'app'.
# '--bind 0.0.0.0:5000' tells gunicorn to listen on all network interfaces on port 5000,
# which is necessary for the container to be reachable from the outside.
CMD ["gunicorn", "--bind", "0.0.0.0:5000", "app:app"]
