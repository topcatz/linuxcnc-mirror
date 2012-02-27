import interpreter 

def retainparam1(self,x):
    self.param1 = x

def checkparam1_retained(self):
    if hasattr(self,'param1'):
        print "param1 was retained, value = ", self.param1
    else:
        return "param1 was not retained across invocations"

    # test object identity
    if hasattr(interpreter,'this'):
	print "this == self:", self == interpreter.this
    else:
        print "module interprerter: no 'this' attribute"
        