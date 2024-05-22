FROM python:3.12

RUN pip install pipenv

# Copy the application files
COPY ./src /opt/app/
COPY Pipfile /opt/app/
COPY Pipfile.lock /opt/app/

# Set the working directory
WORKDIR /opt/app/

# Install dependencies
RUN pipenv install --ignore-pipfile

EXPOSE 8000

CMD ["pipenv", "run", "uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]