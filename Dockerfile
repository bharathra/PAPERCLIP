# Use a modern and secure Python base image
FROM python:3.9-slim

# Set the working directory
WORKDIR /app

# Install system dependencies for PyQt6 and GUI support
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    libglib2.0-0 \
    libgl1 \
    libegl1 \
    libfontconfig1 \
    libfreetype6 \
    libharfbuzz0b \
    libpng16-16 \
    libjpeg62-turbo \
    libsm6 \
    libxext6 \
    libxrender1 \
    libxkbcommon-x11-0 \
    libxkbcommon0 \
    libxcb-icccm4 \
    libxcb-image0 \
    libxcb-keysyms1 \
    libxcb-randr0 \
    libxcb-render-util0 \
    libxcb-shape0 \
    libxcb-xfixes0 \
    libxcb-xinerama0 \
    libxcb-xkb1 \
    libdbus-1-3 \
    && rm -rf /var/lib/apt/lists/*

# Copy project files
COPY . .

# Install pdm and project dependencies
# We use --no-cache-dir to reduce image size
RUN pip install --no-cache-dir pdm PyQt6
RUN pdm install --prod --no-editable

# Set an entrypoint that allows running scripts or an interactive shell
ENTRYPOINT ["pdm", "run"]

