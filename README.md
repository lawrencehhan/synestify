# synestify
## **Description**
Synestify analyzes a user-uploaded image and user-inputted information to recommend songs curated to reflect the image's visual cues and user's interests. The analysis matches tonal, hue, brightness, user-data, etc. to musical values accepted by Spotify's public API to utilize Spotify's recommendation engine. 

## **Technical Workflow**
Flask and Python were used to set up a web layout for receiving data, displaying recommended songs, and transforming image data into musical parameters. Upon generating musical parameters, Synestify connects to the Spotify for Developers API using the OAuth 2.0 client credentials flow. Synestify then sends HTTP calls to Spotify's recommendations endpoint to retrieve recommended song details and display results on a webpage.

## **Usage**
- Clone the repository to a local IDE
- Set up a virtual environment and run pip install -r requirements.txt to download required project packages
- Run the src/main.py file to start up a local Flask app
- Open a web browser and navigate to http://127.0.0.1:5000/ (local url) to input user music preferences and upload image
- Click submit to view the top three recommendations from Spotify's recommendation engine

## **Creators**
[Charles Chen](https://github.com/charlesyjchen) + 
[Lawrence Han](https://github.com/lawrencehhan)