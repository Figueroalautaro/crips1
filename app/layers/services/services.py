# capa de servicio/lógica de negocio

from ..transport import transport
from ..persistence import repositories
from ..utilities import translator
from django.contrib.auth import get_user


# función que devuelve un listado de cards. Cada card representa una imagen de la API de HP.
import random
from ..utilities.translator import fromRequestIntoCard
def getAllImages():
    
    raw_images = transport.getAllImages()  # 1) Traemos el listado de  las imágenes crudas desde la API
    
    
    cards = []  # 2) Convertimos cada imagen en una card vacia
    
    for character in raw_images:
        card = fromRequestIntoCard(character) #Convertimos la imagen cruda en una card
        
        if not card.alternate_names:
            card.alternate_names = "no tiene nombre alternativo"
        
        else:
            card.alternate_names = random.choice(card.alternate_names)
        
        cards.append(card) # 3) Añadimos la card al nuevo listado de cards
        
    return cards  #retorna el listado de las cards
    



# función que filtra según el nombre del personaje.
def filterByCharacter(name):
    filtered_cards = []

    for card in getAllImages():
        # debe verificar si el name está contenido en el nombre de la card, antes de agregarlo al listado de filtered_cards.
        if name.lower() in card.name.lower():
            filtered_cards.append(card)

    return filtered_cards

# función que filtra las cards según su casa.
def filterByHouse(house_name):
    filtered_cards = []

    for card in getAllImages():
        # debe verificar si la casa de la card coincide con la recibida por parámetro. Si es así, se añade al listado de filtered_cards.
        filtered_cards.append(card)

    return filtered_cards

# añadir favoritos (usado desde el template 'home.html')
def saveFavourite(request):
    fav = '' # transformamos un request en una Card (ver translator.py)
    fav.user = get_user(request) # le asignamos el usuario correspondiente.

    return repositories.save_favourite(fav) # lo guardamos en la BD.

# usados desde el template 'favourites.html'
def getAllFavourites(request):
    if not request.user.is_authenticated:
        return []
    else:
        user = get_user(request)

        favourite_list = [] # buscamos desde el repositories.py TODOS Los favoritos del usuario (variable 'user').
        mapped_favourites = []

        for favourite in favourite_list:
            card = '' # convertimos cada favorito en una Card, y lo almacenamos en el listado de mapped_favourites que luego se retorna.
            mapped_favourites.append(card)

        return mapped_favourites

def deleteFavourite(request):
    favId = request.POST.get('id')
    return repositories.delete_favourite(favId) # borramos un favorito por su ID
