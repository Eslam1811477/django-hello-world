from dotenv import load_dotenv
import os

load_dotenv()



env_data = {
    'SECRET_KEY': os.environ.get('SECRET_KEY')
}




