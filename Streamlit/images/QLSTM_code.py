
ps_code = """
    def parameter_shift(self,input,target,shift=PARAMETER_SHIFT_ANGLE):

        forward_prediction = None
        backward_prediction = None
        forward_loss = None
        backward_loss = None
        gradient = None

        i = 1
        for circuit in self.circuits:
            print(f"Shifting Parameters on VQC_{i}")
            for i_qub in range(circuit.NQ):
                for i_lay in range(circuit.depth):
                    print(f"...qubit_{i_qub} layer_{i_lay}")
                    for i_dim in range(3):
                        print("Shifting new parameter")
                        #shift forward
                        circuit.shift_param(shift,i_qub,i_lay,i_dim)
                        self.run_cell(input,train=True)
                        forward_prediction = scale_vector(self.output)
                        forward_loss = sum((forward_prediction[i] - target[i])**2 for i in range(DATA_DIMENSIONS))

                        #shift backward
                        circuit.shift_param(-2*shift,i_qub,i_lay,i_dim)
                        self.run_cell(input,train=True)
                        backward_prediction = scale_vector(self.output)
                        backward_loss = sum((backward_prediction[i] - target[i])**2 for i in range(DATA_DIMENSIONS))

                        # update parameter using gradient
                        gradient = (forward_loss-backward_loss)/(2*sin(shift))
                        circuit.update_parameter(gradient,i_qub,i_lay,i_dim,shift)
        return
"""


circuit_code = """
from qiskit import QuantumCircuit
from qiskit.quantum_info import Statevector, Pauli
from globals import *


class VQC:

    def __init__(self, parameters, N_qubits=DATA_DIMENSIONS*2, depth = VARIATIONAL_DEPTH):
          
        self.NQ = N_qubits
        self.depth = depth 

        # this stores a list of 3 dimensions of rotation gradients...
        # ...inside a list of layers
        # ...inside a list of qubits
        # so the total number of parameters for a circuit is 3*depth*N_qubits
        self.gradient_parameters = parameters

        self.qc = QuantumCircuit(N_qubits) 

        self.measurement = None

        return
        
    # takes vector and encodes it into angles (Bloch Vectors)
    def encode_vector(self,data_vec):

        # Check for size inconsistency
        if len(data_vec) != self.NQ:
            print("Vector size does not match Number of Qubits")
            print("nV -> ",len(data_vec)," | nQ -> ",self.NQ)
            return

        for i in range(self.NQ):
  
            # superpose qubit
            self.qc.h(i)                    

            # Calculate rotation angles
            theta_y = np.arctan(data_vec[i]) 
            theta_z = np.arctan(data_vec[i] ** 2) # x^2 creates "higher-order terms" after entanglement

            # Rotate around y and z axis
            self.qc.ry(theta_y,i)
            self.qc.rz(theta_z,i)

        return

    def variational_layer(self):

        for l in range(self.depth):

            # cycle through qubits to apply cnots
                # All qubits with a fixed adjacency 1 and 2 get entangled
            for a in range(1,3):
                x = 0
                y = a
                while x < self.qc.num_qubits:
                    self.qc.cx(x,y)
                    x += 1
                    y =  (y+1) % self.qc.num_qubits

            # Apply Gradients
            for i in range(self.NQ):
                self.qc.rx(self.gradient_parameters[i][l][0],i)
                self.qc.ry(self.gradient_parameters[i][l][1],i)
                self.qc.rz(self.gradient_parameters[i][l][2],i)
            
        #print(self.qc)
        return

    def run(self, data_array):

        print("Running a circuit")
        
        # reset qubits
        self.qc.reset(range(self.NQ))

        # run layers of circuit
        self.encode_vector(data_array)
        self.variational_layer()
        
        # Measures qubits
        state = Statevector.from_instruction(self.qc)
        self.measurement = []
        for i in range(self.NQ):
            op = Pauli(f'{"I"*(self.NQ-1-i)}Z{"I"*(i)}')
            expval = state.expectation_value(op)
            self.measurement.append(expval.real)
            #print(f"⟨Z⟩ on qubit {i}: {expval.real}")
        return
        
    # only returns second half of qubits measurments to get output vectors when truncate==True
    def get_result(self, truncate=True):
        if self.measurement == None:
            print("Circuit must be run first")
            return
        return (self.measurement[DATA_DIMENSIONS:] if truncate==True else self.measurement)
    
    def shift_param(self,shift,qubit,layer,dimension):
        self.gradient_parameters[qubit][layer][dimension] += shift
        return

    # updates single parameter with gradient
    def update_parameter(self,gradient,qubit,layer,dimension,shift = 0):
        self.gradient_parameters[qubit][layer][dimension] += shift - (LEARNING_RATE*gradient)
        return


    # returns array of parameter states in following format:
        # (e.g. q1l1 = depth layer 1 of qubit 1)
        # Circuit Parameters = 
        # [
        #   [
        #      [ q0l0.alpha, q0l0.beta, g0l0.gamma]
        #      [ q0l1.alpha, q0l1.beta, g0l1.gamma]
        #   ],
        #   [
        #      [ q1l0.alpha, q1l0.beta, g1l0.gamma]
        #      [ q1l1.alpha, q1l1.beta, g1l1.gamma]
        #   ]
        #   etc.
        # ]
    def get_parameters(self):
        return self.gradient_parameters
"""

