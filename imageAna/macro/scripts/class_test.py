class Animal():
 def __init__(self, name=None):
  print ("init")
  self.name = name
 def change(self):
  namelist = ["a","b","c"]
  for self.name in namelist:
     print (self.name)
  

class NEWC():
  def __init__(self,newname=None):
      print ("new init")
      self.newname = newname
  def getname(self):
      k = Animal()
      k.change()
      print("new",k.name)
#a = Animal(name="dog")
#print("1",a.name)
#a.change()
#print("2",a.name)
#s =  Animal()
#print("3",s.name)
#s.change()
#print("4",s.name)
a = Animal()
a.change()
#s = Animal()
#s.change()
#s.name

class Bank_acount:
      def __init__(self):
          self.a = 100
      def num(self):
          return self.a

class Bank_acount2:
      def __init__(self):
          self.a = 100
      @property
      def num(self):
          return self.a
B=Bank_acount()
B2=Bank_acount2()

print(type(B.num),B.num) #function
print(type(B.num()),B.num()) # return value

B.num = 200
print(type(B.num), B.num) # change B.num to int
print(type(B2.num), B2.num) # property value
#B2.num=200 # <= cann't be attribute
#print(B2.num()) # fail
