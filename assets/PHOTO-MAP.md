# Which photograph is in which slot

Source photographs came from Mark's two emails, `Special_Green_Website_Photos_Part_1.zip`
and `Part_2.zip`. They are **not** in this repository: they are about 30 MB, and the Pages
workflow uploads the whole repo, so committing them would ship them to every visitor for no
reason. `assets/incoming/` is gitignored.

This file records what went where, so the site can be rebuilt from the originals. Drop the
zips' contents into `assets/incoming/` renamed per the first column and run
`python3 tools/prepare-photos.py`.

| Slot | Source photograph | Crop |
| --- | --- | --- |
| `hero-outdoor-living` | Residential_Landscaping/04_Backyard_Garden | centre |
| `crew-portrait` | French_Drain/05_Pipe_Installation | centre |
| `crew-group` | French_Drain/03_Excavation | `--top` |
| `crew-trimmer` | French_Drain/04_Filter_Fabric | `--top` |
| `crew-truck-load` | French_Drain/06_Gravel_Base | `--top` |
| `commercial-crew-trucks` | Lake_Plaza_Commercial/04_After_Angle | centre |
| `customer-crew-leader` | Residential_Landscaping/05_Front_Garden | centre |
| `cta-sunset` | French_Drain/01_Layout | `--top` |
| `service-lawn-care` | Residential_Landscaping/03_Lawn_and_Mulch | centre |
| `service-landscaping` | Seasonal_Color/02_Flower_Installation | centre |
| `service-irrigation` | French_Drain/02_Excavation_Side | centre |
| `detail-edging` | Residential_Landscaping/07_Mulched_Beds | centre |
| `detail-trimmer` | Residential_Landscaping/06_Trimmed_Shrubs | centre |
| `detail-blower` | Residential_Landscaping/10_Front_Bed_Closeup | centre |
| `detail-irrigation-valve` | French_Drain/07_Final_Layer | centre |
| `project-patio-landscape` | Planters/01_Poolside_Planters | `--top` |
| `project-front-yard` | Residential_Landscaping/09_Front_Bed_Design | **left 16% trimmed first**, see below |
| `project-irrigation` | Seasonal_Color/05_Front_Bed | centre |
| `project-office-park` | Lake_Plaza_Commercial/03_After_Front | centre |
| `before-01-before` | Residential_Landscaping/01_Before | centre |
| `before-01-after` | Residential_Landscaping/02_After_Red_Mulch | centre |
| `before-02-before` | Lake_Plaza_Commercial/01_Before | centre |
| `before-02-after` | Lake_Plaza_Commercial/02_After_Front | centre |
| `before-03-before` | Commercial_Garden/01_Before | centre |
| `before-03-after` | Commercial_Garden/02_After | centre |
| `mobile-break-01` | Residential_Landscaping/08_Trellis_Planting | centre |
| `mobile-break-02` | Seasonal_Color/04_Mulch_and_Flowers | centre |

## The one manual edit

`project-front-yard` has a thumb over the lens at the left edge, about two thirds down.
The left 16% is trimmed before the slot crop, which removes it and tightens the composition.
The house, the bed and the lawn all survive it.

```python
from PIL import Image, ImageOps
im = ImageOps.exif_transpose(Image.open('09_Front_Bed_Design.jpeg')).convert('RGB')
w, h = im.size
im.crop((int(w * 0.16), 0, w, h)).save('assets/incoming/project-front-yard.jpeg', quality=95)
```

`Residential_Landscaping/06_Trimmed_Shrubs` has the same problem but the square crop removes
it on its own, so it needs no edit.

## Photographs still worth taking

Every slot has a real photograph now, but three slots carry a picture that is close to,
rather than exactly, what the section claims. None of them is untrue — the alt text describes
what is actually in frame — but a better photograph exists to be taken:

- **The Irrigation service card** shows PVC pipe in an open trench, which is drainage work.
  Irrigation is a service the company sells and the card copy is about sprinkler heads and
  controllers, so a photograph of heads running at golden hour belongs here.
- **`crew-group`** wants the full team in orange in front of the trucks. What is there is two
  crew working a trench. The team shot is the single most valuable photograph missing.
- **`customer-crew-leader`** wants a homeowner talking with a crew leader. What is there is a
  finished bed.

Nothing in the set shows a blower, a sprinkler head or a valve box. The detail strip and the
irrigation project were relabelled to match their photographs rather than the reverse:
`Blowing` became `Bed Design`, `Irrigation Repair` became `Drainage`, and the irrigation
project became `Seasonal Color Install`. Change them back when the photographs exist.