lstm_code = """
from circuit import VQC
from globals import *

class QLSTM_Cell:

    def __init__(self,state):

        self.cell_state = state["Cell_State"]
        self.hidden_state = state["Hidden_State"]

        self.output = None 
        self.gate_input = None

        # Initialize Qunatum Circuits
        self.circuits = [
            VQC(state["Parameters"]["VQC_1"]),                    # VQC_1 forget gate
            VQC(state["Parameters"]["VQC_2"]),                    # VQC_2 input gate forget
            VQC(state["Parameters"]["VQC_3"]),                    # VQC_3 input gate
            VQC(state["Parameters"]["VQC_4"]),                    # VQC_4 output gate forget
            VQC(state["Parameters"]["VQC_5"], DATA_DIMENSIONS),  # VQC_5 outputs the next hidden state
            VQC(state["Parameters"]["VQC_6"], DATA_DIMENSIONS)   # VQC_6 outputs the prediction
        ]


    # Returns forget modifier
        # Defaults to VQC_1 for cell_state modifier, argue for input and output forget circuits
    def forget_gate(self,circuit=None):
        if circuit == None: circuit = self.circuits[0]
        circuit.run(self.gate_input)
        result = circuit.get_result()
        return sigmoid(result)

    # Returns value to be added to cellstate
    def input_gate(self):

        self.circuits[2].run(self.gate_input)
        result = tanh(self.circuits[2].get_result())

        # apply forget
        f_mod = self.forget_gate(circuit = self.circuits[1])
        for i in range(len(result)):
            result[i] *= f_mod[i]

        return result
    
    # returns a tuple (output/prediction, new hiddenstate)
    def output_gate(self):

        result = tanh(self.cell_state)
        f_mod = self.forget_gate(circuit = self.circuits[3])
        for i in range(DATA_DIMENSIONS):
            result[i] *= f_mod[i]

        self.circuits[4].run(result)
        hs = self.circuits[4].get_result(False)

        self.circuits[5].run(result)
        output = self.circuits[5].get_result(False)

        return (output, hs)
    
    # input should be normalized to [0,1]
    def run_cell(self, input, train=False):

        #save previous states locally
        prev_cs = self.cell_state
        prev_hs = self.hidden_state

        # Concentenate hidden state and input
        self.gate_input = self.hidden_state+input

        # Forget and Input blocks to cell_state
        cs_fmod = self.forget_gate()
        cs_add = self.input_gate()
        for i in range(DATA_DIMENSIONS):
            self.cell_state[i] *= cs_fmod[i]
            self.cell_state[i] += cs_add[i]

        # Output Block
        self.output, self.hidden_state = self.output_gate()

        # reset cell and hidden states while parameter shifting
        if train:
            self.cell_state = prev_cs
            self.hidden_state = prev_hs
    
        return
    
    #input and target should be normalized to [0,1]
    def parameter_shift(self,input,target,shift=PARAMETER_SHIFT_ANGLE):

        forward_prediction = None
        backward_prediction = None
        forward_loss = None
        backward_loss = None
        gradient = None

        i = 1
        for circuit in self.circuits:
            print(f"Shifting Parameters on VQC_{i}")
            for i_qub in range(circuit.NQ):
                for i_lay in range(circuit.depth):
                    print(f"...qubit_{i_qub} layer_{i_lay}")
                    for i_dim in range(3):
                        print("Shifting new parameter")
                        #shift forward
                        circuit.shift_param(shift,i_qub,i_lay,i_dim)
                        self.run_cell(input,train=True)
                        forward_prediction = scale_vector(self.output)
                        forward_loss = sum((forward_prediction[i] - target[i])**2 for i in range(DATA_DIMENSIONS))

                        #shift backward
                        circuit.shift_param(-2*shift,i_qub,i_lay,i_dim)
                        self.run_cell(input,train=True)
                        backward_prediction = scale_vector(self.output)
                        backward_loss = sum((backward_prediction[i] - target[i])**2 for i in range(DATA_DIMENSIONS))

                        # update parameter using gradient
                        gradient = (forward_loss-backward_loss)/(2*sin(shift))
                        circuit.update_parameter(gradient,i_qub,i_lay,i_dim,shift)
        return
    
    # trains model with list of time series inputs
        # inputs should be normalized to [0,1]
    def train_epoch(self, inputs):

        loss = None
        losses = []

        i = 0
        while i < len(inputs)-1:

            print(f"Training step {i+1} of {len(inputs)}")

            # optimize
            self.parameter_shift(inputs[i],inputs[i+1])

            #step forward in time series
            self.run_cell(inputs[i])
            i+=1

            #calculate loss at each step
            prediction = scale_vector(self.output)
            loss = sum((prediction[d]-inputs[i][d])**2 for d in range(DATA_DIMENSIONS))
            losses.append(loss)

            
        return losses

    # returns dictionary to save state of cell
    def get_state(self):
        params = {}
        for i in range(len(self.circuits)):
            params[f"VQC_{i+1}"] = self.circuits[i].get_parameters()
            
        dic = {
            "Cell_State":self.cell_state,
            "Hidden_State":self.hidden_state,
            "Output": self.output,
            "Parameters":params
        }
        return dic
"""