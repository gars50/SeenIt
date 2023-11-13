# SeenIt
SeenIt allows user to delete/abandon the media they watch/request on Plex/Ombi

## Planned
### Issues
- APScheduler only runs after a trigger, not after a restart of the application.
- Login/logout does not always work in dev, but works fine in prod
    - Seems to be a cookie issue, maybe related to gevent/gunicorn?
- Logs stop after 30 seconds with gunicorn with gevent
    - It just timeouts with no logs without gevent
- Flash messages not appearing in users

### Improvements
- Website looks
    - Settings
        - Tabbed settings
        - Better settings selection for updating the db (schedule)
- Add option to send email for errors
    - Add option to save email settings inside the app instead of configuration file
- Change user config so that a user is either a Plex user or a SeenIt user.
    - Add information on user type
    - Add Plex Auth Key to profile
- Plex login displays a warning about location of the application?
- Add option to change the jobs' schedule
- Automate mass delete
    - Tie the settings for mass delete with the actual APScheduler task
- Limit to one line for all text per row
    - Use ellipsis?
- Delete Ombi Requests when user deletes Ombi Request pick
- API Authentication
    - Add an API key in the settings for external use
- Add pick_method table instead of string
- Make Media agnostic, move mediaDB ids and urls, and media_manager ids
    - Add media_type class to differentiate between the two.

## In Progress
- Rework Users and Roles to allow decorators

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
- Import from Radarr/Sonarr
    - Add them to the permanent collection
- Change the updating of infos from Radarr/Sonarr by downloading the whole movie thing instead of constant API calls
- Add a better way to show storage
- Add storage used per user in users
- Add option to view the logs within the application
- Figure out a better way to mass delete
- Change datatables to AJAX
- Rework the poster preview as it's not showing up dynamically
- Fix "abandonned" typo in backend
- Remove last user for media. It is not necessary now with the abandoned date.
- Remove Pick Method when showing the Permanent Collection

## Possible improvements
- Add possibility to configure the notification agents in Tautulli from the SeenIt
    - Add Tautulli app information in settings
- Add Picks by seasons to allow deletion of a few season at a time.
- Allow admins and users to add picks manually? Is it needed?
- Logs for each day instead of lumped into one

## Cancelled
- Retrieve watchlist from plex?
    - Requests are done through Ombi, and requests will be deleted at the same time