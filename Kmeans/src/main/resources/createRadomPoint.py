#createRomdomPoint.py
import sys
import random
 
def main(argv):
    K=argv[1]
    x_center = 50
    y_center = 50
    length = 100
    width = 100
    file_handle=open('test.txt','a+')
    file_handle.write("%s\n"%K)
    count = 0
    while count < 100:
        count += 1
        x = x_center + (random.random() - 0.5) * length
        y = y_center + (random.random() - 0.5) * width
        print("%f,%f"%(x,y))
        file_handle.write("%f,%f\n"%(x,y))
    file_handle.write("--END--\n")
    file_handle.close()
if __name__ == "__main__":
    main(sys.argv)

# 调用方法：python createRomdomPoint.py [x_center, y_center, length, width]