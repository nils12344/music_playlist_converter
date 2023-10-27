import streamlit as st
from PIL import Image
import pandas as pd

import streamlit as st
from streamlit import components
import urllib.request 


from ytmusicapi import YTMusic
import spotipy
import helper_functions as hf

youtube_pic = "https://tubesights.de/wp-content/uploads/2018/06/YouTube_Music_Logo_Header.jpg"
urllib.request.urlretrieve(youtube_pic, "youtube_pic.png") 
image = Image.open("youtube_pic.png")
youtube_pic = image.resize((600, 300))

spotify_pic = "https://fiverr-res.cloudinary.com/images/q_auto,f_auto/gigs/334184780/original/e35b7c83e16677b2e5f305376975dfa083276128/upload-your-music-or-song-in-spotify-all-digital-platforms.jpg"
urllib.request.urlretrieve(spotify_pic, "spotify_pic.png") 
image = Image.open("spotify_pic.png")
spotify_pic = image.resize((600, 300))

coming_soon_pic =  "https://media.istockphoto.com/id/984996502/de/vektor/kommen-bald-vektor-template-design.jpg?s=612x612&w=0&k=20&c=jGDi0WGAcP4qtm3yLs1z6kPwBvAMgXRsWMfK7RQD5XU="
urllib.request.urlretrieve(coming_soon_pic, "coming_soon_pic.png") 
image = Image.open("coming_soon_pic.png")
coming_soon_pic = image.resize((600, 300))

arrow_pic = "https://static.vecteezy.com/system/resources/previews/008/490/277/non_2x/hand-drawn-arrow-clipart-free-png.png"
# urllib.request.urlretrieve(arrow_pic, "arrow_pic.png") 
# image = Image.open("arrow_pic.png")
# arrow_pic = image.resize((600, 400))



def main():
    st.title('Playlist Converter')

    st.write('## Step 1: Select Platforms')

    col1, col2, col3 = st.columns(3)

    with col1:
        selected_picture_1 = st.radio('',
                                     ('Youtube Music', 'Spotify', 'More coming soon'),
                                     key='selection1')
        if selected_picture_1 == 'Youtube Music':
            st.image(youtube_pic,
                     caption='Youtube Music',
                     width=200,
                     use_column_width=True)
        elif selected_picture_1 == 'Spotify':
            st.image(spotify_pic,
                     caption='Spotify',
                     width=200,
                     use_column_width=True)
        elif selected_picture_1 == 'More coming soon':
            st.image(coming_soon_pic,
                     caption='More coming soon',
                     width=200,
                     use_column_width=True)
    
    with col2:
        #st.write('→')  # Arrow pointing to the other field
        st.image(arrow_pic,width=200, use_column_width=True)


    with col3:
        selected_picture_2 = st.radio('',
                                     ('Youtube Music', 'Spotify', 'More coming soon'),
                                     key='selection2')
        if selected_picture_2 == 'Youtube Music':
            st.image(youtube_pic,
                     caption='Youtube Music',
                     width=200,  
                     use_column_width=True)
        elif selected_picture_2 == 'Spotify':
            st.image(spotify_pic,
                     caption='Spotify',
                     width=200,
                     use_column_width=True)

        elif selected_picture_2 == 'More coming soon':
            st.image(coming_soon_pic,
                     caption='More coming soon',
                     width=200,
                     use_column_width=True)

    
    st.write('## Step 2: Setup Spotify and Youtube Music API')
    if selected_picture_1 == 'Spotify' and selected_picture_2 == 'Youtube Music':
        col1, col2 = st.columns(2)
        with col1: 
            st.write("Spotify Setup:")
            client_id = st.text_input('Client ID:', '')
            client_secret = st.text_input('Client Secret:', '')
        with col2: 
            st.write("Youtube Setup:")
            # if st.button("Create OAUTH file"):
            #     from ytmusicapi.auth import oauth
            #     oauth
            oauth_string = st.text_input("Paste OAUTH here.")
             
            #path_to_oauth = st.file_uploader("Outh.json file:",type="json")
            #st.text_input("Path to 'oauth.json' file: ")
        if not client_id or not client_secret:
            st.write("### Someting is missing. Please check Client ID or Client Secret.")
            st.write("How to find Client ID and Client Secret:")
            st.write("https://stevesie.com/docs/pages/spotify-client-id-secret-developer-api")
        elif not oauth_string:# or not path_to_oauth:
            st.write("### Someting is missing. Please create oauth.json and upload it.")
            st.write("How to create 'oauth.json' file:")
            st.write("")
        else:
            # connect spotify api 
            auth_manager = spotipy.oauth2.SpotifyClientCredentials(client_id=client_id, client_secret=client_secret)
            sp = spotipy.Spotify(auth_manager=auth_manager)

            # import json
            # oauth_json = json.load(path_to_oauth)
            # st.write(path_to_oauth)
            # st.write(oauth_json)
            # connect ytmusic
            yt = YTMusic(oauth_string)


            st.write("## Step 3: Input Spotify Playlist Link")
            spotify_playlist_link = st.text_input('Spotify Playlist Link', '')
            st.write(spotify_playlist_link)

            if "spotify.com" in spotify_playlist_link:
                st.write("## Step 4:")

                #
                try: 
                    spotify_playlist = sp.playlist(spotify_playlist_link)
                    name = spotify_playlist["name"]
                    description = spotify_playlist["description"]
                    tracks = spotify_playlist["tracks"]["items"]
                    br = hf.build_results(tracks)
                    df_br = pd.DataFrame(br)
                    st.write(df_br)
                except: 
                    st.error("Wrong Client ID and/or Client Secret!")
                #st.write("## Step 5: Youtube Songs:")

                # with st.spinner("waiting"):
                #     a = yt.search("Calvin Harris Feel so Close")
                #     vidIDS, results = hf.search_songs(yt_class=yt, tracks = br, limiter=5)
                # st.write(a)
                st.write("## Step 5: Add to new or existing YT Playlist")
                with st.spinner("waiting to load VidIds"):
                    vidIDS = hf.search_songs(yt_class=yt, tracks = br, limiter=0)

                all_playlists = yt.get_library_playlists()
                filtered_playlists = {}
                for playlist in all_playlists: 
                    filtered_playlists[playlist["title"]]=playlist["playlistId"]
                # Add an element as the first element
                new_element = {'NEW PLAYLIST': "NEW PLAYLIST"}
                filtered_playlists = {**new_element, **filtered_playlists}


                selected_option = st.selectbox('Select a playlist', list(filtered_playlists.keys()))
                if selected_option=="NEW PLAYLIST":
                    new_playlist_name_for_yt = st.text_input("Name of new Youtube Playlist:",'')
                    playlistId = yt.create_playlist(new_playlist_name_for_yt, "Converted from Spotify --- Spotify description: "+description)
                    yt.add_playlist_items(playlistId, vidIDS)
                else:
                    yt.add_playlist_items(filtered_playlists[selected_option], vidIDS)
                
                st.write("Succesfully converted!")


            elif not spotify_playlist_link:
                st.error("Please insert a Spotify Playlist Link") 
            else:
                st.error("Not a real Spotify link")



    
    else:
        st.write("coming soon")
        st.write("To use playlist converter select combination: Spotify --> Youtube")

    
if __name__ == '__main__':
    main()
