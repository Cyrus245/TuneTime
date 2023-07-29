import requests
from dotenv import dotenv_values
from time_machine import Time_machine

config = {

    **dotenv_values('.env')

}

user_input = input("Which Year you want to travel to?Type the date in this format YYYY-MM-DD:")

# requesting billboard track list of a particular timeframe

data = requests.get(f"https://www.billboard.com/charts/hot-100/{user_input}/").text

tm = Time_machine(config=config, u_input=user_input, billboard_data=data)
