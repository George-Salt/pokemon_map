import folium

from django.shortcuts import render, get_list_or_404, get_object_or_404
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
    active_pokemons_entities = pokemons_entities.filter(
        appeared_at__lt=localtime(),
        disappeared_at__gt=localtime()
    )

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
            'pokemon_id': pokemon.pk,
            'img_url': request.build_absolute_uri(pokemon.image.url),
            'title_ru': pokemon.title_ru,
        })

    return render(request, 'mainpage.html', context={
        'map': folium_map._repr_html_(),
        'pokemons': pokemons_on_page,
    })


def show_pokemon(request, pokemon_id):
    requested_pokemon = get_object_or_404(Pokemon, id=pokemon_id)
    requested_pokemon_entities = get_list_or_404(
        PokemonEntity,
        appeared_at__lt=localtime(),
        disappeared_at__gt=localtime(),
        pokemon=pokemon_id
    )

    folium_map = folium.Map(location=MOSCOW_CENTER, zoom_start=12)
    pokemon_specs = {
        'pokemon_id': requested_pokemon.pk,
        'entities': [],
        'img_url': request.build_absolute_uri(requested_pokemon.image.url),
        'title_ru': requested_pokemon.title_ru,
        'title_en': requested_pokemon.title_en,
        'title_jp': requested_pokemon.title_jp,
        'description': requested_pokemon.description
    }

    if requested_pokemon.previous_evolutions:
        pokemon_specs['previous_evolution'] = {
            'title_ru': requested_pokemon.previous_evolutions.title_ru,
            'pokemon_id': requested_pokemon.previous_evolutions.pk,
            'img_url': request.build_absolute_uri(
                requested_pokemon.previous_evolutions.image.url
            )
        }
    next_evolutions = requested_pokemon.next_evolutions.all()
    if next_evolutions:
        for evolution in next_evolutions:
            pokemon_specs['next_evolution'] = {
                'title_ru': evolution.title_ru,
                'pokemon_id': evolution.pk,
                'img_url': request.build_absolute_uri(evolution.image.url)
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
