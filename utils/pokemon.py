import logging
import requests
from typing import Tuple
from bs4 import BeautifulSoup


logger = logging.getLogger(__file__)


def find_pokemon_name(pokemon_name):
    # Find pokemon zh-hant name
    res = requests.get(
        'https://tw.portal-pokemon.com/play/pokedex/api/v1?key_word='+pokemon_name)
    logger.debug('Find pokemon name is: '+pokemon_name)
    result = res.json()['pokemons']
    if not result:
        logger.info('Could not find TW name: ' + pokemon_name)
        return pokemon_name, None
    else:
        return result[0]['pokemon_name'], result[0]['pokemon_type_name']


def find_pokemon_body(height: float, weight: float, tolerance: float = 0.1):
    """
    Find Pokémon with height and weight close to the given values.
    Dynamically increase tolerance if no Pokémon is found.
    :param height: Height of the Pokémon in centimeters.
    :param weight: Weight of the Pokémon in kilograms.
    :param tolerance: Initial percentage tolerance for matching height and weight.
    :return: List of Pokémon with similar height and weight.
    """
    url = "https://tw.portal-pokemon.com/play/pokedex/api/v1?a=1"
    try:
        response = requests.get(url)
        response.raise_for_status()  # Raise an exception for HTTP errors
        data = response.json()
        all_pokemon = data.get("pokemons", [])
        if not all_pokemon:
            logger.warning("No Pokémon data found in the API response.")
            return []
    except requests.RequestException as e:
        logger.error(f"Failed to fetch Pokémon data: {e}")
        return []

    nearby_pokemon = []
    current_tolerance = tolerance

    while not nearby_pokemon and current_tolerance <= 1.0:  # Cap tolerance at 100%
        for pokemon in all_pokemon:
            try:
                pokemon_height_cm = float(pokemon["height"]) * 100  # Convert Pokémon height to centimeters
                pokemon_weight = float(pokemon["weight"])

                if (abs(pokemon_height_cm - height) / height <= current_tolerance and
                        abs(pokemon_weight - weight) / weight <= current_tolerance):
                    nearby_pokemon.append({
                        "name": pokemon["pokemon_name"],
                        "height": pokemon_height_cm,  # Keep height in centimeters
                        "weight": pokemon_weight
                    })
            except (KeyError, ValueError) as e:
                logger.warning(f"Skipping invalid Pokémon data: {e}")

        if not nearby_pokemon:
            logger.info(f"No Pokémon found with tolerance {current_tolerance}. Increasing tolerance.")
            current_tolerance += 0.1  # Increment tolerance by 10%

    return nearby_pokemon


def pokemon_wiki(pokemon_name, language='zh'):
    url = "https://wiki.52poke.com/{}/{}".format(
        'zh-hant',
        '%E5%AE%9D%E5%8F%AF%E6%A2%A6%E5%88%97%E8%A1%A8%EF%BC%88%E5%9C%A8%E5%85%B6%E4%BB%96%E8%AF%AD%E8%A8%80%E4%B8%AD%EF%BC%89')
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    pokemon_table = soup.select('table')[1]
    pokemon_rows = pokemon_table.select('tr')[2:]

    for row in pokemon_rows:
        if language == 'en':
            name = row.select('td')[7].text
        elif language == 'jp':
            name = row.select('td')[6].text
        else:
            name = row.select('td')[2].text

        if pokemon_name in name:
            logger.debug(f"Found Pokemon '{pokemon_name}'")
            return row

    logger.debug("Pokemon '{}' not found in wiki".format(pokemon_name))
    return None


def find_pokemon_image(pokemon_row_list: BeautifulSoup) -> Tuple[str, str]:
    eng_name = pokemon_row_list.select('td')[7].text.rstrip()
    poke_image_name = "".join(eng_name.replace("-", "")).lower()
    poke_img = f'https://play.pokemonshowdown.com/sprites/gen5/{poke_image_name}.png'
    logger.debug(f'Pokemon image url is: {poke_img}')
    return eng_name, poke_img


def find_pokemon_image_from_api(pokemon_name: str) -> str:
    """
    Fetch the Pokémon image URL using the English name from the API.
    :param pokemon_name: Name of the Pokémon.
    :return: Image URL of the Pokémon.
    """
    url = f"https://tw.portal-pokemon.com/play/pokedex/api/v1?key_word={pokemon_name}"
    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        pokemons = data.get("pokemons", [])
        if pokemons:
            img_url = pokemons[0].get("file_name", "")
            if img_url:
                return f'https://tw.portal-pokemon.com/play/resources/pokedex{img_url}'
            else:
                logger.warning(f"No English name found for Pokémon: {pokemon_name}")
                return ""
        else:
            logger.warning(f"No Pokémon data found for: {pokemon_name}")
            return ""
    except requests.RequestException as e:
        logger.error(f"Failed to fetch Pokémon image from API: {e}")
        return ""


def arrange_text(text: str):
    return list(filter(None, text.rstrip().split('\n')))
