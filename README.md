## Installation

### Cloning the Repository

1. **Install Git from the official website: [https://git-scm.com/downloads](https://git-scm.com/downloads)**

2. **Open a terminal.**

3. **Clone the repository to your local directory.**

```
git clone https://github.com/akkalame/file_manipulation.git
```

4. **Navigate to the project directory.**

```
cd file_manipulation
```

### Creating the Virtual Environment

5. **Create a Python virtual environment.**

```
python -m venv env
```

6. **Activate the virtual environment.**

**Windows:**

```
env\Scripts\activate
```

**Linux and Mac:**

```
source env/bin/activate
```

### Installing Dependencies

7. **Install the requirements from the `requirements.txt` file.**

```
pip install -r requirements.txt
```

### Running the Program

8. **Run the program.**

```
flask run
```

### Note

If you get an error that the port is already in use when you run `flask run`, you can change it using the `--port` flag. For example:

```
flask run --port 8000
```

Open your web browser and navigate to the address `http://localhost:8000`.

### Support

If you need help with this program, you can create an issue in the following repository:

[https://github.com/akkalame/file_manipulation](https://github.com/akkalame/file_manipulation)