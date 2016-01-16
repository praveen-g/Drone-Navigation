
__author__ = "Praveen Gupta"

import numpy as np
from priorityDict import priorityDictionary
import sys
class Navigation(object):

	def __init__(self, noOfRoads,names,radii,intersections,noOfIntersctn, intersectionPositions, start,startPoint,direction,end,endPoint):

		self.noOfRoads=noOfRoads
		self.name=names
		self.radius={} #dictionary of roads and corresponding radii
		self.intersections=[]
		self.intersctn={}#dictionary to store each road connects which road on which point
		for i,x in enumerate(self.name):
			self.radius[x]=int(radii[i])
			self.intersections=int(intersections[i])
			self.intersctn[x]={}

		self.noOfIntersctn=noOfIntersctn
		
		for x in intersectionPositions:
			self.intersctn[x[0]].update({x[2]:int(x[1])})

		self.start=start
		self.startPoint=int(startPoint)
		self.direction=direction
		self.end=end
		self.endPoint=int(endPoint)
		
		self.commands=[]
		self.totalTime=0
			
	def display(self):

		print "Roads and their radii"
		print self.radius
		print "Intersection Information" 
		print self.intersctn


	#implementation

	def Dijkstra(self):

		distances={}
		individual_dist={}
		reverse={}
		path={}
		final_dist = {}	# dictionary of final distances
		Q = priorityDictionary()  # distances of non final predecessors
		Q[self.start] = 0
		visited=[]

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
					if self.direction == '+':
						self.direction=='-'
					else:
						self.direction=='+'

			for neighbour in self.intersctn[road]:
				if road==self.end:
					starting=self.intersctn[neighbour][road]
					ending=self.endPoint
				else:
					starting=self.intersctn[road][neighbour]
					ending=self.intersctn[neighbour][road]
				if neighbour in visited or starting == ending:
						continue
				dist,reverseTime= self.calcDist(road, starting,neighbour, ending,self.direction)
				totalDist = final_dist[road] + dist
				
				if neighbour not in Q or (totalDist <= Q[neighbour] ):
					Q[neighbour] = totalDist
					path[neighbour] = road
					reverse[neighbour]=reverseTime
					distances[neighbour]=dist+reverseTime
					if road==self.start:
						distances[self.start],reverse[self.start]=self.calcDist(self.start,self.startPoint,neighbour,self.intersctn[self.start][neighbour],self.direction)
			if len(visited)==self.noOfRoads: 
				break
		return (distances,path,reverse)

	def shortestPath(self):

		D,P,R= self.Dijkstra()
		Path = []
		reverse=[]
		while 1:
			Path.append(R[self.end])
			Path.append(self.end)

			if self.end == self.start: break
			self.end = P[self.end]
		Path.reverse()
		return D,Path,

	def convertPathToTime(self):
		distances, path = self.shortestPath()
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
					self.appendCommands("TRANSFER "+path[i+2],0.1)

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

	def calcDist(self,start, position, end, destination,direction):
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
			if start==end:
				angle=0
			else:
				angle = 180
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
	file_name= raw_input("enter file name ")
	input_file=open(file_name,'r')
	given_input=input_file.read().splitlines()
	noOfRoads=int(given_input[0].strip())
	names=[0]*noOfRoads
	radii=[0]*noOfRoads
	intersections=[0]*noOfRoads
	
	for i in range(1,noOfRoads+1):
		line=given_input[i].strip().split(' ')
		names[i-1]=line[0]
		radii[i-1]=line[1]
		intersections[i-1]=line[2]

	noOfIntersctn=int(given_input[noOfRoads+2].strip())

	intersectionPositions=[]
	for i in range(noOfRoads+3,noOfIntersctn+noOfRoads+3):
		line=given_input[i].strip().split(' ')
		intersectionPositions.append(line)
	line=given_input[-2].strip().split(' ')
	start=line[0]
	startPoint=line[1]
	direction=line[2]
	line=given_input[-1].strip().split(' ')
	end=line[0]
	endPoint=line[1]

	print intersections
	obj = Navigation(noOfRoads,names,radii,intersections,noOfIntersctn,intersectionPositions,start,startPoint,direction,end,endPoint)
	#obj = Navigation(5,['a','b','c','d','e'],[2500,1000,1000,1000,3500,4500],[3,3,3,4,3],16,[['a',0,'b',180],['a',0,'d',0],['a',180,'c',0],['b',0,'e',0],['b',180,'a',0],['b',180,'d',0],['c',0,'a',180],['c',180,'d',180],['c',180,'e',180],['d',0,'a',0],['d',0,'b',180],['d',180,'c',180],['d',180,'e',180],['e',0,'b',0],['e',180,'c',180],['e',180,'d',180]], 'a',355,'+','b',0)
	obj.display()
	print obj.convertPathToTime()
	print "Commands"
	print obj.commands
	print "TOTAL TIME"
	print round(obj.totalTime,1)
