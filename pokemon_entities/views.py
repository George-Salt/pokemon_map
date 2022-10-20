import folium
import json

from django.core.exceptions import ObjectDoesNotExist
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

    try:
        requested_pokemon = pokemons_objects.get(id=pokemon_id)
    except ObjectDoesNotExist:
        return '<h1>Такой покемон не найден</h1>'

    try:
        requested_pokemon_entities = active_pokemons_entities.filter(pokemon=pokemon_id)
    except ObjectDoesNotExist:
        return '<h1>Такой покемон не найден</h1>'

    folium_map = folium.Map(location=MOSCOW_CENTER, zoom_start=12)
    pokemon_specs = {
        'pokemon_id': requested_pokemon.id,
        'entities': [],
        'img_url': request.build_absolute_uri(requested_pokemon.image.url),
        'title_ru': requested_pokemon.title,
        'description': requested_pokemon.description,
    }

    for entity in requested_pokemon_entities:
        pokemon_entity = {
            'lat': entity.lat,
            'lon': entity.lon
        }
        add_pokemon(
            folium_map, pokemon_entity['lat'],
            pokemon_entity['lon'],
            pokemon_specs['img_url']
        )
        pokemon_specs['entities'].append(pokemon_entity)

    return render(request, 'pokemon.html', context={
        'map': folium_map._repr_html_(), 'pokemon': pokemon_specs
    })
