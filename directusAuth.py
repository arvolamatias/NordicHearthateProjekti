import requests
import config

# VARIABLES USED BY THE SESSION MANAGEMENT
LOGIN_URL = config.LOGIN_URL

# these should be placed in the local properties file and used by BuildConfig
# JSON_URL should be WITHOUT a trailing slash (/)!
JSON_URL = config.JSON_URL

# if using username + password in the service (e.g. Directus), use these
username = config.DIRECTUS_USERNAME
password = config.DIRECTUS_PASSWORD

# state booleans to determine our session state
loggedIn = False
needsRefresh = False

# stored tokens. refresh is used when our session token has expired
# access token in this case is the same as session token
refreshToken = ""
accessToken = ""


def loginAction():
    print("login")
    print(JSON_URL + " login")
    request = requests.post(LOGIN_URL,
                            headers={"Accept": "application/json", "Content-Type": "application/json; charset=utf-8"},
                            json={"email": username, "password": password})
    if request.status_code == 200:
        responseJSON = request.json()
        accessToken = responseJSON["data"]["access_token"]
        refreshToken = responseJSON["data"]["refresh_token"]
        print(accessToken)
        loggedIn = True
        # after login's done, get data from API
        dataAction()
    else:
        print(request.text)


def refreshLogin():
    if needsRefresh:
        loggedIn = False
        # use this if using refresh logic
        # refreshRequestQueue?.add(loginRefreshRequest)

        # if using refresh logic, comment this line out
        loginAction()


def dataAction():
    if loggedIn:
        request = requests.get(JSON_URL,
                               headers={"Authorization": f"Bearer {accessToken}", "Accept": "application/json"})
        if request.status_code == 200:
            print(request.json())
        else:
            print(request.text)


def main():
    # start with login
    loginAction()


if __name__ == "__main__":
    main()