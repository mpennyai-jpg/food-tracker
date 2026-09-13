"""Turn a raw RealTracs export into the worked CSV every later step reads.

    python prep.py --csv "<export>.csv" --out "<subject> - MLS worked.csv" \
        --lat <subject lat> --lon <subject lon> --origin YYYY-MM-DD

Produces these columns, which are the ones the rest of the workup expects:

    Mls Status Address Subdiv Yr Age SF Bd FB HB Baths LP OLP SP Closed Mon
    DOM L2C Acres Gar Carport GarTot Bsmt Stories Cond CondWhy PPSF DistMi
    Fin SellerPart Roof Constr Remarks

Two things here are method, not convenience:

* **L2C (ListToContractDays) is the measurement basis, not DOM.** DOM resets on
  withdrawal and relist. Both are carried so the disagreement can be measured and
  reported on every assignment.
* **CondWhy records the phrase that classed each listing.** Condition classing is
  a keyword read of remarks and some of it will be wrong; without the matched
  phrase in the file there is no way to spot-check it, and an unauditable screen
  has no business anywhere near an adjustment.
"""
import argparse, csv, math, re, sys
from datetime import datetime

# Every phrase is matched on WORD BOUNDARIES. Substring matching classed six
# renovated listings as distressed because "new gutters" contains "gut".
DISTRESSED = [
    "handyman", "fixer", "fixer[- ]upper", "as[- ]is", "sold as is", "needs work",
    "needs some work", "needs tlc", "needs repair", "needs a lot of work", "tlc",
    "investor special", "disrepair", "rehab", "gutted", "gut job", "not habitable",
    "uninhabitable", "cash only", "bring your contractor", "at auction",
    "foreclos\\w*", "no property condition disclosure", "sold in its present condition",
]
# Whole-house language only. A single new component is NOT a renovation — "new
# roof, windows, cabinets, plumbing and electrical in 2022" reads as a maintained
# average house, not a renovated one, and treating it as renovated moves it across
# the largest adjustment in the analysis.
RENOVATED = [
    "completely remodel\\w*", "fully renovated", "totally renovated", "renovated",
    "remodeled", "newly updated", "updated throughout", "updated", "down to the studs",
    "to the studs", "like new", "new construction",
]
# Components: counted, never decisive on their own. Recorded in CondWhy so the
# borderline cases can be reviewed.
COMPONENTS = [
    "new roof", "new hvac", "new windows", "new kitchen", "new flooring", "new lvp",
    "new appliances", "new plumbing", "new electrical", "new siding", "new gutters",
    "new water heater", "new cabinets", "new countertops",
]
# Pitches about what the NEXT owner could do. They are not statements about
# condition, and they were the other half of the false-distressed problem.
NOT_CONDITION = [
    "investment opportunity", "great investment", "room to grow", "opportunity to",
    "investment in growing", "value[- ]add", "estate sale", "perfect for first time",
]
# A whole-house word scoped to one room is a partial update, not a renovation.
# The lookbehinds stop "beautifully updated 3-bedroom, 1-bath home" from reading as
# a bathroom-only update: in a bed/bath count the room word follows a digit.
ROOMS = r"(?<!\d)(?<!\d-)(?<!\d )(kitchen|bathrooms?|primary suite|master bath|laundry)"


def num(v):
    if v is None:
        return ""
    s = str(v).strip().replace("$", "").replace(",", "")
    if s in ("", "-", "--", "N/A", "NA", "None"):
        return ""
    try:
        f = float(s)
        return int(f) if f == int(f) else f
    except ValueError:
        return ""


def pdate(s):
    s = (s or "").strip()
    if not s:
        return None
    for fmt in ("%Y-%m-%d", "%m/%d/%Y", "%m/%d/%y", "%Y-%m-%dT%H:%M:%S", "%Y/%m/%d"):
        try:
            return datetime.strptime(s.split("T")[0] if "T" in s else s, fmt).date()
        except ValueError:
            pass
    return None


def haversine(lat1, lon1, lat2, lon2):
    r = 3958.8
    p1, p2 = math.radians(lat1), math.radians(lat2)
    dp, dl = math.radians(lat2 - lat1), math.radians(lon2 - lon1)
    a = math.sin(dp / 2) ** 2 + math.cos(p1) * math.cos(p2) * math.sin(dl / 2) ** 2
    return 2 * r * math.asin(math.sqrt(a))


