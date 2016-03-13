# thanks to https://gist.github.com/domenic/ec8b0fc8ab45f39403dd
#!/bin/sh
set -e

git clone --depth=1 "https://${GH_TOKEN}@github.com/fossasia/2016.fossasia.org" fa16-repo

python scraper.py
node schedule/generator > fa16-repo/schedule/index.html

cd fa16-repo
git config user.name "Travis CI"
git config user.email "noreply+travis@fossasia.org"

CHANGED=$(git status -s)
if [ "$CHANGED" != "" ]
then
  git commit -am '[Auto] updated schedule'
  git push origin gh-pages
else
  echo "no changes"
fi

exit 0
