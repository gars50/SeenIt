# SeenIt
SeenIt allows user to delete/abandon the media they watch/request on Plex/Ombi

## Planned
### Issues
- APScheduler only runs after a trigger, not after a restart of the application.
- Logs stop after 30 seconds with gunicorn
    - It just timeouts with no logs without gevent
- Cookie issues in Dev
    - Flash messages not appearing in users
    - Login/logout does not always work if you do not select remember me.
- Fix issue where server gets rate-limited with DNS queries. Python's "requests" does a lookup at each request. (https://stackoverflow.com/questions/36087637/how-often-does-python-requests-perform-dns-queries#:~:text=Yes%2C%20the%20Python%20requests%20lib,with%20the%20python%20requests%20library)
    - Still happens on a Delete

### Improvements
- Website looks
    - Settings
        - Tabbed settings
        - Better settings selection for updating the db (schedule)
- Add option to send email for errors
    - Add option to save email settings inside the app instead of configuration file
- Change user config so that a user is either a Plex user or a SeenIt user.
    - Add Plex Auth Key to profile
- Add option to change the jobs' schedule
- Automate mass delete
    - Tie the settings for mass delete with the actual APScheduler task
- Limit to one line for all text per row in datatables
    - Use ellipsis?
- Delete Ombi Requests when user deletes Ombi Request pick
- API Authentication
    - Add an API key in the settings for external use (Tautulli)
- Make Media agnostic, move mediaDB ids and urls, and media_manager ids
    - Add media_type class to differentiate between the two.
- Move methods away from app.scripts.media into their respective classes
    - Create API Classes for Radarr, Sonarr, Ombi

## In Progress
- Add pick_method table instead of string

## Possible improvements
- Add possibility to configure the notification agents in Tautulli from the SeenIt
    - Add Tautulli app information in settings
- Add Picks by seasons to allow deletion of a few season at a time.
- Logs for each day instead of lumped into one
- Plex login displays a warning about location of the application?

## Cancelled
- Retrieve watchlist from plex?
    - Requests are done through Ombi, and requests will be deleted at the same time