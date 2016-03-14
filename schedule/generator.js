'use strict'

const fs = require('fs')
const crypto = require('crypto')
const moment = require('moment')
const handlebars = require('handlebars')

const tpl = handlebars.compile(fs.readFileSync(__dirname + '/schedule.tpl').toString('utf-8'))
const sessionsData = require('../out/sessions.json')
const speakersData = require('../out/speakers.json')

function slugify(str) {
  return str.replace(/[^\w]/g, '-').replace(/-+/g, '-').toLowerCase()
}

function speakerNameWithOrg(speaker) {
  return speaker.organisation ? 
    `${speaker.name} (${speaker.organisation})` : 
    speaker.name
}

function foldByDate(tracks) {
  let dateMap = new Map() 

  tracks.forEach(track => {
    if (!dateMap.has(track.date)) dateMap.set(track.date, {
      caption: track.date, 
      tracks: []
    })
    dateMap.get(track.date).tracks.push(track)
  })

  let dates = Array.from(dateMap.values())
  dates.forEach(date => date.tracks.sort(byProperty('sortKey')))

  return dates;
}

function byProperty(key) {
  return (a, b) => {
    if (a[key] > b[key]) return 1
    if (a[key] < b[key]) return -1
    else return 0
  }
}

function sessionId(session) {
  let data = [session.title, session.session_id, session.start].join('|')
  return crypto.createHash('md5').update(data).digest('hex');
}

function zeroFill(num) {
  if (num >= 10) return num.toString()
  else return '0' + num.toString()
}

function foldByTrack(sessions, speakers) {
  let trackData = new Map()
  let speakersMap = new Map(speakers.map(s => [s.id, s]));

  sessions.forEach(session => {
    if (!session.start_time)
      return

    // generate slug/key for session
    let date = moment(session.start_time).format('YYYY-MM-DD') 
    let slug = date + '-' + slugify(session.track.name)
    let track = null

    // set up track if it does not exist
    if (!trackData.has(slug)) {
      track = {
        title: session.track.name,
        date: moment(session.start_time).format('ddd, MMM DD'),
        slug: slug, 
        sortKey: date + '-' + zeroFill(session.track.order),
        sessions: []
      }
      trackData.set(slug, track)
    } else {
      track = trackData.get(slug)
    }

    track.sessions.push({
      start: moment(session.start_time).utcOffset(8).format('hh:mm a'),
      title: session.title,
      type: session.type,
      location: session.location,
      speakers: session.speakers.map(speakerNameWithOrg),
      speakers_list: session.speakers.map(speaker => speakersMap.get(speaker.id)),
      description: session.description,
      uniqid: sessionId(session),
      session_id: session.session_id
    })
  })

  let tracks = Array.from(trackData.values())
  tracks.sort(byProperty('sortKey'))

  return tracks
}

function transformData(sessions, speakers) {
  let tracks = foldByTrack(sessions.sessions, speakers.speakers)
  let days = foldByDate(tracks)
  return {tracks, days}
}

const data = transformData(sessionsData, speakersData)
process.stdout.write(tpl(data))
