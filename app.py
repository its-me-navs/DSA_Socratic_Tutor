import streamlit as st
import requests

BASE_URL = "http://127.0.0.1:8000"

def api(method, endpoint, data=None, token=None):
    headers = {"Authorization": f"Bearer {token}"} if token else {}
    if method == "POST":
        return requests.post(f"{BASE_URL}{endpoint}", json=data, headers=headers)
    return requests.get(f"{BASE_URL}{endpoint}", headers=headers, params=data)

def login_page():
    st.title("DSA Socratic Tutor")
    st.subheader("Login")
    email = st.text_input("Email")
    password = st.text_input("Password", type="password")
    col1, col2 = st.columns(2)
    with col1:
        if st.button("Login", use_container_width=True):
            res = requests.post(f"{BASE_URL}/auth/login", data={"username": email, "password": password})
            if res.status_code == 200:
                st.session_state.token = res.json()["access_token"]
                st.session_state.page = "chat"
                st.rerun()
            else:
                st.error("Invalid credentials")
    with col2:
        if st.button("Register", use_container_width=True):
            res = api("POST", "/auth/register", {"email": email, "password": password})
            if res.status_code == 200:
                st.success("Registered! Please login.")
            else:
                st.error(res.json().get("detail", "Registration failed"))

def chat_page():
    st.title("DSA Socratic Tutor")
    token = st.session_state.token

    with st.sidebar:
        st.subheader("New Session")
        title = st.text_input("Session Title", placeholder="e.g. Two Sum Practice")
        problem = st.text_input("Problem", placeholder="e.g. Two Sum")
        if st.button("Start Session"):
            res = api("POST", "/chat/session",
                     {"title": title, "mode": "practice", "problem": problem},
                     token=token)
            if res.status_code == 200:
                st.session_state.session_id = res.json()["session_id"]
                st.session_state.messages = []
                st.rerun()

        st.divider()
        if st.button("Review Queue"):
            st.session_state.page = "review"
            st.rerun()
        if st.button("Logout"):
            for key in list(st.session_state.keys()):
                del st.session_state[key]
            st.rerun()

    if "session_id" not in st.session_state:
        st.info("Create a new session from the sidebar to start practicing.")
        return

    st.subheader(f"Session: {title if title else 'Active'}")

    for msg in st.session_state.get("messages", []):
        with st.chat_message(msg["role"]):
            st.write(msg["content"])

    user_input = st.chat_input("Type your message...")
    if user_input:
        st.session_state.messages.append({"role": "user", "content": user_input})
        with st.chat_message("user"):
            st.write(user_input)

        with st.spinner("Thinking..."):
            res = api("POST", f"/chat/session/{st.session_state.session_id}/message",
                     {"content": user_input}, token=token)

        if res.status_code == 200:
            reply = res.json()["response"]
            st.session_state.messages.append({"role": "assistant", "content": reply})
            with st.chat_message("assistant"):
                st.write(reply)
        else:
            st.error("Something went wrong.")

def review_page():
    st.title("Review Queue")
    token = st.session_state.token

    if st.button("← Back to Chat"):
        st.session_state.page = "chat"
        st.rerun()

    res = api("GET", "/review/due", token=token)
    if res.status_code == 200:
        items = res.json()
        if not items:
            st.success("No reviews due today!")
        else:
            st.subheader(f"{len(items)} problem(s) due for review")
            for item in items:
                with st.container(border=True):
                    col1, col2 = st.columns([3, 1])
                    with col1:
                        st.write(f"**{item['problem']}**")
                        st.caption(f"Stage: {item['stage']} | Due: {item['next_review'][:10]}")
                    with col2:
                        if st.button("✓ Done", key=f"done_{item['id']}"):
                            api("POST", f"/review/{item['id']}/complete", token=token)
                            st.rerun()
    else:
        st.error("Could not load review queue.")

if "page" not in st.session_state:
    st.session_state.page = "login"

if st.session_state.page == "login":
    login_page()
elif st.session_state.page == "chat":
    chat_page()
elif st.session_state.page == "review":
    review_page()