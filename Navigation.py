
__author__ = "Praveen Gupta"

import numpy as np
from priorityDict import priorityDictionary
class Navigation(object):

	def __init__(self):

		self.noOfRoads=0
		self.name=[]
		self.radius={} #dictionary of roads and corresponding radii
		self.noOfIntersctn=0
		self.intersctn={}
		self.commands=[]
		self.totalTime=0

	def get_input(self):

		self.noOfRoads= int(raw_input("Enter number of Roads "))
		print "Enter road, radius and number of Intersections "
		no = np.zeros(5 ,dtype=np.int)
		self.name = [0]*self.noOfRoads
		
		for i in range(self.noOfRoads):
			self.name[i] = raw_input("enter name ")
			radi = int(raw_input("enter radius "))
			no[i] = int(raw_input("enter number of Intersections "))
			self.radius[self.name[i]] = radi
			self.intersctn[self.name[i]]={}


		self.noOfIntersctn = int(raw_input("Enter total number of intersections "))
		print "Enter the intersection details in order of specified format\n Road Name 1: first point of Intersection: Road Name 2: second point of Intersection "
		k=1
		for i in self.name:
			if k<=self.noOfIntersctn:
				for j in range(no[self.name.index(i)]):
					print "Intersection No "+str(k)
					strtRoad=raw_input()
					strtpt = raw_input()
					endRoad = raw_input()
					endpt=raw_input()
					self.intersctn[strtRoad].update({endRoad:strtpt}) #converting airport to graph
					k+=1
			else:
				print "Your number of Intersections don't tally"
				return
					

	def display(self):

		print "Roads and their radii"
		print self.radius
		print "Intersection Information" 
		print self.intersctn


	#implementation

	def Dijkstra(self, start, startPoint, end, endPoint,direction):

		distances={}
		individual_dist={}
		reverse={}
		path={}
		final_dist = {}	# dictionary of final distances
		Q = priorityDictionary()  # distances of non final predecessors
		Q[start] = 0
		visited=[]
		mainDirection=direction

		for road in Q:
			if road in distances:
				individual_dist[road]=distances[road]
			if road in visited:
				continue
			if road not in visited:
				visited.append(road)
			final_dist[road] = Q[road]
			if road in reverse:
				if reverse[road]==0.3:
					if direction == '+':
						direction=='-'
					else:
						direction=='+'

			for neighbour in self.intersctn[road]:

				if road==end:
					starting=self.intersctn[neighbour][road]
					ending=endPoint
				elif road==start:
					starting=startPoint
					ending=self.intersctn[road][neighbour]
				else:
					starting=self.intersctn[road][neighbour]
					ending=self.intersctn[neighbour][road]
				if neighbour in visited or starting == ending:
						continue
				dist,reverseTime= self.calcDist(road, starting,ending,direction)
				totalDist = final_dist[road] + dist
				
				if neighbour not in Q or (totalDist <= Q[neighbour] ):
					Q[neighbour] = totalDist
					path[neighbour] = road
					reverse[neighbour]=reverseTime
					distances[neighbour]=dist+reverseTime
					if road==start:
						reverse[start]=reverseTime
						distances[road]=totalDist
			if len(visited)==self.noOfRoads: 
				break
		return (distances,path,reverse)

	def shortestPath(self,start,startPoint,end,endPoint,direction):

		D,P,R= self.Dijkstra(start,startPoint,end,endPoint,direction)
		Path = []
		reverse=[]
		while 1:
			Path.append(R[end])
			Path.append(end)

			if end == start: break
			end = P[end]
		Path.reverse()
		return D,Path,

	def convertPathToTime(self,start,startPoint,end,endPoint,direction):
		distances, path = self.shortestPath(start,startPoint,end,endPoint,direction)
		totalTime=0
		
		for i in range(0,len(path)):
			if i%2==0:
				dist=distances[path[i]]
				if path[i+1]==0.3:
					if i!=0:
						dist-=8
						self.appendCommands("STOP",4)
					self.appendCommands("REVERSE",0.3)
				time = self.calcTime(dist,1)#(-8) to account for deacceleration
				self.appendCommands("GO",time)
				if i!=len(path)-2:
					self.appendCommands("TRANSFER "+path[i],0.1)

	def calcTime(self,dist,flag):
		#flag is used to denote if acceleration is required
		time=0
		if flag==1:
			#according to v = u+ at  and  s=ut+0.5at^2, full velocity is reached in 4 sec and 8m
			if dist<8:
				return (2*dist)**(1/2.0)
			elif dist >=8 :
				time+=4
				dist-=8
		time += dist/4 #max velocity mentioned is 4 m/s
		return time

	def calcDist(self,start, position, destination,direction):
		position = int(position)
		destination= int(destination)
		angle=0
		flag=True
		time=0
		#check if its in anticlockwise motion
		if direction == '-':
			flag = False
		#compute angle to be covered
		diff = destination-position
		if diff > 180 or (diff<0 and diff>-180):
			if flag ==True:
				direction = '-'
				time=0.3
			if destination>position:
					angle= 360 - abs(diff)
			else:
				angle = abs(diff)
		elif diff == 180 or diff == 0:
			angle = abs(diff)
			time=0
		else:
			if flag==False:
				direction = '+'
				time=0.3
			if destination<position:
				angle= 360 - abs(diff)
			else:
				angle = abs(diff)
		return ((float(angle)/360) * 2 * 3.14 * self.radius[start]),time

	def appendCommands(self,command,value):
		self.totalTime+=value
		self.commands.append(command + '(' + str(value)+')')
		


if __name__ == "__main__":
	
	choice = 'y'
	while choice == 'y':
		obj = Navigation()
		obj.get_input()
		start = raw_input("Enter Starting Road ")
		startPoint = int(raw_input("Enter Starting Position "))
		direction = raw_input("Enter + for clockwise, - for anti clockwise ")
		end = raw_input("Enter Ending Road ")
		endPoint =  int(raw_input("Enter End Point "))
		obj.display()
		print obj.convertPathToTime(start,startPoint,end,endPoint,direction)
		print "Commands"
		print obj.commands
		print "TOTAL TIME"
		print round(obj.totalTime,1)
		choice = raw_input("To continue press 'y'")
