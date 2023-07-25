# SeenIt
SeenIt allows user to delete/abandon the media they watch/request on Plex

### Planned
- Monitor if someone is watching before deleting
    -This might be automatically done with Tautulli webhooks
- Configure housekeeping jobs to keep database up to date
    - Update file sizes
    - Import new Ombi requests
- Add logging
- Tabbed settings

### In Progress


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

### Possible Ameliorations
- Add webhook in Tautulli and POST in SeenIt to add pick to media when they start watching something
    - Add Tautulli app information in settings
    - Add possibility to configure the notification agent in Tautulli from the app
- Add Picks by seasons to allow deletion of a few season at a time.
- Allow admins and users to add picks manually? Is it needed?