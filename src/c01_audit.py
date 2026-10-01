import json
from crop_common import *

out = {}
raw = load_fao(False); cl = load_fao(True)
g = raw.groupby(FAO_KEY)
out["fao"] = {
    "rows": len(raw), "unique_records": len(cl),
    "frac_rows_repeating": float(1 - len(cl) / len(raw)),
    "frac_rows_in_repeated_keys": float((g["yield"].transform("size") > 1).mean()),
    "icc_country_clean": {c: icc_oneway(cl[c], cl.country) for c in ["rain", "temp", "pest"]},
    "max_distinct_yields_per_key": int(g["yield"].nunique().max()),
    "n_countries": int(raw.country.nunique()), "n_crops": int(raw.crop.nunique()),
    "years": [int(raw.year.min()), int(raw.year.max())],
    "icc_country": {c: icc_oneway(raw[c], raw.country) for c in ["rain", "temp", "pest"]},
    "icc_logyield_country_crop": icc_oneway(raw.ly, raw.country + "|" + raw.crop),
    "icc_logyield_country_crop_clean": icc_oneway(cl.ly, cl.country + "|" + cl.crop),
}
raw_i = load_india(False); ind = load_india(True)
out["india"] = {
    "rows_raw": len(raw_i), "rows_clean": len(ind), "states": int(ind.state.nunique()),
    "districts_raw": int(raw_i.state.add(raw_i.district).nunique()),
    "districts_clean": int(ind.dist_id.nunique()), "crops_raw": int(raw_i.crop.nunique()),
    "crops_clean": int(ind.crop.nunique()), "years": [int(ind.year.min()), int(ind.year.max())],
    "icc_logyield_district_crop": icc_oneway(ind.ly, ind.dist_id + "|" + ind.crop),
    "icc_logyield_state_crop": icc_oneway(ind.ly, ind.state + "|" + ind.crop),
}
json.dump(out, open(os.path.join(RES, "audit.json"), "w"), indent=1)
print(json.dumps(out, indent=1))
