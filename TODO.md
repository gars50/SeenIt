# SeenIt
SeenIt allows user to delete/abandon the media they watch/request on Plex/Ombi

## Planned
### Issues
- APScheduler only runs after a trigger, not after a restart of the application.
- Add a better way to show storage

### Improvements
- Website looks
    - Settings
        - Tabbed settings
        - Better settings selection for updating the db (schedule)
    - Figure out a better way to mass delete
- Add option to send email for errors
- Add option to save email settings inside the app instead of configuration file
- Change user config so that a user is either a Plex user or a SeenIt user.
    - Add information on user type
- Add option to view the logs within the application
- Plex login displays a warning about location of the application?
- Add option to change the jobs' schedule
- Change datatables to AJAX
- Import from Radarr/Sonarr
    - Add them to the permanent collection
- Add storage used per user in users

## In Progress


## Completed
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
- Add check for admin on data update
- Add storage information per user / total
- Add explanation to the index page
- Feedback on "Abandonned" vs "Let go" only for the user
- Fix deletion date
    - When changing deletion date options, update deletion dates of abandonned media
- Add logging
- Allow users to change their alias
- Fix issue where server gets rate-limited with DNS queries. Python's "requests" does a lookup at each request. (https://stackoverflow.com/questions/36087637/how-often-does-python-requests-perform-dns-queries#:~:text=Yes%2C%20the%20Python%20requests%20lib,with%20the%20python%20requests%20library)
    - This happens when importing everything as there are multiple queries to Ombi/Radarr/Sonarr
- Fix sort by date
- Add delete confirm prompt for Media deletion
- Add title from Tautulli for better logs
- Pick dates in admin, wrong timezone
- Change API calls to an API route
- Test services to come from the application instead of client browser
- Application settings, Media Deletion. Date is UTC, not moment
- Add poster picture on mouseover of the title
- Add permanent collection

## Possible improvements
- Add possibility to configure the notification agent in Tautulli from the app
    - Add Tautulli app information in settings
- Add Picks by seasons to allow deletion of a few season at a time.
- Allow admins and users to add picks manually? Is it needed?
- Logs for each day instead of lumped into one
- Retrieve watchlist from plex?