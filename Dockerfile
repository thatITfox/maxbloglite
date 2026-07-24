FROM python:3.13
WORKDIR /usr/local/app

# Copy the application code
COPY . .

# Install the application dependencies
RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 80

# Start the application
CMD ["python", "app.py"]