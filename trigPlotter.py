xfile = 'Data/Oct20_50.txt'
yfile = 'Data/Oct20_51.txt'

from pylab import *
from numpy import *
#python has matrices y,x


def mirror(y):
  return list(flip(y[0:32]))+list(flip(y[32:64]))+list(flip(y[64:96]))+list(flip(y[96:128]))+list(flip(y[128:160]))+list(flip(y[160:192]))



def load_data(file):
  data = open(file, "r") #loads file
  data=data.read()       #reads file
  data=data.split("\n")[0:-2] #turn one giant string into a list of line strings. The last line is "" and drops it.
  return data

def process_data(data): #turns data from a string of "s 8ns fibre" to (time,fiber)
  processed_data=[]
  line_count=0
  for line in data:
    try: 
      s=int(line.split(" ")[1])    
      ns=int(line.split(" ")[0])
      time= ns*8*1e-9 + s
      fibers=line.split(" ")[2]
      processed_data.append([time,fibers]) 
      line_count+=1
    except: pass #blank lines in data that would otherwise crash program
  return processed_data

def veto_ambiguous_events(data):
  processed_data=[]
  for line in data:
    fibers=line[1]
    if fibers.count("1") == 1:
      # if fibers[fibers.find("1")+1] == "1":
        processed_data.append(line)
  return processed_data



datax = load_data(xfile)
datax = process_data(datax)
print("actual event entries in x     ",len(datax))
datax = veto_ambiguous_events(datax)
print("unambiguous event entries in x",len(datax))

datay = load_data(yfile)
datay = process_data(datay)
print("actual event entries in y     ",len(datay))
datay = veto_ambiguous_events(datay)
print("unambiguous event entries in y",len(datay))
#print(datax)



def pair_up(datax,datay):
  dt=1e-7 #maximum time difference between pairs
  pairs=[]
  ix=0
  iy=0
  thrown_event_count=0
  #pairs up events based on time difference
  while ix < len(datax)-1 and iy < len(datay)-1: 
    if datax[ix][0] < datay[iy][0]-dt:
      ix+=1
      thrown_event_count+=1
    elif (datay[iy][0]-dt < datax[ix][0] and datax[ix][0] < datay[iy][0]+dt) or datay[iy][0] == datax[ix][0]:
      #print("succesfully paired with time difference of "+ str(datay[iy][0]-datax[ix][0]))
      pairs.append([datax[ix],datay[iy]])
      ix+=1;iy+=1;  
    elif datay[iy][0]+dt < datax[ix][0] :
      iy+=1    
      thrown_event_count+=1
    else: 
      print(datay[iy][0], datax[ix][0])
      print(datay[iy][0]- datax[ix][0])
      print(ix,iy)      
      raise("eternal loop yo")  

  print("Number of corellatabale event pairs",len(pairs))
  #print("Number of uncorellatabale events",thrown_event_count)
  Matrix = [[0 for x in datax[0][1]] for x in datax[0][1]]

  for pair in pairs: 
    eventx=pair[0][1]
    eventx=list(eventx)
    eventx=mirror(eventx)
    eventy=pair[1][1]
    eventy=list(eventy)
    eventy=mirror(eventy)
    Matrix[eventy.index("1")][eventx.index("1")] +=1

  Matrix=[i[3*16:9*16] for i in Matrix[3*16:9*16]] #crops off blank channels
  return Matrix  


Matrix = pair_up(datax,datay)

matshow(Matrix,cmap=get_cmap("BuPu"))




x=range(len(Matrix))
y=[sum(i) for i in Matrix]
bar(x,y,width=1)
#show()

MT=array(Matrix).transpose()
y2=[sum(i) for i in MT]
barh(x,y2,height=1)
#show()

def scatter_hist(x, y, ax, ax_histx, ax_histy,Matrix):
    # no labels
    ax_histx.tick_params(axis="x", labelbottom=False)
    ax_histy.tick_params(axis="y", labelleft=False)



    ax.matshow(Matrix,cmap=get_cmap("BuPu"))
    ax.tick_params(axis="x", labelbottom=True)
    yticks([20,40,60,80,100])

    ax_histx.bar(range(len(x)),x,width=1,color="darkorchid")
    ax_histy.barh(range(len(y)),y,height=1,color="darkorchid")






# definitions for the axes
left, width = 0.1, 0.65
bottom, height = 0.1, 0.65
spacing = 0.005


rect_scatter = [left, bottom, width, height]
rect_histx = [left, bottom + height + spacing, width, 0.2]
rect_histy = [left + width + spacing, bottom, 0.2, height]

# start with a square Figure
fig = figure(figsize=(8, 8))

ax = fig.add_axes(rect_scatter)

xlabel("Channel #")
ylabel("Channel #")

ax_histx = fig.add_axes(rect_histx, sharex=ax)
ylabel("Hits")

ax_histy = fig.add_axes(rect_histy, sharey=ax)
xlabel("Hits")



scatter_hist(y, y2, ax, ax_histx, ax_histy, Matrix)




#

savefig("Plots/plot.png",dpi=300)
#show()