import pyrebase
import glob
import os
import authentication

def upload(firebase):
    storage = firebase.storage()
    logos = glob.glob('logo/*')
    for logo in logos:
        storage.child(logo).put(logo)

def main():
    firebase,user = authentication.authentication()
    upload(firebase)

if __name__ == "__main__":
    main()
