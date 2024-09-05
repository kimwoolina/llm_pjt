# RealTimeWeatherBot
A chatbot website that leverages **OpenAI's GPT model** and the **KMA (Korea Meteorological Administration) API** to provide real-time weather information. Users can input weather-related queries on the website, and the chatbot fetches the latest weather data through the KMA API to provide real-time responses.

<br>

## TechStack
- :art: **Front-End**

  - **Language**
    - ![HTML5](https://img.shields.io/badge/HTML5-E34F26?style=for-the-badge&logo=html5&logoColor=white) ![CSS3](https://img.shields.io/badge/CSS3-1572B6?style=for-the-badge&logo=css3&logoColor=white)

      <br>
      
- :computer: **Back-End**

  - **Language**
    - ![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=Python&logoColor=white)

  - **Framework**
    - ![Django](https://img.shields.io/badge/Django-092E20?style=for-the-badge&logo=django&logoColor=white)

<br>

- :cloud: **APIs**

  - **Language Model**
    - ![OpenAI](https://img.shields.io/badge/OpenAI-GPT-000000?style=for-the-badge&logo=openai&logoColor=white)

  - **Weather Data**
    - ![KMA](https://img.shields.io/badge/KMA-Weather-005B8A?style=for-the-badge&logo=kma&logoColor=white)

<br><br>

## Setup

To set up and run the project, follow these steps:

1. **Clone the project repository:**

    ```bash
    git clone https://github.com/kimwoolina/llm_pjt.git
    ```

2. **Navigate to the project directory:**

    ```bash
    cd /Users/YourPC/Your_Cloned_Folder/llm_pjt/
    ```

3. **Install the required dependencies:**

    ```bash
    pip install -r requirements.txt
    ```

4. **Create and configure the `config.py` file:**

    Create a file named `config.py` in the project root directory and add the following content:

    ```python
    # config.py

    DJANGO_SECRET_KEY = "your_django_secret_key_here"

    OPENAI_API_KEY = "your_openai_api_key_here"

    # Weather API
    SERVICE_KEY = "your_weather_api_key_here"
    ```

5. **Configure the Django settings:**

    Update the `settings.py` file in your Django project to include the configuration from `config.py`:

    ```python
    from . import config

    SECRET_KEY = config.DJANGO_SECRET_KEY
    OPEN_API_KEY = config.OPENAI_API_KEY
    SERVICE_KEY = config.SERVICE_KEY
    ```

6. **Apply database migrations:**

    ```bash
    python manage.py makemigrations
    python manage.py migrate
    ```

7. **Run the development server:**

    ```bash
    python manage.py runserver
    ```

8. **Open your browser and visit:**

    [http://127.0.0.1:8000/](http://127.0.0.1:8000/)

<br><br>

## RESTful API Specification

| Name          | Endpoint                | Method | Description                                                 |
|---------------|--------------------------|--------|-------------------------------------------------------------|
| Weather Query | `/chatgpt/weather-chat/` | POST   | Endpoint for sending weather-related queries to the chatbot. The chatbot retrieves real-time weather data from the KMA API and provides a response. |

