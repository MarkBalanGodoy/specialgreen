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

The emailed set showed no blower, sprinkler head or valve box, so the detail strip and the
irrigation project were relabelled to match their photographs rather than the reverse:
`Blowing` became `Bed Design`, `Irrigation Repair` became `Drainage`, and the irrigation
project became `Seasonal Color Install`.

The Facebook set then supplied a real backpack blower, so `Blowing` has its name back.
`Drainage` and `Seasonal Color Install` still stand, because nothing yet shows a sprinkler
head or a valve box.


## Second pass: photographs from the Facebook page

Jon sent the company's Facebook photo library as a set of zips (213 unique images
after de-duplication). Fourteen slots moved to those photographs, chosen for the
brightest light, the highest resolution available, and crew at work wherever the
slot could carry it. Thirty-five of the Facebook images are 2048px wide, which
beats the 1536px ceiling of the emailed set, so most full-bleed slots got sharper
as well as brighter.

These files are not in the repo either. The filenames below are Facebook's own
CDN names, as downloaded.

| Slot | Source | File |
| --- | --- | --- |
| `hero-outdoor-living` | Facebook set | `668743495_935107805936540_6745819076879702438_n.jpg` |
| `service-lawn-care` | Facebook set | `471147360_570161635764494_8367175150090850378_n.jpg` |
| `service-landscaping` | Facebook set | `496149419_684334921013831_5177710913840970155_n.jpg` |
| `crew-group` | Facebook set | `500552108_18006541412765338_6936249543574964612_n.jpg` |
| `crew-truck-load` | Facebook set | `441921028_17960254721765338_1887255107908847863_n.jpg` |
| `detail-blower` | Facebook set | `500368396_18006541343765338_601788723376770463_n.jpg` |
| `detail-edging` | Facebook set | `471546766_576359261811398_2915042605784808024_n.jpg` |
| `detail-trimmer` | Facebook set | `668222321_935107795936541_564298851195051515_n.jpg` |
| `project-patio-landscape` | Facebook set | `670077460_18045474278765338_3938220201719971602_n.jpg` |
| `project-front-yard` | Facebook set | `499770551_684334934347163_8119803631497757145_n.jpg` |
| `project-irrigation` | Facebook set | `670906099_18045473963765338_9020040632630491522_n.jpg` |
| `commercial-crew-trucks` | Facebook set | `699891159_964077773039543_1574845214990911035_n.jpg` |
| `project-office-park` | Facebook set | `699906897_964077683039552_3417082931043932461_n.jpg` |
| `customer-crew-leader` | Facebook set | `470883895_570161599097831_3779435024549193296_n.jpg` |

Kept from the emailed set, because nothing in the Facebook library beat them:
`crew-portrait` (crew member cutting drain pipe), `service-irrigation`,
`detail-irrigation-valve`, `cta-sunset`, both mobile breaks, and all six
before/after frames.

### One photograph deliberately not used

A strong shot of a crew member in an orange shirt carrying a roll of sod was the
obvious pick for a crew slot, but the back of the shirt reads "BEST QUAL…",
which is not Special Green branding. It may well be their own shirt, but
captioning someone as a Special Green crew member on the strength of a guess is
not worth it. Confirm the shirt and it goes straight in.

### Still open

Two photographs Jon is getting: sprinklers running, and the team standing in
front of the equipment with a finished landscape behind them. The first fixes
the Irrigation service card, which still carries drainage pipe. The second is
the crew group shot the About section has wanted from the start.
