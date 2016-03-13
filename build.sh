# thanks to https://gist.github.com/domenic/ec8b0fc8ab45f39403dd
#!/bin/sh
set -e

git config --global user.name "Travis CI"
git config --global user.email "noreply+travis@fossasia.org"

python scraper.py

# don't continue if no changes
if git diff-index --quiet HEAD -- out/*.json; then
  exit 0
fi

git commit -m '[Auto] updated json files [ci skip]' out/*.json
git push "https://${GH_TOKEN}@github.com/fossasia/open-event-scraper" HEAD:master

git clone --depth=1 "https://${GH_TOKEN}@github.com/fossasia/2016.fossasia.org" fa16-repo

node schedule/generator > fa16-repo/schedule/index.html

cd fa16-repo

if git diff-index --quiet HEAD -- schedule/index.html; then
  exit 0
fi

git commit -m '[Auto] updated schedule' schedule/index.html
git push origin gh-pages

exit 0
