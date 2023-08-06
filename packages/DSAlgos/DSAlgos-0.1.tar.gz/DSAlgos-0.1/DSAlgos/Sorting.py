def BubbleSort(arr,swap=False):
    s=0
    for i in range(len(arr)):
        for j in range(i+1,len(arr)):
            if arr[i]>arr[j]:
                s+=1
                arr[i],arr[j]=arr[j],arr[i]
    if swap==True:
        return [arr,s]
    else:
        return arr
        
def InsertionSort(arr,swap=False):
    s=0
    for i in range(0,len(arr)):
        for j in range(0,i+1):
            if arr[i]<arr[j]:
                s+=1
                arr[i],arr[j]=arr[j],arr[i]
    if swap==True:
        return [arr,s]
    else:
        return arr
        
def SelectionSort(arr,swap=False):
    s=0
    for i in range(len(arr)):
        m=0
        mi=arr[i]
        for j in range(i+1,len(arr)):
            if mi>arr[j]:
                mi=arr[j]
                m=j
        if m!=0:
            s+=1
            arr[i],arr[m]=arr[m],arr[i]
    if swap==True:
        return [arr,s]
    else:
        return arr

def MergeSort(arr):
   
    if len(arr)<=0:
        return arr
    mid=len(arr)//2
    p=arr[mid]
    arr.pop(mid)
    greater=[]
    smaller=[]
    for i in arr:
        if i>p:
            greater.append(i)
        else:
            smaller.append(i)
    return MergeSort(smaller)+[p]+MergeSort(greater)

def _quicksort(arr,pivot):
    if len(arr)<=1:
        return arr
    greater=[]
    smaller=[]
    p=arr[pivot]
    arr.pop(pivot)
    for i in arr:
        if i>p:
            greater.append(i)
        else:
            smaller.append(i)
    return _quicksort(smaller,pivot)+[p]+_quicksort(greater,pivot)
    
def QuickSort(arr,pivot=["beg","end","mid",0]):
    if pivot=="beg":
        return _quicksort(arr,0)
    elif pivot=="end":
        return _quicksort(arr,-1)
    elif pivot=="mid":
        return MergeSort(arr)