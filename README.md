# synestify
Synestify analyzes a user-uploaded image and user-inputted information to recommend songs curated to reflect the image's visual cues and user's interests. The analysis matches tonal, hue, brightness, and user-data (genre selection) to musical values accepted by Spotify's public API to utilize Spotify's recommendation engine. 

## **Technical Workflow**
React was used to create a front-end user interface, and Flask and Python were used to set up an API to receive user-submissions, accessing Spotify's API, and transforming the image data into musical parameters. Upon generating musical parameters, Synestify connects to the Spotify for Developers API using the OAuth 2.0 client credentials flow. Synestify then sends HTTP calls to Spotify's recommendations endpoint to retrieve recommended song details and display results on a webpage. 

**Example Input Page**

![Sample Input Page](tests/assets/example_input_page.jpg?raw=true "Sample Input Page")

**Example Output Page**

![Sample Output Page](tests/assets/example_output_page.jpg?raw=true "Sample Output Page")

## **Usage**
- **REQUIREMENT: You must have a Spotify account (free or paid plan)**
### Part 1
- Log into the [Spotify Developer](https://developer.spotify.com/dashboard/) page (anyone with a Spotify account can log in)
- Click on "Create An App" and enter an app name (ex. Synestify)
- Save the Client ID and Client Secret on the left side of the page

### Part 2
- Clone the Synestify repository to a local IDE
- Set up a virtual environment and run `pip install -r requirements.txt` in your terminal to download required project packages
- Create a duplicate of the `.env.example` file within the repository and rename it `.env`
- Replace the `CLIENT_ID` and `CLIENT_SECRET` values with the saved values from Part 1
- Run the `synestify/src/main.py` file to start up a local Flask app
- Run the React app found in the frontend directory (via 'npm start')
- Select the genre to receive song recommmendations for
- Click submit to view the top 12 song recommendations based on the parameters and image you provided!

## **Creators**
[Charles Chen](https://github.com/charlesyjchen) + 
[Lawrence Han](https://github.com/lawrencehhan)
