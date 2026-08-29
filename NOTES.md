1. auth.py
    hashing and verifying is done using CryptContext class of Passlib library's Passlib.context module
        hashing scheme - bcrypt, deprecated- auto (HAVENT CHANGED TO DEPREC YET)
        auto coz, if there r multiple schemes mentioned : first one is primary, others r marked as deprecated - old users, after successfull logins, their pwds will be reshashed using the firs hash
    what hashing does
        adds salt and work factor(rounds - how mnay times the hashing algo will be applied) and additionally a pepper(unlike salt whcih is random, unique and stored in the hash itself, pepper is stored in ur system and is the same for all)
        this means that hashing is one-way - u cannot get the original from its hash
    access tokens 
        JWT is three base64-encoded parts separated by dots — header.payload.signature. The payload contains your data ({"sub": "5", "exp": ...}), and the signature is created using your SECRET_KEY — so only your server can verify it's genuine.

        JWT is mainly used for signing and verifying         
        access token is a key unique to each user per each login (coz of the signature added to it by the server, created using the secret_key) 
        any chnages to the access token idicates its been tampered with
        while active, access token help fasten the verifying proces by skipping the db checking of username and pwd each time for each request
    oauth2_scheme
        tells fastapi to look for a Bearer token in the Authorization header of incoming requests, and if it's missing, return 401 before even reaching the route function.
        acts as a dependency to access routes
        expired → 401 "token expired", tampered → 401 "invalid token", user deleted → 401 "user not found"

2. routes/auth
    apirouter 
        is a tool used to organise the application by grouping related routes to different files
    RegisterRequest 
        is a class that checks if the recieved email and password through a request are both strings(here, but otherwise checks if all required fields are prestna and are of the  and if not raises 422 error). if yes, it continues to start the function, else, it raises an error
    get_db
        is a generator (python functions usually use the keyword 'return' to exit the function, but generators are python functions that use the keyword 'yield' to pause the fucntion, store local values, maybe send a value to another fucntion etc....so it doesnt leave the gen fucntion completely yet)
    session
        session=depends(get_db) is a dependency that first calls the get_db function, which in turn does the work of opening a new db connection...and that connection is stored in db
    register route
        is an endpoint that first checks if the given user and password is already registered by querying the database...if it exists, httpexception is raised else the new user object is first made by hashing the pwd, and the connection adds the object(lets sqlalchemy know that such an object exists) and commits it
    login route
        verification of the entered login details occurs
        oauth2passworresuestform
            depedndecny that stores the username and pasword from the entred form into form_data
        get_db
            the db connection is opened using get_db generator and is stored in db
        querying
            the querying is done by checking the enterde udername to see if it exists in db USer, if it doesnt 401 erroor saiyng invalid cred. if the pwd doesnt match, thenagain 401 invalid cred\
        returns token
            the fucntion returns the access toekn  by first calling the crate_access_token function, which in turn returns a jwt string whcih becomes the bearer token, which means that whoever owns this token is given access (with checking with server first about tampering, expiry, and user identity w/o having to open db connection, query, verify_pwd etc) without having to enter username and pwd each time
3. routes/chats
    the 