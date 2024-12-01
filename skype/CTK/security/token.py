import requests


def get_token(email, password):
    url = "http://localhost/server_token/main.php"
    print(email, password)
    data = {"email": email, "password": password}

    print(data)
    try:
        # Gửi request POST tới API
        response = requests.post(url, json=data)

        # Kiểm tra mã trạng thái phản hồi
        if response.status_code == 200:
            print("HTTP 200 OK")
            response_data = response.json()
            print("Full API response:", response_data)

            # Kiểm tra trạng thái thành công
            if response_data.get("status") == "success":
                token = response_data.get("token")

                try:
                    with open("token.txt", "w") as f:
                        f.write(token)
                except Exception as e:
                    print("Error while writing token:", e)
                    import traceback
                    print("Traceback:", traceback.format_exc())
            else:
                print("Login failed:", response_data.get("message", "Unknown error"))
        else:
            print("HTTP Error:", response.status_code)
    except requests.exceptions.RequestException as e:
        print("Request failed:", e)

def verify_token(token):
    url = "http://localhost/server_token/vertify_token.php"
    data = {"token": token}
    response = requests.get(url, headers=data)
    if response.status_code == 200 and response.json().get("status") == "success":
        print(response.json())
        data = response.json()["data"]
        return data