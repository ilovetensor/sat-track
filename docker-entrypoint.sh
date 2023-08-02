# docker-entrypoint.sh

# If this is going to be a cron container, set up the crontab.
if [ "$1" = cron ]; then
  ./manage.py crontab add
fi

# Launch the main container command passed as arguments.
exec "$@"