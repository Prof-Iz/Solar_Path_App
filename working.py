from image_process import overlay_graph
import graph_maker as gm
from time import sleep
path_of_fish = r"C:\Users\User\Documents\GitHub\Solar_Path_App\test_pics\blob2.jpg"
path_of_graph = r'C:\Users\User\Documents\GitHub\Solar_Path_App\test_pics\graphed.png'


def main():

    gm.make_graph(3,101.7321333)
    
    
    overlay_graph(path_of_fish,path_of_graph)

if __name__ == '__main__':
    main()