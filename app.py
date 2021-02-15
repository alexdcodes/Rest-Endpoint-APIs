# Education from Tutorial how to build Rest API Endpoint From Scratch

#   _____  .__                  ________  .__ __
#  /  _  \ |  |   ____ ___  ___ \______ \ |__|  | __ ___________
# /  /_\  \|  | _/ __ \\  \/  /  |    |  \|  |  |/ // __ \_  __ \
#/    |    \  |_\  ___/ >    <   |    `   \  |    <\  ___/|  | \/
#\____|__  /____/\___  >__/\_ \ /_______  /__|__|_ \\___  >__|
#        \/          \/      \/         \/        \/    \/
#
from flask import Flask
from flask_restful import Resource, Api, reqparse
import pandas as pd
import ast
import smtplib

app = Flask(__name__)
api = Api(app)


class Device(Resource):
    def get(self):
        data = pd.read_csv('devices.csv')
        data = data.to_dict()
        return {'data': data}, 200

    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('placeID', required=True)
        parser.add_argument('ip', required=True)
        parser.add_argument('device', required=True)
        args = parser.parse_args()

        data = pd.read_csv('Device.csv')

        if args['placeID'] in list(data['placeID']):
            return {
                       'message': f"'{args['placeID']}' already exists."
                   }, 409
        else:
            new_data = pd.DataFrame({
                'placeID': [args['placeID']],
                'ip': [args['ip']],
                'device': [args['device']],
                'locations': [[]]
            })
            data = data.append(new_data, ignore_index=True)
            data.to_csv('Device.csv', index=False)
            return {'data': data.to_dict()}, 200

    def put(self):
        parser = reqparse.RequestParser()
        parser.add_argument('placeID', required=True)
        parser.add_argument('location', required=True)
        args = parser.parse_args()

        # read our CSV
        data = pd.read_csv('Device.csv')

        if args['placeID'] in list(data['placeID']):

            data['locations'] = data['locations'].apply(
                lambda x: ast.literal_eval(x)
            )
            device_data = data[data['placeID'] == args['placeID']]

            device_data['locations'] = device_data['locations'].values[0] \
                .append(args['location'])

            data.to_csv('Device.csv', index=False)
            return {'data': data.to_dict()}, 200

        else:
            return {
                       'message': f"'{args['placeID']}' device not found."
                   }, 404

    def delete(self):
        parser = reqparse.RequestParser()
        parser.add_argument('placeID', required=True)
        args = parser.parse_args()

        data = pd.read_csv('Device.csv')

        if args['placeID'] in list(data['placeID']):
            data = data[data['placeID'] != args['placeID']]

            data.to_csv('Device.csv', index=False)
            return {'data': data.to_dict()}, 200
        else:
            return {
                       'message': f"'{args['placeID']}' user not found."
                   }, 404


class SendMail(Resource):
    def get(self):
        print("")
        to = 'alex.diker@github.com'
        user = 'alex.diker@github.com'
        smtpserver = smtplib.SMTP("", 11)
        smtpserver.ehlo()
        smtpserver.starttls()
        smtpserver.ehlo()
        header = 'To:' + to + '\n' + 'From: ' + user + '\n' + 'Subject: Sending Mail Attachment\n'
        print(header)
        msg = header + '\n This mailbox has sent an attachment.\n\n'
        smtpserver.sendmail(user, to, msg)
        print('INFO: Email notification successfully sent')
        smtpserver.close()

    def post(self):
        print("")
        to = 'alex.diker@github.com'
        user = 'alex.diker@github.com'
        smtpserver = smtplib.SMTP("", 11)
        smtpserver.ehlo()
        smtpserver.starttls()
        smtpserver.ehlo()
        header = 'To:' + to + '\n' + 'From: ' + user + '\n' + 'Subject: Rest API Python - Sending Mail Attachment\n'
        print(header)
        msg = header + '\n This mailbox has sent an attachment.\n\n'
        smtpserver.sendmail(user, to, msg)
        print('INFO: Email notification successfully sent')
        smtpserver.close()

    def patch(self):
        parser = reqparse.RequestParser()
        parser.add_argument('userId', required=True, type=int)
        parser.add_argument('ip', store_missing=False)
        parser.add_argument('subject', store_missing=False)
        args = parser.parse_args()

        data = pd.read_csv('sendmail.csv')

        if args['userId'] in list(data['userId']):
            device_data = data[data['userId'] == args['userId']]

            if 'ip' in args:
                device_data['ip'] = args['ip']
            if 'subject' in args:
                device_data['subject'] = args['subject']


            data[data['userId'] == args['userId']] = device_data
            data.to_csv('sendmail.csv', index=False)
            return {'data': data.to_dict()}, 200

        else:
            return {
                       'message': f"'{args['userId']}' location does not exist."
                   }, 404

    def delete(self):
        parser = reqparse.RequestParser()
        parser.add_argument('userId', required=True, type=int)
        args = parser.parse_args()

        data = pd.read_csv('sendmail.csv')

        if args['userId'] in list(data['userId']):
            data = data[data['userId'] != args['userId']]
            data.to_csv('sendmail.csv', index=False)
            return {'data': data.to_dict()}, 200

        else:

            return {
                'message': f"'{args['userId']}' location does not exist."
            }


api.add_resource(Device, '/devices')
api.add_resource(SendMail, '/SendMail')


bootstrap = """<link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/4.1.0/css/bootstrap.min.css">
  <script src="https://ajax.googleapis.com/ajax/libs/jquery/3.3.1/jquery.min.js"></script>
  <script src="https://cdnjs.cloudflare.com/ajax/libs/popper.js/1.14.0/umd/popper.min.js"></script>
  <script src="https://maxcdn.bootstrapcdn.com/bootstrap/4.1.0/js/bootstrap.min.js"></script>"""

beauty = """<nav class="navbar navbar-expand-lg navbar-light bg-light">
  <a class="navbar-brand" href="#">Alex Diker Technologies</a>
  <button class="navbar-toggler" type="button" data-toggle="collapse" data-target="#navbarSupportedContent" aria-controls="navbarSupportedContent" aria-expanded="false" aria-label="Toggle navigation">
    <span class="navbar-toggler-icon"></span>
  </button>

  <div class="collapse navbar-collapse" id="navbarSupportedContent">
    <ul class="navbar-nav mr-auto">
      <li class="nav-item active">
        <a class="nav-link" href="#">Send Email <span class="sr-only">(current)</span></a>
      </li>
      <li class="nav-item">
        <a class="nav-link" href="#">Attachments</a>
      </li>
      <li class="nav-item dropdown">
        <a class="nav-link dropdown-toggle" href="#" id="navbarDropdown" role="button" data-toggle="dropdown" aria-haspopup="true" aria-expanded="false">
          Applications
        </a>
        <div class="dropdown-menu" aria-labelledby="navbarDropdown">
          <a class="dropdown-item" href="#">Action Item
          </a>
          <a class="dropdown-item" href="#">Another action</a>
          <div class="dropdown-divider"></div>
          <a class="dropdown-item" href="#">Something else here</a>
        </div>
      </li>
      <li class="nav-item">
      </li>
    </ul>
    <form class="form-inline my-2 my-lg-0">
      <input class="form-control mr-sm-2" type="search" placeholder="Search" aria-label="Search">
      <button class="btn btn-outline-success my-2 my-sm-0" type="submit">Search</button>
    </form>
  </div>
</nav>"""

@app.route('/')
def start_page():
    return bootstrap + beauty + '<hr></hr>Send Email Dashboard Reuseable: <p> <b>Send Email</b>'


if __name__ == '__main__':
    app.run()