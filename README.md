# open-event-scraper

Google spreadsheet parsing for FOSSASIA 2016

## setup

```shell
pip install -r requirements.txt
./run.sh
```

#Configuration on heroku server
```shell

$ heroku login

$ heroku create

$ git push heroku master

$ heroku run bundle install

$ heroku config:set GIT_REPO=fossasia/open-event-scraper
$ heroku config:set GITHUB_TOKEN=Your token
$ heroku config:set GH_TOKEN=Your token
```

## License

[MIT](./LICENSE)
