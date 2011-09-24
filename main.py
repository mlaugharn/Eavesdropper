import bottle, json, urllib

mumbleJSON = json.loads(urllib.urlopen("http://aypsela.servegame.com/mumble-django/mumble/embed/1.json").read())
users = []

for user in mumbleJSON['root']['users']:
  users.append([user['name'], user['selfMute'], user['selfDeaf'], user['userid']])

def usersHTML():
  output = """
<!DOCTYPE html>
<html>
<head>
  <title>AYPSELA mumble stats</title>
  <link href="/static/style.css" rel="stylesheet" type="text/css">
</head>
<body>
  <table>
    <tr>
      <th>Username</th>
      <th>Registered</th>
      <th>Muted</th>
      <th>Deafened</th>
    </tr>
"""
  for user in users:
    output += "<tr><td><h1>" + user[0] + "</h1>"
    output += "</td><td>"
    output += '<img src="/static/heart.png" alt="Registered"' if (user[3]) > 0 else ''
    output += "</td><td>" + '<img src="/static/muted.png" alt="Muted"' if user[1] else ''
    output += "</td><td>" + '<img src="/static/deaf.png" alt="Deafened"' if user[2] else ''
    output += "</td></tr>"
  output += """
  </table>
  <footer>
    Made by <a href="github.com/mlaugharn" alt="Marc Laugharn">mlaugharn</a>
  </footer>
</body>
</html>"""
  return output


@bottle.route('/static/:filename')
def send_image(filename):
    return bottle.static_file(filename, root='./static')

@bottle.route('/')
def index():
  return usersHTML()

bottle.run()
