from flask import Flask, url_for, render_template, jsonify, send_from_directory
import os, json, io, yaml, pathlib
from kubernetes import client, config, utils


### K8s setup
# Configs can be set in Configuration class directly or using helper utility
config.load_kube_config(r"/etc/rancher/k3s/k3s.yaml")
v1 = client.CoreV1Api()
k8s_client = client.ApiClient()
NAMESPACE = os.getenv("KUBERNETES_OWN_NAMESPACE", "default")

### Flask setup
app = Flask(__name__)


### Flask basic routes
@app.route('/')
def index():
    return app.send_static_file('public/index.html')

@app.route('/build/<path:path>')
def send_build(path):
    return send_from_directory('static/public/build', path)

@app.route('/layouts/<path:path>')
def send_layouts(path):
    return send_from_directory('static/public/layouts', path)

@app.route('/pages/<path:path>')
def send_pages(path):
    return send_from_directory('static/public/pages', path)


#### Flask IAS routes
@app.route('/api/pods')
def pods():
    ret = v1.list_namespaced_pod(NAMESPACE)
    return jsonify({
        "pod_names":[
            "{}".format(str(x.metadata.name)) for x in ret.items
            ],
        "namespace": NAMESPACE
        })

@app.route('/api/deploy/<string:name>')
def deploy(name):
    inst = render_template('deploy.template', name=name)
    with open('deploy.yaml', 'w') as f:
        f.write(inst)

    ret = utils.create_from_yaml(k8s_client, './deploy.yaml', namespace=NAMESPACE)

    return jsonify({
        # "status": ret.metadata,
        "namespace": NAMESPACE
        })
    


if __name__ == '__main__':
    app.run(debug=os.getenv("DEBUG_MODE", True), host='0.0.0.0')