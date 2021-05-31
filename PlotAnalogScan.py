def Read(filename="/home/pi/demofile2.txt"):
    with open(filename) as f:
    content = f.readlines()
    Res=[]
    # Show the file contents line by line.
    # We added the comma to print single newlines and not double newlines.
    # This is because the lines contain the newline character '\n'.
    for line in content:
        print(line),
        line1=line.strip()
        line2=line1.spli(" ")
        Res.append(int(line2))
        #x=[]
        print("len is",len(R[0]))
        print("A rate is",A.rate)

        x=[]
        i=0
        plt.plot(Res)
        plt.show()
