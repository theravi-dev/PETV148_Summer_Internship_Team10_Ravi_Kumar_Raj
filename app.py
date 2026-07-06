from flask import Flask, render_template, request, Response
import requests
import time

app = Flask(__name__)
last_results = []
websites = {
    "🐙 GitHub": "https://github.com/{}",
    "📸 Instagram": "https://www.instagram.com/{}/",
    "👽 Reddit": "https://www.reddit.com/user/{}",
    "📌 Pinterest": "https://www.pinterest.com/{}/",
    "🎵 TikTok": "https://www.tiktok.com/@{}",
    "💼 LinkedIn": "https://www.linkedin.com/in/{}",
    "📘 Facebook": "https://www.facebook.com/{}",
    "▶️ YouTube": "https://www.youtube.com/@{}",
    "❌ X (Twitter)": "https://x.com/{}",
    "💻 Stack Overflow": "https://stackoverflow.com/users/{}",
    "🐙 GitLab": "https://gitlab.com/{}",
    "🎮 Steam": "https://steamcommunity.com/id/{}",
    "💬 Discord": "https://discord.com/users/{}",
    "🎵 SoundCloud": "https://soundcloud.com/{}",
    "📝 Medium": "https://medium.com/@{}"
}
   
@app.route('/')
def home():
    return render_template('index.html')

@app.route('/search', methods=['POST'])
def search():

    username = request.form['username']
    start = time.time()

    found = 0
    not_found = 0
    error = 0

    results = []

    for site, url in websites.items():

        profile = url.format(username)

        try:
            response = requests.get(profile, timeout=5)

            if response.status_code == 200:
                status = "Found"
                found += 1
            else:
                status = "Not Found"
                not_found += 1

        except:
            status = "Error"
            error += 1

        results.append({
            "site": site,
            "status": status,
            "url": profile
        })
    search_time = round(time.time() - start, 2)
    global last_results
    last_results = results

    return render_template(
        
        "result.html",
        username=username,
        results=results,
        found=found,
        not_found=not_found,
        error=error,
       total=len(websites),
       search_time=search_time
    )
@app.route("/download")
def download():

    import csv
    from io import StringIO

    output = StringIO()

    writer = csv.writer(output)

    writer.writerow(["Website", "Status", "Profile"])

    for result in last_results:
       writer.writerow([
    result["site"],
    result["status"],
    result["url"]
])

    return Response(
        output.getvalue(),
        mimetype="text/csv",
        headers={
            "Content-Disposition":
            "attachment; filename=search_results.csv"
        }
    )
if __name__ == "__main__":
    app.run(debug=True)