def _hit(patterns, text):
    for p in patterns:
        m = re.search(r"\b" + p + r"\b", text)
        if m:
            return m.group(0)
    return None


def classify(remarks):
    """-1 distressed, 0 average, +1 renovated, plus the phrase that decided it."""
    t = " " + re.sub(r"\s+", " ", (remarks or "").lower()) + " "
    for p in NOT_CONDITION:
        t = re.sub(r"\b" + p + r"\b", " ", t)
    d = _hit(DISTRESSED, t)
    r = _hit(RENOVATED, t)
    if d:
        # A defect governs the class even when the remarks also boast about
        # finishes: a renovated kitchen in a house that "needs work" is still a
        # house that needs work.
        return -1, ("'%s'%s" % (d, " (over '%s')" % r if r else ""))
    if r:
        # scoped to one room = partial update, not a renovation
        scoped = re.search(r"\b" + r + r"\b[^.]{0,25}\b" + ROOMS, t) or \
                 re.search(ROOMS + r"[^.]{0,25}\b" + r + r"\b", t)
        if scoped:
            comps = [c for c in COMPONENTS if re.search(r"\b" + c + r"\b", t)]
            return 0, "'%s' scoped to %s — partial%s" % (
                r, scoped.group(0)[:40], (", %d components" % len(comps)) if comps else "")
        return 1, "'%s'" % r
    comps = [c for c in COMPONENTS if re.search(r"\b" + c + r"\b", t)]
    if len(comps) >= 3:
        # Three or more separately named new components is a renovation described
        # component by component. One or two is maintenance.
        return 1, "%d components: %s" % (len(comps), ", ".join("'%s'" % c for c in comps[:4]))
    if comps:
        return 0, "components only (%d): %s — review" % (
            len(comps), ", ".join("'%s'" % c for c in comps))
    if re.search(r"\b(currently rented|tenant occupied|tenant in place|tenant wants to stay|"
                 r"active .{0,14}rental|currently operating as a[n]? .{0,14}rental)\b", t):
        # Tenant-occupied investor listings often price like distressed stock
        # while saying nothing about condition. Flag it, never auto-class it.
        return 0, "no condition language; tenant-occupied — review"
    return 0, "no condition language"


# Central heat and air is a real adjustment item in older stock, and MLS carries it
# as free text in two columns. CentAir is the discriminator that matters: a house can
# have central heat and still cool on window units, and it is the cooling that shows
# up in the price. HVAC = both.
def hvac_flags(heat, cool):
    h = (heat or "").lower()
    c = (cool or "").lower()
    ch = 1 if "central heat" in h else 0
    ca = 1 if "central air" in c else 0
    return ch, ca, (1 if (ch and ca) else 0)


