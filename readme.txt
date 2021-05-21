1. Run PPK from U-Blox GNSS Rover (raw_*.obs/raw_*.nav/raw_*.sbs) with multiple base stations (*.21o, *.OBS) with rnx2rtkp CUI.
2. Run RTKpost GUI to create Events.pos time events. 
3. Convert .pos -> .kml -> .gpx with set of option flags.
4. Run filtering algorithm and merge func on GPS Track Editor: (velocity < 16 km/h; acceleration(forward/backward/angular) < 1.4 m/s^2)
5. Merge tracks with re-filtration and export as .csv.
6. Read EXIFs from images in instaOne directory and create list.
7. UTC(from GNSS-GPST) and EXIF_time delta definition and compensation algorithm.
8. Сomparison of moment in time, coordinates and direction between photos and GNSS.
