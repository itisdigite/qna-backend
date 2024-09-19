# QNA Flask Application Setup

This repository contains the source code for a Flask-based web application with MySQL as the database, which runs inside a Docker container. This guide will walk you through setting up the project locally on Windows, Linux, and macOS.

## Prerequisites

Ensure the following software is installed on your system before proceeding:

- Python 3.10 or higher
- Docker
- Git

### Verify Installation:
- Python: `python --version`
- Docker: `docker --version`
- Git: `git --version`

---

## 1. Clone the Repository

To get started, clone the repository using Git. Open a terminal (Command Prompt/PowerShell for Windows, Terminal for Linux/macOS) and run:

```bash
git clone https://github.com/itisdigite/qna-backend.git
cd qna-backend
```

## 2. Create a virtual environment: `python3 -m venv .venv`.
### Activate the virtual environment:
    - For Windows: `.venv\Scripts\activate`.
    - For macOS/Linux: `source .venv/bin/activate`.

## 3. Install the required dependencies: `pip install -r requirements.txt`.

## 4. Set Up the MySQL Database in Docker: 
  To run the MySQL database in a Docker container, follow these steps:
    -Ensure Docker is installed and running.
    -Open a terminal and navigate to the project directory.
    -Run the following command to start the MySQL container:

    -Note: If you have mysql service running on your local system then stop it using sudo systemctl stop mysql command.

```bash
docker-compose up -d
```

## 5. Initialize the Database
  After starting the MySQL container, the next step is to initialize the database with the required tables. To do this:
  Ensure the Docker container is running (you can check with docker ps).
  Run the following command to initialize the database:

```bash
python db.py
```

## 6. Run the Flask Application
  Once the database is set up, you can start the Flask application. Ensure the virtual environment is activated and run:

  ```bash
  python login_page.py
  ```

  This will start the application on http://localhost:8000. You can now open this URL in your browser to access the app.


## Contributing
If you would like to contribute to this project, please follow these guidelines:

1. Fork the repository.
2. Create a new branch: `git checkout -b feature/your-feature-name`.
3. Make your changes and commit them: `git commit -m 'Add your feature'`.
4. Push to the branch: `git push origin feature/your-feature-name`.
5. Submit a pull request.

## License
This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for more information.
