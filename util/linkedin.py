# this will create resumes on the bases of the template and the data provided by the user
# extract the data from the user linkedin profile

# take the template.json file fields as template and create a resume on the bases of the data provided by the user

# request "POST https://www.linkedin.com/oauth/v2/accessToken HTTP/1.1
# Content-Type: application/x-www-form-urlencoded
# grant_type=client_credentials
# client_id={your_client_id}
# client_secret={your_client_secret}"

import requests

# GET https://www.linkedin.com/oauth/v2/authorization?response_type=code&client_id=77xcd71557lqtc&redirect_uri=https%3A%2F%2Fwww.linkedin.com%2Fcompany%2Fidku%2F&scope=r_liteprofile

def get_access_token():
    # request "POST https://www.linkedin.com/oauth/v2/accessToken HTTP/1.1
    # Content-Type: application/x-www-form-urlencoded
    # grant_type=client_credentials
    # client_id={your_client_id}
    # client_secret={your_client_secret}"
    r = requests.post("https://www.linkedin.com/oauth/v2/accessToken",
                    data={
                        "grant_type": "client_credentials",
                        "client_id": "77xcd71557lqtc",
                        "client_secret": "gRfGHfIpi4j9drPm"
                    },
                    headers={
                        "Content-Type": "application/x-www-form-urlencoded"
                    })
    print(r.json())
    if r.status_code == 200:
        return r.json()["access_token"]
    else:
        return ""

ret= get_access_token()
print(ret)