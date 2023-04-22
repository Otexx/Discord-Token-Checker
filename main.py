import requests
import json

class Data:
    def __init__(self):
        self.email_verified = 0
        self.not_verified = 0

def main():
    with open("tokens.txt", "r") as tokens_file, \
         open("Results/email-verified.txt", "w") as email_verified_file, \
         open("Results/not-verified.txt", "w") as not_verified_file:

        data = Data()
        tokens = []

        for token in tokens_file:
            token = token.strip()
            token_parts = token.split(":")

            if len(token_parts) == 1:
                token_type = ""
                token_value = token
            elif len(token_parts) == 3:
                token_type = ""
                token_value = token_parts[2]
            else:
                print(f"Invalid token format - removed from file")
                continue

            profile_of_user = validate_token(token_value)
            if profile_of_user is None:
                print(f"Invalid token - removed from file")
                continue

            tokens.append(token)

            if profile_of_user["verified"]:
                email_verified_file.write(token + "\n")
                data.email_verified += 1
                print(f"\033[32m{token_type.capitalize()}Token is verified.\033[0m")
            else:
                not_verified_file.write(token + "\n")
                data.not_verified += 1
                print(f"\033[31m{token_type.capitalize()}Token is not verified.\033[0m")

        tokens_file.close()
        email_verified_file.close()
        not_verified_file.close()

        with open("tokens.txt", "w") as output_file:
            output_file.write("\n".join(tokens))

        print(f"\033[34mFinished Checking\nEmail Verified: {data.email_verified} | Not Verified: {data.not_verified}\033[0m\n")

def validate_token(token):
    check_req = requests.get("https://discord.com/api/v9/users/@me", headers={"Authorization": token})

    if check_req.status_code == 200:
        profile = json.loads(check_req.text)
        return {"username": profile["username"], "discriminator": profile["discriminator"], "verified": profile["verified"]}
    else:
        return None

if __name__ == "__main__":
    main()