OUT = ["Mls", "Status", "Address", "Subdiv", "Yr", "Age", "SF", "Bd", "FB", "HB",
       "Baths", "LP", "OLP", "SP", "Closed", "Mon", "DOM", "L2C", "Acres", "Gar",
       "Carport", "GarTot", "Bsmt", "Stories", "Cond", "CondWhy", "CentHeat", "CentAir",
       "HVAC", "Heat", "Cool", "PPSF", "DistMi", "Fin", "SellerPart", "Roof", "Constr",
       "Remarks"]


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--csv", required=True)
    p.add_argument("--out", required=True)
    p.add_argument("--lat", type=float)
    p.add_argument("--lon", type=float)
    p.add_argument("--origin", default=None, help="YYYY-MM-DD for the Mon column")
    p.add_argument("--effective", default=None, help="YYYY-MM-DD; ages listings to this date")
    args = p.parse_args()

    with open(args.csv, newline="", encoding="utf-8-sig") as fh:
        rows = list(csv.DictReader(fh))
    if not rows:
        print("empty export"); sys.exit(1)

    closed = [pdate(r.get("ClosedDate")) for r in rows]
    closed = [d for d in closed if d]
    origin = pdate(args.origin) or (min(closed) if closed else None)
    eff = pdate(args.effective)
    effyear = (eff or (max(closed) if closed else datetime.today().date())).year

    out, l2c_gap = [], 0
    for r in rows:
        cond, why = classify(r.get("Remarks"))
        ch, ca, hv = hvac_flags(r.get("Heating"), r.get("Cooling"))
        cd = pdate(r.get("ClosedDate"))
        yr = num(r.get("YearBuilt"))
        sf = num(r.get("SqFtTotal"))
        sp = num(r.get("SalesPrice"))
        gar, car = num(r.get("GarageSpaces")) or 0, num(r.get("CarportSpaces")) or 0
        dom, l2c = num(r.get("DaysOnMarket")), num(r.get("ListToContractDays"))
        if dom != "" and l2c != "" and dom != l2c:
            l2c_gap += 1
        lat, lon = num(r.get("Latitude")), num(r.get("Longitude"))
        row = {
            "Mls": r.get("MlsNumber", ""), "Status": r.get("ListingStatus", ""),
            "Address": r.get("Address", ""), "Subdiv": r.get("Subdivision", ""),
            "Yr": yr, "Age": (effyear - yr) if yr != "" else "",
            "SF": sf, "Bd": num(r.get("TotalBedrooms")),
            "FB": num(r.get("TotalFullBaths")) or 0, "HB": num(r.get("TotalHalfBaths")) or 0,
            "LP": num(r.get("ListPrice")), "OLP": num(r.get("OriginalListPrice")),
            "SP": sp, "Closed": cd.isoformat() if cd else "",
            "Mon": round(((cd.year - origin.year) * 12 + (cd.month - origin.month)
                          + (cd.day - origin.day) / 30.44), 2) if (cd and origin) else "",
            "DOM": dom, "L2C": l2c, "Acres": num(r.get("Acres")),
            "Gar": gar, "Carport": car, "GarTot": gar + car,
            "Bsmt": r.get("Basement", ""), "Stories": num(r.get("NumOfStories")),
            "Cond": cond, "CondWhy": why,
            "CentHeat": ch, "CentAir": ca, "HVAC": hv,
            "Heat": r.get("Heating", ""), "Cool": r.get("Cooling", ""),
            "PPSF": round(sp / sf, 2) if (sp != "" and sf not in ("", 0)) else "",
            "DistMi": (round(haversine(args.lat, args.lon, lat, lon), 2)
                       if (args.lat is not None and lat != "" and lon != "") else ""),
            "Fin": r.get("BuyerFinancing", ""), "SellerPart": r.get("SellerParticipation", ""),
            "Roof": r.get("RoofMaterial", ""), "Constr": r.get("ConstructionType", ""),
            "Remarks": re.sub(r"\s+", " ", r.get("Remarks", "") or "").strip(),
        }
        row["Baths"] = (row["FB"] or 0) + 0.5 * (row["HB"] or 0)
        out.append(row)

    with open(args.out, "w", newline="", encoding="utf-8") as fh:
        w = csv.DictWriter(fh, fieldnames=OUT, quoting=csv.QUOTE_ALL)
        w.writeheader()
        for row in out:
            w.writerow({k: row.get(k, "") for k in OUT})

    n = len(out)
    cl = sum(1 for r in out if str(r["Status"]).lower().startswith("closed"))
    counts = {c: sum(1 for r in out if r["Cond"] == c) for c in (-1, 0, 1)}
    print("wrote %s" % args.out)
    print("  %d listings, %d closed" % (n, cl))
    print("  condition classes: distressed %d / average %d / renovated %d"
          % (counts[-1], counts[0], counts[1]))
    # On ordinary stock the distressed tier is usually small or empty. That is the
    # expected shape — but a tier that thin cannot carry a condition adjustment.
    for name, c in (("distressed", counts[-1]), ("renovated", counts[1])):
        if 0 < c < 8:
            print("  NOTE: %s tier has only %d sales — too thin to carry a condition"
                  " adjustment on its own. Use the regression coefficient, or widen"
                  " the segment and say what you widened it to." % (name, c))
    print("  DOM disagrees with ListToContractDays on %d of %d rows" % (l2c_gap, n))
    noair = sum(1 for r in out if str(r["Status"]).lower().startswith("closed") and not r["CentAir"])
    print("  closed sales without central air: %d" % noair)
    print("  SPOT-CHECK CondWhy before using any condition number.")


if __name__ == "__main__":
    main()
