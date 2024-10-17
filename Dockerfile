# Use an official Python runtime as the base image
FROM python:3.9-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV DJANGO_ALLOWED_HOSTS=0.0.0.0
# ENV ALLOWED_ORIGIN=https://fcccolumbus.com
ENV SECRET_KEY="Pf+6tX!5CWTcCK}3N"
ENV API_KEY="s*2NQT2!iT4uhr&'q"
ENV MEETUP_ID="276932425"
ENV MEETUP_EXPORT_URL="https://www.meetup.com/techlifecolumbus/events/ical/"


# Set the working directory in the container
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
COPY requirements.txt .
RUN pip install --upgrade pip && pip install -r requirements.txt

# Install Gunicorn
RUN pip install gunicorn

# Copy the project code into the container
COPY . .

# Collect static files
RUN python MeetupUpdateAPI/manage.py collectstatic --noinput

# Run the application
CMD ["gunicorn", "--chdir", "MeetupUpdateAPI", "--bind", "0.0.0.0:8000", "MeetupUpdateAPI.wsgi:application"]

