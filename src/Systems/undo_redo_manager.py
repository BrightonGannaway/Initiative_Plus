import copy

class Undo_Redo_Manager:
    def __init__(self):
        self.undo_Stack = []
        self.redo_Stack = []
        self.HISTORY_LIMIT = 10 #Max history depth = 10
        self.limit = lambda h: h.pop(0) if len(h) > self.HISTORY_LIMIT else None

    def save_state(self, current_state):
        """Save the current state to the undo stack and clear redo."""
        self.undo_Stack.append(copy.deepcopy(current_state))
        self.limit(self.undo_Stack)
        self.redo_Stack.clear()
        
        if (len(self.undo_Stack) > self.HISTORY_LIMIT): 
            self.undo_Stack.pop(0)

    def undo(self, current_state):
        if self.undo_Stack:
            self.redo_Stack.append(copy.deepcopy(current_state))
            self.limit(self.undo_Stack)
            return self.undo_Stack.pop()
        return current_state
    
    def redo(self, current_state):
        if self.redo_Stack:
            self.undo_Stack.append(copy.deepcopy(current_state))
            new_state = self.redo_Stack.pop()
            return new_state
        return current_state
    
    def get_history(self):
        return {"Undo History": self.undo_Stack, "Redo History": self.redo_Stack}
    
    def set_history(self, undo_history, redo_history):
        self.undo_Stack = undo_history
        self.redo_Stack = redo_history

    def get_history_length(self):
        return ("Undo Length: ", len(self.undo_Stack))
    
    