input("Make sure you have vtk file ready inside coordinate/membrane")
print("Running xyzp generator...")
from scipy import spatial
import pandas as pd
import os

filename = "membrane/" + str(os.listdir("membrane")[0])
vtk = open(filename)
lines = vtk.readlines()
total_points = lines[4].split(" ")[1]
points_header = "POINTS " + total_points + " float\n"
pressure_header = "POINT_DATA  " + total_points + "\n"
count = 0


# function to get the line length
def line_count(count):
    with open(filename, 'r') as f:
        for line in f:
            count += 1
    return count


# function to get the starting index
def get_start_index(data_type):
    if data_type == "point":
        for i in range(0, line_count(count)):
            if lines[i] == points_header:
                return i + 1
    if data_type == "pressure":
        for i in range(0, line_count(count)):
            if lines[i] == pressure_header:
                return i + 3


def get_end_index(data_type):
    global lines
    if data_type == "point":
        for i in range(0, line_count(count)):
            if "POLYGONS" in lines[i]:
                return i
    if data_type == "pressure":
        return line_count(count)


def data_capture(data_type, start_index, end_index):
    global lines
    point_list = []
    if data_type == "point":
        for i in range(start_index, end_index):
            splited_lines = lines[i].split(" ")
            for j in range(0, len(splited_lines)):
                try:
                    point_list.append(float(splited_lines[j]))
                except ValueError:
                    None
        return point_list
    if data_type == "pressure":
        for i in range(start_index, end_index):
            splited_lines = lines[i].split(" ")
            # print(splited_lines)
            for j in range(0, len(splited_lines)):
                try:
                    point_list.append(float(splited_lines[j]))
                except ValueError:
                    None
        return point_list


def point_structuring(point_list, pressure_list):
    df1 = pd.DataFrame()
    j = 0
    for i in range(0, int(len(point_list) / 3)):
        data = ({'x': [point_list[j]],
                 'y': [point_list[j + 1]],
                 'z': [point_list[j + 2]],
                 'p': [pressure_list[i]]
                 })
        df2 = pd.DataFrame(data)
        df1 = df1.append(df2)
        j += 3
    return df1


point_list = data_capture("point", get_start_index("point"), get_end_index("point"))
pressure_list = data_capture("pressure", get_start_index("pressure"), get_end_index("pressure"))
xyzp = point_structuring(point_list, pressure_list)


###################################################################################################################


# read all the csv files
rawdata = xyzp.reset_index()
del rawdata['index']
topcoordinate = pd.read_csv('top.csv')
bottomcoordinate = pd.read_csv('bottom.csv')
mid = pd.read_csv('mid.csv')

# interpolation for top
#=============================================
# convert pandas dataframe into numpy array
cloud = rawdata[['x', 'y', 'z']].to_numpy(dtype=float) # this is the cloud points
top_interpolator = topcoordinate.to_numpy(dtype=float) #this is the interpolator points

# coordinate interpolator
distance, topindex = spatial.KDTree(cloud).query(top_interpolator, k=1) # taking the index between

# filter pressure from raw data based on index
#top_p = pd.read_csv(raw_filename, usecols=['x', 'y', 'z', 'p'])
                               
top_x = rawdata.x*1000
top_y = rawdata.y*1000
top_z = rawdata.z*1000

top_p1 = pd.concat([top_x, top_y, top_z, rawdata.p], axis=1)
#=============================================



# interpolation for bottom
#=============================================
# convert pandas dataframe into numpy array
bottom_interpolator = bottomcoordinate.to_numpy(dtype=float)

# coordinate interpolator
distance, bottomindex = spatial.KDTree(cloud).query(bottom_interpolator, k=1)

# filter pressure from raw data based on index
bottom_x = rawdata.x*1000
bottom_y = rawdata.y*1000
bottom_z = rawdata.z*1000

bottom_p1 = pd.concat([bottom_x, bottom_y, bottom_z, rawdata.p], axis=1)
#=============================================

# filtering the top and bottom pressure
top_with_p_rawindex = top_p1.iloc[(topindex)]
top_with_p = top_with_p_rawindex.reset_index()
bottom_with_p_rawindex = bottom_p1.iloc[(bottomindex)]
bottom_with_p = bottom_with_p_rawindex.reset_index()

# net pressure calculation
#=============================================
#merge csv together
xyzpraw = pd.concat([mid*1000,(((top_with_p.p)*-1)+bottom_with_p.p)],axis=1)

xmid = (max(mid.x)-min(mid.x))/2
xdist = min(mid.x)+xmid
ymid = (max(mid.y)-min(mid.y))/2
ydist = min(mid.y)+ymid
zmid = (max(mid.z)-min(mid.z))/2
zdist = min(mid.z)+zmid

trans_coord = [{'x': xdist*1000, 'y': ydist*1000, 'z': zdist*1000, 'p':'0.00'}]
trans_coord_df = pd.DataFrame(trans_coord)

x = xyzpraw.x-xdist*1000
y = xyzpraw.y-ydist*1000
z = xyzpraw.z-zdist*1000

xyzp1 = pd.concat([x,y,z,round(xyzpraw.p,2)], axis=1)

xyzp = pd.concat([trans_coord_df, xyzp1])
xyzp.to_csv(r'LoadCase_.xyzp', index=False, float_format='%10.2f')
input("Load case file ready")