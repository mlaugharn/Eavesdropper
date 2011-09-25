import bottle, json, urllib, datetime

# http://stackoverflow.com/questions/775049/python-time-seconds-to-hms
def GetInHMS(seconds):
    hours = seconds / 3600
    seconds -= 3600*hours
    minutes = seconds / 60
    seconds -= 60*minutes
    if hours == 0:
        return "%02d:%02d" % (minutes, seconds)
    return "%02d:%02d:%02d" % (hours, minutes, seconds)


users = []
server_info = {}
mumbleJSON = None

@bottle.route('/static/:filename')
def send_image(filename):
    return bottle.static_file(filename, root='./static')

@bottle.route('/')
def index():
  global users
  global mumbleJSON
  users = []
  mumbleJSON = json.loads(urllib.urlopen("http://aypsela.servegame.com/mumble-django/mumble/embed/1.json").read())
  server_info["uptime"] = GetInHMS(mumbleJSON["x_uptime"])
  for user in mumbleJSON['root']['users']:
    users.append([user['name'], user['selfMute'], user['selfDeaf'], user['userid']])
  output = usersHTML()
  return output

@bottle.route('/channels/:channel')
def channelHTML(channel):
  global users
  users = []
  global mumbleJSON
  mumbleJSON = json.loads(urllib.urlopen("http://aypsela.servegame.com/mumble-django/mumble/embed/1.json").read())
  server_info["uptime"] = GetInHMS(mumbleJSON["x_uptime"])
  for user in mumbleJSON['root']['channels'][int(channel)]['users']:
    users.append([user['name'], user['selfMute'], user['selfDeaf'], user['userid']])
  output = usersHTML(channel)
  return output

def usersHTML(channel='root'):
  global mumbleJSON
  output = """
<!DOCTYPE html>
<html>
<head>
  <title>AYPSELA mumble stats</title>
  <link href="/static/style.css" rel="stylesheet" type="text/css">
</head>
<body>
  <div class="section">
  <h1>"""
  if channel!= 'root':
      output += mumbleJSON['root']['channels'][int(channel)]['name']
  else: output += "Root"
  output += """</h1>
  <table id="users">
    <tr>
      <th>Username</th>
      <th>Registered</th>
      <th>Muted</th>
      <th>Deafened</th>
    </tr>
"""
  for user in users:
    output += "<tr><td><h2>" + user[0] + "</h2>"
    output += "</td><td>"
    output += '<img src="/static/heart.png" alt="Registered"' if (user[3]) > 0 else ''
    output += "</td><td>" + '<img src="/static/muted.png" alt="Muted"' if user[1] else ''
    output += "</td><td>" + '<img src="/static/deaf.png" alt="Deafened"' if user[2] else ''
    output += "</td></tr>"
  if channel == 'root':
      output += """
      </table>
      </div>
      <div class="section">
      <table id="channels">
        <tr>
          <th>Channels</th>
        </tr>
      """
      for channel in mumbleJSON['root']['channels']:
          output += "<tr><td><h3>"
          output += '<a href="/channels/' + str(channel['id']-1) + '">'
          output += channel['name'] + " (" + str(len(channel['users'])) + ")"
          output += "</a></h3></td></tr>"
      output += """</table></div>
  <footer>
    Made by <a href="http://github.com/mlaugharn" alt="Marc Laugharn">mlaugharn</a> and <a href="http://github.com/atamis" alt="Andrew Amis">atamis</a><br>
"""
  output += "Generated at " + str(datetime.datetime.now())
  print(server_info)
  output += "<br />" + "Mumble server online for " + server_info["uptime"]
  output += """
  </footer>
  <script type="text/javascript">
    function reFresh() {
      location.reload(true)
    }
    window.setInterval("reFresh()",60000);
  </script>
</body>
</html>"""
  return output

bottle.debug(True)
bottle.run(host="0.0.0.0", port=9333)
