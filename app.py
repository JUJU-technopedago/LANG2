from flask import Flask, render_template, request
import process_svg

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        # Collect the proficiency levels from the form
        levels = {
            "skill_1": request.form["skill_1"],
            "skill_2": request.form["skill_2"],
            "skill_3": request.form["skill_3"],
            "skill_4": request.form["skill_4"],
            "skill_5": request.form["skill_5"],
            "skill_6": request.form["skill_6"],
        }
        # Generate the updated SVG
        output_svg = process_svg.update_svg(levels)
        return render_template("result.html", svg_path=output_svg)
    
    return render_template("index.html")

if __name__ == "__main__":
    app.run(debug=True)
