from flask import Flask ,redirect, jsonify, flash,url_for,render_template ,request
from lxml import etree
from io import StringIO
import webbrowser
import os

app = Flask(__name__)

#fonction separate pour la validation par dtd intern
#consiste a parcourir le fichier qui contient le code xml et la dtd et d'extraire la dtd de xml

def separete(mon_fichier) :
    import lxml
    with open(mon_fichier, 'r') as file:
        info = file.read().rstrip('\n')
    file.close()
    x = info.find("<!DOCTYPE")
    y = info.find("]>")
    dtd = info[x:y+2]
    xml = info.replace(dtd, '')
    x = dtd.find("[")
    y = dtd.find("]")
    dtd = dtd[x+1:y]
    with open('dossier_dtd/dtd.dtd', 'w') as fi:
        fi.write(dtd)
    fi.close()
    with open('dossier_dtd/xml.xml', 'w') as fo:
        fo.write(xml)
    fo.close()
    try :
        xml_file = lxml.etree.parse("dossier_dtd/xml.xml")
        xml_validator = lxml.etree.DTD(file="dossier_dtd/dtd.dtd")
        is_valid = xml_validator.validate(xml_file)
    except:
        return False
    return(is_valid)


@app.route("/")
def index():
    return render_template('index.html')

@app.route("/dtd")
def dtd():
    return render_template("dtd.html")

@app.route("/xs")
def xs():
    return render_template("xs.html")

#dtd editeur pour la validation par dtd extern
@app.route('/indtd', methods=['POST','GET'])
def indtd():
    dtdd = request.form['dtdex']
    f = open("xml.xml", "w")
    f.write(request.form['xmlex'])
    f.close()
    try:
        dtd = etree.DTD(StringIO(dtdd))
        tree = etree.parse("xml.xml")
        if(dtd.validate(tree)) : 
            return jsonify(result = True)
        else:
            return jsonify(result = False)
    except:
        return jsonify(result = False)

#editeur pour validation par dtd intern
@app.route('/intdtd', methods=['POST','GET'])
def intdtd():
    dtdd = request.form['dtdin']
    print(dtdd)
    f = open("xml.xml", "w")
    f.write(dtdd)
    f.close()
    v=separete("xml.xml")
    print(v)
    if(v):
        return jsonify(result = True)
    else:
        return jsonify(result = False)

#fichierspour la validation par dtd extern
@app.route('/indtdfile', methods=['POST','GET'])
def indtdfile():
    f1 = request.files['file1']
    f2 = request.files['file2']
    f1.save(f1.filename)
    f2.save(f2.filename)
    dtd = etree.DTD(f1.filename)
    tree = etree.parse(f2.filename)
    os.remove(f1.filename)
    os.remove(f2.filename)
    if(dtd.validate(tree)) : 
        return jsonify(result = True)
    else :
        return jsonify(result = False)

#fichier pour la validation par dtd intern    
@app.route('/interndtd', methods=['POST','GET'])
def interndtd():
    f3 = request.files['file3']
    f3.save(f3.filename)
    v=separete(f3.filename)
    os.remove(f3.filename)
    if(v):
        return jsonify(result = True)
    else:
        return jsonify(result = False)

# editeur pour la validation par xmlschema
@app.route('/xst', methods=['POST','GET'])
def xst():
    f = open("xml.xml", "w")
    f.write(request.form['xmlt'])
    f.close()
    f = open("xml.xsd", "w")
    f.write(request.form['xst'])
    f.close()
    try:
        xsc = etree.XMLSchema(file="xml.xsd")
        tree = etree.parse("xml.xml")
        if(xsc.validate(tree)) :
            return jsonify(result = True)
        else:
            return jsonify(result = False)
    except:
        return jsonify(result = False)

@app.route('/xsf', methods=['POST','GET'])
def xsf():
    
    f1 = request.files['xsf']
    f2 = request.files['xmlf']
    f1.save(f1.filename)
    f2.save(f2.filename)
    xsc = etree.XMLSchema(file=f1.filename)
    tree = etree.parse(f2.filename)
    os.remove(f1.filename)
    os.remove(f2.filename)
    if(xsc.validate(tree)) : 
        return jsonify(result = True)
    else :
        return jsonify(result = False)
    

if __name__ == '__main__':
    app.run(debug=True)
    