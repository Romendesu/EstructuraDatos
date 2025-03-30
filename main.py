import time  # Import the time library to measure execution 

class Stack:
    def __init__(self,maxSize):
        self.__maxSize = maxSize
        self.__stack = [None]*maxSize
        self.__nItems = 0
        self.__ptr = -1
    
    def isEmpty(self):
        return self.__nItems == 0
    
    def isFull(self):
        return self.__nItems == self.__maxSize
    
    def __len__(self):
        return self.__nItems
    
    def push(self, element):
        if (self.isFull()):
            raise Exception("Stack overflow")
        self.__ptr += 1
        self.__stack[self.__ptr] = element
        self.__nItems += 1
        return f"Element: {element} push"
    
    def pop(self):
        if (self.isEmpty()): 
            raise Exception("Stack underflow")
        elementPopped = self.__stack[self.__ptr]
        self.__stack[self.__ptr] = None
        self.__ptr -= 1
        self.__nItems -= 1
        return elementPopped
    
    def peek(self):
        return self.__stack[self.__ptr]
    
    def __str__(self):
        stackForm = "{"
        for element in range(self.__nItems):
            stackForm += f"{self.__stack[element]}"
            if element != self.__nItems - 1:  
                stackForm += ", "
        stackForm += "}"
        return stackForm

def identity(x): return x

class Queue(object):
    def __init__(self, size):  # Constructor
        self.__maxSize = size  # Size of [circular] array
        self.__que = [None] * size  # Queue stored as a list
        self.__front = 1  # Empty Queue has front 1
        self.__rear = 0  # After rear and
        self.__nItems = 0  # No items in queue

    def insert(self, item):  # Insert item at rear of queue
        if self.isFull():  # If not full
            raise Exception("Queue overflow")
        self.__rear += 1  # Rear moves one to the right
        if self.__rear == self.__maxSize:  # Wrap around circular array
            self.__rear = 0
        self.__que[self.__rear] = item  # Store item at rear
        self.__nItems += 1
        return True

    def remove(self):  # Remove front item of queue
        if self.isEmpty():  # And return it, if not empty
            raise Exception("Queue underflow")
        front = self.__que[self.__front]  # Get the value at front
        self.__que[self.__front] = None  # Remove item reference
        self.__front += 1  # Front moves one to the right
        if self.__front == self.__maxSize:  # Wrap around circular array
            self.__front = 0
        self.__nItems -= 1
        return front

    def peek(self):  # Return frontmost item
        return None if self.isEmpty() else self.__que[self.__front]

    def isEmpty(self):
        return self.__nItems == 0

    def isFull(self):
        return self.__nItems == self.__maxSize

    def __len__(self):
        return self.__nItems

    def __str__(self):  # Convert queue to string
        ans = "["  # Start with left bracket
        for i in range(self.__nItems):  # Loop through current items
            if len(ans) > 1:  # Except next to left bracket,
                ans += ", "  # Separate items with comma
            j = i + self.__front  # Offset from front
            if j >= self.__maxSize:  # Wrap around circular array
                j -= self.__maxSize
            ans += str(self.__que[j])  # Add string form of item
        ans += "]"  # Close with right bracket
        return ans

# Functions to use
import re  # Import the regular expression library

def isValid(expression):
    # Remove spaces from the expression
    expression = expression.replace(" ", "")
    
    # Check if the expression is empty
    if not expression:
        return False
    
    # Check if parentheses are balanced (number of '(' and ')')
    if expression.count('(') != expression.count(')'):
        return False
    
    # Regular expression to check if the syntax is valid (numbers, operators, parentheses)
    pattern = r"^[0-9()+\-*/.]+$"
    if not re.match(pattern, expression):
        return False
    
    # Check that operators are in correct places (no consecutive operators, etc.)
    # This regular expression ensures no consecutive operators or operators at the start or end
    errorPattern = r"(^[+\-*/])|([+\-*/]{2,})|([+\-*/]$)"
    if re.search(errorPattern, expression):
        return False
    
    # If we reach here, the expression seems valid
    return True

def precedence(operator, operators=["|", "&", "+-", "*/%", "^", "()"]):
    # Iterate through the operators to return the precedence value of the given operator
    for p, ops in enumerate(operators):
        if operator in ops:
            return p + 1  # Return the precedence of the operator, starting from 1

def isDelimiter(char, operators=["|", "&", "+-", "*/%", "^", "()"]):
    # Return True if the character is a delimiter, based on its precedence
    return precedence(char) == len(operators)

def nextToken(s):  # Parse the next token from the input string
    token = ""  # The token can be an operator or an operand
    s = s.strip()  # Remove leading and trailing spaces from the string
    if len(s) > 0:  # If we haven't reached the end of the string
        if precedence(s[0]):  # Check if the first character is an operator
            token = s[0]  # The token is a single-character operator
            s = s[1:]  # Remove the operator from the string
        else:  # If it's an operand, take the characters up to the next operator or space
            while len(s) > 0 and not (
                precedence(s[0]) or s[0].isspace()
            ):
                token += s[0]
                s = s[1:]
    return token, s  # Return the token and the remaining string

