from flask import Flask

app = Flask(__name__)
app.secret_key = "&30so#7rw$jmb4@x$u_b8uf0)v0t(l%58)+#3xk$4p3@@f=3#m"


from app.routers.router import index