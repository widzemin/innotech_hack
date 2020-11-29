from flask import request, redirect, render_template
from werkzeug.utils import secure_filename
from flask import Flask
 

app = Flask(__name__)

import os

app.config["IMAGE_UPLOADS"] = "images_uploaded"
app.config["ALLOWED_IMAGE_EXTENSIONS"] = ["JPEG", "JPG", "PNG", "GIF"]
app.config["MAX_IMAGE_FILESIZE"] = 1024 * 1024 * 1024


def allowed_image(filename):
    if not "." in filename:
        return False

    ext = filename.rsplit(".", 1)[1]

    if ext.upper() in app.config["ALLOWED_IMAGE_EXTENSIONS"]:
        return True
    else:
        return False


def allowed_image_filesize(filesize):
    if int(filesize) <= app.config["MAX_IMAGE_FILESIZE"]:
        return True
    else:
        return False


@app.route("/upload-image", methods=["GET", "POST"])
def upload_image():
    if request.method == "POST":
        f = open('links', 'w')
        
        if request.files:
            f.write(request.form['name'])
            from parser_from_vk import is_close, get_info
            import pandas as pd
            with open('links', 'r') as f:
                tmp = f.readlines()
                links = []
                for e in tmp:
                    links += e.split()
                for i in range(len(links)):
                    links[i] = links[i].split('/')[-1]
                df = pd.DataFrame(columns=['id', 'photo'])
                for new_id in links:
                    new_photo = get_info(new_id)['photo_max']
                    df = df.append({'id' : ' '.join(new_id.split()), 'photo' : ' '.join(new_photo.split())}, ignore_index=True)
                df.to_csv('Profiles.csv')
            import sys
            sys.path.append('../')
            import final
            image = request.files["image"]
            if image.filename == "":
                print("No filename")
                return redirect(request.url)
        
            if allowed_image(image.filename):
                filename = secure_filename(image.filename)
                
                image.save(os.path.join(app.config["IMAGE_UPLOADS"], 'img_temp.jpg'))
                
                print("Image saved")
                name1 = final.first_name
                second_name1 = final.second_name
                prof1 = final.profession
                city1 = final.city
                salary1 = final.salary
                id1 = final.ans
                mapa1 = str(final.MAPA)
                return render_template("upload_image.html", id=id1, name=name1, second_name=second_name1,
                                       prof=prof1, city=city1, salary=salary1, mapa=mapa1)
                #return redirect(request.url)
            
            else:
                print("That file extension is not allowed")
                return redirect(request.url)

    return render_template("upload_image.html")


if __name__ == "__main__":
    app.run(debug=True, port=1337)

