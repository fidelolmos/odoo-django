import os
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "odoodjango.odoodjango.settings")
django.setup()
import json

from laws.models import ViolationDetail
from vehicles.models import Vehicle
from locations.models import Location

violation_lookup = {}
for vd in ViolationDetail.objects.select_related("paragraph__subsection__fraction__article").all():
    art = vd.paragraph.subsection.fraction.article.number.strip()
    frac = vd.paragraph.subsection.fraction.number.strip()
    inc = vd.paragraph.subsection.letter.strip() if vd.paragraph.subsection.letter else "-----"
    par = vd.paragraph.number.strip() if vd.paragraph.number else ""
    key = f"{art},{frac},{inc},{par}"
    violation_lookup[key] = vd.id

vehicle_lookup = {v.plate.upper(): v.plate for v in Vehicle.objects.all()}

location_lookup = {}
for loc in Location.objects.select_related("neighborhood__municipality").all():
    street = loc.street.strip()
    neighborhood = loc.neighborhood.name.strip()
    municipality = loc.neighborhood.municipality.name.strip()
    key = f"{street}|{neighborhood}|{municipality}"
    location_lookup[key] = loc.id

os.makedirs("lookup_data", exist_ok=True)
with open("lookup_data/violation_lookup.json", "w", encoding="utf-8") as f:
    json.dump(violation_lookup, f, ensure_ascii=False, indent=4)
with open("lookup_data/vehicle_lookup.json", "w", encoding="utf-8") as f:
    json.dump(vehicle_lookup, f, ensure_ascii=False, indent=4)
with open("lookup_data/location_lookup.json", "w", encoding="utf-8") as f:
    json.dump(location_lookup, f, ensure_ascii=False, indent=4)
print("Diccionarios de lookup guardados en 'lookup_data'.")
