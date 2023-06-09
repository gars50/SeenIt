# SeenIt
SeenIt allows user to delete/abandon the media they watch/request on Plex

### Planned
- Configure deletions in Ombi, Sonarr and Radarr. Add safe mode.
    - Monitor if someone is watching before deleting
- Display the time according to user's time zone (Pick date)

### In Progress
- Add expiry date / auto-deletion
- Add popup on picks for admins
- Add time Javascript (moments)

### Completed
- Add a search option in medias
- Merge toastr and flash notifications
- Add an option to "order by" fields in media
- Add Plex login
    - Find a way to load app_settings with a unique ID for Plex
- Add adoption/requested date
- Users now have "picks", which allows multiple users per media

### Possible Ameliorations
- Add webhook in Tautulli and POST in SeenIt to add pick to media when they start watching something
    - Add Tautulli app information in settings
    - Add possibility to configure the notification agent in Tautulli from the app
- Add Picks by seasons to allow deletion of a few season at a time.