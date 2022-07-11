# Flask App with Admin

A Flask app made with HTML5, Bootstrap, Python, and Flask with templating by Jinja.
App is containerized with Docker for portability.
Production environment uses nginx as a reverse proxy to enable SSL

## Installation

Make sure you have `docker` and `docker-compose` installed.

## Usage

Create a .env file using the example.env template (make a copy using the variables inside of the template)

Start Development Server
```bash
$ docker compose -f docker-compose.dev.yml up -d
```

Stop Development Server
```bash
$ docker compose -f docker-compose.dev.yml down
```

Start Production Server
```bash
$ docker compose -f docker-compose.prod.yml up -d --build
```

Stop Production Server
```bash
$ docker compose -f docker-compose.prod.yml down
```


For Development you'll be able to access `localhost:5000` or `127.0.0.1:5000` in the browser! 


## Contributing

Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.
