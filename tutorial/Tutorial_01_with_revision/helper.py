# quick hack to display computation graph (you do not need to understand this)
import time
from IPython.display import clear_output, Image, display, HTML, display_javascript, Javascript
#%matplotlib inline
import matplotlib.pyplot as plt
import seaborn as sns
import tensorflow as tf
import numpy as np

def strip_consts(graph_def, max_const_size=32):
    """Strip large constant values from graph_def."""
    strip_def = tf.GraphDef()
    for n0 in graph_def.node:
        n = strip_def.node.add() 
        n.MergeFrom(n0)
        if n.op == 'Const':
            tensor = n.attr['value'].tensor
            size = len(tensor.tensor_content)
            if size > max_const_size:
                tensor.tensor_content = "<stripped %d bytes>"%size
    return strip_def

def show_graph(graph_def, max_const_size=32, sec=8):
    """Visualize TensorFlow graph."""
    if hasattr(graph_def, 'as_graph_def'):
        graph_def = graph_def.as_graph_def()
    strip_def = strip_consts(graph_def, max_const_size=max_const_size)
    code = """
    <script   src="https://code.jquery.com/jquery-3.2.1.min.js"   integrity="sha256-hwg4gsxgFZhOsEEamdOYGBf13FyQuiTwlAQgxVSNgt4="   crossorigin="anonymous"></script>
        <script>
          function load() {{
            document.getElementById("{id}").pbtxt = {data};
        }}
        </script>
        <link rel="import" href="https://tensorboard.appspot.com/tf-graph-basic.build.html" onload=load()>
        <div style="height:600px">
          <tf-graph-basic id="{id}"></tf-graph-basic>
        </div>
    """.format( data=repr(str(strip_def)), id='graph'+str(np.random.rand()))

    iframe = """
        <iframe class="interactive-graph" seamless style="width:100%;height:620px;border:0" srcdoc="{}"></iframe>
    """.format(code.replace('"', '&quot;'))
    display(HTML(iframe))
    #time.sleep(sec)
    #display_javascript(Javascript('$(".interactive-graph").contents().find(".tf-graph-basic").css({"left": 0} );'));
    #display_javascript(Javascript('$(".interactive-graph").contents().find(".side").css({"display":"none"} );'));

def patch():
  from notebook.services.config import ConfigManager
  from IPython.paths import locate_profile
  cm = ConfigManager(profile_dir=locate_profile(get_ipython().profile))
  cm.update('livereveal', {'width': '100%', 'height': 700, 'margin': 0.2,}) 
  from IPython.display import HTML
  HTML('''<style>.CodeMirror{min-width:100% !important;}</style>''')
