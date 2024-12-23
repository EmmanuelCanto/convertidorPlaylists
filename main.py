import requests
import json
from spotipy import Spotify
from spotipy.oauth2 import SpotifyOAuth


def get_playlist_tracks():
    # Configura las credenciales de tu aplicación
    TU_CLIENT_ID = "495c95a5dbae476a8c6a1d8868dc92f5"
    TU_CLIENT_SECRET = "c55fe9b1fa9149798f03921c6187339e"
    TU_REDIRECT_URI = "http://localhost:5000/callback"
    
    # Autenticación
    auth_manager = SpotifyOAuth(
        client_id=TU_CLIENT_ID,
        client_secret=TU_CLIENT_SECRET,
        redirect_uri=TU_REDIRECT_URI,
        scope="playlist-read-private"
    )
    
    sp = Spotify(auth_manager=auth_manager)
    
    # Obtén el token de acceso
    token = auth_manager.get_access_token(as_dict=False)
    
    # Define la URL base de la playlist
    playlist_id = "5hfh0YHHuvngjgHlFTVFb0"
    url = f"https://api.spotify.com/v1/playlists/{playlist_id}/tracks"
    
    # Encabezados para la solicitud
    headers = {
        "Authorization": f"Bearer {token}"
    }
    
    all_tracks = []
    offset = 0
    limit = 100  # Spotify limita a 100 resultados por página
    
    # Paginación
    while True:
        params = {
            "offset": offset,
            "limit": limit
        }
        
        response = requests.get(url, headers=headers, params=params)
        
        if response.status_code == 200:
            data = response.json()
            items = data['items']
            
            # Guarda los datos relevantes de cada canción
            for track in items:
                track_info = {
                    "name": track['track']['name'],
                    "artist": track['track']['artists'][0]['name'],
                    "album": track['track']['album']['name'],
                    "duration_ms": track['track']['duration_ms'],
                    "url": track['track']['external_urls']['spotify']
                }
                all_tracks.append(track_info)
            
            # Verifica si hay más páginas
            if len(items) < limit:
                break  # No hay más canciones, sal del bucle
            
            offset += limit  # Incrementa el offset para la siguiente página
        
        else:
            print(f"Error: {response.status_code}, {response.json()}")
            break
    
    # Guarda todas las canciones en un archivo JSON
    with open("playlist_tracks.json", "w", encoding="utf-8") as f:
        json.dump(all_tracks, f, indent=4, ensure_ascii=False)

    print(f"Playlist guardada correctamente con {len(all_tracks)} canciones.")

# Llama a la función
get_playlist_tracks()
