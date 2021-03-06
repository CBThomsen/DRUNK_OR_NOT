from keras.models import Sequential
from keras.models import model_from_json
from keras import backend as K
import tensorflow as tf
from tensorflow.python.tools import freeze_graph
import os

# Load existing model.
with open("model.json",'r') as f:
    modelJSON = f.read()

model = model_from_json(modelJSON)
model.load_weights("model.h5")

# All new operations will be in test mode from now on.
K.set_learning_phase(0)

# Serialize the model and get its weights, for quick re-building.
config = model.get_config()
weights = model.get_weights()

# Re-build a model where the learning phase is now hard-coded to 0.
new_model = Sequential.from_config(config)
new_model.set_weights(weights)

temp_dir = "graph"
checkpoint_prefix = os.path.join(temp_dir, "saved_checkpoint")
checkpoint_state_name = "checkpoint_state"
input_graph_name = "input_graph.pb"
output_graph_name = "output_graph.pb"

# Temporary save graph to disk without weights included.
saver = tf.train.Saver()
checkpoint_path = saver.save(K.get_session(), checkpoint_prefix, global_step=0, latest_filename=checkpoint_state_name)
tf.train.write_graph(K.get_session().graph, temp_dir, input_graph_name)

input_graph_path = os.path.join(temp_dir, input_graph_name)
input_saver_def_path = ""
input_binary = False
output_node_names = "dense_1/Softmax" # model dependent
restore_op_name = "save/restore_all"
filename_tensor_name = "save/Const:0"
output_graph_path = os.path.join(temp_dir, output_graph_name)
clear_devices = False

# Embed weights inside the graph and save to disk.
freeze_graph.freeze_graph(input_graph_path, input_saver_def_path,
                          input_binary, checkpoint_path,
                          output_node_names, restore_op_name,
                          filename_tensor_name, output_graph_path,
                          clear_devices, "")