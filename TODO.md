# SeenIt
SeenIt allows user to delete/abandon the media they watch/request on Plex

### Planned
- Website looks
    - Tabbed settings
    - Better settings selection for updating the db (schedule)
    - Figure out a better way to mass delete
- Add logging
- Add check for admin on data update
- Test services to come from the application instead of client
- Fix error where server gets rate-limited with DNS queries. Python's "requests" does a lookup at each request. (https://stackoverflow.com/questions/36087637/how-often-does-python-requests-perform-dns-queries#:~:text=Yes%2C%20the%20Python%20requests%20lib,with%20the%20python%20requests%20library.)

### In Progress
- Add logging

### Completed
- Add a search option in medias
- Merge toastr and flash notifications
- Add an option to "order by" fields in media
- Add Plex login
    - Find a way to load app_settings with a unique ID for Plex
- Add adoption/requested date
- Users now have "picks", which allows multiple users per media
- Add popup on picks for admins, admins can delete picks.
- Add expiry date on media, and calculate its deletion date
- Display the time according to user's time zone (Pick date)
    - Add time Javascript (moments)
- Implement APScheduler / BackgroundScheduler
- Configure connections to Radarr/Sonarr
- Media deletion works
- Monitor if someone is watching before deleting
    -This might be automatically done with Tautulli webhooks
- Add webhook in Tautulli and POST in SeenIt to add pick to media when they start watching something
- Configure housekeeping jobs to keep database up to date
    - Check if the media was added to Sonarr/Radarr
        - Update file sizes
    - Import new Ombi requests
- Website looks
    - Better login/welcome screen
- Add Safe Mode

### Possible Ameliorations
- Add possibility to configure the notification agent in Tautulli from the app
    - Add Tautulli app information in settings
- Add Picks by seasons to allow deletion of a few season at a time.
- Allow admins and users to add picks manually? Is it needed?
- Add storage information per user / total