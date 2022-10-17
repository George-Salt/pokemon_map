import folium
import json

from django.http import HttpResponseNotFound
from django.shortcuts import render
from django.utils.timezone import localtime
from .models import Pokemon, PokemonEntity


MOSCOW_CENTER = [55.751244, 37.618423]
DEFAULT_IMAGE_URL = (
    'https://vignette.wikia.nocookie.net/pokemon/images/6/6e/%21.png/revision'
    '/latest/fixed-aspect-ratio-down/width/240/height/240?cb=20130525215832'
    '&fill=transparent'
)


def add_pokemon(folium_map, lat, lon, image_url=DEFAULT_IMAGE_URL):
    icon = folium.features.CustomIcon(
        image_url,
        icon_size=(50, 50),
    )
    folium.Marker(
        [lat, lon],
        icon=icon,
    ).add_to(folium_map)


def show_all_pokemons(request):
    pokemons_objects = Pokemon.objects.all()
    pokemons_entities = PokemonEntity.objects.all()
    active_pokemons_entities = pokemons_entities.filter(appeared_at__lt=localtime(), disappeared_at__gt=localtime())

    folium_map = folium.Map(location=MOSCOW_CENTER, zoom_start=12)
    for pokemon_entity in active_pokemons_entities:
        add_pokemon(
            folium_map, pokemon_entity.lat,
            pokemon_entity.lon,
            request.build_absolute_uri(pokemon_entity.pokemon.image.url)
        )

    pokemons_on_page = []
    for pokemon in pokemons_objects:
        pokemons_on_page.append({
            'pokemon_id': pokemon.id,
            'img_url': request.build_absolute_uri(pokemon.image.url),
            'title_ru': pokemon.title,
        })

    return render(request, 'mainpage.html', context={
        'map': folium_map._repr_html_(),
        'pokemons': pokemons_on_page,
    })


def show_pokemon(request, pokemon_id):
    pokemons_objects = Pokemon.objects.all()
    pokemons_entities = PokemonEntity.objects.all()
    active_pokemons_entities = pokemons_entities.filter(appeared_at__lt=localtime(), disappeared_at__gt=localtime())

    for pokemon in pokemons_objects:
        if pokemon.id == int(pokemon_id):
            requested_pokemon_entities = active_pokemons_entities.filter(pokemon=pokemon)
            break
        else:
            return HttpResponseNotFound('<h1>Такой покемон не найден</h1>')

    folium_map = folium.Map(location=MOSCOW_CENTER, zoom_start=12)
    for entity in requested_pokemon_entities:
        pokemon = {
            'pokemon_id': entity.pokemon.id,
            'lat': entity.lat,
            'lon': entity.lon,
            'img_url': request.build_absolute_uri(entity.pokemon.image.url),
            'title_ru': entity.pokemon.title,
        }
        add_pokemon(
            folium_map, pokemon["lat"],
            pokemon["lon"],
            pokemon["img_url"]
        )

    return render(request, 'pokemon.html', context={
        'map': folium_map._repr_html_(), 'pokemon': pokemon
    })
