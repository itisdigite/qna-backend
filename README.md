This repository contains the backend code for the QNA project.

## Installation for application side
To get started, make sure you have Python 3.x installed on your machine. Then, follow these steps:

1. Clone this repository to your local machine.
2. Navigate to the project directory: `cd qna-backend`.
3. Create a virtual environment: `python3 -m venv .venv`.
4. Activate the virtual environment:
    - For Windows: `.venv\Scripts\activate`.
    - For macOS/Linux: `source .venv/bin/activate`.
5. Install the required dependencies: `pip install -r requirements.txt`.

## Installation for DB side
1. Install mysql servers - $sudo apt-get install mysql-server
2. We need to create one user for our DB
    $sudo mysql
    $CREATE USER 'qnauser'@'localhost' IDENTIFIED BY 'Pass@000';
    $GRANT ALL PRIVILEGES ON qna.* TO 'qnauser'@'localhost';
    $FLUSH PRIVILEGES;


## Now to run application go to qna-backend and run login_page.py
To run the backend server, execute the following command:

```bash
python login_page.py 
```

The server will start running on `http://localhost:8000`.

## Contributing
If you would like to contribute to this project, please follow these guidelines:

1. Fork the repository.
2. Create a new branch: `git checkout -b feature/your-feature-name`.
3. Make your changes and commit them: `git commit -m 'Add your feature'`.
4. Push to the branch: `git push origin feature/your-feature-name`.
5. Submit a pull request.

## License
This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for more information.
