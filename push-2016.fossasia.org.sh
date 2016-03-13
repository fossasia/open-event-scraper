# thanks to https://gist.github.com/domenic/ec8b0fc8ab45f39403dd
#!/bin/sh
set -e

if ! git diff-index --quiet HEAD schedule/index.html; then
  git clone "https://${GH_TOKEN}@github.com/fossasia/2016.fossasia.org" repo_out
  cp schedule/index.html repo_out/schedule/index.html
  cd repo_out
  git config user.name "Travis CI"
  git config user.email "noreply-travis@fossasia.org"
  git commit -m 'Regenerated schedule/index.html' schedule/index.html
  git push origin gh-pages
fi
