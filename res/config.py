TIMESTAMP_PATTERN = r'.*(\d\d\d\d-\d\d-\d\d_\d\d-\d\d-\d\d).*'

FILE_NAME_PATTERN = r'(\d+)__(\d+)__\d\d\d\d-\d\d-\d\d_\d\d-\d\d-\d\d__(.*)\.'

STYLE_SHEET = """
BODY {
    font-family: Tahoma;
    font-size: 8pt;
    font-weight: none;
    text-align: center;
}

TH {
    font-family: Tahoma;
    font-size: 8pt;
    font-weight: bold;
    text-align: center;
}

TD {
    font-family: Tahoma;
    font-size: 8pt;
    font-weight: none;
    text-align: center;
    border: 1px solid gray; 
}
"""

# includes data heading for video player
#
# HTML_TEMPLATE = """</html>
# <head>
# <title>Events as at {}</title>
# <style type="text/css">
# {}
# </style>
# </head>
#
# <body>
# <h1>Events as at {}</h1>
#
# <center>
# <table width="90%">
#
# <tr>
# <th>Event ID</th>
# <th>Camera ID</th>
# <th>Timestamp</th>
# <th>Size</th>
# <th>Camera</th>
# <th>Screenshot</th>
# <th>Download</th>
# <th>Watch</th>
# </tr>
#
# {}
#
# </table>
# <center>
#
# </body>
# </html>
# """

HTML_TEMPLATE = """</html>
<head>
<title>Events as at {}</title>
<style type="text/css">
{}
</style>
</head>

<body>
<h1>Events as at {}</h1>

<center>
<table width="90%">

<tr>
<th>Event ID</th>
<th>Camera ID</th>
<th>Timestamp</th>
<th>Size</th>
<th>Camera</th>
<th>Screenshot</th>
<th>Download</th>
</tr>

{}

</table>
<center>

</body>
</html>
"""

# includes data column for video player
#
# HTML_REPEATER = """<tr>
# <td>{}</td>
# <td>{}</td>
# <td>{}</td>
# <td>{}</td>
# <td>{}</td>
# <td style="width: 320px";><a target="_blank" href="{}"><img src="{}" alt="{}" width="320" height="180" /></a></td>
# <td><a href="{}">Download</a></td>
# <td style="width: 320px";>
# <video controls width="320">
# <source src="{}" />
# </video>
# </td>
# </tr>"""

HTML_REPEATER = """<tr>
<td>{}</td>
<td>{}</td>
<td>{}</td>
<td>{}</td>
<td>{}</td>
<td style="width: 320px";><a target="_blank" href="{}"><img src="{}" alt="{}" width="320" height="180" /></a></td>
<td><a href="{}">Download</a></td>
</tr>"""

HTML_SEPARATOR = '<tr><th colspan="8" style="background-color: silver;">{}</th></tr>'
