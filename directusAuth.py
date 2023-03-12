import requests
import config
import time

# VARIABLES USED BY THE SESSION MANAGEMENT
LOGIN_URL = config.LOGIN_URL

# these should be placed in the local properties file and used by BuildConfig
# JSON_URL should be WITHOUT a trailing slash (/)!
JSON_URL = config.JSON_URL
REFRESH_URL = config.REFRESH_URL

# if using username + password in the service (e.g. Directus), use these
username = config.DIRECTUS_USERNAME
password = config.DIRECTUS_PASSWORD

# state booleans to determine our session state
loggedIn = False
needsRefresh = True

# stored tokens. refresh is used when our session token has expired
# access token in this case is the same as session token
refreshToken = ""
accessToken = ""
refreshTimer = time.time()

def loginAction():
    print("login")
    print(JSON_URL + " login")
    request = requests.post(LOGIN_URL,
                            headers={"Accept": "application/json", "Content-Type": "application/json; charset=utf-8"},
                            json={"email": username, "password": password})
    if request.status_code == 200:
        responseJSON = request.json()
        accessToken = responseJSON["data"]["access_token"]
        print(accessToken)
        refreshToken = responseJSON["data"]["refresh_token"]
        loggedIn = True

        # after login's done, get data from API
        dataAction(loggedIn,accessToken)
        return refreshToken

    else:
        print(request.text)


def refreshLogin(refreshToken):
    print('refreshLogin()')
    token = refreshToken
    if needsRefresh:
        loggedIn = False
        print(REFRESH_URL + " login")
        print(token + ' Refresh')
        request = requests.post(REFRESH_URL,
                                headers={"Accept": "application/json",
                                         "Content-Type": "application/json; charset=utf-8"},
                                json={"refresh_token": token})
        if request.status_code == 200:
            responseJSON = request.json()
            accessToken = responseJSON["data"]["access_token"]
            token = responseJSON["data"]["refresh_token"]
            loggedIn = True


            # after login's done, get data from API
            dataAction(loggedIn,accessToken)
            return token
        else:
            print(request.text)

def dataAction(loggedIn,accessToken):
    if loggedIn:
        print("dataAction()")
        request = requests.get(JSON_URL,
                               headers={"Authorization": f"Bearer {accessToken}", "Accept": "application/json"})
        if request.status_code == 200:
            print(request.json())
        else:
            print(request.text)
        return loggedIn,accessToken



def main():
    # start with login
    refreshToken = loginAction()

    if time.time() - refreshTimer > 3:
        needsRefresh = True
        refreshLogin(refreshToken)




if __name__ == "__main__":
    main()