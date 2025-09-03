import os
try:
    from flask import Flask, render_template, request, redirect, url_for
    import pandas as pd
except:
    os.system('pip install Flask')
    os.system('pip install pandas')
    import pandas as pd
    from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

tasks = []
HISTORY_FILE = "history.csv"

if not os.path.exists(HISTORY_FILE) or os.stat(HISTORY_FILE).st_size == 0:
    pd.DataFrame(columns=["Task"]).to_csv(HISTORY_FILE, index=False)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/todo", methods=['GET', 'POST'])
def todo():
    edit_id = request.args.get("edit_id", default=None, type=int)

    if request.method == 'POST':
        task_text = request.form.get('task')
        if task_text:
            tasks.append({"text": task_text, "completed": False})

        return redirect(url_for("todo"))

    return render_template("todo.html", tasks=tasks, edit_id=edit_id)

@app.route("/todo/delete/<int:task_id>", methods=['POST'])
def delete_task(task_id):
    if 0 <= task_id < len(tasks):
        tasks.pop(task_id)
    return redirect(url_for("todo"))

@app.route("/todo/complete/<int:task_id>", methods=['POST'])
def complete_task(task_id):
    if 0 <= task_id < len(tasks):
        tasks[task_id]["completed"] = True
        task_text = tasks[task_id]["text"]
        new_entry = pd.DataFrame([[task_text]], columns=["Task"])
        new_entry.to_csv(HISTORY_FILE, mode="a", header=False, index=False)
    return redirect(url_for("todo"))

@app.route("/todo/edit/<int:task_id>", methods=['POST'])
def edit_task(task_id):
    if 0 <= task_id < len(tasks):
        new_text = request.form.get('task')
        if new_text:
            tasks[task_id]["text"] = new_text
    return redirect(url_for("todo"))

@app.route("/history")
def history():
    try:
        df = pd.read_csv(HISTORY_FILE)
    except pd.errors.EmptyDataError:
        df = pd.DataFrame(columns=["Task"])
    completed_tasks = df["Task"].tolist()
    return render_template("history.html", tasks=completed_tasks)

port = int(os.environ.get("PORT", 8000))

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=port)#This is for deployment.
    '''app.debug = True
    app.run()''' #This is for local host.
