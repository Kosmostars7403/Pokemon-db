import folium
import os

from django.http import HttpResponseNotFound
from django.shortcuts import render
from pokemon_entities.models import Pokemon, PokemonEntity

MOSCOW_CENTER = [55.751244, 37.618423]
DEFAULT_IMAGE_URL = "https://vignette.wikia.nocookie.net/pokemon/images/6/6e/%21.png/revision/latest/fixed-aspect-ratio-down/width/240/height/240?cb=20130525215832&fill=transparent"


def add_pokemon(folium_map, lat, lon, name, image_url=DEFAULT_IMAGE_URL):
    icon = folium.features.CustomIcon(
        image_url,
        icon_size=(50, 50),
    )
    folium.Marker(
        [lat, lon],
        tooltip=name,
        icon=icon,
    ).add_to(folium_map)


def show_all_pokemons(request):
    pokemons = Pokemon.objects.all()
    pokemon_entities = PokemonEntity.objects.all()

    folium_map = folium.Map(location=MOSCOW_CENTER, zoom_start=12)
    for pokemon_entity in pokemon_entities:
        full_image_path = request.build_absolute_uri(pokemon_entity.pokemon.image.url)

        add_pokemon(
            folium_map, pokemon_entity.lat, pokemon_entity.lon,
            pokemon_entity.pokemon.title, full_image_path)

    pokemons_on_page = []
    for pokemon in pokemons:
        pokemons_on_page.append({
            'pokemon_id': pokemon.id,
            'img_url': pokemon.image.url,
            'title_ru': pokemon.title,
        })

    return render(request, "mainpage.html", context={
        'map': folium_map._repr_html_(),
        'pokemons': pokemons_on_page,
    })


def show_pokemon(request, pokemon_id):
    try:
        requested_pokemon = Pokemon.objects.get(id=pokemon_id)
    except Pokemon.DoesNotExist:
        return HttpResponseNotFound('<h1>Такой покемон не найден</h1>')

    pokemon_specification = {
        "title_ru": requested_pokemon.title,
        "title_en": requested_pokemon.english_title,
        "title_jp": requested_pokemon.japanese_title,
        "img_url": requested_pokemon.image.url,
        "description": requested_pokemon.description,
    }

    if requested_pokemon.previous_evolution:
        pokemon_specification['previous_evolution'] = {
            "title_ru": requested_pokemon.previous_evolution.title,
            "pokemon_id": requested_pokemon.previous_evolution.id,
            "img_url": requested_pokemon.previous_evolution.image.url
        }

    pokemon_next_evolution = requested_pokemon.evolutions.first()
    if pokemon_next_evolution:
        pokemon_specification['next_evolution'] = {
            "title_ru": pokemon_next_evolution.title,
            "pokemon_id": pokemon_next_evolution.id,
            "img_url": pokemon_next_evolution.image.url
        }

    pokemon_entities = requested_pokemon.pokemon_entities.all()

    folium_map = folium.Map(location=MOSCOW_CENTER, zoom_start=12)
    for pokemon_entity in pokemon_entities:
        full_image_path = request.build_absolute_uri(pokemon_entity.pokemon.image.url)
        add_pokemon(
            folium_map, pokemon_entity.lat, pokemon_entity.lon,
            pokemon_entity.pokemon.title, full_image_path)

    return render(request, "pokemon.html", context={'map': folium_map._repr_html_(),
                                                    'pokemon': pokemon_specification})
