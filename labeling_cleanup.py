import httplib2
from oauth2client.client import SignedJwtAssertionCredentials
from apiclient.discovery import build
from apiclient import errors

SERVICE_ACCOUNT_EMAIL = "643460748243-5j6p8t6373k4jqheajld7um4s7r64pi2@developer.gserviceaccount.com"



def create_gmail_service(user_email):
    """
    Builds and returns a Gmail service object authorized with the
    application's service account.
    Returns:
        Gmail service object.
    """
    f = file('bprivate.pem', 'rb')
    key = f.read()
    f.close()
    credentials = SignedJwtAssertionCredentials(SERVICE_ACCOUNT_EMAIL, key, scope='https://mail.google.com/', sub=user_email)
    http = httplib2.Http()
    http = credentials.authorize(http)
     
    return build('gmail', 'v1', http=http)


def find_labels(service, user_id):
  try:
    response = service.users().labels().list(userId=user_id).execute()
    labels = response['labels']
    for label in labels:
        if label['name'] == "DELETEME":
            return label['id']  
    else:
        return False
  except errors.HttpError, error:
    print 'An error occurred: %s' % error



def delete_label(service, user_id, label_id):
  """Delete a label.

  Args:
    service: Authorized Gmail API service instance.
    user_id: User's email address. The special value "me"
    can be used to indicate the authenticated user.
    label_id: string id of the label.
  """
  try:
    service.users().labels().delete(userId=user_id, id=label_id).execute()
    print 'Label with id: %s deleted successfully.' % label_id
  except errors.HttpError, error:
    print 'An error occurred: %s' % error

def main():
    user = "cloudbakers@burnhamnationwide.com"
    service = create_gmail_service(user)
    label_id = find_labels(service, user)
    if label_id:
        delete_label(service, user, label_id)
    else:
        print "%s had an error" % user

if __name__ == '__main__':
    main()




