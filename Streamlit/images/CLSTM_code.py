
code = """

class LSTM:

    def __init__(self):

        self.cell_state = 0
        self.short = 0

        # variables for forgetting long-term memory
        self.FG_input_weight = 1
        self.FG_short_weight = 1
        self.FG_bias = 0

        # variables for input gate
        self.IG_input_weight = 1
        self.IG_short_weight = 1
        self.IG_bias = 0
        # forget gate within input gate
        self.IGF_input_weight = 1
        self.IGF_short_weight = 1
        self.IGF_bias = 0

        # variables for forget gate within output gate
        self.OGF_input_weight = 1
        self.OGF_short_weight = 1
        self.OGF_bias = 0


    ## returns forget gate modifier
    def forget_gate(self,input,input_weight=1,short_weight=1,bias=0):
        weighted_input = input*input_weight
        weighted_short = self.short*short_weight
        sum = weighted_short + weighted_input + bias
        result = sigmoid(sum)
        return result

    ## returns value to add to cell state
    def input_gate(self,input):
        weighted_input = input * self.IG_input_weight
        weighted_short = self.short * self.IG_short_weight
        sum = weighted_short + weighted_input + self.IG_bias
        forget_modifier = self.forget_gate(input, self.IGF_input_weight, self.IGF_short_weight, self.IGF_bias)
        result = tanh(sum) * forget_modifier
        return result

    ## returns new hidden state
    def output_gate(self,input):
        forget_modifier = self.forget_gate(input, self.OGF_input_weight, self.OGF_short_weight, self.OGF_bias)
        output = tanh(self.cell_state) * forget_modifier
        return output
    
    def forward(self,input):
        self.cell_state *= self.forget_gate(input, self.FG_input_weight, self.FG_short_weight, self.FG_bias)
        self.cell_state += self.input_gate(input)
        self.short = self.output_gate(input)
        print("Pass Complete:",
            "\n\tInput -> ",input,
            "\n\tNew Short -> ",self.short,
            "\n\tNew Long -> ",self.cell_state)

    # inputs should be normalized 
    def training_step(self,epoch):
        for time_step in epoch:
            self.forward(time_step)
        print("*Sequence Unroll Complete*")
"""