# Rating and Review Segmentation, and Map Box Tiling

Two techniques for the Local Business Database: cutting a market into segments by `total_score` and `reviews_count` so the message fits, and tiling a big metro into `box` searches so each call stays fast.

## Part 1: Rating and review segments

### Thresholds and where they come from

BrightLocal's Local Consumer Review Survey 2026 (1,002 US adults) is the basis. Treat these as starting hypotheses, dated 2026, and test them in your own reply rates.

| Line | Consumer behavior (BrightLocal 2026) | Use in filters |
|---|---|---|
| 4.0 stars | 68% require 4+ stars | `minRating: 4.0` or `maxRating: 3.9` |
| 4.5 stars | 31% require 4.5+ stars | `minRating: 4.5` |
| 20 reviews | 47% will not use a business with fewer than 20 reviews | `maxReviews: 19` or `minReviews: 20` |
| 3 months | 74% look for reviews written in the last three months | The database has no review date filter, so this line cannot be filtered |

### Standard segment cut

| Segment | Filters | Where it sits | Example opening angle |
|---|---|---|---|
| A. Leaders | `minRating: 4.5, minReviews: 20` | Above the 4.5 line 31% use, past the 20-review line | Capacity, staffing, premium pricing, second location |
| B. Solid | `minRating: 4.0, maxRating: 4.4, minReviews: 20` | Between the 4.0 and 4.5 lines | Moving into the 4.5 group |
| C. Thin | `minRating: 4.0, maxReviews: 19` | Rated well but under the 20-review line 47% of consumers use | Review generation, visibility |
| D. At risk | `maxRating: 3.9, minReviews: 1` | Below the 4-star line 68% apply | Reputation repair, response to reviews |
| E. No reviews | `maxReviews: 0` | No rating yet | A separate test |

### Running the cut

For each segment, send the same `keyword` and `location` with the segment filters and `limit: 1`, record `pagination.total`. Then pull each segment with its own cursor. Google ratings carry one decimal, so A (4.5 and up) and B (4.0 to 4.4) do not overlap. B and C split at 20 reviews, D takes everything under 4.0 with at least one review, and E takes businesses with none, so the five groups cover the market once. Still dedupe on business id or `title` plus `address` before the send.

### Segment design for other offers

| Offer | Segments |
|---|---|
| Review management software | D (at risk), C (thin), then B |
| Booking or scheduling software | A (leaders), then B |
| Web design | Any rating, `hasWebsite` false rows from a pull without the flag, split by `reviews_count` 0-19 vs 20+ |
| Local SEO | C (thin) and B (solid), with `hasWebsite: true` |
| Staffing or recruiting | A (leaders) |
| Financing or equipment | A and B |

### Message fit, one line each

| Segment | Example first line (adapt to the offer) |
|---|---|
| A | "Saw 340 reviews at 4.8 for [business]." |
| B | "You're at 4.3 on Google. 31% of consumers only use businesses at 4.5 stars or more." |
| C | "4.7 stars on 11 reviews. 47% of consumers won't use a business with fewer than 20." |
| D | "Noticed [business] is at 3.6 on Google, and 68% of consumers only use businesses with 4 stars or more." |

The bracketed name is filled per row from `title`. The stats in these lines are from BrightLocal 2026; cite them as such in any public copy.

## Part 2: Map box tiling

### Why tile

A search over a dense category in a big metro can run long and return 503. Splitting the metro into boxes gives fast calls, per-tile progress tracking, and a natural unit for daily pulls.

### Box format

`box: "minLat,minLng,maxLat,maxLng"`, for example `"30.1,-97.9,30.5,-97.5"`. West of Greenwich, longitudes are negative, and the min longitude is the more negative number. A box that cannot be read returns 400.

### Sizing

USGS: one degree of latitude is about 69 miles. One degree of longitude is about 54.6 miles at 38 degrees north and shrinks toward the poles (roughly 69 x cos(latitude)).

| Tile step (degrees) | North-south | East-west at 30 N | East-west at 40 N |
|---|---|---|---|
| 0.5 | 34.5 mi | 29.9 mi | 26.4 mi |
| 0.25 | 17.3 mi | 14.9 mi | 13.2 mi |
| 0.1 | 6.9 mi | 6.0 mi | 5.3 mi |

The step is set by counting: any tile that returns 503 splits into four at half the step.

### Tile generator (Python, stdlib)

```python
def tiles(min_lat, min_lng, max_lat, max_lng, step):
    out = []
    lat = min_lat
    while lat < max_lat:
        lng = min_lng
        while lng < max_lng:
            out.append(f"{lat:.4f},{lng:.4f},{min(lat + step, max_lat):.4f},{min(lng + step, max_lng):.4f}")
            lng += step
        lat += step
    return out

# Austin metro, about 30.0 to 30.75 N and -98.0 to -97.4 W, at a 0.25 degree step
for b in tiles(30.0, -98.0, 30.75, -97.4, 0.25):
    print(b)
```

The Austin call above gives 3 rows by 3 columns = 9 tiles (the last column is 0.1 degrees wide). Run each tile with `limit: 1` first, then pull non-empty tiles with the cursor.

### Tile workflow

1. Get the metro's bounding box (from a map, or from `lat`/`lng` min and max in a city-level sample pull).
2. Generate tiles at a starting step.
3. Count each tile. Split any tile that returns 503 into four (half the step).
4. Pull tile by tile with `after`. Log tile, count, last cursor.
5. Dedupe on business id across tiles. A business on a tile edge appears in only one tile when boxes share edges, but dedupe anyway.

### Metro boxes to start from

Approximate bounding boxes; widen them to take in the suburbs you need.

| Metro | box |
|---|---|
| Austin, TX | `30.0,-98.0,30.75,-97.4` |
| Dallas-Fort Worth, TX | `32.5,-97.6,33.25,-96.5` |
| Houston, TX | `29.5,-95.8,30.15,-95.0` |
| Phoenix, AZ | `33.2,-112.4,33.8,-111.6` |
| Denver, CO | `39.55,-105.15,39.95,-104.75` |
| Atlanta, GA | `33.6,-84.6,34.05,-84.2` |
| Chicago, IL | `41.65,-87.95,42.1,-87.5` |
| Miami, FL | `25.6,-80.5,26.0,-80.1` |

### Tiling vs location lists

| Situation | Use |
|---|---|
| Metro of named suburbs | `location` list of cities, up to 2,000 |
| ZIP-based territories (franchise or sales territories) | `location` list of ZIP codes |
| Dense downtown, or territory drawn on a map | `box` tiles |
| Statewide, sparse category | `state` alone |
| Statewide, dense category | `state` plus city list, or tiles |

## Sources

- https://www.brightlocal.com/research/local-consumer-review-survey/
- https://www.usgs.gov/faqs/how-much-distance-does-a-degree-minute-and-second-cover-your-maps
- https://www.npmjs.com/package/scrapercity
- https://github.com/scrapercity/scrapercity-cli
