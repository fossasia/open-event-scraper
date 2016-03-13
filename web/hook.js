'use strict'

const assert = require('assert')
const request = require('request')
const express = require('express')
const bodyParser = require('body-parser')

assert(process.env.GITHUB_TOKEN, 'GITHUB_TOKEN must be set')
assert(process.env.GIT_REPO, 'GIT_REPO must be set')

const API_TOKEN = process.env.GITHUB_TOKEN
const REPO = process.env.GIT_REPO

const app = express()
const travis = request.defaults({
  baseUrl: 'https://api.travis-ci.org',
  json: true
})

app.use(bodyParser.json())

app.get('/', (req, res, next) => {
  res.status(200, 'OK')
})

app.get('/build', (req, res, next) => {
  authorize((err, token) => {
    if (err) next(err)
    else triggerBuild(token, (err, data) => {
      if (err) next(err)
      else res.status(200).json(data)
    })
  })
})

function authorize(cb) {
  travis.post('/auth/github', {
    body: {github_token: API_TOKEN},
    headers: {'User-Agent': 'Travis/1.0'}
  }, (err, _res) => {
    if (err) cb(err)
    else cb(null, _res.body.access_token)
  })
}

function triggerBuild(token, cb) {
  let path = 'repo/' + encodeURIComponent(REPO) + '/requests'
  let body = {branch: 'master', message: 'API request'}
  let headers = {
    'User-Agent': 'Travis/1.0',
    'Travis-API-Version': '3',
    'Authorization': `token ${token}`
  }
  travis.post(path, {body, headers}, (err, res) => {
    if (err) cb(null, err)
    else if (!/^2/.test(res.statusCode.toString())) cb(res.body)
    else cb(null, res.body)
  })
}

app.listen(9000, _ => console.log(':9000'))
