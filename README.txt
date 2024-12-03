- TEST
	- SEEN
		- COORDINATE [SIGNIFICANT WAYPOINT]
		# coordinates of the siginificate waypoint
			- 0.txt
				x1
				y1
				x2
				y2
				...
			- 1.txt
			...
	
		- COORDINATE [TARGET&GOAL]
		# coordinates of the target and goal
			- 0.txt
				x1
				y1
				x2
				y2
			- 1.txt
			...

		- MAP [EXAMPLE]
		# map with target and goal, input of prediction model
			- 0.jpg
			...
		
		- MAP [ORIGINAL]
		# original map, input of path planner
			- 0.jpg
			...
		
		- PATH [2PIXEL]
		# RRT* result, thickness = 2 pixel
			- 0.jpg
			...
		
		- PATH [30PIXEL]
		# ground truth, thickness = 30 pixel
			- 0.jpg
			...
		
		- PATH [COST]
		# path cost of the RRT8 result
			- 0.txt
				cost
			- 1.txt
			...
	- UNSEEN
		...
- TRAIN
	...