class Animal():
 def __init__(self, name=None):
  print ("init")
  self.name = name
 def change(self):
  self.name = "changed"

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
n = NEWC()
n.getname()
#s = Animal()
#s.change()
#s.name


