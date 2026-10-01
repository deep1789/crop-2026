"""Trace the origin of duplicated FAO rows by rebuilding yield_df from its source tables."""
import json
from crop_common import *
D = os.path.join(DATA, "fao")
t = pd.read_csv(f"{D}/temp.csv"); r = pd.read_csv(f"{D}/rainfall.csv"); p = pd.read_csv(f"{D}/pesticides.csv")
y = pd.read_csv(f"{D}/yield.csv"); yd = pd.read_csv(f"{D}/yield_df.csv", index_col=0)
r.columns = ["country", "year", "rain"]; r["rain"] = pd.to_numeric(r["rain"], errors="coerce")
out = {}
# 1. temp.csv rows per country-year vs multiplicity of the yield record in yield_df
nt = t.groupby(["country", "year"]).size().rename("n_temp").reset_index()
m = yd.groupby(["Area", "Item", "Year"]).size().rename("mult").reset_index()
m = m.merge(nt, left_on=["Area", "Year"], right_on=["country", "year"], how="left")
out["fanout"] = {"keys": len(m), "frac_mult_equals_n_temp_rows": float((m.mult == m.n_temp).mean()),
                 "frac_keys_with_temp_match": float(m.n_temp.notna().mean()),
                 "corr_mult_ntemp": float(m[["mult", "n_temp"]].corr().iloc[0, 1])}
# 2. spread of avg_temp inside a country-year in the source
sp = t.groupby(["country", "year"]).avg_temp.agg(["size", "std"])
out["temp_source"] = {"country_years": len(sp), "frac_with_multiple_rows": float((sp["size"] > 1).mean()),
                      "median_within_cy_std": float(sp["std"].dropna().median()),
                      "total_std": float(t.avg_temp.std())}
# 3. does yield_df repeat the same yield with differing temps?
g = yd.groupby(["Area", "Item", "Year"])
out["repeat"] = {"keys_with_repeats": int((g.size() > 1).sum()),
                 "max_distinct_yield": int(g["hg/ha_yield"].nunique().max()),
                 "mean_distinct_temp_per_repeated_key": float(g["avg_temp"].nunique()[g.size() > 1].mean())}
# 4. rainfall: source varies by year within country?
rv = r.dropna().groupby("country").rain.nunique()
out["rain_source"] = {"countries": int(len(rv)), "frac_constant_over_years": float((rv == 1).mean())}
# 5. yield_df yield equals FAO yield.csv for the same key?
yy = y[["Area", "Item", "Year", "Value"]].rename(columns={"Value": "fao_yield"})
j = yd.drop_duplicates(["Area", "Item", "Year"]).merge(yy, on=["Area", "Item", "Year"], how="left")
out["yield_match"] = {"matched": float(j.fao_yield.notna().mean()),
                      "equal": float((j["hg/ha_yield"] == j.fao_yield).mean())}
# 6. pesticides: within-country time variation in source and in yield_df
pp = p[["Area", "Year", "Value"]].copy(); pp["Value"] = pd.to_numeric(pp["Value"], errors="coerce")
out["pesticide_icc"] = {"source_country_year": icc_oneway(pp.dropna().Value, pp.dropna().Area),
                        "yield_df_rows": icc_oneway(yd.pesticides_tonnes, yd.Area),
                        "yield_df_unique_country_year": icc_oneway(*(lambda u: (u.pesticides_tonnes, u.Area))(yd.drop_duplicates(["Area", "Year"])))}
json.dump(out, open(os.path.join(RES, "audit_origin.json"), "w"), indent=1); print(json.dumps(out, indent=1))
