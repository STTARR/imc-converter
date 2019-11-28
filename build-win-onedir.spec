# -*- mode: python ; coding: utf-8 -*-

import gooey
block_cipher = None

def Entrypoint(dist, group, name, **kwargs):
    import pkg_resources

    # get toplevel packages of distribution from metadata
    def get_toplevel(dist):
        distribution = pkg_resources.get_distribution(dist)
        if distribution.has_metadata('top_level.txt'):
            return list(distribution.get_metadata('top_level.txt').split())
        else:
            return []

    kwargs.setdefault('hiddenimports', [])
    packages = []
    for distribution in kwargs['hiddenimports']:
        packages += get_toplevel(distribution)

    kwargs.setdefault('pathex', [])
    # get the entry point
    ep = pkg_resources.get_entry_info(dist, group, name)
    # insert path of the egg at the verify front of the search path
    kwargs['pathex'] = [ep.dist.location] + kwargs['pathex']
    # script name must not be a valid module name to avoid name clashes on import
    script_path = os.path.join(workpath, name + '-script.py')
    print("creating script for entry point", dist, group, name)
    with open(script_path, 'w') as fh:
        print("import", ep.module_name, file=fh)
        print("%s.%s()" % (ep.module_name, '.'.join(ep.attrs)), file=fh)
        for package in packages:
            print("import", package, file=fh)

    return Analysis(
        [script_path] + kwargs.get('scripts', []),
        **kwargs
    )

image_data = [
    ("imcconv/gui/images/config_icon.png", "imcconv/gui/images"),
    ("imcconv/gui/images/program_icon.png", "imcconv/gui/images")
]

a = Entrypoint(
    "imc-converter", "console_scripts", "imcconv-gui",
    binaries=[],
    datas=image_data,
    hiddenimports=[],
    hookspath=[],
    runtime_hooks=[],
    excludes=["matplotlib", "imagecodecs"],  # tifffile optional dependencies
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
)

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)
exe = EXE(pyz,
    a.scripts,
    a.binaries,
    exclude_binaries=True,
    name="IMC Converter",
    debug=False,
    strip=False,
    console=False,
    icon="imcconv/gui/images/program_icon.ico",
)
coll = COLLECT(
    exe,
    a.binaries,
    a.zipfiles,
    a.datas,
    strip=False,
    name="IMC Converter"
)