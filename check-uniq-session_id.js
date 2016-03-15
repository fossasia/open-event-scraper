'use strict'

var sessions=require('./out/sessions.json').sessions;
var map=new Map();
sessions.map(s => s.session_id).forEach((id, index) => {
  let seen = map.get(id);
  if (seen === undefined)
    map.set(id, [index]);
  else
    seen.push(index);
})
var has_dupes = false;
map.forEach((seen, id) => {
  if (seen.length <= 1)
    return;
  has_dupes = true;
  var dupe_sessions = seen.map(id => sessions[id]);
  console.log('there are', seen.length, 'duplicates for session id', id, ': ', dupe_sessions);
});
process.exit(has_dupes ? 1 : 0)
