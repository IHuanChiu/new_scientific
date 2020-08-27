import ROOT
from array import array

FILE_NAME = 'tree_test.root'
KEY_NAME = "tree"

def createTree(nevent):
    f = ROOT.TFile(FILE_NAME, 'RECREATE' )
    tree = ROOT.TTree(KEY_NAME,"treelibrated tree")
     
    x = array('d',[0])
    #x = 0.
    tree.Branch("x",x,'x/D')
    
    #tree.Print()
    for i in range(nevent):
        #if (iev%1000==0) cout<<"Processing event "<<iev<<"..."<<endl;
        x = [12345678.1234] # a number just for a test
        tree.Fill() 
    
    tree.Print()
    tree.Write()

def readTree():
    rootfile = ROOT.TFile.Open(FILE_NAME,'read')
    tree = ROOT.TTree()
    rootfile.GetObject(KEY_NAME,tree)
    return tree


if __name__ == "__main__":
    #createTree(nevent=1000000)

    tree = readTree()
    
    choice = True
    #choice = False

    print 'choice = ', choice

    if choice:
        alist = []
        for event in tree:
            alist += [event.x]
    
        print len(alist)
    else:
        tree.Draw("x","")
    

