"""Live public accommodation metadata collection service for StayWise.

Uses OpenStreetMap Nominatim for city lookup and Overpass for public place tags.
It deliberately does not collect guest-review text or bypass access controls.
"""
from fastapi import HTTPException
import requests
from datetime import datetime, timezone

NOMINATIM_URL = "https://nominatim.openstreetmap.org/search"
OVERPASS_URL = "https://overpass-api.de/api/interpreter"
SCRAPER_HEADERS = {"User-Agent": "StayWiseStudentProject/1.0 (educational hotel-rating demo)"}

def _city_bounds(city: str):
    response = requests.get(
        NOMINATIM_URL,
        params={"q": city + ", India", "format": "jsonv2", "limit": 1},
        headers=SCRAPER_HEADERS,
        timeout=30,
    )
    response.raise_for_status()
    places = response.json()
    if not places:
        raise HTTPException(404, f"Could not find the city '{city}'. Try Mumbai, Delhi, Jaipur, Goa, Udaipur or Bengaluru.")
    south, north, west, east = map(float, places[0]["boundingbox"])
    display_name = places[0].get("display_name", city)
    return south, north, west, east, display_name

def _fetch_osm_hotels(city: str, limit: int):
    south, north, west, east, display_name = _city_bounds(city)
    query = f"""
    [out:json][timeout:45];
    (
      node["tourism"~"hotel|guest_house|hostel|motel"]({south},{west},{north},{east});
      way["tourism"~"hotel|guest_house|hostel|motel"]({south},{west},{north},{east});
      relation["tourism"~"hotel|guest_house|hostel|motel"]({south},{west},{north},{east});
    );
    out center tags;
    """
    response = requests.post(
        OVERPASS_URL, data={"data": query}, headers=SCRAPER_HEADERS, timeout=60
    )
    response.raise_for_status()
    elements = response.json().get("elements", [])
    rows = []
    for item in elements:
        tags = item.get("tags", {})
        name = tags.get("name")
        if not name:
            continue
        center = item.get("center", {})
        tourism_type = tags.get("tourism", "hotel")
        # These are explicitly proxy categories for the model's known category vocabulary.
        proxy_map = {"hostel": "Budget", "motel": "Budget", "guest_house": "Boutique", "hotel": "Business"}
        hotel_type_proxy = proxy_map.get(tourism_type, "Boutique")
        stars_raw = tags.get("stars", "")
        try:
            stars = float(str(stars_raw).replace(",", ".").split(";")[0]) if stars_raw else None
            stars = min(5, max(1, stars)) if stars is not None else None
        except (TypeError, ValueError):
            stars = None
        osm_type = item.get("type", "")
        osm_id = item.get("id", "")
        rows.append({
            "hotel_name": name,
            "city": city.title(),
            "hotel_type_source": tourism_type,
            "hotel_type_proxy": hotel_type_proxy,
            "star_category": stars,
            "address": ", ".join(x for x in [
                tags.get("addr:housenumber", ""), tags.get("addr:street", ""),
                tags.get("addr:suburb", ""), tags.get("addr:city", ""),
                tags.get("addr:postcode", "")
            ] if x),
            "latitude": item.get("lat", center.get("lat")),
            "longitude": item.get("lon", center.get("lon")),
            "website": tags.get("website", tags.get("contact:website", "")),
            "phone": tags.get("phone", tags.get("contact:phone", "")),
            "osm_type": osm_type,
            "osm_id": str(osm_id),
            "source": "OpenStreetMap",
            "source_url": f"https://www.openstreetmap.org/{osm_type}/{osm_id}",
            "scraped_at_utc": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        })
        if len(rows) >= limit:
            break
    if not rows:
        raise HTTPException(404, f"No named accommodation listings were returned for {city}. Try another city or retry later.")
    return rows, display_name

