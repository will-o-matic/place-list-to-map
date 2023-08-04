# place-list-to-map
 Scripts to take a text file with business or place names and emoji and turn them into kmz files for mapping.

## Workflow
- Save a file (.txt) with a list of business names.  Include icons as descriptions.  See 'Sample Business List.txt' for some examples.
- Run get-businesses.py to use ChatGPT and Google Places API to identify businesses matching the list supplied.
- Run create-kml.py to create the KML file for importing into your favorite mapping app.

*Note*: If the KML fails to load icons as you expect, you might need to first create a Google My Maps map (with any businesses you want, it doesn't matter) that uses the icons you need.  Then use that as the foundation for the new KML export.

