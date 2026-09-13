"""OLS with standard errors and t-statistics, standard library only.

Penny-AI has no pandas, no numpy, no statsmodels and no sklearn, and installing
them is not part of this workflow. This does the whole job in stdlib: read the
CSV, derive columns, filter rows, solve the normal equations by Gauss-Jordan,
and report coefficients with the standard errors and t-statistics that decide
whether a coefficient is usable support or noise.

    python ols.py --csv "<subject> - MLS worked.csv" \
        --y SP --x SF,BATHS,COND,MONTHS \
        --derive "BATHS=FB+0.5*HB" \
        --derive "MONTHS=months_since(Closed,2025-01-01)" \
        --filter "Status=Closed" --min-n 8

Prints a table and a JSON block. Rows with a missing or non-numeric value in any
model variable are dropped and counted, because a silent drop changes n and n is
the first thing a reviewer checks.
"""
import argparse, csv, json, math, re, sys
from datetime import date


def parse_date(s):
    s = (s or "").strip()
    if not s:
        return None
    for fmt in ("%Y-%m-%d", "%m/%d/%Y", "%m/%d/%y", "%Y/%m/%d"):
        try:
            from datetime import datetime
            return datetime.strptime(s, fmt).date()
        except ValueError:
            pass
    return None


def months_since(datestr, origin):
    d = parse_date(datestr)
    o = parse_date(origin)
    if not d or not o:
        return None
    return (d.year - o.year) * 12 + (d.month - o.month) + (d.day - o.day) / 30.44


def num(v):
    if v is None:
        return None
    s = str(v).strip().replace("$", "").replace(",", "").replace("%", "")
    if s in ("", "-", "--", "N/A", "NA", "None"):
        return None
    try:
        return float(s)
    except ValueError:
        return None


SAFE = re.compile(r"^[A-Za-z0-9_+\-*/(). ,:]+$")


def derive(expr, row):
    """Arithmetic over column names, plus months_since(col, YYYY-MM-DD)."""
    if not SAFE.match(expr):
        raise ValueError("unsafe derive expression: " + expr)
    env = {"months_since": lambda c, o: months_since(row.get(c, c), o)}
    for k, v in row.items():
        key = re.sub(r"\W", "_", k)
        n = num(v)
        env[key] = n if n is not None else float("nan")
        env[key + "__raw"] = v
    # bare date column names inside months_since must survive as strings
    def repl(m):
        return "months_since('%s','%s')" % (m.group(1).strip(), m.group(2).strip())
    expr2 = re.sub(r"months_since\(([^,]+),([^)]+)\)", repl, expr)
    env2 = dict(env)
    env2["months_since"] = lambda c, o: months_since(row.get(c), o)
    try:
        return eval(expr2, {"__builtins__": {}}, env2)  # noqa: S307 - local tool, guarded by SAFE
    except Exception:
        return None


def solve(xtx, xty):
    """Gauss-Jordan with partial pivoting; returns (beta, inverse)."""
    k = len(xty)
    a = [row[:] + [1.0 if i == j else 0.0 for j in range(k)] + [xty[i]]
         for i, row in enumerate(xtx)]
    for col in range(k):
        piv = max(range(col, k), key=lambda r: abs(a[r][col]))
        if abs(a[piv][col]) < 1e-12:
            raise ValueError("singular matrix — variables are collinear")
        a[col], a[piv] = a[piv], a[col]
        p = a[col][col]
        a[col] = [v / p for v in a[col]]
        for r in range(k):
            if r == col:
                continue
            f = a[r][col]
            if f:
                a[r] = [v - f * w for v, w in zip(a[r], a[col])]
    beta = [a[i][-1] for i in range(k)]
    inv = [[a[i][k + j] for j in range(k)] for i in range(k)]
    return beta, inv


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--csv", required=True)
    p.add_argument("--y", required=True)
    p.add_argument("--x", required=True, help="comma-separated column names")
    p.add_argument("--derive", action="append", default=[], help="NAME=expression")
    p.add_argument("--filter", action="append", default=[], help="COL=value (exact, case-insensitive)")
    p.add_argument("--min-n", type=int, default=8)
    p.add_argument("--label", default="model")
    args = p.parse_args()

    with open(args.csv, newline="", encoding="utf-8-sig") as fh:
        rows = list(csv.DictReader(fh))

    for f in args.filter:
        col, _, val = f.partition("=")
        rows = [r for r in rows if str(r.get(col.strip(), "")).strip().lower() == val.strip().lower()]

    for d in args.derive:
        name, _, expr = d.partition("=")
        for r in rows:
            r[name.strip()] = derive(expr.strip(), r)

    xs = [c.strip() for c in args.x.split(",")]

    # Column names are matched case-insensitively, and a name that is not in the
    # file at all fails here rather than quietly dropping every row: an n of 0
    # and a typo look identical in the output otherwise.
    have = {}
    for r in rows:
        for k in r:
            have.setdefault(k.lower(), k)
    for want in [args.y] + xs:
        real = have.get(want.lower())
        if real is None:
            print(json.dumps({"error": "no such column: " + want,
                              "available": sorted(have.values())}, indent=1))
            sys.exit(2)
        if real != want:
            for r in rows:
                r[want] = r.get(real)

    data, dropped = [], 0
    for r in rows:
        yv = num(r.get(args.y))
        xv = [num(r.get(c)) for c in xs]
        if yv is None or any(v is None or (isinstance(v, float) and math.isnan(v)) for v in xv):
            dropped += 1
            continue
        data.append(([1.0] + xv, yv))

    n, k = len(data), len(xs) + 1
    if n < max(args.min_n, k + 1):
        print(json.dumps({"error": "too few usable rows", "n": n, "dropped": dropped}))
        sys.exit(1)

    xtx = [[sum(row[i] * row[j] for row, _ in data) for j in range(k)] for i in range(k)]
    xty = [sum(row[i] * y for row, y in data) for i in range(k)]
    beta, inv = solve(xtx, xty)

    ybar = sum(y for _, y in data) / n
    sse = sum((y - sum(b * v for b, v in zip(beta, row))) ** 2 for row, y in data)
    sst = sum((y - ybar) ** 2 for _, y in data)
    dof = n - k
    sigma2 = sse / dof
    se = [math.sqrt(max(sigma2 * inv[i][i], 0.0)) for i in range(k)]
    r2 = 1 - sse / sst if sst else float("nan")
    adj = 1 - (1 - r2) * (n - 1) / dof
    names = ["Intercept"] + xs

    print("%s  n=%d  dropped=%d  R2=%.3f  adj R2=%.3f  RMSE=%s"
          % (args.label, n, dropped, r2, adj, "{:,.0f}".format(math.sqrt(sigma2))))
    print("%-14s %14s %12s %8s  %s" % ("variable", "coefficient", "std. error", "t", "read"))
    out = []
    for i, nm in enumerate(names):
        t = beta[i] / se[i] if se[i] else float("nan")
        read = "significant" if abs(t) >= 2 else ("marginal" if abs(t) >= 1.5 else "NOT significant")
        print("%-14s %14s %12s %8.2f  %s"
              % (nm, "{:,.0f}".format(beta[i]), "{:,.0f}".format(se[i]), t, read))
        out.append({"name": nm, "coef": beta[i], "se": se[i], "t": t, "read": read})
    print()
    print(json.dumps({"label": args.label, "n": n, "dropped": dropped, "r2": r2,
                      "adj_r2": adj, "rmse": math.sqrt(sigma2), "coefficients": out}, indent=1))


if __name__ == "__main__":
    main()
