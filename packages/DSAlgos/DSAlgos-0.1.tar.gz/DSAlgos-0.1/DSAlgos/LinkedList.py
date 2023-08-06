class Node:
    def __init__(self,data):
        self.data=data
        self.next=None

class SingularLinkedList():
    def __init__(self,data=None):
        if data==None:
            self.root=None
        else:
            self.root=Node(data)

    def insert(self,data):
        if self.root==None:
            self.root=Node(data)
        else:
            temp=self.root
            while temp.next!=None:
                temp=temp.next
            temp.next=Node(data)
    def printlist(self):
        if self.root==None:
            raise IndexError("Linked List in empty")
        else:
            temp=self.root
            while temp!=None:
                print(temp.data)
                temp=temp.next
    def insert_at_begining(self,data):
        if self.root==None:
            self.root=Node(data)
        else:
            temp=self.root
            self.root=Node(data)
            self.root.next=temp
    def size(self):
        if self.root==None:
            return 0
        else:
            c=0
            temp=self.root
            while temp!=None:
                c+=1
                temp=temp.next
            return c
    def search(self,data):
        if self.root==None:
            return -1
        else:
            temp=self.root
            c=0
            while temp!=None:
                if temp.data==data:
                    return c
                c+=1
                temp=temp.next
            return -1
    
    def insert_at_mid_acc_pos(self,data,pos):
        if self.root==None:
            raise IndexError("Linked List is empty")
            
        if pos>=self.size():
            raise IndexError ("Sequence index out of range")
            
        
        else:
            temp=self.root
            c=0
            while temp!=None:
                if pos-1==c:
                    break
                temp=temp.next
                c+=1
            t=temp.next
            temp.next=Node(data)
            temp.next.next=t
    
    def insert_at_mid_acc_data(self,data,data_search):
        if self.root==None:
            raise IndexError("Linked List is Empty")
            
        s=self.search(data_search)
        if s==-1:
            raise KeyError("Data not present in list")
            
        else:
            self.insert_at_mid_acc_pos(data,s)
            return None
    def delete_pos(self,pos):
        if self.root==None:
            raise IndexError("Linked List is empty")
           
        if pos==0:
            self.root=self.root.next
            return None
        if pos>=self.size():
            raise IndexError("Sequence index out of range")
            
        else:
            temp=self.root
            c=0
            while temp!=None:
                if pos-1==c:
                    break
                temp=temp.next
                c+=1
            temp.next=temp.next.next
    def delete_data(self,data):
        if self.root==None:
            raise IndexError("Linked List is empty")
        s=self.search(data)
        if s==-1:
            raise KeyError("Data not present in list")
        else:
            self.delete_pos(s)
            return None

class Noded():
    def __init__(self,data):
        self.data=data
        self.prev=None
        self.next=None
            
class DoublyLinkedList():
    def __init__(self,data=None):
        if data==None:
            self.root=None
        else:
            self.root=Node(data)

    def insert(self,data):
        if self.root==None:
            self.root=Noded(data)
        else:
            temp=self.root
            while temp.next!=None:
                temp=temp.next
            temp.next=Noded(data)
            temp.next.prev=temp
    
    def insert_at_beg(self,data):
        if self.root==None:
            self.root=Noded(data)
        else:
            s=self.root
            self.root=Noded(data)
            self.root.next=s
            self.root.next.prev=self.root
    def size(self):
        if self.root==None:
            return 0
        else:
            c=0
            temp=self.root
            while temp!=None:
                c+=1
                temp=temp.next
            return c
    
    def search(self,data):
        if self.root==None:
            return -1
        else:
            temp=self.root
            c=0
            while temp!=None:
                if temp.data==data:
                    return c
                c+=1
                temp=temp.next
            return -1
        
        
    def printlist(self):
        if self.root==None:
            raise IndexError("Linked List is empty")
        else:
            temp=self.root
            while temp!=None:
                print(temp.data)
                temp=temp.next
    def insert_at_mid_acc_pos(self,data,pos):
        if self.root==None:
            raise IndexError("Linked List is empty")
        if pos>=self.size():
            raise IndexError("Sequence index out of range")
        if pos==self.size()-1:
            return insert(data)
        if pos==0:
            return insert_at_beg(data)
        
        else:
            temp=self.root
            c=0
            while temp!=None:
                if pos==c:
                    break
                temp=temp.next
                c+=1
            t=temp
            temp=Noded(data)
            t.prev.next=temp
            temp.prev=t.prev
            temp.next=t
            t.prev=temp
            return None
    
    def insert_at_mid_acc_data(self,data,data_search):
        if self.root==None:
            raise IndexError("Linked List is empty")
        s=self.search(data_search)
        if s==-1:
            raise KeyError("Data not present in list")
        else:
            self.insert_at_mid_acc_pos(data,s)
            return None

    def delete_pos(self,pos):
        if self.root==None:
            raise IndexError("Linked List is empty")
        if pos==0:
            self.root=self.root.next
            return None
        if pos>=self.size():
            raise IndexError("Sequence index out of range")
        else:
            temp=self.root
            c=0
            while temp!=None:
                if pos-1==c:
                    break
                c+=1
                temp=temp.next
            
            temp.next.prev=None
            temp.next=temp.next.next
            temp.next.prev=temp
    
    def delete_data(self,data):
        if self.root==None:
            raise IndexError("Linked List is empty")
        s=self.search(data)
        if s==-1:
            raise KeyError("Data not present in list")
        else:
            self.delete_pos(s)
            return None
