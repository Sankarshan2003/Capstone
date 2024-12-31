
source_pallets = [[] for _ in range(4)]
buffer_spurce_pallet=[[] for _ in range(4)]
dest_pallet = [[] for _ in range(5)]


for pallet in source_pallets:
	for i in range(0,12):
		pallet.append([1]*4)

for pallet in buffer_spurce_pallet:
	for i in range(0,12):
		pallet.append([1]*4)
            
for pallet in dest_pallet:
	for i in range(0,12):
		pallet.append([0]*4)
          



source_pallet_coord = [[20,90],#35 91
                     [40,200],
                     [346,90],
                     [345,202]]

dest_pallet_coord = [[298.5,296],
                     [298.5,296],
                     [298.5,296],
                     [298.5,296],
                     [298.5,296]]


pallet1_2_coord = [] 
pallet3_4_coord = [] 


# pallet1_frame_bounds = [[99, 177], [640, 169], [645, 388], [98, 396]]
# pallet2_frame_bounds = [[95, -38], [639, -41], [639, 177], [101, 183]]
# pallet3_frame_bounds = [[104, 179], [647, 169], [649, 390], [109, 403]]
# pallet4_frame_bounds = [[100, -38], [645, -42], [647, 175], [105, 181]]

pallet_vis_coord = [[86,782],
	    [86,612],
        [565,782],
	    [565,612]]

current_position = [0,0,0,1]