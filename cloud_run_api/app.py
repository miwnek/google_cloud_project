from flask import Flask, request, Response, jsonify
from google.cloud import firestore

app = Flask(__name__)
db = firestore.Client(database="urlsdb")

# @app.post("/urls")
# def add_url():
#     data = request.json
#     db.collection("urls").add({"url": data["url"], "active": True})
#     return jsonify({"status": "ok"})

# @app.get("/urls")
# def list_urls():
#     docs = db.collection("urls").stream()
#     return jsonify([doc.to_dict() for doc in docs])

# CREATE
@app.post("/urls")
def add_url():
    data = request.json
    if not data or "url" not in data:
        return jsonify({"error": "url required"}), 400

    doc_ref = db.collection("urls").add({"url": data["url"], "active": True})
    return jsonify({"status": "ok", "id": doc_ref[1].id})


# READ
@app.get("/urls")
def list_urls():
    docs = db.collection("urls").stream()
    return jsonify([{"id": d.id, **d.to_dict()} for d in docs])


# DELETE
@app.delete("/urls/<doc_id>")
def delete_url(doc_id):
    db.collection("urls").document(doc_id).delete()
    return jsonify({"status": "deleted", "id": doc_id})


# VERY BASIC FRONTEND
@app.get("/")
def frontend():
    html = """
<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8" />
<title>URL Manager</title>
<style>
body { font-family: sans-serif; max-width: 600px; margin: 2rem auto; }
input, button { padding: 0.5rem; font-size: 1rem; }
li { margin: 0.3rem 0; }
button.del { margin-left: 0.5rem; }
</style>
</head>
<body>
<h2>URL Manager</h2>

<input id="urlInput" placeholder="https://example.com">
<button onclick="addUrl()">Add</button>

<ul id="list"></ul>

<script>
async function loadUrls() {
  const res = await fetch("/urls");
  const data = await res.json();
  const list = document.getElementById("list");
  list.innerHTML = "";
  data.forEach(u => {
    const li = document.createElement("li");
    li.textContent = u.url;
    const btn = document.createElement("button");
    btn.textContent = "Delete";
    btn.className = "del";
    btn.onclick = () => deleteUrl(u.id);
    li.appendChild(btn);
    list.appendChild(li);
  });
}

async function addUrl() {
  const url = document.getElementById("urlInput").value;
  await fetch("/urls", {
    method: "POST",
    headers: {"Content-Type": "application/json"},
    body: JSON.stringify({url})
  });
  document.getElementById("urlInput").value = "";
  loadUrls();
}

async function deleteUrl(id) {
  await fetch("/urls/" + id, { method: "DELETE" });
  loadUrls();
}

loadUrls();
</script>
</body>
</html>
"""
    return Response(html, mimetype="text/html")