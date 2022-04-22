import folium

from django.http import HttpResponseNotFound
from django.shortcuts import render

from pokemon_entities.models import (Pokemon, PokemonEntity)


MOSCOW_CENTER = [55.751244, 37.618423]
DEFAULT_IMAGE_URL = (
    'https://vignette.wikia.nocookie.net/pokemon/images/6/6e/%21.png/revision'
    '/latest/fixed-aspect-ratio-down/width/240/height/240?cb=20130525215832'
    '&fill=transparent'
)
POKEMON_DEFAULT_IMAGE = 'images/Question_mark.png'


def add_pokemon(folium_map, lat, lon, image_url=DEFAULT_IMAGE_URL):
    icon = folium.features.CustomIcon(
        image_url,
        icon_size=(50, 50),
    )
    folium.Marker(
        [lat, lon],
        # Warning! `tooltip` attribute is disabled intentionally
        # to fix strange folium cyrillic encoding bug
        icon=icon,
    ).add_to(folium_map)


def show_all_pokemons(request):
    pokemons = PokemonEntity.objects.all()
    folium_map = folium.Map(location=MOSCOW_CENTER, zoom_start=12)
    for pokemon in pokemons:
        if not pokemon.Pokemon.image:
            pokemon.Pokemon.image = POKEMON_DEFAULT_IMAGE
        add_pokemon(
            folium_map, pokemon.Lat,
            pokemon.Lon,
            request.build_absolute_uri('/media/' + str(pokemon.Pokemon.image))
        )

    pokemons_on_page = []
    pokemon_objects = Pokemon.objects.all()
    for pokemon in pokemon_objects:
        if not pokemon.image:
            pokemon.image = POKEMON_DEFAULT_IMAGE
        pokemons_on_page.append({
            'pokemon_id': pokemon.id,
            'img_url': request.build_absolute_uri('/media/' + str(pokemon.image)),
            'title_ru': pokemon.title,
        })

    return render(request, 'mainpage.html', context={
        'map': folium_map._repr_html_(),
        'pokemons': pokemons_on_page,
    })


def show_pokemon(request, pokemon_id):
    requested_pokemon = Pokemon.objects.get(id=int(pokemon_id))
    try:
        pokemons = PokemonEntity.objects.filter(Pokemon=requested_pokemon)
    except PokemonEntity.DoesNotExist:
        return HttpResponseNotFound('<h1>Такой покемон не найден</h1>')
    folium_map = folium.Map(location=MOSCOW_CENTER, zoom_start=12)
    for pokemon in pokemons:
        if not pokemon.Pokemon.image:
            pokemon.Pokemon.image = POKEMON_DEFAULT_IMAGE
        add_pokemon(
            folium_map, pokemon.Lat,
            pokemon.Lon,
            request.build_absolute_uri('/media/' + str(pokemon.Pokemon.image))
        )
    pokemon_next_evolutions = requested_pokemon.next_evolutions.first()
    pokemon_previous_evolution = requested_pokemon.previous_evolution
    if not requested_pokemon.image:
        requested_pokemon.image = POKEMON_DEFAULT_IMAGE
    images = {
        'pokemon_image': request.build_absolute_uri('/media/' + str(requested_pokemon.image)),
        'next_pokemon_image': request.build_absolute_uri('/media/' + str(pokemon_next_evolutions.image)) if pokemon_next_evolutions else '',
        'prev_pokemon_image': request.build_absolute_uri('/media/' + str(pokemon_previous_evolution.image)) if pokemon_previous_evolution else '',
    }
    return render(request, 'pokemon.html', context={
        'map': folium_map._repr_html_(),
        'pokemon': requested_pokemon,
        'pokemon_next_evolutions': pokemon_next_evolutions,
        'pokemon_previous_evolution': pokemon_previous_evolution,
        'images': images,
})
