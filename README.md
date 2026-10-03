# amph-styleprint-validate

**F3 VERIFY** -- negative controls prove the axes move

An instrument nobody has tried to break is an opinion. This runs the negative controls that prove each axis can actually fail.

## Licence -- read this first

**Noncommercial.** `amph-styleprint-validate` is licensed under the
[PolyForm Noncommercial License 1.0.0](https://polyformproject.org/licenses/noncommercial/1.0.0).
You may use, copy, modify and distribute it for any noncommercial purpose, and
for any commercial purpose only with a separate written grant from the copyright holder. Full text is in
`LICENSE`.

The calibration numbers this module ships were measured on a specific corpus,
not derived from first principles. Read `## Known limits` before trusting a
threshold -- that section is the reason the module is worth having.

## Run it

```bash
pip install -e .
python3 selftest.py
```

## Where this came from

Copied byte-for-byte from `amph-public/engine/validate_styleprint.py`.

Every file here is emitted by `amph-comic/tools/build_modules.py`, which copies
from `amph-public/engine/`. Nothing in this repo is hand-maintained. Regenerate
and verify with:

```bash
python3 tools/build_modules.py --check --out <this repo's parent>
```

## Known limits

This module ships its own limits rather than hiding them -- see `validate_styleprint.py.py
--known-limits`, or `known-limits.json` in the F8 repo, which harvests all four.

## The corpus

This module's full self-check reads the 48-image reference corpus, which is
**not in this repo** — it is the campaign's art, and it stays in
`amph-public`. Point the module at your own reference set, or a symlink:

```bash
ln -s /path/to/your/art work/art
python3 selftest.py
```

That is a deliberate dependency, not a packaging gap: the axes and the frame
tolerance are *calibrated* on a specific corpus, and shipping those numbers
without the corpus they came from would invite a buyer to trust a tolerance
measured against art they have never seen.