def postfixTranslate(formula):  # Translate an infix formula to postfix
    if not isValid(formula): raise Exception("The expression is not valid.")  # Check if the formula is valid
    postfix = Queue(100)  # Store the postfix expression temporarily in a queue
    stack = Stack(100)  # Use a stack for operators while parsing the formula
    result = []  # Store the steps for visualization
    
    token, formula = nextToken(formula)  # Get the first token of the formula
    while token:  # While there are tokens to process
        tokenPrecedence = precedence(token)  # Get the precedence of the token
        isDelimiterToken = isDelimiter(token)  # Check if the token is a delimiter
        
        if isDelimiterToken:  # If the token is a delimiter (like parentheses)
            if token == '(':  # If it's an opening parenthesis
                stack.push(token)  # Push the opening parenthesis onto the stack
            else:  # If it's a closing parenthesis
                while not stack.isEmpty():  # Pop elements from the stack
                    top = stack.pop()
                    if top == '(':  # Until an opening parenthesis is found
                        break
                    else:  # Put the rest in the output queue (postfix notation)
                        postfix.insert(top)
        
        elif tokenPrecedence:  # If the token is an operator
            while not stack.isEmpty():  # Check the operator on top of the stack
                top = stack.pop()
                if top == '(' or precedence(top) < tokenPrecedence:  # If it's an opening parenthesis or a lower precedence operator
                    stack.push(top)  # Push it back onto the stack
                    break  # Stop the loop
                else:  # If the operator on top has higher precedence, move it to the queue
                    postfix.insert(top)
            stack.push(token)  # Push the current operator onto the stack
        
        else:  # If the token is an operand (a number)
            postfix.insert(token)  # Directly add it to the queue
        
        # Show the state after each iteration
        result.append(f"Token: {token}, Precedence: {tokenPrecedence if tokenPrecedence else 'N/A'}, Type: {'Operator' if tokenPrecedence else 'Operand'}")
        result.append(f"Stack: {stack}")
        result.append(f"Queue: {postfix}\n")
        
        token, formula = nextToken(formula)  # Get the next token
    
    while not stack.isEmpty():  # At the end of the input, empty the stack
        postfix.insert(stack.pop())  # Put the remaining operators in the queue
    
    ans = ""
    while not postfix.isEmpty():  # Convert the queue to a string
        if len(ans) > 0:
            ans += " "  # Separate tokens with spaces
        ans += postfix.remove()
    
    result.append(f"The postfix representation of {formula} is {ans}")
    return result

def postfixEvaluate(formula):  # Translate infix to postfix and evaluate the result
    postfixSteps = postfixTranslate(formula)  # Get the steps of the conversion
    postfixExpression = postfixSteps[-1].split()  # The final postfix expression (last item in the list)
    
    # Filter only valid numbers and operators
    validTokens = [token for token in postfixExpression if token.isdigit() or token in "|&+-*/%^"]
    
    operandStack = Stack(100)  # Stack to store operands
    for token in validTokens:
        tokenPrecedence = precedence(token)  # Check if the token is an operator
        
        if tokenPrecedence:  # If the token is an operator
            right = operandStack.pop()  # Get the right operand
            left = operandStack.pop()  # Get the left operand
            
            # Perform the corresponding operations
            if token == '|':  # OR operation
                operandStack.push(left | right)
            elif token == '&':  # AND operation
                operandStack.push(left & right)
            elif token == '+':  # Addition
                operandStack.push(left + right)
            elif token == '-':  # Subtraction
                operandStack.push(left - right)
            elif token == '*':  # Multiplication
                operandStack.push(left * right)
            elif token == '/':  # Division
                operandStack.push(left / right)
            elif token == '%':  # Modulus
                operandStack.push(left % right)
            elif token == '^':  # Power
                operandStack.push(left ^ right)
        else:  # If the token is an operand (number)
            operandStack.push(int(token))  # Convert the token to an integer and push it
        
        # Show the state after processing each token
        print(f"After processing {token}, the stack holds: {operandStack}")
    
    print(f"Final result = {operandStack.pop()}")  # At the end of the input, print the result

if __name__ == "__main__":
    infixExpression = input("Enter the arithmetic expression: ")  # Ask the user for input
    startTime = time.time()  # Save the start time
    postfixSteps = postfixTranslate(infixExpression)  # Convert the infix expression to postfix
    print("\n".join(postfixSteps))  # Show the step-by-step process only once
    postfixEvaluate(infixExpression)  # Evaluate the postfix expression
    endTime = time.time()  # Save the end time
    totalTime = endTime - startTime  # Calculate the total execution time
    print(f"Execution time: {totalTime}")  # Show the total execution time
