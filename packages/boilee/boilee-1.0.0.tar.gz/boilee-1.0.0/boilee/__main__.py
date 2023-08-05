from importlib import metadata

cli = metadata.entry_points()["console_scripts"][0].load()
cli()
