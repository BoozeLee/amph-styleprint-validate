# Vendored dependencies

- `styleprint.py` <- amph-public/engine/styleprint.py

These are byte-identical copies, kept flat and unrenamed so this module's own
`sys.path.insert(0, str(HERE))` resolves them without any edit to its source.

Do not patch them here. The upstream copy in `amph-public/engine/` is the source
of truth, and `tools/build_modules.py --check` fails if any vendored byte
differs from it.
